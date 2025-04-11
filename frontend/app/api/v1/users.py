"""
Ce fichier contient les endpoints de l'API pour la gestion des utilisateurs.
Il définit les routes pour créer, récupérer, mettre à jour et supprimer des utilisateurs.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade
from .decorators import admin_required

api = Namespace('users', description='Opérations sur les utilisateurs')

# Définition du modèle utilisateur pour la validation des entrées et la documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Prénom de l\'utilisateur'),
    'last_name': fields.String(required=True, description='Nom de famille de l\'utilisateur'),
    'email': fields.String(required=True, description='Adresse email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur'),
    'role': fields.String(required=False, description='Rôle de l\'utilisateur (user, admin)', enum=['user', 'admin'])
})

# Définition d'un modèle pour les mises à jour d'utilisateur où les champs sont optionnels
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='Prénom de l\'utilisateur'),
    'last_name': fields.String(required=False, description='Nom de famille de l\'utilisateur'),
    'email': fields.String(required=False, description='Adresse email de l\'utilisateur'),
    'password': fields.String(required=False, description='Mot de passe de l\'utilisateur'),
    'role': fields.String(required=False, description='Rôle de l\'utilisateur (user, admin)', enum=['user', 'admin'])
})

@api.route('/')
class UserList(Resource):
    """
    Ressource pour gérer la collection d'utilisateurs.
    Permet de créer un nouvel utilisateur et de récupérer la liste de tous les utilisateurs.
    """
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully registered')
    @api.response(400, 'Validation error')
    def post(self):
        """
        Enregistre un nouvel utilisateur.
        
        Cette méthode crée un nouvel utilisateur dans le système avec les informations fournies.
        Elle vérifie d'abord si l'email est déjà utilisé pour éviter les doublons.
        """
        user_data = api.payload
        
        try:
            # Check if email is already registered
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400
                
            # Create the new user (is_admin defaults to False)
            new_user = facade.create_user(user_data)
            
            # Return success message with user ID
            return {'id': new_user.id, 'message': 'User successfully registered'}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Liste des utilisateurs récupérée avec succès')
    def get(self):
        """
        Récupère tous les utilisateurs.
        
        Cette méthode renvoie une liste de tous les utilisateurs enregistrés dans le système,
        avec leurs informations de base (id, prénom, nom, email).
        """
        users = facade.get_all_users()
        user_list = [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'role': user.role} for user in users]
        return user_list, 200

@api.route('/<user_id>')
class UserResource(Resource):
    """
    Ressource pour gérer un utilisateur spécifique.
    Permet de récupérer, mettre à jour et supprimer les détails d'un utilisateur par son ID.
    """
    @api.response(200, 'Détails de l\'utilisateur récupérés avec succès')
    @api.response(404, 'Utilisateur non trouvé')
    def get(self, user_id):
        """
        Récupère les détails d'un utilisateur par son ID.
        
        Cette méthode renvoie les informations détaillées d'un utilisateur spécifique
        identifié par son ID unique.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'Utilisateur non trouvé'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'role': user.role}, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'Utilisateur mis à jour avec succès')
    @api.response(404, 'Utilisateur non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(401, 'Non autorisé - Authentification requise')
    @api.response(403, 'Interdit - Vous ne pouvez modifier que vos propres informations')
    @jwt_required()
    def put(self, user_id):
        """
        Met à jour les détails d'un utilisateur.
        
        Cette méthode permet de modifier les informations d'un utilisateur existant.
        Seuls les champs fournis dans la requête seront mis à jour.
        Nécessite une authentification JWT.
        
        Les utilisateurs normaux ne peuvent modifier que leurs propres informations et ne peuvent pas modifier
        leur email ou mot de passe.
        
        Les administrateurs peuvent modifier n'importe quel utilisateur, y compris l'email et le mot de passe.
        """
        try:
            # Récupère l'identité de l'utilisateur à partir du token JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Vérifie si l'utilisateur authentifié est celui qu'on essaie de modifier ou un admin
            if user_id != current_user_id and not is_admin:
                api.abort(403, 'Unauthorized action')
            
            # Vérifie si l'utilisateur existe
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'Utilisateur non trouvé'}, 404
                
            # Crée un nouveau dictionnaire avec uniquement les champs autorisés
            user_data = dict(api.payload)
            
            # Empêche la modification de l'email et du mot de passe pour les utilisateurs non-admin
            if not is_admin and ('email' in user_data or 'password' in user_data):
                api.abort(400, 'You cannot modify email or password')
            
            # Vérifie si l'email est déjà utilisé par un autre utilisateur
            if is_admin and 'email' in user_data:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email déjà utilisé par un autre utilisateur'}, 400
                
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'Utilisateur non trouvé'}, 404
            return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email, 'role': updated_user.role}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
            
    @api.response(200, 'Utilisateur supprimé avec succès')
    @api.response(404, 'Utilisateur non trouvé')
    @api.response(401, 'Non autorisé - Authentification requise')
    @api.response(403, 'Interdit - Vous ne pouvez supprimer que votre propre compte')
    @jwt_required()
    def delete(self, user_id):
        """
        Supprime un utilisateur.
        
        Cette méthode permet de supprimer un utilisateur existant.
        Nécessite une authentification JWT.
        
        Les utilisateurs normaux ne peuvent supprimer que leur propre compte.
        Les administrateurs peuvent supprimer n'importe quel compte.
        
        La suppression d'un utilisateur entraîne également la suppression de tous ses lieux et avis.
        """
        try:
            # Récupère l'identité de l'utilisateur à partir du token JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Vérifie si l'utilisateur authentifié est celui qu'on essaie de supprimer ou un admin
            if user_id != current_user_id and not is_admin:
                api.abort(403, 'Unauthorized action')
            
            # Vérifie si l'utilisateur existe
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'Utilisateur non trouvé'}, 404
            
            # Supprime l'utilisateur
            facade.delete_user(user_id)
            
            return {'message': 'Utilisateur supprimé avec succès'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
