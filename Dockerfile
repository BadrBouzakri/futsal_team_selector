# Utilisation de Python comme image de base
FROM python:3.9-slim

# Définir le répertoire de travail à /app
WORKDIR /app

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code source dans le conteneur
COPY . .

# Exposer le port 5050 (pour correspondre au README)
EXPOSE 5050

# Définir la commande pour démarrer l'application
CMD ["python", "app.py"]

