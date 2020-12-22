from blog import app, db_session
from blog.models import User, Post, Comment
from blog.database import UserSchema, PostSchema, CommentSchema
from flask import jsonify, request

"""
Demonstration
"""

@app.route('/posts', methods=['GET'])
def get_posts():
    """
    Obtenir tous les posts
    """

    posts = db_session.query(Post).all()
    posts_schema = PostSchema()
    return jsonify(posts_schema.dump(posts, many=True))

@app.route('/posts/<post_id>', methods=['GET'])
def get_post_by_post_id(post_id):
    """
    Obtenir un post à partir de son id.
    """

    post = db_session.query(Post).get(post_id)
    post_schema = PostSchema()
    return jsonify(post_schema.dump(post))

@app.route('/posts', methods=['POST'])
def create_new_post():
    """
    Creer un nouveau post
    """

    user = db_session.query(User).get("39bbed16-447b-11eb-a062-3c15c2bc38f6")
    post = Post.create_new_post(request.form["title"], request.form["body"], user)
    user.posts.append(post)
    db_session.add(user)
    db_session.commit()
    post_schema = PostSchema()
    return jsonify(post_schema.dump(post))