import os
from flask import Flask, render_template, session, redirect, url_for
from flask_login import LoginManager, current_user
import logging
from logging.handlers import RotatingFileHandler

from models import db, User, Player
from config import config

def create_app(config_name='default'):
    """Factory pattern pour créer l'application Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialiser les extensions
    db.init_app(app)
    
    # Configurer le login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Créer les dossiers de données s'ils n'existent pas
    data_dir = os.path.join(app.root_path, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Créer la base de données si elle n'existe pas
    with app.app_context():
        db.create_all()
        
        # Créer un utilisateur admin par défaut s'il n'en existe pas
        if not User.query.filter_by(username=app.config['ADMIN_USERNAME']).first():
            admin = User(
                username=app.config['ADMIN_USERNAME'],
                email=app.config['ADMIN_EMAIL'],
                is_admin=True
            )
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            db.session.commit()
            
        # Importer les joueurs existants si aucun n'est défini
        if Player.query.count() == 0:
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
    
    # Enregistrer les blueprints
    from routes.auth import auth
    from routes.admin import admin
    from routes.main import main
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(main)
    
    # Route pour rediriger les anciennes URLs pour la rétrocompatibilité
    @app.route('/admin', methods=['GET', 'POST'])
    def admin_redirect():
        """Redirection de l'ancien chemin d'admin vers le nouveau"""
        return redirect(url_for('auth.admin_login'))
    
    # Gestionnaire d'erreurs
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Configuration des logs en production
    if not app.debug and not app.testing:
        if app.config.get('LOG_TO_STDOUT'):
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            log_dir = os.path.join(app.root_path, 'logs')
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            file_handler = RotatingFileHandler(
                os.path.join(log_dir, 'futsal.log'),
                maxBytes=10240,
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Démarrage de l\'application Futsal Team Selector')
    
    # Template context global
    @app.context_processor
    def inject_context():
        return {
            'current_user': current_user,
            'app_name': 'Futsal Team Selector',
            'app_version': '2.0.0',
            'app_author': 'Badr'
        }
    
    return app

# Créer l'application avec la configuration par défaut si exécuté directement
if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG', 'default'))
    app.run(host='0.0.0.0', port=5000)
