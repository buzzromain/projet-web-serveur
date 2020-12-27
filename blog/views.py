from blog import app
from blog.services import PostService, UserService, UserAuthService, CommentService
from blog.models import User, Post, Comment
from blog.schema import UserProfileSchema, PostSchema, CommentSchema
from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies,
    get_raw_jwt
)
"""
Controleurs des posts
"""
@app.route('/posts', methods=['POST'])
def create_new_post():
    """
    Creer un nouveau post
    """

    post = PostService.create_post(
        request.form["title"],
        request.form["body"], 
        request.form["author_id"]
    )
    post_schema = PostSchema()
    return jsonify(post_schema.dump(post))

@app.route('/posts/<post_id>', methods=['GET'])
def get_post_by_id(post_id):
    """
    Obtenir un post à partir de son id.
    """

    post = PostService.get_post_by_id(post_id)
    post_schema = PostSchema()
    return jsonify(post_schema.dump(post))

@app.route('/posts', methods=['GET'])
def get_all_posts():
    """
    Obtenir tous les posts
    """
    posts = PostService.get_all_post()
    post_schema = PostSchema()
    return jsonify(post_schema.dump(posts, many=True))

@app.route('/posts/<post_id>', methods=['DELETE'])
def delete_post_by_id(post_id):
    """
    Supprimer un post
    """

    post = PostService.delete_post(post_id)
    post_schema = PostSchema()
    return jsonify(post_schema.dump(post))

"""
Controleur pour les utilisateurs
"""
@app.route('/auth/register', methods=['POST'])
def register_user():
    """
    Creer un nouvel utilisateur
    """

    tokens = UserAuthService.register(request.form["username"], request.form["password"])
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    resp = jsonify({'register': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp

@app.route('/auth/login', methods=['POST'])
def login_user():
    """
    Creer un nouvel utilisateur
    """

    tokens = UserAuthService.login(request.form["username"], request.form["password"])
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp

@app.route('/test_jwt', methods=['GET'])
@jwt_required
def test_jwt():
    """
    Test de l'authentification utilisateur
    """
    user_id = get_jwt_identity()
    user = UserService.get_user_by_id(user_id)
    user_schema = UserProfileSchema()
    
    return jsonify(user_schema.dump(user))


@app.route('/users', methods=['GET'])
def get_all_users():
    """
    Creer un nouveau post
    """
    
    users = UserService.get_all_users()
    user_schema = UserProfileSchema()
    return jsonify(user_schema.dump(users, many=True))

"""
Controleur pour les commentaires
"""

@app.route('/posts/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    """
    Poster un nouveau commentaire
    """
    
    comments = CommentService.create_comment(request.form['body'], request.form['author_id'], post_id)
    comment_schema = CommentSchema()
    return jsonify(comment_schema.dump(comments))
    
@app.route('/posts/<post_id>/comments/<id>', methods=['GET'])
def get_comment_by_id(post_id, id):
    """
    Obtenir un commentaire à partir de son id
    """
    
    comments = CommentService.get_comment_by_id(post_id, id)
    comment_schema = CommentSchema(exclude=["post"])
    return jsonify(comment_schema.dump(comments))

@app.route('/posts/<post_id>/comments', methods=['GET'])
def get_all_post_comments(post_id):
    """
    Obtenir tous les commentaires d'un post
    """
    
    comments = CommentService.get_all_post_comments(post_id)
    comment_schema = CommentSchema(exclude=["post"])
    return jsonify(comment_schema.dump(comments, many=True))

@app.route('/posts/<post_id>/comments/<id>', methods=['DELETE'])
def delete_comment(post_id, id):
    """
    Obtenir tous les commentaires d'un post
    """
    
    comments = CommentService.delete_comment(post_id, id)
    comment_schema = CommentSchema(exclude=["post"])
    return jsonify(comment_schema.dump(comments))