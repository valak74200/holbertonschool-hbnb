"""
Ce fichier contient les endpoints de l'API pour les opérations d'administration.
Il définit les routes pour gérer les utilisateurs, les équipements, les lieux et les avis
qui nécessitent des privilèges d'administrateur.
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace('admin', description='Opérations d\'administration')

# Définition du modèle utilisateur pour la validation des entrées et la documentation
user_model = api.model('AdminUser', {
    'first_name': fields.String(required=True, description='Prénom de l\'utilisateur'),
    'last_name': fields.String(required=True, description='Nom de famille de l\'utilisateur'),
    'email': fields.String(required=True, description='Adresse email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur'),
    'role': fields.String(required=False, description='Rôle de l\'utilisateur (user, admin)', enum=['user', 'admin']),
    'is_admin': fields.Boolean(required=False, description='Indique si l\'utilisateur est un administrateur')
})

# Définition d'un modèle pour les mises à jour d'utilisateur où les champs sont optionnels
user_update_model = api.model('AdminUserUpdate', {
    'first_name': fields.String(required=False, description='Prénom de l\'utilisateur'),
    'last_name': fields.String(required=False, description='Nom de famille de l\'utilisateur'),
    'email': fields.String(required=False, description='Adresse email de l\'utilisateur'),
    'password': fields.String(required=False, description='Mot de passe de l\'utilisateur'),
    'role': fields.String(required=False, description='Rôle de l\'utilisateur (user, admin)', enum=['user', 'admin']),
    'is_admin': fields.Boolean(required=False, description='Indique si l\'utilisateur est un administrateur')
})

@api.route('/users')
class AdminUserList(Resource):
    """
    Ressource pour gérer la collection d'utilisateurs en tant qu'administrateur.
    Permet de créer un nouvel utilisateur avec des privilèges d'administrateur.
    """
    @api.expect(user_model, validate=True)
    @api.response(201, 'Utilisateur créé avec succès')
    @api.response(400, 'Email déjà enregistré ou données d\'entrée invalides')
    @api.response(401, 'Non autorisé - Authentification requise')
    @api.response(403, 'Interdit - Privilèges d\'administrateur requis')
    @jwt_required()
    def post(self):
        """
        Enregistre un nouvel utilisateur en tant qu'administrateur.
        
        Cette méthode crée un nouvel utilisateur dans le système avec les informations fournies.
        Elle vérifie d'abord si l'email est déjà utilisé pour éviter les doublons.
        Nécessite des privilèges d'administrateur.
        """
        # Vérifie si l'utilisateur est un administrateur
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'message': 'Admin privileges required'}, 403
        
        user_data = api.payload

        try:
            # Vérifie l'unicité de l'email
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email déjà enregistré'}, 400

            new_user = facade.create_user(user_data)
            # Modifié pour ne retourner que l'ID et un message de succès, conformément aux exigences de sécurité
            return {'id': new_user.id, 'message': 'Utilisateur créé avec succès'}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    """
    Ressource pour gérer un utilisateur spécifique en tant qu'administrateur.
    Permet de mettre à jour les détails d'un utilisateur, y compris l'email et le mot de passe.
    """
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'Utilisateur mis à jour avec succès')
    @api.response(404, 'Utilisateur non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(401, 'Non autorisé - Authentification requise')
    @api.response(403, 'Interdit - Privilèges d\'administrateur requis')
    @jwt_required()
    def put(self, user_id):
        """
        Met à jour les détails d'un utilisateur en tant qu'administrateur.
        
        Cette méthode permet de modifier les informations d'un utilisateur existant,
        y compris l'email et le mot de passe.
        Nécessite des privilèges d'administrateur.
        """
        # Vérifie si l'utilisateur est un administrateur
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'message': 'Admin privileges required'}, 403
        
        try:
            # Vérifie si l'utilisateur existe
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'Utilisateur non trouvé'}, 404
            
            # Crée un nouveau dictionnaire avec uniquement les champs présents dans le payload
            user_data = dict(api.payload)
            
            # Vérifie si l'email est déjà utilisé par un autre utilisateur
            if 'email' in user_data:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email déjà utilisé par un autre utilisateur'}, 400
            
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'Utilisateur non trouvé'}, 404
            
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'role': updated_user.role,
                'is_admin': updated_user.is_admin
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/amenities')
class AdminAmenityList(Resource):
    """
    Ressource pour gérer la collection d'équipements en tant qu'administrateur.
    Permet de créer un nouvel équipement.
    """
    @api.expect(api.model('AdminAmenity', {
        'name': fields.String(required=True, description='Nom de l\'équipement')
    }), validate=True)
    @api.response(201, 'Équipement créé avec succès')
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(401, 'Non autorisé - Authentification requise')
    @api.response(403, 'Interdit - Privilèges d\'administrateur requis')
    @jwt_required()
    def post(self):
        """
        Enregistre un nouvel équipement en tant qu'administrateur.
        
        Cette méthode crée un nouvel équipement dans le système avec le nom fourni.
        Elle vérifie que le nom est présent et valide.
        Nécessite des privilèges d'administrateur.
        """
        # Vérifie si l'utilisateur est un administrateur
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'message': 'Admin privileges required'}, 403
        
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/amenities/<amenity_id>')
class AdminAmenityResource(Resource):
    """
    Ressource pour gérer un équipement spécifique en tant qu'administrateur.
    Permet de mettre à jour les détails d'un équipement.
    """
    @api.expect(api.model('AdminAmenityUpdate', {
        'name': fields.String(required=False, description='Nom de l\'équipement')
    }), validate=True)
    @api.response(200, 'Équipement mis à jour avec succès')
    @api.response(404, 'Équipement non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(401, 'Non autorisé - Authentification requise')
    @api.response(403, 'Interdit - Privilèges d\'administrateur requis')
    @jwt_required()
    def put(self, amenity_id):
        """
        Met à jour les informations d'un équipement en tant qu'administrateur.
        
        Cette méthode permet de modifier le nom d'un équipement existant.
        Elle vérifie que le nouveau nom est valide.
        Nécessite des privilèges d'administrateur.
        """
        # Vérifie si l'utilisateur est un administrateur
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'message': 'Admin privileges required'}, 403
        
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
                return {'error': str(e)}, 404
            else:
                return {'error': str(e)}, 400
