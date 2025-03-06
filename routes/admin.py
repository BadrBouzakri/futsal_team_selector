from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
import csv
import io
from werkzeug.utils import secure_filename

from models import db, Player, Match, MatchTeam, MatchPlayer
from forms import PlayerForm

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def index():
    """Page principale de l'administration"""
    if not current_user.is_admin:
        flash('Vous n\'avez pas les droits d\'administration', 'danger')
        return redirect(url_for('main.index'))
    
    # Statistiques pour le tableau de bord
    stats = {
        'total_players': Player.query.count(),
        'total_matches': Match.query.count(),
        'recent_matches': Match.query.order_by(Match.date.desc()).limit(5).all()
    }
    
    return render_template('admin/index.html', stats=stats)

@admin.route('/console', methods=['GET', 'POST'])
@login_required
def console():
    """Console d'administration pour la gestion des joueurs (compatibilité avec l'ancien système)"""
    # Vérifier si l'utilisateur est admin ou si la session admin est active
    if not current_user.is_admin and not session.get('admin_logged_in'):
        flash('Vous n\'avez pas les droits d\'administration', 'danger')
        return redirect(url_for('auth.admin_login'))
    
    form = PlayerForm()
    
    if form.validate_on_submit():
        player = Player(
            name=form.name.data,
            skill_level=form.skill_level.data
        )
        
        db.session.add(player)
        db.session.commit()
        
        flash(f'Le joueur {player.name} a été ajouté avec succès', 'success')
        return redirect(url_for('admin.console'))
    
    players = Player.query.order_by(Player.name).all()
    
    # Convertir les joueurs en dictionnaire pour compatibilité avec l'ancien template
    players_dict = {player.name: player.skill_level for player in players}
    
    return render_template('admin_console.html', players=players_dict, form=form)

@admin.route('/players')
@login_required
def players():
    """Liste des joueurs avec interface améliorée"""
    if not current_user.is_admin:
        flash('Vous n\'avez pas les droits d\'administration', 'danger')
        return redirect(url_for('main.index'))
    
    players = Player.query.order_by(Player.name).all()
    return render_template('admin/players.html', players=players)

@admin.route('/players/add', methods=['GET', 'POST'])
@login_required
def add_player():
    """Ajout d'un nouveau joueur"""
    if not current_user.is_admin:
        flash('Vous n\'avez pas les droits d\'administration', 'danger')
        return redirect(url_for('main.index'))
    
    form = PlayerForm()
    
    if form.validate_on_submit():
        player = Player(
            name=form.name.data,
            skill_level=form.skill_level.data
        )
        
        db.session.add(player)
        db.session.commit()
        
        flash(f'Le joueur {player.name} a été ajouté avec succès', 'success')
        return redirect(url_for('admin.players'))
    
    return render_template('admin/player_form.html', form=form, title='Ajouter un joueur')

@admin.route('/players/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_player(id):
    """Modification d'un joueur existant"""
    if not current_user.is_admin:
        flash('Vous n\'avez pas les droits d\'administration', 'danger')
        return redirect(url_for('main.index'))
    
    player = Player.query.get_or_404(id)
    form = PlayerForm()
    
    if request.method == 'GET':
        form.name.data = player.name
        form.skill_level.data = player.skill_level
    
    # Stocker l'id du joueur pour la validation du nom
    form.player_id = player.id
    
    if form.validate_on_submit():
        player.name = form.name.data
        player.skill_level = form.skill_level.data
        
        db.session.commit()
        
        flash(f'Le joueur {player.name} a été modifié avec succès', 'success')
        return redirect(url_for('admin.players'))
    
    return render_template('admin/player_form.html', form=form, title='Modifier un joueur')

@admin.route('/players/delete/<int:id>', methods=['POST'])
@login_required
def delete_player(id):
    """Suppression d'un joueur"""
    if not current_user.is_admin:
        flash('Vous n\'avez pas les droits d\'administration', 'danger')
        return redirect(url_for('main.index'))
    
    player = Player.query.get_or_404(id)
    
    db.session.delete(player)
    db.session.commit()
    
    flash(f'Le joueur {player.name} a été supprimé', 'success')
    return redirect(url_for('admin.players'))

@admin.route('/matches')
@login_required
def matches():
    """Liste des matchs"""
    if not current_user.is_admin:
        flash('Vous n\'avez pas les droits d\'administration', 'danger')
        return redirect(url_for('main.index'))
    
    matches = Match.query.order_by(Match.date.desc()).all()
    return render_template('admin/matches.html', matches=matches)

@admin.route('/import', methods=['GET', 'POST'])
@login_required
def import_players():
    """Import de joueurs depuis un CSV"""
    if not current_user.is_admin:
        flash('Vous n\'avez pas les droits d\'administration', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Aucun fichier sélectionné', 'danger')
            return redirect(url_for('admin.import_players'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('Aucun fichier sélectionné', 'danger')
            return redirect(url_for('admin.import_players'))
        
        if file and file.filename.endswith('.csv'):
            # Lire le fichier CSV en mémoire
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.reader(stream)
            
            # Ignorer l'en-tête si présent
            header = next(csv_reader, None)
            
            count = 0
            for row in csv_reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    try:
                        skill = int(row[1].strip())
                        
                        # Vérifier si le joueur existe déjà
                        existing_player = Player.query.filter_by(name=name).first()
                        
                        if existing_player:
                            existing_player.skill_level = skill
                        else:
                            player = Player(name=name, skill_level=skill)
                            db.session.add(player)
                        
                        count += 1
                    except ValueError:
                        flash(f'Valeur invalide pour {name}: {row[1]}', 'warning')
            
            db.session.commit()
            flash(f'{count} joueurs importés/mis à jour avec succès', 'success')
            return redirect(url_for('admin.players'))
        
        flash('Le fichier doit être au format CSV', 'danger')
    
    return render_template('admin/import.html')

@admin.route('/export')
@login_required
def export_players():
    """Export des joueurs au format CSV"""
    if not current_user.is_admin:
        flash('Vous n\'avez pas les droits d\'administration', 'danger')
        return redirect(url_for('main.index'))
    
    # Créer un fichier CSV en mémoire
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Écrire l'en-tête
    writer.writerow(['Nom', 'Niveau', 'Matchs joués', 'Victoires', 'Taux de victoire (%)'])
    
    # Écrire les données des joueurs
    players = Player.query.order_by(Player.name).all()
    for player in players:
        writer.writerow([
            player.name,
            player.skill_level,
            player.games_played,
            player.wins,
            player.win_rate
        ])
    
    # Préparer la réponse
    from flask import Response
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=joueurs.csv"}
    )
