from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SelectMultipleField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError, EqualTo
from models import Player, User

class LoginForm(FlaskForm):
    """Formulaire de connexion"""
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class RegistrationForm(FlaskForm):
    """Formulaire d'inscription pour les administrateurs"""
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField('Confirmer le mot de passe', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé.')

class PlayerForm(FlaskForm):
    """Formulaire d'ajout/modification de joueur"""
    name = StringField('Nom du joueur', validators=[DataRequired(), Length(min=2, max=100)])
    skill_level = IntegerField('Niveau de compétence (0-100)', 
                             validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Enregistrer')
    
    def validate_name(self, name):
        player = Player.query.filter_by(name=name.data).first()
        if player and player.id != getattr(self, 'player_id', None):
            raise ValidationError('Ce nom de joueur existe déjà.')

class TeamSelectionForm(FlaskForm):
    """Formulaire de sélection des joueurs pour générer des équipes"""
    players = SelectMultipleField('Sélectionnez les joueurs', coerce=int)
    submit = SubmitField('Générer les équipes')
    
    def __init__(self, *args, **kwargs):
        super(TeamSelectionForm, self).__init__(*args, **kwargs)
        self.players.choices = [(p.id, p.name) for p in Player.query.all()]

class MatchResultForm(FlaskForm):
    """Formulaire pour enregistrer les résultats d'un match"""
    winner = SelectField('Équipe gagnante', choices=[
        (0, 'Match nul'), 
        (1, 'Équipe 1'), 
        (2, 'Équipe 2')
    ], coerce=int)
    submit = SubmitField('Enregistrer le résultat')
