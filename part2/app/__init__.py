"""
Ce fichier est le point d'entrée de l'application Flask.
Il initialise l'application et configure les routes API.
"""

from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

def create_app():
    """
    Crée et configure l'instance de l'application Flask.
    
    Cette fonction initialise une nouvelle instance de l'application Flask,
    configure l'API REST avec Flask-RESTX, et enregistre tous les espaces de noms
    (namespaces) pour les différentes ressources de l'API.
    
    Returns:
        Flask: L'instance de l'application Flask configurée
    """
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='API de l\'application HBnB')

    # Enregistrement des espaces de noms
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    return app
