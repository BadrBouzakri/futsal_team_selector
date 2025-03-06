"""
Tests unitaires pour les modèles de l'application
"""
import pytest
from models import User, Player, Match, MatchTeam, MatchPlayer

def test_user_password_hashing():
    """Test du hachage des mots de passe"""
    u = User(username="test", email="test@example.com")
    u.set_password("testpassword")
    
    # Vérifier que le mot de passe est haché
    assert u.password_hash is not None
    assert u.password_hash != "testpassword"
    
    # Vérifier que le mot de passe est correctement vérifié
    assert u.check_password("testpassword") is True
    assert u.check_password("wrongpassword") is False

def test_player_creation(app):
    """Test de la création d'un joueur"""
    # Créer un joueur
    player = Player(name="TestPlayer", skill_level=75)
    
    # Vérifier les propriétés du joueur
    assert player.name == "TestPlayer"
    assert player.skill_level == 75
    assert player.games_played == 0
    assert player.wins == 0
    assert player.win_rate == 0

def test_player_win_rate(app):
    """Test du calcul du taux de victoire"""
    # Créer un joueur
    player = Player(name="TestPlayer", skill_level=75)
    
    # Cas où le joueur n'a pas encore joué
    assert player.win_rate == 0
    
    # Cas où le joueur a joué mais n'a pas gagné
    player.games_played = 5
    player.wins = 0
    assert player.win_rate == 0
    
    # Cas où le joueur a gagné tous ses matchs
    player.games_played = 5
    player.wins = 5
    assert player.win_rate == 100
    
    # Cas où le joueur a gagné la moitié de ses matchs
    player.games_played = 10
    player.wins = 5
    assert player.win_rate == 50

def test_match_creation(app):
    """Test de la création d'un match"""
    from datetime import datetime
    
    # Créer un match
    match = Match()
    
    # Vérifier les propriétés par défaut
    assert match.winner_team is None
    assert isinstance(match.date, datetime)
    assert len(match.teams) == 0

def test_team_balance_logic(app):
    """Test de la logique d'équilibrage des équipes"""
    from routes.main import balance_teams
    from models import db, Player
    
    with app.app_context():
        # Récupérer tous les joueurs de test
        players = Player.query.all()
        player_ids = [p.id for p in players]
        
        # S'assurer qu'il y a suffisamment de joueurs
        assert len(player_ids) >= 10
        
        # Tester avec 10 joueurs
        team1, team2 = balance_teams(player_ids[:10])
        
        # Vérifier que les équipes sont équilibrées en nombre
        assert len(team1) + len(team2) == 10
        assert abs(len(team1) - len(team2)) <= 1
        
        # Vérifier que les équipes sont équilibrées en niveau
        team1_skill = sum(p.skill_level for p in team1)
        team2_skill = sum(p.skill_level for p in team2)
        
        # La différence de niveau ne devrait pas être trop grande
        assert abs(team1_skill - team2_skill) < 50
