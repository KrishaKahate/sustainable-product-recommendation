"""
Configuration module — loads environment variables once and exposes them
as simple module-level constants. Every other module imports from here.
"""

import os
from dotenv import load_dotenv

# Load .env from the project root (one level above backend/)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# ── API Keys ────────────────────────────────────────────────────────────
XAI_API_KEY = os.getenv("XAI_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# ── Grok Model ──────────────────────────────────────────────────────────
# Configurable via env; sensible default if left blank.
GROK_MODEL = os.getenv("GROK_MODEL") or "qwen/qwen3.8-27b"

# ── xAI API Endpoint ───────────────────────────────────────────────────
XAI_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# ── Tavily API Endpoint ────────────────────────────────────────────────
TAVILY_API_URL = "https://api.tavily.com/search"

# ── Timeouts (seconds) ─────────────────────────────────────────────────
GROK_TIMEOUT = 60
TAVILY_TIMEOUT = 30

# ── Result Limits ──────────────────────────────────────────────────────
TAVILY_MAX_RESULTS_PER_QUERY = 5
MAX_PRODUCTS_RETURNED = 12
