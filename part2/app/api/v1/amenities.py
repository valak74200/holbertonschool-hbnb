"""
Ce fichier contient les endpoints de l'API pour la gestion des équipements.
Il définit les routes pour créer, récupérer, mettre à jour et supprimer des équipements.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

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
    def post(self):
        """
        Enregistre un nouvel équipement.
        
        Cette méthode crée un nouvel équipement dans le système avec le nom fourni.
        Elle vérifie que le nom est présent et valide.
        """
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
    Permet de récupérer et de mettre à jour les détails d'un équipement par son ID.
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
    def put(self, amenity_id):
        """
        Met à jour les informations d'un équipement.
        
        Cette méthode permet de modifier le nom d'un équipement existant.
        Elle vérifie que le nouveau nom est valide.
        """
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
