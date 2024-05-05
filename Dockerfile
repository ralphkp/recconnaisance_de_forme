# Utilisez une image Python officielle en tant qu'image de base
FROM python:3.9.6

# Copiez les fichiers de votre application dans le conteneur
COPY . /app
WORKDIR /app

# Installez les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposez le port sur lequel l'application Flask s'exécute
EXPOSE 5001

# Commande par défaut pour exécuter l'application Flask
CMD ["python", "app.py"]
