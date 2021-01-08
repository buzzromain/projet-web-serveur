from blog import jwt
from blog.services import PostService, ResourceNotFound, UserNotFound, UnauthorizedUser

from blog.models import Post
from blog.schema import PostSchema
from blog.utils import connected_user
from flask import render_template, redirect, Blueprint

from flask_jwt_extended import jwt_optional, get_jwt_identity

from flask.views import MethodView

home_blueprint = Blueprint('home', __name__)

class Home(MethodView):
    @jwt_optional
    def get(self):
        """
        Page d'accueil
        """
        posts = PostService.get_all_post()
        post_schema = PostSchema(exclude=["comments"])
        return render_template(
            'home.html',
            title="Accueil",
            posts=post_schema.dump(posts, many=True),
            current_connected_user = connected_user(get_jwt_identity())
        )

class About(MethodView):
    @jwt_optional
    def get(self):
        """
        Page a propos
        """

        return render_template(
            'about.html',
            title="A propos",
            current_connected_user = connected_user(get_jwt_identity())
        )

home_view = Home.as_view('home')
about_view = About.as_view('about')

home_blueprint.add_url_rule(
    '/',
    view_func=home_view,
    methods=['GET']
)

home_blueprint.add_url_rule(
    '/about',
    view_func=about_view,
    methods=['GET']
)