"""
/api/recommend — Product research route.

Flow: validate → Grok query generation → Tavily search → parse → respond.
"""

import logging
from flask import Blueprint, request, jsonify

from backend.prompts.query_generation import build_query_generation_prompt
from backend.services.grok_service import generate_search_queries
from backend.services.tavily_service import search as tavily_search
from backend.services.product_parser import parse_products

logger = logging.getLogger(__name__)
recommend_bp = Blueprint("recommend", __name__)


@recommend_bp.route("/api/recommend", methods=["POST"])
def recommend():
    """Handle a product-research request."""

    # ── 1. Validate input ───────────────────────────────────────────────
    body = request.get_json(silent=True)
    if not body or not body.get("query", "").strip():
        return jsonify({
            "success": False,
            "data": None,
            "error": "Please provide a product query.",
        }), 400

    user_query = body["query"].strip()
    logger.info("POST /api/recommend — query: %s", user_query[:80])

    try:
        # ── 2. Grok: generate search queries ────────────────────────────
        messages = build_query_generation_prompt(user_query)
        grok_result = generate_search_queries(messages)
        search_queries = grok_result.get("search_queries", [])

        if not search_queries:
            return jsonify({
                "success": False,
                "data": None,
                "error": "The AI couldn't generate research queries for this request.",
            }), 500

        # ── 3. Tavily: web research ─────────────────────────────────────
        tavily_results = tavily_search(search_queries)

        if not tavily_results:
            return jsonify({
                "success": True,
                "data": {
                    "user_query": user_query,
                    "products": [],
                    "research": {
                        "category": grok_result.get("category", "general"),
                        "queries_used": search_queries,
                    },
                },
                "error": None,
            }), 200

        # ── 4. Parse & normalise ────────────────────────────────────────
        products = parse_products(tavily_results)

        logger.info(
            "Returning %d products for query: %s",
            len(products),
            user_query[:60],
        )

        return jsonify({
            "success": True,
            "data": {
                "user_query": user_query,
                "products": products,
                "research": {
                    "category": grok_result.get("category", "general"),
                    "queries_used": search_queries,
                },
            },
            "error": None,
        }), 200

    except ValueError as exc:
        logger.error("Controlled error in /api/recommend: %s", exc)
        return jsonify({
            "success": False,
            "data": None,
            "error": str(exc),
        }), 500

    except Exception as exc:
        logger.exception("Unexpected error in /api/recommend")
        return jsonify({
            "success": False,
            "data": None,
            "error": "An unexpected error occurred. Please try again.",
        }), 500
