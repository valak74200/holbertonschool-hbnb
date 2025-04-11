"""
Ce fichier est le point d'entrée de l'application Flask.
Il initialise l'application et configure les routes API.
"""

from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from app.extensions import bcrypt, jwt, db
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns


def create_app(config_class="config.DevelopmentConfig"):
    """
    Crée et configure l'instance de l'application Flask.
    
    Cette fonction initialise une nouvelle instance de l'application Flask,
    configure l'API REST avec Flask-RESTX, et enregistre tous les espaces de noms
    (namespaces) pour les différentes ressources de l'API.
    
    Args:
        config_class (str): Chemin vers la classe de configuration à utiliser
    
    Returns:
        Flask: L'instance de l'application Flask configurée
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    api = Api(app, version='1.0', title='HBnB API', description='API de l\'application HBnB')

    # Enregistrement des espaces de noms
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    return app