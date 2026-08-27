
"""
Flask application entry point for the PQ Assistant.

Creates and configures the Flask application, registers API
routes, middleware, and error handlers.
"""

from flask import Flask, jsonify

from config.logging_config import configure_logging
from web.middleware import register_middleware
from web.routes import web_bp


def create_app() -> Flask:
    """
    Create and configure the PQ Assistant Flask application.

    Returns:
        Flask: Configured Flask application.
    """
    # Configure application logging.
    configure_logging()

    app = Flask(__name__)

    # Flask configuration.
    app.config["JSON_SORT_KEYS"] = False

    # Register API routes.
    app.register_blueprint(web_bp)

    # Register middleware and global error handlers.
    register_middleware(app)

    @app.route("/", methods=["GET"])
    def index():
        """Return basic API information."""
        return jsonify(
            {
                "success": True,
                "service": "PQ Assistant",
                "version": "1.0.0",
                "message": "PQ Assistant API is running.",
            }
        ), 200

    @app.route("/health", methods=["GET"])
    def health_check():
        """Return application health status."""
        return jsonify(
            {
                "success": True,
                "status": "healthy",
                "service": "PQ Assistant",
            }
        ), 200

    return app


# Application instance.
app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )
