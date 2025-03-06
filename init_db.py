#!/usr/bin/env python
"""
Script d'initialisation de la base de données pour Futsal Team Selector
- Crée la base de données si elle n'existe pas
- Ajoute un administrateur par défaut
- Charge les joueurs par défaut
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Ajout du répertoire parent au path pour permettre l'importation des modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from models import db, User, Player, Match, MatchTeam, MatchPlayer
from config import config

def init_database(app, create_sample_data=False):
    """Initialise la base de données avec des données de base"""
    with app.app_context():
        # Créer les tables
        db.create_all()
        
        # Ajouter un administrateur par défaut
        if not User.query.filter_by(username=app.config['ADMIN_USERNAME']).first():
            print("Création de l'utilisateur administrateur...")
            admin = User(
                username=app.config['ADMIN_USERNAME'],
                email=app.config['ADMIN_EMAIL'],
                is_admin=True
            )
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            db.session.commit()
            print("Utilisateur administrateur créé avec succès")
        else:
            print("L'utilisateur administrateur existe déjà")
        
        # Ajouter les joueurs par défaut si aucun n'existe
        if Player.query.count() == 0:
            print("Ajout des joueurs par défaut...")
            default_players = {
                "Badr": 70, "Aymane": 90, "Yassine": 80, "Mounir": 60,
                "Luis": 50, "Mehdi": 90, "Tano": 90, "Elie": 85,
                "Jeremy": 80, "Abdelilah": 65, "Malik": 75, "Abdel": 80,
                "Houcine": 70, "Saber": 80, "Sandra": 65, "Nadir": 80,
                "Jalal": 70, "Younes": 80, "Naim": 70, "Meh": 80, "Mehdi le r": 90,
                "Vincent": 70, "Kevin": 70, "Saad": 80, "Aziz": 90, "Abdallah": 70
            }
            
            for name, skill in default_players.items():
                player = Player(name=name, skill_level=skill)
                db.session.add(player)
            
            db.session.commit()
            print(f"{len(default_players)} joueurs ajoutés avec succès")
        else:
            print("Des joueurs existent déjà dans la base de données")
        
        # Créer des données d'exemple pour le développement
        if create_sample_data:
            create_sample_matches(app)

def create_sample_matches(app):
    """Crée des données d'exemple pour les matchs"""
    with app.app_context():
        # Vérifier si des matchs existent déjà
        if Match.query.count() > 0:
            print("Des matchs existent déjà dans la base de données")
            return
        
        print("Création de matchs d'exemple...")
        
        # Récupérer tous les joueurs
        players = Player.query.all()
        
        if len(players) < 10:
            print("Pas assez de joueurs pour créer des matchs d'exemple")
            return
        
        # Créer 10 matchs sur les 30 derniers jours
        for i in range(10):
            # Date du match (répartie sur les 30 derniers jours)
            match_date = datetime.now() - timedelta(days=i*3)
            
            # Créer un match
            match = Match(date=match_date)
            db.session.add(match)
            db.session.flush()  # Pour obtenir l'ID du match
            
            # Sélectionner 10 joueurs aléatoirement
            selected_players = random.sample(players, 10)
            
            # Trier par niveau
            sorted_players = sorted(selected_players, key=lambda p: p.skill_level, reverse=True)
            
            # Diviser en deux équipes équilibrées
            team1, team2 = [], []
            team1_score, team2_score = 0, 0
            
            for player in sorted_players:
                if team1_score <= team2_score:
                    team1.append(player)
                    team1_score += player.skill_level
                else:
                    team2.append(player)
                    team2_score += player.skill_level
            
            # Créer les équipes
            team1_record = MatchTeam(match_id=match.id, team_number=1)
            team2_record = MatchTeam(match_id=match.id, team_number=2)
            
            db.session.add(team1_record)
            db.session.add(team2_record)
            db.session.flush()
            
            # Ajouter les joueurs aux équipes
            for player in team1:
                db.session.add(MatchPlayer(team_id=team1_record.id, player_id=player.id))
            
            for player in team2:
                db.session.add(MatchPlayer(team_id=team2_record.id, player_id=player.id))
            
            # Définir un gagnant pour les matchs terminés (80% des matchs)
            if i < 8:  # 8 sur 10 matchs ont un résultat
                # Déterminer le gagnant (légèrement favoriser l'équipe avec le score total le plus élevé)
                if random.random() < 0.6:  # 60% de chance que l'équipe la plus forte gagne
                    winner = 1 if team1_score > team2_score else 2
                else:
                    winner = 2 if team1_score > team2_score else 1
                    
                match.winner_team = winner
                
                # Mettre à jour les statistiques des joueurs
                winners = team1 if winner == 1 else team2
                for player in selected_players:
                    player.games_played += 1
                    if player in winners:
                        player.wins += 1
            
        db.session.commit()
        print("10 matchs d'exemple ont été créés avec succès")

def main():
    """Fonction principale"""
    # Détecter l'environnement à partir des variables d'environnement
    env = os.environ.get('FLASK_ENV', 'development')
    create_samples = '--with-samples' in sys.argv
    
    # Créer l'application avec la configuration appropriée
    app = create_app(env)
    
    # Initialiser la base de données
    try:
        init_database(app, create_sample_data=create_samples)
        print("Base de données initialisée avec succès")
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
