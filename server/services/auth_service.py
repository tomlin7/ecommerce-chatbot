import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from werkzeug.security import check_password_hash
import uuid

from models.user import User

logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication and user management"""

    @staticmethod
    def register_user(name: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user"""
        try:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {
                    "success": False,
                    "message": "Пользователь с таким email уже существует",
                }

            user_id = str(uuid.uuid4())
            user = User(id=user_id, email=email, name=name, password=password)

            from app import db

            db.session.add(user)
            db.session.commit()

            access_token = create_access_token(identity=user_id)
            refresh_token = create_refresh_token(identity=user_id)

            logger.info(f"User registered successfully: {email}")

            return {
                "success": True,
                "message": "Пользователь успешно зарегистрирован",
                "user": user.to_dict(),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

        except Exception as e:
            logger.error(f"Error registering user: {str(e)}")
            from app import db

            db.session.rollback()
            return {"success": False, "message": "Ошибка при регистрации"}

    @staticmethod
    def login_user(email: str, password: str) -> Dict[str, Any]:
        """Authenticate user and return tokens"""
        try:
            user = User.query.filter_by(email=email).first()

            if not user or not user.check_password(password):
                return {"success": False, "message": "Неверный email или пароль"}

            if not user.is_active:
                return {"success": False, "message": "Аккаунт деактивирован"}

            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            user.updated_at = datetime.utcnow()
            from app import db

            db.session.commit()

            logger.info(f"User logged in successfully: {email}")

            return {
                "success": True,
                "message": "Вход выполнен успешно",
                "user": user.to_dict(),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

        except Exception as e:
            logger.error(f"Error logging in user: {str(e)}")
            return {"success": False, "message": "Ошибка при входе"}

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            return User.query.get(user_id)
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}")
            return None

    @staticmethod
    def update_user_preferences(
        user_id: str, preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update user preferences"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"success": False, "message": "Пользователь не найден"}

            user.set_preferences(preferences)
            from app import db

            db.session.commit()

            logger.info(f"Updated preferences for user: {user.email}")

            return {
                "success": True,
                "message": "Настройки успешно обновлены",
                "user": user.to_dict(),
            }

        except Exception as e:
            logger.error(f"Error updating user preferences: {str(e)}")
            from app import db

            db.session.rollback()
            return {"success": False, "message": "Не удалось обновить настройки"}

    @staticmethod
    def refresh_token(current_user_id: str) -> Dict[str, Any]:
        """Generate new access token"""
        try:
            user = User.query.get(current_user_id)
            if not user or not user.is_active:
                return {"success": False, "message": "Некорректный пользователь"}

            access_token = create_access_token(identity=current_user_id)

            return {"success": True, "access_token": access_token}

        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}")
            return {"success": False, "message": "Ошибка обновления токена"}

    @staticmethod
    def deactivate_user(user_id: str) -> Dict[str, Any]:
        """Deactivate user account"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"success": False, "message": "Пользователь не найден"}

            user.is_active = False
            user.updated_at = datetime.utcnow()

            from app import db

            db.session.commit()

            logger.info(f"User deactivated: {user.email}")

            return {"success": True, "message": "Аккаунт пользователя деактивирован"}

        except Exception as e:
            logger.error(f"Error deactivating user: {str(e)}")
            from app import db

            db.session.rollback()
            return {"success": False, "message": "Не удалось деактивировать пользователя"}
