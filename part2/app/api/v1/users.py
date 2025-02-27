"""
Ce fichier contient les endpoints de l'API pour la gestion des utilisateurs.
Il définit les routes pour créer, récupérer, mettre à jour et supprimer des utilisateurs.
"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('users', description='Opérations sur les utilisateurs')

# Définition du modèle utilisateur pour la validation des entrées et la documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Prénom de l\'utilisateur'),
    'last_name': fields.String(required=True, description='Nom de famille de l\'utilisateur'),
    'email': fields.String(required=True, description='Adresse email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur')
})

# Définition d'un modèle pour les mises à jour d'utilisateur où les champs sont optionnels
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='Prénom de l\'utilisateur'),
    'last_name': fields.String(required=False, description='Nom de famille de l\'utilisateur'),
    'email': fields.String(required=False, description='Adresse email de l\'utilisateur'),
    'password': fields.String(required=False, description='Mot de passe de l\'utilisateur')
})

@api.route('/')
class UserList(Resource):
    """
    Ressource pour gérer la collection d'utilisateurs.
    Permet de créer un nouvel utilisateur et de récupérer la liste de tous les utilisateurs.
    """
    @api.expect(user_model, validate=True)
    @api.response(201, 'Utilisateur créé avec succès')
    @api.response(400, 'Email déjà enregistré ou données d\'entrée invalides')
    def post(self):
        """
        Enregistre un nouvel utilisateur.
        
        Cette méthode crée un nouvel utilisateur dans le système avec les informations fournies.
        Elle vérifie d'abord si l'email est déjà utilisé pour éviter les doublons.
        """
        user_data = api.payload

        try:
            # Vérifie l'unicité de l'email (à remplacer par une validation réelle avec persistance)
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email déjà enregistré'}, 400

            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
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
        user_list = [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users]
        return user_list, 200

@api.route('/<user_id>')
class UserResource(Resource):
    """
    Ressource pour gérer un utilisateur spécifique.
    Permet de récupérer et de mettre à jour les détails d'un utilisateur par son ID.
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
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'Utilisateur mis à jour avec succès')
    @api.response(404, 'Utilisateur non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    def put(self, user_id):
        """
        Met à jour les détails d'un utilisateur.
        
        Cette méthode permet de modifier les informations d'un utilisateur existant.
        Seuls les champs fournis dans la requête seront mis à jour.
        """
        user_data = api.payload
        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'Utilisateur non trouvé'}, 404
            return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
