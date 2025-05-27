#!/bin/bash

# Script de démarrage pour l'application Futsal Teams Generator
# Usage: ./start.sh [mode]
# Modes: docker, local, dev

MODE=${1:-docker}
APP_NAME="futsal-teams-generator"
IMAGE_NAME="futsal-teams-app"
PORT=5050

echo "🏆 Démarrage de l'application Futsal Teams Generator"
echo "Mode: $MODE"
echo "----------------------------------------"

case $MODE in
    "docker")
        echo "📦 Démarrage avec Docker..."
        
        # Vérifier si Docker est installé
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
            exit 1
        fi
        
        # Arrêter le conteneur existant s'il existe
        if [ "$(docker ps -q -f name=$APP_NAME)" ]; then
            echo "⏹️  Arrêt du conteneur existant..."
            docker stop $APP_NAME
        fi
        
        if [ "$(docker ps -aq -f name=$APP_NAME)" ]; then
            echo "🗑️  Suppression du conteneur existant..."
            docker rm $APP_NAME
        fi
        
        # Construire l'image
        echo "🔨 Construction de l'image Docker..."
        docker build -t $IMAGE_NAME .
        
        # Créer le répertoire de données
        mkdir -p ./data
        
        # Lancer le conteneur
        echo "🚀 Lancement du conteneur..."
        docker run -d \
            --name $APP_NAME \
            -p $PORT:$PORT \
            -v "$(pwd)/data:/app/data" \
            --restart unless-stopped \
            $IMAGE_NAME
        
        if [ $? -eq 0 ]; then
            echo "✅ Application démarrée avec succès!"
            echo "🌐 Accès: http://localhost:$PORT"
            echo "📊 Logs: docker logs $APP_NAME"
        else
            echo "❌ Erreur lors du démarrage"
            exit 1
        fi
        ;;
        
    "compose")
        echo "🐳 Démarrage avec Docker Compose..."
        
        if ! command -v docker-compose &> /dev/null; then
            echo "❌ Docker Compose n'est pas installé."
            exit 1
        fi
        
        docker-compose up -d --build
        
        if [ $? -eq 0 ]; then
            echo "✅ Application démarrée avec Docker Compose!"
            echo "🌐 Accès: http://localhost:$PORT"
        else
            echo "❌ Erreur lors du démarrage"
            exit 1
        fi
        ;;
        
    "local"|"dev")
        echo "🐍 Démarrage en mode local..."
        
        # Vérifier si Python est installé
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python 3 n'est pas installé."
            exit 1
        fi
        
        # Créer l'environnement virtuel s'il n'existe pas
        if [ ! -d "venv" ]; then
            echo "📦 Création de l'environnement virtuel..."
            python3 -m venv venv
        fi
        
        # Activer l'environnement virtuel
        echo "🔧 Activation de l'environnement virtuel..."
        source venv/bin/activate || source venv/Scripts/activate
        
        # Installer les dépendances
        echo "📥 Installation des dépendances..."
        pip install -r requirements.txt
        
        # Créer le répertoire de données
        mkdir -p ./data
        
        # Configurer les variables d'environnement pour le développement
        export FLASK_CONFIG=development
        export FLASK_DEBUG=true
        
        # Lancer l'application
        echo "🚀 Lancement de l'application..."
        python app.py
        ;;
        
    "stop")
        echo "⏹️  Arrêt de l'application..."
        
        if [ "$(docker ps -q -f name=$APP_NAME)" ]; then
            docker stop $APP_NAME
            echo "✅ Conteneur Docker arrêté"
        fi
        
        if command -v docker-compose &> /dev/null; then
            docker-compose down
            echo "✅ Docker Compose arrêté"
        fi
        ;;
        
    "logs")
        echo "📊 Affichage des logs..."
        
        if [ "$(docker ps -q -f name=$APP_NAME)" ]; then
            docker logs -f $APP_NAME
        else
            echo "❌ Aucun conteneur en cours d'exécution"
        fi
        ;;
        
    "status")
        echo "📊 Statut de l'application..."
        
        if [ "$(docker ps -q -f name=$APP_NAME)" ]; then
            echo "✅ Conteneur Docker en cours d'exécution"
            docker ps -f name=$APP_NAME
        else
            echo "❌ Aucun conteneur en cours d'exécution"
        fi
        ;;
        
    *)
        echo "❓ Usage: $0 [docker|compose|local|dev|stop|logs|status]"
        echo ""
        echo "Modes disponibles:"
        echo "  docker   - Démarrer avec Docker (par défaut)"
        echo "  compose  - Démarrer avec Docker Compose"
        echo "  local    - Démarrer en mode local avec Python"
        echo "  dev      - Démarrer en mode développement"
        echo "  stop     - Arrêter l'application"
        echo "  logs     - Afficher les logs"
        echo "  status   - Vérifier le statut"
        exit 1
        ;;
esac