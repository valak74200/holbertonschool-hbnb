"""
Ce module gère la persistance des données pour l'application HBnB.
Il fournit des interfaces et des implémentations pour stocker et récupérer
les objets du modèle de l'application.
"""

from .repository import Repository, InMemoryRepository
from .sqlalchemy_repository import SQLAlchemyRepository
from .user_repository import UserRepository

__all__ = ['Repository', 'InMemoryRepository', 'SQLAlchemyRepository', 'UserRepository']
