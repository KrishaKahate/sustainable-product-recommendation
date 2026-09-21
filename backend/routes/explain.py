"""
/api/explain — "Why This Product?" route.

Called lazily when the user clicks the explanation button for a specific product.
"""

import logging
from flask import Blueprint, request, jsonify

from backend.prompts.product_explanation import build_explanation_prompt
from backend.services.grok_service import generate_explanation

logger = logging.getLogger(__name__)
explain_bp = Blueprint("explain", __name__)


@explain_bp.route("/api/explain", methods=["POST"])
def explain():
    """Generate an evidence-grounded explanation for a product match."""

    # ── 1. Validate input ───────────────────────────────────────────────
    body = request.get_json(silent=True)
    if not body:
        return jsonify({
            "success": False,
            "data": None,
            "error": "Invalid request body.",
        }), 400

    user_query = body.get("user_query", "").strip()
    product = body.get("product")

    if not user_query:
        return jsonify({
            "success": False,
            "data": None,
            "error": "Missing user_query.",
        }), 400

    if not product or not isinstance(product, dict):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Missing or invalid product data.",
        }), 400

    product_name = product.get("name", "Unknown")
    logger.info("POST /api/explain — product: %s", product_name[:60])

    try:
        # ── 2. Call Grok for explanation ────────────────────────────────
        messages = build_explanation_prompt(user_query, product)
        explanation = generate_explanation(messages)

        if not explanation:
            return jsonify({
                "success": False,
                "data": None,
                "error": "Grok returned an empty explanation.",
            }), 500

        logger.info("Explanation generated for: %s", product_name[:60])

        return jsonify({
            "success": True,
            "data": {
                "product_name": product_name,
                "explanation": explanation,
            },
            "error": None,
        }), 200

    except ValueError as exc:
        logger.error("Controlled error in /api/explain: %s", exc)
        return jsonify({
            "success": False,
            "data": None,
            "error": str(exc),
        }), 500

    except Exception:
        logger.exception("Unexpected error in /api/explain")
        return jsonify({
            "success": False,
            "data": None,
            "error": "Couldn't generate the explanation right now. Please try again.",
        }), 500
