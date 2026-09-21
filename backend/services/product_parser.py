"""
Product parser — transforms raw Tavily search results into clean,
UI-ready product objects using deterministic Python parsing.

Because web pages vary wildly, the parser tolerates incomplete data and
never invents information.
"""

import re
import logging
from urllib.parse import urlparse
from backend.config import MAX_PRODUCTS_RETURNED

logger = logging.getLogger(__name__)

# ── Currency patterns used to extract price ─────────────────────────────
_PRICE_PATTERNS = [
    re.compile(r"₹[\s]*[\d,]+(?:\.\d{1,2})?"),
    re.compile(r"Rs\.?\s*[\d,]+(?:\.\d{1,2})?"),
    re.compile(r"INR\s*[\d,]+(?:\.\d{1,2})?"),
    re.compile(r"\$[\d,]+(?:\.\d{1,2})?"),
    re.compile(r"€[\d,]+(?:\.\d{1,2})?"),
    re.compile(r"£[\d,]+(?:\.\d{1,2})?"),
]

# Keywords that hint at sustainability information
_SUSTAINABILITY_KEYWORDS = [
    "recycled", "sustainable", "eco-friendly", "eco friendly",
    "biodegradable", "organic", "renewable", "carbon neutral",
    "carbon footprint", "energy efficient", "solar", "bamboo",
    "plant-based", "plant based", "fair trade", "fairtrade",
    "compostable", "reclaimed", "upcycled", "green",
    "environmentally", "recyclable", "non-toxic", "vegan",
    "ocean plastic", "refurbished", "certified", "bpa free",
    "FSC", "B Corp",
]


def _extract_price(text: str) -> str:
    """Try to pull the first price string from text."""
    for pattern in _PRICE_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(0).strip()
    return "Not available"


def _extract_features(text: str) -> list[str]:
    """
    Heuristically extract bullet-like features from a snippet.
    Looks for short sentences / phrases that feel like product highlights.
    """
    features: list[str] = []
    # Try splitting on common list separators
    for sep in ["\n", " - ", " • ", " · ", "; ", " | "]:
        if sep in text:
            parts = [p.strip() for p in text.split(sep) if 10 < len(p.strip()) < 150]
            if len(parts) >= 2:
                features = parts[:5]
                break

    # Fallback: use the first few sentences
    if not features:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        features = [s.strip() for s in sentences if 15 < len(s.strip()) < 150][:3]

    return features


def _extract_sustainability(text: str) -> list[str]:
    """Pull sentences that mention sustainability-related keywords."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    hits: list[str] = []
    for sentence in sentences:
        lower = sentence.lower()
        for kw in _SUSTAINABILITY_KEYWORDS:
            if kw.lower() in lower:
                clean = sentence.strip()
                if 10 < len(clean) < 200 and clean not in hits:
                    hits.append(clean)
                break  # one keyword match per sentence is enough
    return hits[:3]


def _derive_product_name(title: str, content: str) -> str:
    """Best-effort product name from the search-result title."""
    if not title:
        # Fallback: first meaningful chunk of content
        words = content.split()[:8]
        return " ".join(words) if words else "Unknown Product"
    # Strip common site-name suffixes like " - Amazon.in" or " | Flipkart"
    name = re.split(r"\s*[-|–—]\s*", title)[0].strip()
    return name if name else title


def _normalise_url(url: str) -> str:
    """Basic URL validation/cleanup."""
    if not url or not url.startswith("http"):
        return ""
    return url.strip()


def _source_domain(url: str) -> str:
    """Extract the domain from a URL for display."""
    try:
        return urlparse(url).netloc.replace("www.", "")
    except Exception:
        return "Unknown source"


def _is_likely_duplicate(existing: list[dict], candidate_name: str) -> bool:
    """Rough duplicate check by comparing lowered product names."""
    candidate_lower = candidate_name.lower().strip()
    if len(candidate_lower) < 5:
        return False
    for product in existing:
        existing_lower = product["name"].lower().strip()
        # If one name is a substring of the other, consider duplicate
        if candidate_lower in existing_lower or existing_lower in candidate_lower:
            return True
    return False


# ── Public API ──────────────────────────────────────────────────────────

def parse_products(tavily_results: list[dict]) -> list[dict]:
    """
    Transform raw Tavily results into clean product objects.

    Each product:
    {
        "name": str,
        "price": str,
        "description": str,
        "features": [str],
        "sustainability_info": [str],
        "source_title": str,
        "source_url": str,
    }
    """
    products: list[dict] = []

    for result in tavily_results:
        title = result.get("title", "")
        content = result.get("content", "")
        url = _normalise_url(result.get("url", ""))
        combined_text = f"{title} {content}"

        name = _derive_product_name(title, content)

        # Skip obvious non-product pages
        if not name or not url:
            continue

        # Duplicate check
        if _is_likely_duplicate(products, name):
            continue

        # Truncate description to a readable length
        description = content[:300].strip()
        if len(content) > 300:
            description += "…"

        product = {
            "name": name,
            "price": _extract_price(combined_text),
            "description": description or "No description available.",
            "features": _extract_features(content),
            "sustainability_info": _extract_sustainability(combined_text),
            "source_title": _source_domain(url),
            "source_url": url,
        }

        products.append(product)

        if len(products) >= MAX_PRODUCTS_RETURNED:
            break

    logger.info("Parsed %d products from %d Tavily results", len(products), len(tavily_results))
    return products
