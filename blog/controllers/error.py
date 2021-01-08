from blog import jwt, app
from blog.utils import connected_user
from flask import render_template, redirect
from flask_jwt_extended import jwt_optional, get_jwt_identity

from jwt.exceptions import ExpiredSignatureError

@jwt.unauthorized_loader
def invalid_token_callback(expired_token):
    return render_template(
            'error_page.html',
            title="401",
            label="401. Unauthorized",
            current_connected_user = connected_user(get_jwt_identity())
        ), 401


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    return render_template(
            'login.html',
            title="Se connecter",
            current_connected_user = connected_user(get_jwt_identity()),
            label="Reconnectez-vous"
        ), 200

@app.errorhandler(404)
@jwt_optional
def page_not_found(e):
    return render_template(
            'error_page.html',
            title="404",
            label="404. Not Found",
            current_connected_user = connected_user(get_jwt_identity())
        ), 404

@app.errorhandler(500)
@jwt_optional
def page_not_found(e):
    return render_template(
            'error_page.html',
            title="500",
            label="500. Internal Server Error",
            current_connected_user = connected_user(get_jwt_identity())
        ), 404

@app.errorhandler(ExpiredSignatureError)
def _handle_expired_signature(error):
    return render_template(
            'login.html',
            title="Se connecter",
            current_connected_user = connected_user(get_jwt_identity()),
            label="Reconnectez-vous"
        ), 200
    return redirect('/auth/login')
