from blog import jwt
from blog.services import (UserService, UserAuthService,
ResourceNotFound, UserNotFound, UnauthorizedUser
) 
from blog.models import User
from blog.schema import UserProfileSchema
from blog.utils import connected_user
from flask import jsonify, request, render_template, redirect, Blueprint

from flask_jwt_extended import (
    jwt_required, jwt_optional,
    jwt_refresh_token_required,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from flask.views import MethodView

"""
Controleur authentification utilisateur
"""
auth_blueprint = Blueprint('auth', __name__)

class Register(MethodView):
    @jwt_optional
    def get(self):
        """
        Page d'inscription d'un utilisateur
        """
        current_connected_user = connected_user(get_jwt_identity())
        if current_connected_user is not None:
            user_id = current_connected_user['id']
            return redirect(f'/users/{user_id}')

        return render_template(
            'sign_up.html',
            title="S'inscrire",
        )

    def post(self):
        """
        Creer un nouvel utilisateur
        """
        try:
            tokens = UserAuthService.register(request.form["username"], request.form["password"])
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]
            resp = redirect('/')
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp
        except Exception as e:
            return redirect('/auth/register')

class Login(MethodView):
    @jwt_optional
    def get(self):
        """
        Page connexion d'un utilisateur
        """
        current_connected_user = connected_user(get_jwt_identity())
        if current_connected_user is not None:
            user_id = current_connected_user['id']
            return redirect(f'/users/{user_id}')
        return render_template(
            'login.html',
            title="Se connecter",
            label="Connectez-vous"
        )

    def post(self):
        """
        Connexion d'un utilisateur
        """
        try:
            tokens = UserAuthService.login(request.form["username"], request.form["password"])
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]
            resp = redirect('/')
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp
        except Exception as e:
            return redirect('/auth/login')
    
class Logout(MethodView):
    def get(self):
        """
        Deconnexion d'un utilisateur
        """
        resp = redirect(request.referrer)
        unset_jwt_cookies(resp)
        return resp

class Administration(MethodView):
    @jwt_required
    def get(self):
        """
        Page d'administration du site
        """
        users = UserService.get_all_users()
        user_schema = UserProfileSchema()
        return render_template(
            'administration.html',
            title="Administration",
            current_connected_user = connected_user(get_jwt_identity()),
            users = user_schema.dump(users, many=True)
        ), 200

class RefreshToken(MethodView):
    @jwt_refresh_token_required
    def get(self):
        """
        Rafraichit le token d'authentification
        """
        user_id = get_jwt_identity()
        access_token = UserAuthService.refresh_token(user_id)
        resp = redirect(request.url)
        set_access_cookies(resp, access_token)
        return resp, 200

registration_view = Register.as_view('register')
login_view = Login.as_view('login')
logout_view = Logout.as_view('logout')
refresh_token_view = RefreshToken.as_view('refresh_token')
administration_view = Administration.as_view('administration')

auth_blueprint.add_url_rule(
    '/auth/signup',
    view_func=registration_view,
    methods=['GET', 'POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['GET', 'POST']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['GET']
)

auth_blueprint.add_url_rule(
    '/admin',
    view_func=administration_view,
    methods=['GET']
)

auth_blueprint.add_url_rule(
    '/auth/refresh_token',
    view_func=refresh_token_view,
    methods=['POST']
)