# Utilisation de Python 3.9 slim comme image de base pour une image plus légère
FROM python:3.9-slim

# Métadonnées de l'image
LABEL maintainer="Badr"
LABEL description="Application de génération d'équipes de futsal équilibrées"
LABEL version="2.0"

# Créer un utilisateur non-root pour la sécurité
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements en premier pour optimiser le cache Docker
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code source de l'application
COPY . .

# Créer le répertoire pour les données persistantes et ajuster les permissions
RUN mkdir -p /app/data && \
    chown -R appuser:appuser /app

# Changer vers l'utilisateur non-root
USER appuser

# Exposer le port 5050
EXPOSE 5050

# Variables d'environnement
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Vérification de santé du conteneur
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5050/ || exit 1

# Volume pour persister l'historique des équipes
VOLUME ["/app/data"]

# Commande pour démarrer l'application
CMD ["python", "app.py"]
