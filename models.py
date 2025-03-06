import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Player(db.Model):
    """Modèle pour les joueurs"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    skill_level = db.Column(db.Integer, nullable=False)  # Score de 0 à 100
    games_played = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Player {self.name}>'
    
    @property
    def win_rate(self):
        if self.games_played == 0:
            return 0
        return round((self.wins / self.games_played) * 100, 1)

class Match(db.Model):
    """Modèle pour stocker l'historique des matchs"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    winner_team = db.Column(db.Integer, nullable=True)  # 1 ou 2, peut être NULL si match nul
    
    # Relations
    teams = db.relationship('MatchTeam', backref='match', lazy=True)
    
    def __repr__(self):
        return f'<Match {self.id} on {self.date}>'

class MatchTeam(db.Model):
    """Modèle pour stocker les équipes d'un match"""
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    team_number = db.Column(db.Integer, nullable=False)  # 1 ou 2
    
    # Relations
    players = db.relationship('MatchPlayer', backref='team', lazy=True)

class MatchPlayer(db.Model):
    """Modèle pour stocker les joueurs d'une équipe dans un match"""
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('match_team.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    
    # Relations
    player = db.relationship('Player', backref='matches')

class User(db.Model):
    """Modèle pour les utilisateurs administrateurs"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
