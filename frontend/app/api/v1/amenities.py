"""
Ce fichier contient les endpoints de l'API pour la gestion des équipements.
Il définit les routes pour créer, récupérer, mettre à jour et supprimer des équipements.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from .decorators import admin_required

api = Namespace('amenities', description='Opérations sur les équipements')

# Définition du modèle d'équipement pour la validation des entrées et la documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Nom de l\'équipement')
})

# Définition d'un modèle pour les mises à jour d'équipement où les champs sont optionnels
amenity_update_model = api.model('AmenityUpdate', {
    'name': fields.String(required=False, description='Nom de l\'équipement')
})

@api.route('/')
class AmenityList(Resource):
    """
    Ressource pour gérer la collection d'équipements.
    Permet de créer un nouvel équipement et de récupérer la liste de tous les équipements.
    """
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Équipement créé avec succès')
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(401, 'Non autorisé - Authentification requise')
    @jwt_required()
    def post(self):
        """
        Enregistre un nouvel équipement.
        
        Cette méthode crée un nouvel équipement dans le système avec le nom fourni.
        Elle vérifie que le nom est présent et valide.
        Nécessite une authentification JWT.
        """
        # Récupère l'identité de l'utilisateur à partir du token JWT
        current_user_id = get_jwt_identity()
        
        # L'authentification JWT est suffisante pour créer un équipement
        # Aucune vérification d'administrateur n'est nécessaire
        
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'Liste des équipements récupérée avec succès')
    def get(self):
        """
        Récupère une liste de tous les équipements.
        
        Cette méthode renvoie une liste de tous les équipements enregistrés dans le système,
        avec leurs informations de base (id, nom).
        """
        amenities = facade.get_all_amenities()
        return [{
            'id': amenity.id,
            'name': amenity.name
        } for amenity in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
    Ressource pour gérer un équipement spécifique.
    Permet de récupérer, mettre à jour et supprimer les détails d'un équipement par son ID.
    """
    @api.response(200, 'Détails de l\'équipement récupérés avec succès')
    @api.response(404, 'Équipement non trouvé')
    def get(self, amenity_id):
        """
        Récupère les détails d'un équipement par son ID.
        
        Cette méthode renvoie les informations détaillées d'un équipement spécifique
        identifié par son ID unique.
        """
        try:
            amenity = facade.get_amenity(amenity_id)
            return {
                'id': amenity.id,
                'name': amenity.name
            }, 200
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(amenity_update_model, validate=True)
    @api.response(200, 'Équipement mis à jour avec succès')
    @api.response(404, 'Équipement non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(401, 'Non autorisé - Authentification requise')
    @jwt_required()
    def put(self, amenity_id):
        """
        Met à jour les informations d'un équipement.
        
        Cette méthode permet de modifier le nom d'un équipement existant.
        Elle vérifie que le nouveau nom est valide.
        Nécessite une authentification JWT.
        """
        # Récupère l'identité de l'utilisateur à partir du token JWT
        current_user_id = get_jwt_identity()
        
        # L'authentification JWT est suffisante pour mettre à jour un équipement
        # Aucune vérification d'administrateur n'est nécessaire
        
        amenity_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'message': 'Équipement mis à jour avec succès',
                'amenity': {
                    'id': updated_amenity.id,
                    'name': updated_amenity.name
                }
            }, 200
        except ValueError as e:
            if "non trouvé" in str(e):
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))
                
    @api.response(200, 'Équipement supprimé avec succès')
    @api.response(404, 'Équipement non trouvé')
    @api.response(401, 'Non autorisé - Authentification requise')
    @jwt_required()
    def delete(self, amenity_id):
        """
        Supprime un équipement.
        
        Cette méthode permet de supprimer un équipement existant.
        Nécessite une authentification JWT.
        
        Tout utilisateur authentifié peut supprimer un équipement.
        """
        # Récupère l'identité de l'utilisateur à partir du token JWT
        current_user_id = get_jwt_identity()
        
        try:
            # Vérifie si l'équipement existe
            amenity = facade.get_amenity(amenity_id)
            
            # Supprime l'équipement
            facade.delete_amenity(amenity_id)
            
            return {'message': 'Équipement supprimé avec succès'}, 200
        except ValueError as e:
            api.abort(404, str(e))
