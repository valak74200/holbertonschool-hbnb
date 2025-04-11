"""
Ce fichier initialise l'API REST pour l'application HBnB.
Il configure l'API principale et enregistre tous les espaces de noms (namespaces)
pour les différentes ressources de l'API.
"""

from flask_restx import Api
from .v1.users import api as users_ns
from .v1.amenities import api as amenities_ns
from .v1.places import api as places_ns
from .v1.reviews import api as reviews_ns
from .v1.auth import api as auth_ns
from .v1.admin import api as admin_ns

# Création de l'instance principale de l'API
api = Api(
    title='HBnB API',
    version='1.0',
    description='API pour l\'application HBnB',
)

# Enregistrement des espaces de noms pour chaque ressource
# Chaque espace de nom correspond à un ensemble d'endpoints liés à une ressource spécifique
api.add_namespace(users_ns, path='/api/v1/users')
api.add_namespace(amenities_ns, path='/api/v1/amenities')
api.add_namespace(places_ns, path='/api/v1/places')
api.add_namespace(reviews_ns, path='/api/v1/reviews')
api.add_namespace(auth_ns, path='/api/v1/auth')
api.add_namespace(admin_ns, path='/api/v1/admin')
