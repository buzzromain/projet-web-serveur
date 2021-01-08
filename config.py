import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(app_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = False
    JWT_SECRET_KEY = 'l]Q3+J;V9cLy9*ytPwq#2?0d;rb\Xf9wSd2a8sI.o6NXlxrw2;'
    JWT_BLACKLIST_ENABLED = False
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SECURE = False