# 🏆 Générateur d'Équipes Futsal

**Application créée par Badr**

Une application web moderne et intuitive pour générer des équipes équilibrées de futsal. L'application propose plusieurs méthodes d'équilibrage, un système d'historique, et une interface d'administration complète.

## ✨ Fonctionnalités

### 🎯 Génération d'équipes
- **Sélection interactive** : Interface moderne avec cartes de joueurs
- **3 méthodes d'équilibrage** :
  - 🎯 **Par compétence** : Équilibrage intelligent selon le niveau
  - 🐍 **Serpent** : Distribution alternée 1-2-2-1
  - 🎲 **Aléatoire** : Répartition totalement hasard
- **Sélection assistée** : Boutons pour sélection aléatoire et équilibrée
- **Validation en temps réel** : Compteur de joueurs sélectionnés

### 📊 Analyse et statistiques
- **Indicateur d'équilibre** : Pourcentage d'équilibre entre les équipes
- **Statistiques détaillées** : Force totale et moyenne par équipe
- **Visualisation moderne** : Interface avec gradients et animations

### 📅 Historique
- **Sauvegarde automatique** : Les 20 dernières formations d'équipes
- **Recréation facile** : Possibilité de recréer des équipes précédentes
- **Partage** : Fonction de partage des équipes

### ⚙️ Administration
- **Gestion des joueurs** : Ajout, modification, suppression
- **Interface moderne** : Design responsive et intuitif
- **Statistiques** : Vue d'ensemble des joueurs et niveaux
- **Contrôles avancés** : Recherche, tri, filtrage

### 🎨 Interface utilisateur
- **Design moderne** : Interface avec gradients et effets visuels
- **Responsive** : Optimisé pour mobile et desktop
- **Animations** : Transitions fluides et interactives
- **Accessibilité** : Interface intuitive et accessible

## 🚀 Installation et démarrage

### Prérequis
- **Docker** (recommandé)
- Ou **Python 3.9+** pour installation locale

### 📦 Installation avec Docker (Recommandée)

#### 1. Cloner le projet
```bash
git clone git@github.com:BadrBouzakri/futsal_team_selector.git
cd futsal_team_selector
```

#### 2. Construire l'image Docker
```bash
docker build -t futsal-teams-app .
```

#### 3. Lancer l'application
```bash
docker run -d -p 5050:5050 --name futsal-app futsal-teams-app
```

#### 4. Accéder à l'application
Ouvrez votre navigateur et allez sur : `http://localhost:5050`

### 🐍 Installation locale avec Python

#### 1. Cloner le projet
```bash
git clone git@github.com:BadrBouzakri/futsal_team_selector.git
cd futsal_team_selector
```

#### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

#### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 4. Lancer l'application
```bash
python app.py
```

### ⚡ Démarrage rapide avec le script

```bash
chmod +x start.sh

# Démarrage avec Docker
./start.sh docker

# Démarrage local
./start.sh local

# Démarrage avec Docker Compose
./start.sh compose

# Voir le statut
./start.sh status

# Arrêter l'application
./start.sh stop
```

## 🎮 Utilisation

### 🏠 Page d'accueil
1. **Sélectionner 10 joueurs** parmi la liste disponible
2. **Choisir une méthode** d'équilibrage
3. **Générer les équipes** avec le bouton principal

### 👥 Gestion des équipes
- Visualisation claire des deux équipes
- Statistiques d'équilibre en temps réel
- Options d'impression et de partage
- Possibilité de regénérer avec les mêmes joueurs

### 📅 Consulter l'historique
- Accès aux 20 dernières formations
- Possibilité de recréer des équipes précédentes
- Statistiques de chaque formation

### ⚙️ Administration
**Accès** : `http://localhost:5050/admin`
- **Identifiants par défaut** : `admin` / `admin`

**Fonctionnalités** :
- Ajouter de nouveaux joueurs
- Modifier les niveaux des joueurs
- Supprimer des joueurs
- Consulter les statistiques globales

## 📁 Structure du projet

```
futsal_team_selector/
├── app.py                      # Application Flask principale
├── config.py                   # Configuration modulaire
├── requirements.txt            # Dépendances Python
├── Dockerfile                  # Configuration Docker
├── docker-compose.yml          # Orchestration Docker
├── start.sh                    # Script de démarrage
├── README.md                   # Documentation
├── .env.example                # Variables d'environnement
├── .gitignore                  # Fichiers à ignorer
├── teams_history.json          # Historique des équipes (généré)
└── templates/                  # Templates HTML
    ├── index.html              # Page d'accueil
    ├── teams.html              # Affichage des équipes
    ├── history.html            # Historique des équipes
    ├── admin.html              # Connexion admin
    └── admin_console.html      # Console d'administration
```

## 🛠️ Commandes Docker utiles

```bash
# Voir les conteneurs en cours
docker ps

# Arrêter l'application
docker stop futsal-app

# Redémarrer l'application
docker start futsal-app

# Voir les logs
docker logs futsal-app

# Supprimer le conteneur
docker rm -f futsal-app

# Supprimer l'image
docker rmi futsal-teams-app
```

## 🐳 Docker Compose

```bash
# Démarrer avec Docker Compose
docker-compose up -d --build

# Arrêter
docker-compose down

# Voir les logs
docker-compose logs -f
```

## 🌐 API Routes

### Routes principales
- **`/`** : Page d'accueil avec sélection des joueurs
- **`/teams`** : Affichage des équipes générées
- **`/history`** : Historique des formations d'équipes
- **`/admin`** : Page de connexion administrateur
- **`/admin/console`** : Console d'administration

### API endpoints
- **`/api/suggest-players`** : Suggestion de sélection équilibrée (GET)

## ⚙️ Configuration

### Variables d'environnement

Copiez `.env.example` vers `.env` et modifiez selon vos besoins :

```bash
cp .env.example .env
```

**Variables principales** :
- `FLASK_CONFIG` : Mode de configuration (development/production)
- `SECRET_KEY` : Clé secrète pour les sessions
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` : Identifiants admin
- `MAX_HISTORY_ITEMS` : Nombre max d'éléments dans l'historique

## 🎨 Fonctionnalités techniques

### Frontend
- **CSS moderne** : Gradients, animations, responsive design
- **JavaScript vanilla** : Pas de dépendances externes
- **Progressive Web App** : Fonctionnalités web modernes

### Backend
- **Flask** : Framework web Python léger
- **Sessions** : Gestion des données utilisateur
- **JSON** : Stockage de l'historique
- **API RESTful** : Endpoints pour les fonctionnalités avancées

### Améliorations apportées
- ✅ **Interface modernisée** avec design responsive
- ✅ **Suppression des pourcentages** visibles côté utilisateur
- ✅ **Système d'historique** complet
- ✅ **Sélection assistée** de joueurs
- ✅ **API de suggestions** intelligentes
- ✅ **Administration améliorée** avec statistiques
- ✅ **Animations et transitions** fluides
- ✅ **Optimisation mobile** complète
- ✅ **Configuration modulaire** avec variables d'environnement
- ✅ **Docker optimisé** avec sécurité renforcée
- ✅ **Script de démarrage** automatisé

## 🐞 Dépannage

### Problèmes courants

**L'application ne démarre pas** :
```bash
# Vérifier les logs
docker logs futsal-app

# Vérifier la configuration
cat .env
```

**Port déjà utilisé** :
```bash
# Changer le port dans docker-compose.yml ou .env
PORT=5051
```

**Permissions Docker** :
```bash
# Sur Linux, ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
```

## 🚀 Déploiement en production

### Configuration recommandée

1. **Variables d'environnement** :
```bash
FLASK_CONFIG=production
SECRET_KEY=your-super-secret-key
ADMIN_PASSWORD=secure-password
```

2. **Proxy reverse (Nginx)** :
```nginx
location / {
    proxy_pass http://localhost:5050;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

3. **SSL/HTTPS** :
```bash
# Avec Let's Encrypt
certbot --nginx -d your-domain.com
```

## 🤝 Contribution

Pour contribuer au projet :
1. Fork le repository
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🔄 Changelog

### Version 2.0 (Actuelle)
- 🎨 Interface utilisateur complètement redessinée
- 📅 Système d'historique des équipes
- ⚙️ Configuration modulaire avec variables d'environnement
- 🐳 Docker optimisé avec sécurité renforcée
- 📱 Responsive design pour mobile
- 🎲 Sélection assistée et suggestions intelligentes
- 📊 Statistiques avancées et indicateurs d'équilibre

### Version 1.0
- ⚽ Génération d'équipes de base
- 🎯 Trois méthodes d'équilibrage
- 👥 Gestion simple des joueurs
- 🔧 Administration basique

## 👨‍💻 Auteur

**Badr** - Développeur principal
- 🔗 GitHub : [@BadrBouzakri](https://github.com/BadrBouzakri)

## 🙏 Remerciements

- Merci à tous les joueurs de futsal qui utilisent cette application
- Inspiration tirée des meilleures pratiques de développement web moderne
- Interface inspirée par les tendances de design contemporain

## 📞 Support

Si vous rencontrez des problèmes ou avez des questions :
1. Consultez la section [Dépannage](#-dépannage)
2. Ouvrez une [issue](https://github.com/BadrBouzakri/futsal_team_selector/issues) sur GitHub
3. Consultez la [documentation](https://github.com/BadrBouzakri/futsal_team_selector/wiki)

---

**Bon match ! ⚽🏆**

*Application Futsal Teams Generator - Créez des équipes équilibrées en quelques clics !*
