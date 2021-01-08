from blog import jwt
from blog.services import PostService, ResourceNotFound, UserNotFound, UnauthorizedUser

from blog.models import User, Post, Comment
from blog.schema import PostSchema
from blog.utils import connected_user
from flask import jsonify, request, render_template, redirect, Blueprint

from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity

from flask.views import MethodView

"""
Controleur posts
"""

post_blueprint = Blueprint('post', __name__)

class CreatePost(MethodView):

    @jwt_required
    def get(self):
        """
        Page de création d'un nouveau post
        """
        current_connected_user = connected_user(get_jwt_identity())

        return render_template(
            'create_post.html',
            title="Créer un nouvel article",
            current_connected_user = connected_user(get_jwt_identity())
        )

class PostList(MethodView):

    @jwt_optional
    def get(self):
        """
        Obtenir tous les posts
        """
        posts = PostService.get_all_post()
        post_schema = PostSchema(exclude=["comments"])
        return render_template(
            'posts.html',
            title="Articles",
            posts=post_schema.dump(posts, many=True),
            current_connected_user = connected_user(get_jwt_identity())
        )

    @jwt_required
    def post(self):
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
            return str(), 400

class Post(MethodView):

    @jwt_optional
    def get(self, post_id):
        """
        Obtenir un post à partir de son id.
        """
        try:
            post = PostService.get_post_by_id(post_id)
            post_schema = PostSchema()
            return render_template(
                'post.html',
                title=post.title,
                post=post_schema.dump(post),
                current_connected_user = connected_user(get_jwt_identity())
            )
        except ResourceNotFound as e:
            return render_template(
                '404.html',
                title="Article non trouvé",
                current_connected_user = connected_user(get_jwt_identity())
            ), 404

    @jwt_required
    def put(self, post_id):
        """
        Mettre à jour un post
        """
        user_id = get_jwt_identity()
        try:
            content = request.json
            if content is None:
                return str(), 400
            new_title = content['title']
            new_body = content['body']
            post = PostService.update_post_by_id(new_title, new_body, post_id, user_id)
            post_schema = PostSchema()
            return jsonify(post_schema.dump(post))
        except ResourceNotFound as e:
            return str(), 404
        except UnauthorizedUser as e:
            return str(), 401

    @jwt_required
    def delete(self, post_id):
        """
        Supprimer un post
        """
        user_id = get_jwt_identity()
        try:
            post = PostService.delete_post(post_id, user_id)
            return "OK", 200
        except ResourceNotFound as e:
            return str(), 204
        except UnauthorizedUser as e:
            return str(), 401


create_post_view = CreatePost.as_view('create_post')
post_list_view = PostList.as_view('post_list')
post_view = Post.as_view('post')

post_blueprint.add_url_rule(
    '/posts/create',
    view_func=create_post_view,
    methods=['GET']
)

post_blueprint.add_url_rule(
    '/posts',
    view_func=post_list_view,
    methods=['GET', 'POST']
)

post_blueprint.add_url_rule(
    '/posts/<post_id>',
    view_func=post_view,
    methods=['GET', 'PUT', 'DELETE']
)