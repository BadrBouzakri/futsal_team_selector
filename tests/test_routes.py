"""
Tests unitaires pour les routes de l'application
"""
import pytest
from flask import session
from models import User, Player

def test_home_page(client):
    """Test de la page d'accueil"""
    response = client.get('/')
    
    # Vérifier que la page se charge correctement
    assert response.status_code == 200
    assert b'Futsal Team Selector' in response.data

def test_login_page(client):
    """Test de la page de connexion"""
    response = client.get('/auth/login')
    
    # Vérifier que la page se charge correctement
    assert response.status_code == 200
    assert b'Connexion' in response.data
    assert b'Nom d\'utilisateur' in response.data
    assert b'Mot de passe' in response.data

def test_login_logout(client, app):
    """Test de la connexion et déconnexion"""
    # Tester la connexion avec des identifiants valides
    response = client.post('/auth/login', data={
        'username': 'testadmin',
        'password': 'testpass',
        'remember': False
    }, follow_redirects=True)
    
    # Vérifier que la connexion a réussi
    assert response.status_code == 200
    
    # Tester la déconnexion
    response = client.get('/auth/logout', follow_redirects=True)
    
    # Vérifier que la déconnexion a réussi
    assert response.status_code == 200

def test_invalid_login(client):
    """Test de la connexion avec des identifiants invalides"""
    response = client.post('/auth/login', data={
        'username': 'wronguser',
        'password': 'wrongpass',
        'remember': False
    }, follow_redirects=True)
    
    # Vérifier que la connexion a échoué
    assert response.status_code == 200
    assert b'Identifiant ou mot de passe incorrect' in response.data

def test_protected_admin_route(client):
    """Test d'accès à une route protégée sans être connecté"""
    response = client.get('/admin/', follow_redirects=True)
    
    # Vérifier que l'accès est refusé et redirigé vers la page de connexion
    assert response.status_code == 200
    assert b'Connexion' in response.data

def test_team_creation(client, app):
    """Test de la création d'équipes"""
    with app.app_context():
        # Récupérer les IDs des joueurs de test
        players = Player.query.limit(10).all()
        player_ids = [str(p.id) for p in players]
        
        # Créer les équipes
        response = client.post('/', data={
            'players': player_ids
        }, follow_redirects=True)
        
        # Vérifier que les équipes sont créées et affichées
        assert response.status_code == 200
        assert b'quipes g' in response.data  # 'Équipes générées' en français
        
        # Vérifier que les données de session sont correctes
        with client.session_transaction() as sess:
            assert 'team1_ids' in sess
            assert 'team2_ids' in sess
            assert len(sess['team1_ids']) + len(sess['team2_ids']) == 10

def test_teams_page_without_generation(client):
    """Test d'accès à la page des équipes sans avoir généré d'équipes"""
    response = client.get('/teams', follow_redirects=True)
    
    # Vérifier que l'utilisateur est redirigé vers la page d'accueil
    assert response.status_code == 200
    assert b'Les équipes n\'ont pas' in response.data

def test_api_endpoints(client, app):
    """Test des endpoints API"""
    # Test de l'endpoint pour obtenir la liste des joueurs
    response = client.get('/api/players')
    
    # Vérifier que la réponse est correcte
    assert response.status_code == 200
    assert response.is_json
    
    # Vérifier que la liste des joueurs est retournée
    players = response.get_json()
    assert isinstance(players, list)
    assert len(players) > 0
    assert 'name' in players[0]
    assert 'skill_level' in players[0]

def test_random_teams_api(client, app):
    """Test de l'API pour générer des équipes aléatoires"""
    with app.app_context():
        # Récupérer les IDs des joueurs de test
        players = Player.query.limit(10).all()
        player_ids = [p.id for p in players]
        
        # Appeler l'API
        response = client.post('/api/random-teams', 
                             json={'player_ids': player_ids},
                             content_type='application/json')
        
        # Vérifier que la réponse est correcte
        assert response.status_code == 200
        assert response.is_json
        
        # Vérifier que les équipes sont retournées
        data = response.get_json()
        assert 'team1' in data
        assert 'team2' in data
        assert len(data['team1']) + len(data['team2']) == 10

def test_admin_player_management(client, app):
    """Test de la gestion des joueurs dans l'administration"""
    # Se connecter en tant qu'administrateur
    client.post('/auth/login', data={
        'username': 'testadmin',
        'password': 'testpass'
    })
    
    # Tester l'ajout d'un joueur
    response = client.post('/admin/players/add', data={
        'name': 'NewTestPlayer',
        'skill_level': '85'
    }, follow_redirects=True)
    
    # Vérifier que le joueur a été ajouté
    assert response.status_code == 200
    
    # Vérifier que le joueur existe dans la base de données
    with app.app_context():
        player = Player.query.filter_by(name='NewTestPlayer').first()
        assert player is not None
        assert player.skill_level == 85
