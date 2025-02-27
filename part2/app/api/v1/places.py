"""
Ce fichier contient les endpoints de l'API pour la gestion des lieux.
Il définit les routes pour créer, récupérer, mettre à jour et supprimer des lieux,
ainsi que pour gérer les avis associés à ces lieux.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Opérations sur les lieux')

# Définition des modèles pour les entités liées
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='ID de l\'équipement'),
    'name': fields.String(description='Nom de l\'équipement')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='ID de l\'utilisateur'),
    'first_name': fields.String(description='Prénom du propriétaire'),
    'last_name': fields.String(description='Nom de famille du propriétaire'),
    'email': fields.String(description='Email du propriétaire')
})

# Définition du modèle d'avis pour les détails du lieu
review_model = api.model('PlaceReview', {
    'id': fields.String(description='ID de l\'avis'),
    'text': fields.String(description='Texte de l\'avis'),
    'rating': fields.Integer(description='Note du lieu (1-5)'),
    'user_id': fields.String(description='ID de l\'utilisateur')
})

# Définition du modèle de lieu pour la validation des entrées et la documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Titre du lieu'),
    'description': fields.String(description='Description du lieu'),
    'price': fields.Float(required=True, description='Prix par nuit'),
    'latitude': fields.Float(required=True, description='Latitude du lieu'),
    'longitude': fields.Float(required=True, description='Longitude du lieu'),
    'owner_id': fields.String(required=True, description='ID du propriétaire'),
    'amenities': fields.List(fields.String, description="Liste des IDs d'équipements"),
    'reviews': fields.List(fields.Nested(review_model), description='Liste des avis')
})

# Définition d'un modèle pour les mises à jour de lieu où les champs sont optionnels
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Titre du lieu'),
    'description': fields.String(required=False, description='Description du lieu'),
    'price': fields.Float(required=False, description='Prix par nuit'),
    'latitude': fields.Float(required=False, description='Latitude du lieu'),
    'longitude': fields.Float(required=False, description='Longitude du lieu'),
    'owner_id': fields.String(required=False, description='ID du propriétaire'),
    'amenities': fields.List(fields.String, required=False, description="Liste des IDs d'équipements")
})

@api.route('/')
class PlaceList(Resource):
    """
    Ressource pour gérer la collection de lieux.
    Permet de créer un nouveau lieu et de récupérer la liste de tous les lieux.
    """
    @api.expect(place_model, validate=True)
    @api.response(201, 'Lieu créé avec succès')
    @api.response(400, 'Données d\'entrée invalides')
    def post(self):
        """
        Enregistre un nouveau lieu.
        
        Cette méthode crée un nouveau lieu dans le système avec les informations fournies.
        Elle vérifie que toutes les données requises sont présentes et valides.
        """
        try:
            new_place = facade.create_place(api.payload)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id
            }, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'Liste des lieux récupérée avec succès')
    def get(self):
        """
        Récupère une liste de tous les lieux.
        
        Cette méthode renvoie une liste de tous les lieux enregistrés dans le système,
        avec leurs informations de base (id, titre, latitude, longitude).
        """
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    """
    Ressource pour gérer un lieu spécifique.
    Permet de récupérer et de mettre à jour les détails d'un lieu par son ID.
    """
    @api.response(200, 'Détails du lieu récupérés avec succès')
    @api.response(404, 'Lieu non trouvé')
    def get(self, place_id):
        """
        Récupère les détails d'un lieu par son ID.
        
        Cette méthode renvoie les informations détaillées d'un lieu spécifique
        identifié par son ID unique, y compris les informations sur le propriétaire
        et les avis associés.
        """
        try:
            place = facade.get_place(place_id)
            owner = facade.get_user(place.owner_id)
            
            # Récupère les avis pour ce lieu
            reviews = []
            if hasattr(place, 'reviews'):
                reviews = [{
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user.id
                } for review in place.reviews]
            
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                },
                'reviews': reviews
            }, 200
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Lieu mis à jour avec succès')
    @api.response(404, 'Lieu non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    def put(self, place_id):
        """
        Met à jour les informations d'un lieu.
        
        Cette méthode permet de modifier les informations d'un lieu existant.
        Seuls les champs fournis dans la requête seront mis à jour.
        """
        try:
            # Vérifie si le lieu existe
            place = facade.get_place(place_id)
        except ValueError as e:
            api.abort(404, str(e))
            
        try:
            # Vérifie que api.payload est un dictionnaire
            if not isinstance(api.payload, dict):
                api.abort(400, 'Payload invalide: dictionnaire attendu')
            
            # Crée un nouveau dictionnaire avec uniquement les champs présents dans le payload
            update_data = {}
            for key, value in api.payload.items():
                if value is not None:
                    update_data[key] = value
            
            try:
                updated_place = facade.update_place(place_id, update_data)
                return {
                    'message': 'Lieu mis à jour avec succès',
                    'place': {
                        'id': updated_place.id,
                        'title': updated_place.title,
                        'description': updated_place.description,
                        'price': updated_place.price,
                        'latitude': updated_place.latitude,
                        'longitude': updated_place.longitude,
                        'owner_id': updated_place.owner_id
                    }
                }, 200
            except ValueError as e:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(400, str(e))

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Ressource pour gérer les avis associés à un lieu spécifique.
    Permet de récupérer tous les avis pour un lieu donné.
    """
    @api.response(200, 'Liste des avis pour le lieu récupérée avec succès')
    @api.response(404, 'Lieu non trouvé')
    def get(self, place_id):
        """
        Récupère tous les avis pour un lieu spécifique.
        
        Cette méthode renvoie une liste de tous les avis associés à un lieu particulier,
        y compris les informations sur les utilisateurs qui ont laissé ces avis.
        """
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name
                }
            } for review in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))
