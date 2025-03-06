from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_required, current_user
import random

from models import db, Player, Match, MatchTeam, MatchPlayer
from forms import TeamSelectionForm, MatchResultForm

main = Blueprint('main', __name__)

def balance_teams(player_ids):
    """Équilibrer les équipes en fonction des compétences des joueurs"""
    players = Player.query.filter(Player.id.in_(player_ids)).all()
    sorted_players = sorted(players, key=lambda p: p.skill_level, reverse=True)
    
    team1, team2 = [], []
    team1_score, team2_score = 0, 0
    
    for player in sorted_players:
        if team1_score <= team2_score:
            team1.append(player)
            team1_score += player.skill_level
        else:
            team2.append(player)
            team2_score += player.skill_level
            
    return team1, team2

@main.route('/', methods=['GET', 'POST'])
def index():
    """Page principale - Sélection des joueurs et génération d'équipes"""
    form = TeamSelectionForm()
    
    # Obtenir tous les joueurs pour l'affichage
    all_players = Player.query.order_by(Player.name).all()
    
    if form.validate_on_submit():
        selected_player_ids = form.players.data
        
        if len(selected_player_ids) != 10:
            flash('Veuillez sélectionner exactement 10 joueurs.', 'warning')
            return redirect(url_for('main.index'))
        
        team1, team2 = balance_teams(selected_player_ids)
        
        # Stocker les équipes dans la session pour affichage
        session['team1_ids'] = [player.id for player in team1]
        session['team2_ids'] = [player.id for player in team2]
        
        # Créer un nouveau match dans la base de données
        match = Match()
        db.session.add(match)
        db.session.flush()  # Pour obtenir l'ID du match
        
        # Créer les équipes dans la base de données
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
        
        db.session.commit()
        
        # Stocker l'ID du match dans la session
        session['current_match_id'] = match.id
        
        return redirect(url_for('main.teams'))
    
    # Conversion pour la compatibilité avec l'ancien template
    players_dict = {player.name: player.skill_level for player in all_players}
    
    return render_template('index.html', all_players=players_dict, form=form)

@main.route('/teams', methods=['GET', 'POST'])
def teams():
    """Afficher les équipes générées et permettre d'enregistrer les résultats"""
    if 'team1_ids' not in session or 'team2_ids' not in session:
        flash('Les équipes n\'ont pas été générées. Veuillez sélectionner les joueurs.', 'info')
        return redirect(url_for('main.index'))
    
    # Récupérer les objets joueurs à partir des IDs
    team1 = Player.query.filter(Player.id.in_(session['team1_ids'])).all()
    team2 = Player.query.filter(Player.id.in_(session['team2_ids'])).all()
    
    # Formulaire pour enregistrer le résultat du match
    form = MatchResultForm()
    
    if form.validate_on_submit() and 'current_match_id' in session:
        match_id = session['current_match_id']
        match = Match.query.get(match_id)
        
        if match:
            # Mettre à jour le gagnant du match
            match.winner_team = form.winner.data if form.winner.data > 0 else None
            db.session.commit()
            
            # Mettre à jour les statistiques des joueurs
            if match.winner_team:
                winning_team = team1 if match.winner_team == 1 else team2
                all_players = team1 + team2
                
                for player in all_players:
                    player.games_played += 1
                    if player in winning_team:
                        player.wins += 1
                
                db.session.commit()
            
            flash('Résultat du match enregistré avec succès!', 'success')
            return redirect(url_for('main.index'))
    
    # Convertir pour la compatibilité avec le template actuel
    team1_names = [player.name for player in team1]
    team2_names = [player.name for player in team2]
    
    return render_template('teams.html', team1=team1_names, team2=team2_names, form=form)

@main.route('/history')
def history():
    """Afficher l'historique des matchs"""
    matches = Match.query.order_by(Match.date.desc()).limit(20).all()
    return render_template('history.html', matches=matches)

@main.route('/ranking')
def ranking():
    """Afficher le classement des joueurs"""
    players = Player.query.filter(Player.games_played > 0).order_by(Player.win_rate.desc(), Player.games_played.desc()).all()
    return render_template('ranking.html', players=players)

@main.route('/api/players')
def api_players():
    """API pour obtenir la liste des joueurs (au format JSON)"""
    players = Player.query.order_by(Player.name).all()
    return jsonify([
        {
            'id': player.id,
            'name': player.name,
            'skill_level': player.skill_level,
            'games_played': player.games_played,
            'wins': player.wins,
            'win_rate': player.win_rate
        }
        for player in players
    ])

@main.route('/api/random-teams', methods=['POST'])
def api_random_teams():
    """API pour générer des équipes aléatoires (sans équilibrage)"""
    data = request.get_json()
    
    if not data or 'player_ids' not in data:
        return jsonify({'error': 'Aucun joueur sélectionné'}), 400
    
    player_ids = data['player_ids']
    players = Player.query.filter(Player.id.in_(player_ids)).all()
    
    # Mélanger les joueurs aléatoirement
    random.shuffle(players)
    
    # Diviser en deux équipes
    half = len(players) // 2
    team1 = players[:half]
    team2 = players[half:]
    
    return jsonify({
        'team1': [{'id': p.id, 'name': p.name, 'skill_level': p.skill_level} for p in team1],
        'team2': [{'id': p.id, 'name': p.name, 'skill_level': p.skill_level} for p in team2]
    })
