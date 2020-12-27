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

from blog import views