import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    """
    Config object containing default configuriation
    """
    TESTING = False
    SESSION_COOKIE_NAME = "session"
    
    
class ProductionConfig(Config):
    """
    ProductionConfig class containing production configuriation, extending Config object
    """
    SECRET_KEY = os.environ.get("FLASK_PRODUCTION_SECRET_KEY")
    
    
class DevelopmentConfig(Config):
    """
    DevelopmentConfig class containing development configuration, extending Config object
    """
    SECRET_KEY = os.environ.get("FLASK_DEVELOPMENT_SECRET_KEY")
    SESSION_COOKIE_NAME = "dev_session"

class TestingConfig(DevelopmentConfig):
    """
    TesttingConfig class containing development configuration, extending Config object
    """
    TESTING = True
    SESSION_COOKIE_NAME = "test_session"