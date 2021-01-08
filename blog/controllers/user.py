from blog import jwt
from blog.services import UserService, ResourceNotFound, UserNotFound, UnauthorizedUser

from blog.models import User
from blog.schema import UserProfileSchema
from blog.utils import connected_user
from flask import jsonify, request, render_template, redirect, Blueprint

from flask_jwt_extended import (
    jwt_required, jwt_optional,
    jwt_refresh_token_required,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies,
    get_raw_jwt,
)
import datetime
from jwt.exceptions import ExpiredSignatureError
from flask.views import MethodView


"""
Controleurs utilisateur
"""

user_blueprint = Blueprint('user', __name__)

class UserList(MethodView):
    def get(self):
        """
        Obtenir tous les utilisateurs du blog
        """
        
        users = UserService.get_all_users()
        user_schema = UserProfileSchema()
        return jsonify(user_schema.dump(users, many=True))

class User(MethodView):
    @jwt_optional
    def get(self, id):
        """
        Obtenir tous les utilisateurs du blog
        """
        try:
            user_profile = UserService.get_user_by_id(id)
            user_schema = UserProfileSchema()
            return render_template(
                'user_profile.html',
                title="Profil de " + user_profile.username,
                user_profile = user_schema.dump(user_profile),
                current_connected_user = connected_user(get_jwt_identity())
            )
        except UserNotFound as e:
            return render_template(
                'error_page.html',
                title="Utilisateur non trouvé",
                current_connected_user = connected_user(get_jwt_identity())
            ), 404

    @jwt_required
    def patch(self, id):
        """
        Mettre à jour un utilisateur du blog
        """
        json_patch = request.json
        if json_patch is None:
            return str(), 400
        try:
            user = UserService.update_user(get_jwt_identity(), id, json_patch)
            user_schema = UserProfileSchema(exclude=['posts'])
            return jsonify(user_schema.dump(user))

        except UserNotFound as e:
            return str(), 404

        except UnauthorizedUser as e:
            return str(), 401

user_list_view = UserList.as_view('user_list')
user_view = User.as_view('user')

user_blueprint.add_url_rule(
    '/users',
    view_func=user_list_view,
    methods=['GET']
)

user_blueprint.add_url_rule(
    '/users/<id>',
    view_func=user_view,
    methods=['GET', 'PATCH']
)