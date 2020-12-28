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
from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies,
    get_raw_jwt,
)

"""
Redirige l'utilisateur lorsque le token d'authentification est invalide
"""
@jwt.unauthorized_loader
def my_invalid_token_callback(expired_token):
    return jsonify({"message": "Unauthorized"}), 401


"""
Controleur authentification utilisateur
"""
@app.route('/auth/signup', methods=['POST'])
def register():
    """
    Creer un nouvel utilisateur
    """

    tokens = UserAuthService.register(request.form["username"], request.form["password"])
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    resp = jsonify({'register': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

@app.route('/auth/login', methods=['POST'])
def login():
    """
    Connexion d'un utilisateur
    """
    try:
        tokens = UserAuthService.login(request.form["username"], request.form["password"])
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        resp = jsonify({'login': True})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200
    except Exception as e:
        return jsonify({'login': False}), 401
    

@app.route('/auth/logout', methods=['POST'])
def logout():
    """
    Deconnexion d'un utilisateur
    """
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

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


@app.route('/test_jwt', methods=['GET'])
@jwt_required
def test_jwt():
    """
    Test de l'authentification utilisateur
    Renvoie le profil de l'utilisateur connecté
    """
    user_id = get_jwt_identity()
    user = UserService.get_user_by_id(user_id)
    user_schema = UserProfileSchema(exclude=["posts"])
    
    return jsonify(user_schema.dump(user))

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
def get_user_by_id(id):
    """
    Obtenir tous les utilisateurs du blog
    """
    try:
        user = UserService.get_user_by_id(id)
        user_schema = UserProfileSchema()
        return jsonify(user_schema.dump(user))
    except UserNotFound as e:
        return jsonify({}), 404

"""
Controleur posts
"""

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
    post_schema = PostSchema()
    return jsonify(post_schema.dump(post))

@app.route('/posts/<post_id>', methods=['GET'])
def get_post_by_id(post_id):
    """
    Obtenir un post à partir de son id.
    """
    try:
        post = PostService.get_post_by_id(post_id)
        post_schema = PostSchema()
        return jsonify(post_schema.dump(post))
    except ResourceNotFound as e:
        return str(), 404

@app.route('/posts', methods=['GET'])
def get_all_posts():
    """
    Obtenir tous les posts
    """
    posts = PostService.get_all_post()
    post_schema = PostSchema()
    return jsonify(post_schema.dump(posts, many=True))

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
        post_schema = PostSchema()
        return jsonify(post_schema.dump(post))
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
        comment_schema = CommentSchema(exclude=["post"])
        return jsonify(comment_schema.dump(comment))
    except ResourceNotFound as e:
        return str(), 404


@app.route('/posts/<post_id>/comments', methods=['GET'])
def get_all_post_comments(post_id):
    """
    Obtenir tous les commentaires d'un post
    """
    
    comments = CommentService.get_all_post_comments(post_id)
    comment_schema = CommentSchema(exclude=["post"])
    return jsonify(comment_schema.dump(comments, many=True))

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
            pass
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
        comment = CommentService.delete_comment(post_id, id, user_id)
        comment_schema = CommentSchema(exclude=["post"])
        return jsonify(comment_schema.dump(comment))
    except ResourceNotFound as e:
        return str(), 404
    except UnauthorizedUser as e:
        return str(), 401