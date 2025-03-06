# Application de Gestion d'Équipes - CI/CD avec Jenkins et Kubernetes

**Application créée par Badr - Améliorée 2025**

Cette application permet de générer des équipes équilibrées à partir d'une liste de joueurs. Elle dispose d'une interface moderne, d'un système de statistiques avancé, et d'une console d'administration complète pour gérer les joueurs et les matchs.

## Table des matières

1. [Fonctionnalités](#fonctionnalités)
2. [Nouvelles améliorations](#nouvelles-améliorations)
3. [Prérequis](#prérequis)
4. [Installation locale avec Docker](#installation-locale-avec-docker)
5. [Installation avec Kubernetes](#installation-avec-kubernetes)
6. [Pipeline CI/CD avec Jenkins](#pipeline-cicd-avec-jenkins)
7. [Structure des fichiers](#structure-des-fichiers)
8. [Accès à l'application](#accès-à-lapplication)
9. [Contributeurs](#contributeurs)

## Fonctionnalités

- Sélectionnez jusqu'à 10 joueurs pour générer des équipes équilibrées.
- Affichage dynamique des équipes générées.
- Console d'administration pour ajouter et gérer des joueurs.
- Authentification pour accéder à la console d'administration.
- Intégration continue avec Jenkins
- Déploiement continu sur Kubernetes (environnements dev, staging et production)
- **Nouvelles** : Base de données persistante, statistiques détaillées, historique des matchs, et classement des joueurs.

## Nouvelles améliorations

### Version 2.0

- **Interface utilisateur moderne** : Refonte complète avec Bootstrap 5 pour une meilleure expérience utilisateur et compatibilité mobile.
- **Architecture améliorée** : Utilisation du modèle Factory et Blueprints Flask pour une meilleure organisation du code.
- **Base de données SQLAlchemy** : Stockage persistant des joueurs, matchs et utilisateurs.
- **Statistiques avancées** : Suivi des victoires, défaites et taux de réussite pour chaque joueur.
- **Historique des matchs** : Visualisation et filtrage de l'historique complet des matchs.
- **Tableau de classement** : Classement des joueurs basé sur leur performance et leur niveau.
- **Sécurité renforcée** : Authentification améliorée, hachage des mots de passe et protection CSRF.
- **Docker multi-stage** : Optimisation des images Docker avec build multi-étapes pour la production.
- **Environnements de déploiement** : Configuration distincte pour le développement, test et production.

## Prérequis

- **Docker** : Pour exécuter l'application dans un conteneur.
- **Kubernetes** : Pour le déploiement dans des environnements dev, staging et production.
- **Jenkins** : Pour l'intégration continue et le déploiement continu.
- **kubectl** : Client en ligne de commande pour Kubernetes.
- **Git** : Pour la gestion du code source.

## Installation locale avec Docker

### Développement local avec Docker Compose

```bash
# Cloner le projet
git clone git@github.com:BadrBouzakri/futsal_team_selector.git
cd futsal_team_selector

# Démarrer l'application avec Docker Compose
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Initialiser la base de données avec des exemples
docker exec -it futsal-app python init_db.py --with-samples
```

L'application sera accessible à l'adresse http://localhost:5000.

L'interface d'administration de la base de données (Adminer) sera disponible à l'adresse http://localhost:8080.

### Démarrage rapide sans Docker

```bash
# Cloner le projet
git clone git@github.com:BadrBouzakri/futsal_team_selector.git
cd futsal_team_selector

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python init_db.py --with-samples

# Lancer l'application
python run.py --debug
```

## Installation avec Kubernetes

### Préparation

1. Assurez-vous que votre cluster Kubernetes est opérationnel et que kubectl est correctement configuré.
2. Créez les répertoires pour les volumes persistants :

```bash
# Sur tous les nœuds du cluster où les pods pourraient être programmés
sudo mkdir -p /mnt/data/futsal-dev /mnt/data/futsal-staging /mnt/data/futsal-prod
sudo chmod 777 /mnt/data/futsal-dev /mnt/data/futsal-staging /mnt/data/futsal-prod
```

### Déploiement dans l'environnement de développement

```bash
# Créer le namespace et les ressources Kubernetes
kubectl apply -f k8s/dev/namespace.yaml
kubectl apply -f k8s/dev/persistent-volume.yaml
kubectl apply -f k8s/dev/persistent-volume-claim.yaml
kubectl apply -f k8s/dev/configmap.yaml
kubectl apply -f k8s/dev/deployment.yaml
kubectl apply -f k8s/dev/service.yaml
kubectl apply -f k8s/dev/hpa.yaml

# Vérifier le déploiement
kubectl get all -n dev
```

### Déploiement dans l'environnement de staging

```bash
# Créer le namespace et les ressources Kubernetes
kubectl apply -f k8s/staging/namespace.yaml
kubectl apply -f k8s/staging/persistent-volume.yaml
kubectl apply -f k8s/staging/persistent-volume-claim.yaml
kubectl apply -f k8s/staging/configmap.yaml
kubectl apply -f k8s/staging/deployment.yaml
kubectl apply -f k8s/staging/service.yaml
kubectl apply -f k8s/staging/hpa.yaml

# Vérifier le déploiement
kubectl get all -n staging
```

### Déploiement dans l'environnement de production

```bash
# Créer le namespace et les ressources Kubernetes
kubectl apply -f k8s/prod/namespace.yaml
kubectl apply -f k8s/prod/persistent-volume.yaml
kubectl apply -f k8s/prod/persistent-volume-claim.yaml
kubectl apply -f k8s/prod/configmap.yaml
kubectl apply -f k8s/prod/deployment.yaml
kubectl apply -f k8s/prod/service.yaml
kubectl apply -f k8s/prod/hpa.yaml

# Vérifier le déploiement
kubectl get all -n prod
```

## Pipeline CI/CD avec Jenkins

Ce projet utilise Jenkins pour l'intégration continue et le déploiement continu. Le pipeline est défini dans le fichier `Jenkinsfile`.

### Configuration de Jenkins

1. Installez Jenkins (avec Docker) :

```bash
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkinsci/blueocean
```

2. Récupérez le mot de passe initial :

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

3. Accédez à http://localhost:8080 et suivez les instructions pour terminer l'installation.

4. Installez les plugins suivants :
   - Docker Pipeline
   - Kubernetes CLI
   - Credentials Plugin

5. Configurez les identifiants Jenkins :
   - Ajoutez votre fichier kubeconfig dans Jenkins (ID: `config`)
   - Configurez l'accès à Docker Hub (ID: `DOCKER_HUB_PASS`)

6. Créez un nouveau pipeline dans Jenkins :
   - Sélectionnez "New Item"
   - Choisissez "Pipeline"
   - Dans la configuration, sélectionnez "Pipeline script from SCM"
   - Spécifiez l'URL de votre dépôt Git et le chemin du Jenkinsfile

### Exécution du pipeline

Le pipeline Jenkins s'exécutera automatiquement à chaque push sur le dépôt Git. Il comprend :
1. Checkout du code
2. Construction de l'image Docker
3. Tests et vérification de l'exécution
4. Push de l'image vers le registre
5. Déploiement en environnement dev
6. Déploiement en environnement staging
7. Déploiement en environnement production (avec validation manuelle)

## Structure des fichiers

```
futsal_team_selector/
├── app.py                     # Point d'entrée de l'application avec Factory pattern
├── config.py                  # Configuration de l'application pour différents environnements
├── models.py                  # Modèles SQLAlchemy pour la base de données
├── forms.py                   # Formulaires WTForms
├── init_db.py                 # Script d'initialisation de la base de données
├── run.py                     # Script de démarrage pour le développement
├── routes/                    # Structure Blueprint Flask
│   ├── __init__.py
│   ├── auth.py                # Routes pour l'authentification
│   ├── admin.py               # Routes pour l'administration
│   └── main.py                # Routes principales de l'application
├── templates/                 # Templates HTML avec Jinja2
│   ├── base.html              # Template de base (parent)
│   ├── index_new.html         # Page d'accueil moderne
│   ├── teams_new.html         # Affichage des équipes moderne
│   ├── ranking.html           # Classement des joueurs
│   ├── history.html           # Historique des matchs
│   ├── errors/                # Pages d'erreur
│   │   ├── 404.html
│   │   └── 500.html
│   ├── auth/                  # Templates d'authentification
│   └── admin/                 # Templates d'administration
├── static/                    # Fichiers statiques (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
├── data/                      # Données persistantes (base de données SQLite)
├── logs/                      # Fichiers de log
├── Dockerfile                 # Configuration Docker multi-stage
├── docker-compose.yml         # Configuration Docker Compose pour le développement
├── Jenkinsfile                # Configuration du pipeline CI/CD
├── k8s/                       # Configurations Kubernetes
│   ├── dev/                   # Environnement de développement
│   ├── staging/               # Environnement de staging
│   └── prod/                  # Environnement de production
└── README.md                  # Documentation du projet
```

## Accès à l'application

### Via NodePort (accès direct)
- **Environnement de développement** : http://[ADRESSE_IP_NODE]:30080
- **Environnement de staging** : http://[ADRESSE_IP_NODE]:30081
- **Environnement de production** : http://[ADRESSE_IP_NODE]:30082

### Via Ingress (nom de domaine)
- **Environnement de développement** : https://dev.foot.badr.cloud
- **Environnement de staging** : https://staging.foot.badr.cloud
- **Environnement de production** : https://foot.badr.cloud

### Administration
- **Admin** : Ajoutez `/auth/login` à l'URL (identifiants par défaut: admin/admin)

## Contributeurs

- **Badr** - Développeur principal de l'application.
