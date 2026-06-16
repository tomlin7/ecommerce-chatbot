import os

from config import config
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db
from utils.logger_config import setup_logging

load_dotenv()


jwt = JWTManager()
migrate = Migrate()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt.init_app(app)

    migrate.init_app(app, db)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    setup_logging(app)

    from routes import register_routes

    register_routes(app)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "message": "Ресурс не найден"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal server error: {str(error)}")
        return jsonify({"success": False, "message": "Внутренняя ошибка сервера"}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "message": "Неверный запрос"}), 400

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"success": False, "message": "Срок действия токена истек"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"success": False, "message": "Недействительный токен"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(
            {"success": False, "message": "Требуется токен авторизации"}
        ), 401

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify(
            {
                "success": True,
                "status": "healthy",
                "message": "API чат-бота электронной коммерции работает",
            }
        ), 200

    @app.before_request
    def initialize_database():
        """Initialize database and seed with sample data"""
        app.before_request_funcs[None].remove(initialize_database)

        try:
            db.create_all()

            from utils.database_seeder import DatabaseSeeder

            seeder = DatabaseSeeder(db)
            seeder.seed_products()

            app.logger.info("Database initialized successfully")

        except Exception as e:
            app.logger.error(f"Error initializing database: {str(e)}")

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
        threaded=True
    )
