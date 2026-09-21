"""
Grok (xAI) service — handles all communication with the xAI chat-completions
API. Used for both query generation and product explanation.
"""

import json
import re
import logging
import requests
from backend.config import XAI_API_KEY, XAI_API_URL, GROK_MODEL, GROK_TIMEOUT

logger = logging.getLogger(__name__)


def _call_grok(messages: list[dict]) -> str:
    """
    Send a chat-completion request to the xAI API and return the assistant's
    text content.  Raises ValueError on failure so callers can handle it.
    """
    if not XAI_API_KEY:
        raise ValueError("XAI_API_KEY is not configured.")

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROK_MODEL,
        "messages": messages,
        "temperature": 0.3,  # low temperature for structured, predictable output
    }

    logger.info("Calling Grok model=%s", GROK_MODEL)

    try:
        response = requests.post(
            XAI_API_URL,
            headers=headers,
            json=payload,
            timeout=GROK_TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error("Grok API request timed out")
        raise ValueError("Grok API request timed out. Please try again.")
    except requests.exceptions.RequestException as exc:
        logger.error("Grok API request failed: %s", exc)
        raise ValueError(f"Grok API request failed: {exc}")

    data = response.json()

    # Navigate the OpenAI-compatible response format
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        logger.error("Unexpected Grok response structure: %s", data)
        raise ValueError("Unexpected response from Grok.")

    return content.strip()


def _extract_json(text: str) -> dict:
    """
    Attempt to parse JSON from Grok's response.  Handles:
      1. Pure JSON
      2. JSON wrapped in markdown ```json ... ``` fences
      3. JSON embedded in surrounding prose
    """
    # 1) Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2) Try extracting from markdown code fences
    fence_match = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if fence_match:
        try:
            return json.loads(fence_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 3) Try finding the first { ... } block
    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError("Could not extract valid JSON from Grok response.")


# ── Public API ──────────────────────────────────────────────────────────

def generate_search_queries(messages: list[dict]) -> dict:
    """
    Call Grok with the query-generation prompt and return parsed JSON with
    category, budget, requirements, sustainability_preferences, search_queries.
    """
    raw = _call_grok(messages)
    parsed = _extract_json(raw)

    # Validate minimum expected fields
    if "search_queries" not in parsed or not isinstance(parsed["search_queries"], list):
        raise ValueError("Grok response missing 'search_queries' list.")

    # Ensure sensible defaults for optional fields
    parsed.setdefault("category", "general")
    parsed.setdefault("budget", None)
    parsed.setdefault("requirements", [])
    parsed.setdefault("sustainability_preferences", [])

    logger.info(
        "Grok generated %d search queries for category='%s'",
        len(parsed["search_queries"]),
        parsed["category"],
    )
    return parsed


def generate_explanation(messages: list[dict]) -> str:
    """
    Call Grok with the explanation prompt and return the plain-text
    explanation string.
    """
    return _call_grok(messages)
