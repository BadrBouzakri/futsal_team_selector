# Utiliser une image officielle de Python comme base
FROM python:3.9-slim AS builder

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances dans une couche distincte
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage de production pour réduire la taille de l'image finale
FROM python:3.9-slim

# Maintainer info
LABEL maintainer="Badr <badrbouzakri@email.com>"

# Définir des variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py

WORKDIR /app

# Copier uniquement les dépendances installées depuis la phase de build
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

# Copier l'application
COPY . .

# Créer un utilisateur non-root pour exécuter l'application
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

# Utiliser l'utilisateur non-root
USER appuser

# Exposer le port
EXPOSE 5000

# Healthcheck pour vérifier que l'application est en cours d'exécution
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Commande pour lancer l'application
CMD ["python", "app.py"]
