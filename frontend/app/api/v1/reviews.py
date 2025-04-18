"""
Ce fichier contient les endpoints de l'API pour la gestion des avis.
Il définit les routes pour créer, récupérer, mettre à jour et supprimer des avis.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Opérations sur les avis')

# Définition du modèle d'avis pour la validation des entrées et la documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Texte de l\'avis'),
    'rating': fields.Integer(required=True, description='Note du lieu (1-5)'),
    'user_id': fields.String(required=True, description='ID de l\'utilisateur'),
    'place_id': fields.String(required=True, description='ID du lieu')
})

# Définition d'un modèle pour les mises à jour d'avis où les champs sont optionnels
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Texte de l\'avis'),
    'rating': fields.Integer(required=False, description='Note du lieu (1-5)')
})

# Définition d'un modèle utilisateur simplifié pour les réponses d'avis
user_model = api.model('ReviewUser', {
    'id': fields.String(description='ID de l\'utilisateur'),
    'first_name': fields.String(description='Prénom de l\'utilisateur'),
    'last_name': fields.String(description='Nom de famille de l\'utilisateur')
})

# Définition d'un modèle de lieu simplifié pour les réponses d'avis
place_model = api.model('ReviewPlace', {
    'id': fields.String(description='ID du lieu'),
    'title': fields.String(description='Titre du lieu')
})

# Définition du modèle de réponse d'avis
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='ID de l\'avis'),
    'text': fields.String(description='Texte de l\'avis'),
    'rating': fields.Integer(description='Note du lieu (1-5)'),
    'user': fields.Nested(user_model, description='Utilisateur ayant écrit l\'avis'),
    'place': fields.Nested(place_model, description='Lieu concerné par l\'avis')
})

@api.route('/')
class ReviewList(Resource):
    """
    Ressource pour gérer la collection d'avis.
    Permet de créer un nouvel avis et de récupérer la liste de tous les avis.
    """
    @api.expect(review_model, validate=True)
    @api.response(201, 'Avis créé avec succès')
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(401, 'Non autorisé - Authentification requise')
    @api.response(403, 'Interdit - Vous ne pouvez pas évaluer votre propre lieu ou créer plusieurs avis pour le même lieu')
    @jwt_required()
    def post(self):
        """
        Enregistre un nouvel avis.
        
        Cette méthode crée un nouvel avis dans le système avec les informations fournies.
        Elle vérifie que toutes les données requises sont présentes et valides,
        notamment l'existence de l'utilisateur et du lieu concernés.
        Nécessite une authentification JWT.
        Les utilisateurs ne peuvent pas évaluer leurs propres lieux et ne peuvent créer qu'un seul avis par lieu.
        """
        try:
            # Récupère l'identité de l'utilisateur à partir du token JWT
            current_user_id = get_jwt_identity()
            
            # Modifie le payload pour s'assurer que l'user_id est celui de l'utilisateur authentifié
            review_data = dict(api.payload)
            review_data['user_id'] = current_user_id
            
            # Récupère le lieu pour vérifier si l'utilisateur en est le propriétaire
            place_id = review_data['place_id']
            place = facade.get_place(place_id)
            
            # Vérifie si l'utilisateur est le propriétaire du lieu
            if place.owner_id == current_user_id:
                api.abort(400, 'You cannot review your own place')
            
            # Vérifie si l'utilisateur a déjà laissé un avis pour ce lieu
            reviews_for_place = facade.get_reviews_by_place(place_id)
            if reviews_for_place:  # Check if reviews_for_place is not None
                for review in reviews_for_place:
                    if review.user.id == current_user_id:
                        api.abort(400, 'You have already reviewed this place')
            
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id
            }, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'Liste des avis récupérée avec succès')
    def get(self):
        """
        Récupère une liste de tous les avis.
        
        Cette méthode renvoie une liste de tous les avis enregistrés dans le système,
        avec leurs informations de base (id, texte, note, utilisateur, lieu).
        """
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        } for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    """
    Ressource pour gérer un avis spécifique.
    Permet de récupérer, mettre à jour et supprimer un avis par son ID.
    """
    @api.response(200, 'Détails de l\'avis récupérés avec succès')
    @api.response(404, 'Avis non trouvé')
    def get(self, review_id):
        """
        Récupère les détails d'un avis par son ID.
        
        Cette méthode renvoie les informations détaillées d'un avis spécifique
        identifié par son ID unique, y compris les informations sur l'utilisateur
        qui a laissé l'avis et le lieu concerné.
        """
        try:
            review = facade.get_review(review_id)
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name
                },
                'place': {
                    'id': review.place.id,
                    'title': review.place.title
                }
            }, 200
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Avis mis à jour avec succès')
    @api.response(404, 'Avis non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(401, 'Non autorisé - Authentification requise')
    @api.response(403, 'Interdit - Vous ne pouvez modifier que vos propres avis')
    @jwt_required()
    def put(self, review_id):
        """
        Met à jour les informations d'un avis.
        
        Cette méthode permet de modifier le texte et/ou la note d'un avis existant.
        Elle vérifie que les nouvelles données sont valides, notamment que la note
        est comprise entre 1 et 5.
        Nécessite une authentification JWT.
        
        Seul l'auteur de l'avis ou un administrateur peut le modifier.
        Les administrateurs peuvent modifier n'importe quel avis.
        """
        try:
            # Récupère l'identité de l'utilisateur à partir du token JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Vérifie si l'avis existe
            review = facade.get_review(review_id)
            
            # Vérifie si l'utilisateur authentifié est l'auteur de l'avis ou un administrateur
            if review.user.id != current_user_id and not is_admin:
                api.abort(403, 'Unauthorized action')
        except ValueError as e:
            api.abort(404, str(e))
            
        try:
            # Crée un nouveau dictionnaire avec uniquement les champs présents dans le payload
            update_data = {}
            for key, value in api.payload.items():
                if value is not None:
                    update_data[key] = value
            
            updated_review = facade.update_review(review_id, update_data)
            return {
                'message': 'Avis mis à jour avec succès',
                'review': {
                    'id': updated_review.id,
                    'text': updated_review.text,
                    'rating': updated_review.rating,
                    'user_id': updated_review.user.id,
                    'place_id': updated_review.place.id
                }
            }, 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'Avis supprimé avec succès')
    @api.response(404, 'Avis non trouvé')
    @api.response(401, 'Non autorisé - Authentification requise')
    @api.response(403, 'Interdit - Vous ne pouvez supprimer que vos propres avis')
    @jwt_required()
    def delete(self, review_id):
        """
        Supprime un avis.
        
        Cette méthode permet de supprimer définitivement un avis du système.
        Elle vérifie d'abord que l'avis existe avant de le supprimer.
        Nécessite une authentification JWT.
        
        Seul l'auteur de l'avis ou un administrateur peut le supprimer.
        Les administrateurs peuvent supprimer n'importe quel avis.
        """
        try:
            # Récupère l'identité de l'utilisateur à partir du token JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Vérifie si l'avis existe
            review = facade.get_review(review_id)
            
            # Vérifie si l'utilisateur authentifié est l'auteur de l'avis ou un administrateur
            if review.user.id != current_user_id and not is_admin:
                api.abort(403, 'Unauthorized action')
                
            facade.delete_review(review_id)
            return {'message': 'Avis supprimé avec succès'}, 200
        except ValueError as e:
            api.abort(404, str(e))
