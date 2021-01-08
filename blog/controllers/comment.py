from blog import jwt
from blog.services import CommentService, ResourceNotFound, UserNotFound, UnauthorizedUser
from blog.models import Comment
from blog.schema import CommentSchema
from blog.utils import connected_user
from flask import jsonify, request, render_template, redirect, Blueprint

from flask_jwt_extended import (
    jwt_required, jwt_optional,
    get_jwt_identity
)

from flask.views import MethodView

comment_blueprint = Blueprint('comment', __name__)

"""
Controleur commentaires
"""

class CommentList(MethodView):

    @jwt_optional
    def get(self, post_id):
        """
        Obtenir tous les commentaires d'un post
        """
        comments = CommentService.get_all_post_comments(post_id)
        comment_schema = CommentSchema()
        return render_template(
                'comments.html',
                title="Commentaires",
                comments = comment_schema.dump(comments, many=True),
                current_connected_user = connected_user(get_jwt_identity()),
                post_id = post_id
        ), 200

    @jwt_required
    def post(self, post_id):
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

class Comment(MethodView):    
    @jwt_optional
    def get(self, post_id, id):
        """
        Obtenir un commentaire à partir de son id
        """
        try:
            comment = CommentService.get_comment_by_id(post_id, id)
            comment_schema = CommentSchema()
            return render_template(
                'comment.html',
                title="Commentaire",
                comment = comment_schema.dump(comment),
                current_connected_user = connected_user(get_jwt_identity()),
            ), 200
        except ResourceNotFound as e:
            return render_template(
                '404.html',
                title="Commentaire non trouvé",
                current_connected_user = connected_user(get_jwt_identity())
            ), 404

    @jwt_required
    def put(self, post_id, id):
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

    @jwt_required
    def delete(self, post_id, id):
        """
        Supprimer un commentaire
        """
        try:
            user_id = get_jwt_identity()
            CommentService.delete_comment(post_id, id, user_id)
            return "OK", 204
        except ResourceNotFound as e:
            return str(), 204
        except UnauthorizedUser as e:
            return str(), 401


comment_list_view = CommentList.as_view('comment_list')
comment_view = Comment.as_view('comment')

comment_blueprint.add_url_rule(
    '/posts/<post_id>/comments',
    view_func=comment_list_view,
    methods=['GET', 'POST']
)

comment_blueprint.add_url_rule(
    '/posts/<post_id>/comments/<id>',
    view_func=comment_view,
    methods=['GET', 'PUT', 'DELETE']
)

