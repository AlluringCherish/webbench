from flask import Flask

# Register blueprints
from app.routes.articles import articles_bp
from app.routes.versions import versions_bp
from app.routes.dashboard import dashboard_bp


def register_routes(app):
    app.register_blueprint(articles_bp)
    app.register_blueprint(versions_bp)
    app.register_blueprint(dashboard_bp)
