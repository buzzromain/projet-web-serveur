from config import BaseConfig
from flask import Flask
from blog.data_access import db_session, start_mappers, init_db
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(BaseConfig)
jwt = JWTManager(app)

init_db()
start_mappers()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

from blog.controllers.auth import auth_blueprint
from blog.controllers.user import user_blueprint
from blog.controllers.post import post_blueprint
from blog.controllers.comment import comment_blueprint
from blog.controllers.home import home_blueprint
from blog.controllers import error
app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(post_blueprint)
app.register_blueprint(comment_blueprint)
app.register_blueprint(home_blueprint)