import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env s'il existe
load_dotenv()

class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-muito-secreta-e-dificil-de-adivinhar'
    
    # Configuration de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Autres configurations générales
    DEBUG = False
    TESTING = False
    
    # Configuration des emails
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Préfixe du titre des emails
    MAIL_SUBJECT_PREFIX = '[Futsal Team]'
    
    # Administrateur par défaut
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///data/dev-football.db'

class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Configuration pour la production"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///data/football.db'
    
    # Configuration de sécurité
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    
    @classmethod
    def init_app(cls, app):
        # Log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

# Dictionnaire des configurations disponibles
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    
    'default': DevelopmentConfig
}
