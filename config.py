import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///secureshop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
class SecureConfig(Config):
    DEBUG = False

class LabConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

config_by_name = dict(
    secure=SecureConfig,
    lab=LabConfig
)
