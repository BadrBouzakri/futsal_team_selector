import os
from datetime import timedelta

class Config:
    """Configuration de base pour l'application"""
    
    # Clé secrète pour les sessions (à changer en production)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey-change-in-production'
    
    # Configuration de l'application
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5050))
    
    # Configuration des sessions
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuration de l'historique
    MAX_HISTORY_ITEMS = int(os.environ.get('MAX_HISTORY_ITEMS', 20))
    HISTORY_FILE = os.environ.get('HISTORY_FILE', 'teams_history.json')
    DATA_DIR = os.environ.get('DATA_DIR', 'data')
    
    # Configuration de l'administration
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
    
    # Configuration des équipes
    TEAM_SIZE = int(os.environ.get('TEAM_SIZE', 5))
    TOTAL_PLAYERS = int(os.environ.get('TOTAL_PLAYERS', 10))
    
    # Niveaux de compétence
    SKILL_LEVELS = {
        'excellent': {'min': 80, 'max': 100, 'color': '#4CAF50'},
        'good': {'min': 65, 'max': 79, 'color': '#FF9800'},
        'average': {'min': 0, 'max': 64, 'color': '#f44336'}
    }
    
    # Configuration de l'équilibrage
    BALANCE_THRESHOLDS = {
        'excellent': 90,
        'good': 75,
        'poor': 0
    }

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    DEBUG = True

# Dictionnaire des configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
