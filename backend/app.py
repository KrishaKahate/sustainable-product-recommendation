"""
Flask application entry point.

Registers all blueprints, enables CORS, provides /api/health,
and configures lightweight logging.
"""

import logging
from flask import Flask, jsonify
from flask_cors import CORS

from backend.routes.recommend import recommend_bp
from backend.routes.explain import explain_bp

# ── Logging ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Application factory."""
    app = Flask(__name__)
    CORS(app)  # allow Streamlit (different port) to call Flask

    # Register route blueprints
    app.register_blueprint(recommend_bp)
    app.register_blueprint(explain_bp)

    # ── Health endpoint ─────────────────────────────────────────────────
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    # ── Global error handler ────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(_):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Endpoint not found.",
        }), 404

    @app.errorhandler(500)
    def internal_error(_):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Internal server error.",
        }), 500

    logger.info("Flask app initialised — routes registered")
    return app


# Module-level app instance for WSGI servers (e.g., Gunicorn)
app = create_app()


# ── Run directly with: python backend/app.py or python -m backend.app ────
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in ("true", "1")
    app.run(host="0.0.0.0", port=port, debug=debug)
