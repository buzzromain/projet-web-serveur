from blog import app, jwt
from blog.services import (
    PostService,
    UserService,
    UserAuthService,
    CommentService,
    ResourceNotFound, UserNotFound, UnauthorizedUser
) 
from blog.models import User, Post, Comment
from blog.schema import UserProfileSchema, PostSchema, CommentSchema
from blog.utils import connected_user
from flask import jsonify, request, render_template, redirect
from flask_jwt_extended import (
    jwt_required, jwt_optional,
    jwt_refresh_token_required,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies,
    get_raw_jwt,
)
import datetime

"""
Redirige l'utilisateur lorsque le token d'authentification est invalide
"""
@jwt.unauthorized_loader
def invalid_token_callback(expired_token):
    return jsonify({"message": "Unauthorized"}), 401

@jwt.expired_token_loader
def expired_token_callback(expired_token):
    return login_page()


@app.errorhandler(404)
@jwt_optional
def page_not_found(e):
    return render_template(
            '404.html',
            title="Blog",
            description='Projet Web-Serveur',
            current_connected_user = connected_user(get_jwt_identity())
        ), 404

"""
Page d'accueil
"""
@app.route('/', methods=['GET'])
@jwt_optional
def home():
    """
    Page d'accueil
    """
    posts = PostService.get_all_post()
    post_schema = PostSchema(exclude=["comments"])
    return render_template(
        'home.html',
        title="Blog",
        description='Projet Web-Serveur',
        posts=post_schema.dump(posts, many=True),
        current_connected_user = connected_user(get_jwt_identity())
    )

"""
Controleur authentification utilisateur
"""
@app.route('/auth/signup', methods=['POST'])
def register():
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

@app.route('/auth/login', methods=['GET'])
@jwt_optional
def login_page():
    """
    Page connexion d'un utilisateur
    """
    current_connected_user = connected_user(get_jwt_identity())
    if current_connected_user is not None:
        user_id = current_connected_user['id']
        return redirect(f'/users/{user_id}')
    return render_template(
        'login.html',
        title="Blog",
        description='Projet Web-Serveur'
    )

@app.route('/auth/login', methods=['POST'])
def login():
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
    
@app.route('/auth/signup', methods=['GET'])
def signup_page():
    """
    Page d'inscription d'un utilisateur
    """
    current_connected_user = connected_user(get_jwt_identity())
    if current_connected_user is not None:
        user_id = current_connected_user['id']
        return redirect(f'/users/{user_id}')

    return render_template(
        'sign_up.html',
        title="Blog",
        description='Projet Web-Serveur'
    )

@app.route('/auth/logout', methods=['GET'])
def logout():
    """
    Deconnexion d'un utilisateur
    """
    resp = redirect(request.referrer)
    unset_jwt_cookies(resp)
    return resp

@app.route('/auth/refresh_token', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    """
    Rafraichit le token d'authentification
    """
    user_id = get_jwt_identity()
    access_token = UserAuthService.refresh_token(user_id)
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


"""
Controleur utilisateur
"""
@app.route('/users', methods=['GET'])
def get_all_users():
    """
    Obtenir tous les utilisateurs du blog
    """
    
    users = UserService.get_all_users()
    user_schema = UserProfileSchema()
    return jsonify(user_schema.dump(users, many=True))

@app.route('/users/<id>', methods=['GET'])
@jwt_optional
def get_user_by_id(id):
    """
    Obtenir tous les utilisateurs du blog
    """
    try:
        user_profile = UserService.get_user_by_id(id)
        user_schema = UserProfileSchema()
        return render_template(
            'user_profile.html',
            title="Blog",
            description='Projet Web-Serveur',
            user_profile = user_schema.dump(user_profile),
            current_connected_user = connected_user(get_jwt_identity())
        )
    except UserNotFound as e:
        return render_template(
            '404.html',
            title="Blog",
            description='Projet Web-Serveur',
            current_connected_user = connected_user(get_jwt_identity())
        ), 404

"""
Controleur posts
"""

@app.route('/posts/create', methods=['GET'])
@jwt_required
def create_new_post_page():
    """
    Page de création d'un nouveau post
    """
    current_connected_user = connected_user(get_jwt_identity())
    if current_connected_user is None:
        print("Aie")

    return render_template(
        'create_post.html',
        title="Blog",
        description='Projet Web-Serveur',
        current_connected_user = connected_user(get_jwt_identity())
    )

@app.route('/posts', methods=['POST'])
@jwt_required
def create_new_post():
    """
    Creer un nouveau post
    """
    user_id = get_jwt_identity()
    post = PostService.create_post(
        request.form["title"],
        request.form["body"], 
        user_id
    )
    if post is not None:
        return redirect(f'/posts/{post.id}')
    else:
        return str(), 404

@app.route('/posts/<post_id>', methods=['GET'])
@jwt_optional
def get_post_by_id(post_id):
    """
    Obtenir un post à partir de son id.
    """
    try:
        post = PostService.get_post_by_id(post_id)
        post_schema = PostSchema()
        return render_template(
            'post.html',
            title="Blog",
            description='Projet Web-Serveur',
            post=post_schema.dump(post),
            current_connected_user = connected_user(get_jwt_identity())
        )
    except ResourceNotFound as e:
        return render_template(
            '404.html',
            title="Blog",
            description='Projet Web-Serveur',
            current_connected_user = connected_user(get_jwt_identity())
        ), 404

@app.route('/posts', methods=['GET'])
@jwt_optional
def get_all_posts():
    """
    Obtenir tous les posts
    """
    posts = PostService.get_all_post()
    post_schema = PostSchema(exclude=["comments"])
    return render_template(
        'posts.html',
        title="Blog",
        description='Projet Web-Serveur',
        posts=post_schema.dump(posts, many=True),
        current_connected_user = connected_user(get_jwt_identity())
    )

@app.route('/posts/<post_id>', methods=['PUT'])
@jwt_required
def update_post_by_id(post_id):
    """
    Mettre à jour un post
    """
    user_id = get_jwt_identity()
    try:
        content = request.json
        if content is None:
            pass
        new_title = content['title']
        new_body = content['body']
        post = PostService.update_post_by_id(new_title, new_body, post_id, user_id)
        post_schema = PostSchema()
        return jsonify(post_schema.dump(post))
    except ResourceNotFound as e:
        return str(), 404
    except UnauthorizedUser as e:
        return str(), 401

@app.route('/posts/<post_id>', methods=['DELETE'])
@jwt_required
def delete_post_by_id(post_id):
    """
    Supprimer un post
    """
    user_id = get_jwt_identity()
    try:
        post = PostService.delete_post(post_id, user_id)
        return "OK", 200
    except ResourceNotFound as e:
        return str(), 404
    except UnauthorizedUser as e:
        return str(), 401


"""
Controleur commentaires
"""

@app.route('/posts/<post_id>/comments', methods=['POST'])
@jwt_required
def create_comment(post_id):
    """
    Poster un nouveau commentaire
    """
    try:
        user_id = get_jwt_identity()
        comments = CommentService.create_comment(request.form['body'], user_id, post_id)
        comment_schema = CommentSchema()
        return jsonify(comment_schema.dump(comments))
    except ResourceNotFound as e:
        return str(), 404

    
@app.route('/posts/<post_id>/comments/<id>', methods=['GET'])
def get_comment_by_id(post_id, id):
    """
    Obtenir un commentaire à partir de son id
    """
    try:
        comment = CommentService.get_comment_by_id(post_id, id)
        comment_schema = CommentSchema()
        return render_template(
            'comment.html',
            title="Blog",
            description='Projet Web-Serveur',
            comment = comment_schema.dump(comment),
            current_connected_user = connected_user(get_jwt_identity()),
        ), 200
    except ResourceNotFound as e:
        return render_template(
            '404.html',
            title="Blog",
            description='Projet Web-Serveur',
            current_connected_user = connected_user(get_jwt_identity())
        ), 404


@app.route('/posts/<post_id>/comments', methods=['GET'])
@jwt_optional
def get_all_post_comments(post_id):
    """
    Obtenir tous les commentaires d'un post
    """
    comments = CommentService.get_all_post_comments(post_id)
    comment_schema = CommentSchema()
    return render_template(
            'comments.html',
            title="Blog",
            description='Projet Web-Serveur',
            comments = comment_schema.dump(comments, many=True),
            current_connected_user = connected_user(get_jwt_identity()),
            post_id = post_id
    ), 200

@app.route('/posts/<post_id>/comments/<id>', methods=['PUT'])
@jwt_required
def update_comment(post_id, id):
    """
    Obtenir tous les commentaires d'un post
    """
    try:
        user_id = get_jwt_identity()
        content = request.json
        if content is None:
            return str(), 400
        new_body = content['body']
        comments = CommentService.update_comment(new_body, post_id, id, user_id)
        comment_schema = CommentSchema(exclude=["post"])
        return jsonify(comment_schema.dump(comments))
    except ResourceNotFound as e:
        return str(), 404
    except UnauthorizedUser as e:
        return str(), 401

@app.route('/posts/<post_id>/comments/<id>', methods=['DELETE'])
@jwt_required
def delete_comment(post_id, id):
    """
    Supprimer un commentaire
    """
    try:
        user_id = get_jwt_identity()
        CommentService.delete_comment(post_id, id, user_id)
        return str(), 204
    except ResourceNotFound as e:
        return str(), 204
    except UnauthorizedUser as e:
        return str(), 401