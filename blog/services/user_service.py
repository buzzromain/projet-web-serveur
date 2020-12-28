from blog.data_access import db_session
from blog import models
from .exceptions import UserNotFound, UnauthorizedUser
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)

class UserAuthService:
    @staticmethod
    def register(username, password):
        """
        Création d'un utilisateur
        """
        user = models.User.create_new_user(username, password)

        db_session.add(user)
        db_session.commit()
        
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    @staticmethod
    def login(username, password):
        """
        Connexion d'un utilisateur
        """
        user = UserService.get_user_by_username(username)  
        if user.check_password(password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        else:
            raise UnauthorizedUser("Username or password are incorrect")

    @staticmethod
    def refresh_token(id):
        """
        Rafraichit le token JWT
        """
        user = UserService.get_user_by_id(id)
        access_token = create_access_token(identity=user.id)
        return access_token
        
class UserService:
    @staticmethod
    def get_user_by_id(id):
        """
        Obtenir un utilisateur à partir de son identifiant
        """
        user = db_session.query(models.User).get(id)
        if user is not None:
            return user
        else:
            raise UserNotFound("User not found")

    @staticmethod
    def get_user_by_username(username):
        """
        Obtenir un utilisateur à partir de son nom d'utilisateur
        """
        user = db_session.query(models.User).filter(models.User.username == username).one()
        if user is not None:
            return user
        else:
            raise UserNotFound("User not found")

    @staticmethod
    def get_all_users():
        """
        Obtenir tous les utilisateurs
        """
        return db_session.query(models.User).all()