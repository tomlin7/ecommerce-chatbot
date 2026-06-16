from .auth_routes import auth_bp
from .cart_routes import cart_bp
from .chat_routes import chat_bp
from .farm_routes import farm_bp
from .like_routes import like_bp
from .product_routes import product_bp


def register_routes(app):
    """Register all route blueprints"""
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(cart_bp, url_prefix="/api")
    app.register_blueprint(like_bp, url_prefix="/api")
    app.register_blueprint(farm_bp, url_prefix="/api/farms")
