import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(app_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopementConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass