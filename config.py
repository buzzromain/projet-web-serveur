import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    pass

class DevelopementConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass