from config import BaseConfig
from flask import Flask
from blog.database import db_session, start_mappers, init_db

app = Flask(__name__)
app.config.from_object(BaseConfig)
app.config['JSON_SORT_KEYS'] = False

init_db()
start_mappers()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

from blog import views