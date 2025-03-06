"""
Configuration des fixtures pour les tests unitaires
"""
import os
import sys
import pytest

# Ajouter le répertoire parent au path pour permettre l'importation des modules
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from app import create_app
from models import db, User, Player

@pytest.fixture
def app():
    """Fixture pour créer une instance de l'application pour les tests"""
    # Créer l'application avec la configuration de test
    app = create_app('testing')
    
    # Créer un contexte d'application
    with app.app_context():
        # Créer les tables
        db.create_all()
        
        # Ajouter des données de test
        test_user = User(username='testadmin', email='test@example.com', is_admin=True)
        test_user.set_password('testpass')
        db.session.add(test_user)
        
        # Ajouter quelques joueurs de test
        test_players = [
            Player(name="TestPlayer1", skill_level=75),
            Player(name="TestPlayer2", skill_level=80),
            Player(name="TestPlayer3", skill_level=60),
            Player(name="TestPlayer4", skill_level=85),
            Player(name="TestPlayer5", skill_level=70),
            Player(name="TestPlayer6", skill_level=90),
            Player(name="TestPlayer7", skill_level=65),
            Player(name="TestPlayer8", skill_level=75),
            Player(name="TestPlayer9", skill_level=85),
            Player(name="TestPlayer10", skill_level=80),
        ]
        
        for player in test_players:
            db.session.add(player)
            
        db.session.commit()
        
        yield app
        
        # Nettoyer la base de données après les tests
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Fixture pour créer un client de test"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Fixture pour créer un testeur de ligne de commande"""
    return app.test_cli_runner()
