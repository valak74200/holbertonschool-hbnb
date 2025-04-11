"""
Ce fichier contient l'implémentation du repository spécifique pour les utilisateurs.
Il étend le SQLAlchemyRepository pour ajouter des fonctionnalités spécifiques aux utilisateurs.
"""

from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """
    Repository spécifique pour les utilisateurs.
    Cette classe étend SQLAlchemyRepository pour ajouter des fonctionnalités
    spécifiques à la gestion des utilisateurs.
    """
    
    def __init__(self):
        """
        Initialise le repository avec le modèle User.
        """
        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Récupère un utilisateur par son adresse email.
        
        :param email: L'adresse email de l'utilisateur à rechercher
        :return: L'utilisateur correspondant ou None s'il n'existe pas
        """
        return self.model.query.filter_by(email=email).first()
    
    def get_users_by_role(self, role):
        """
        Récupère tous les utilisateurs ayant un rôle spécifique.
        
        :param role: Le rôle des utilisateurs à rechercher
        :return: Une liste d'utilisateurs ayant le rôle spécifié
        """
        return self.model.query.filter_by(role=role).all()
    
    def get_admins(self):
        """
        Récupère tous les utilisateurs administrateurs.
        
        :return: Une liste des utilisateurs administrateurs
        """
        return self.model.query.filter_by(is_admin=True).all()
