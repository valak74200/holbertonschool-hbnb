"""
Ce fichier contient l'implémentation du repository spécifique pour les équipements.
Il étend le SQLAlchemyRepository pour ajouter des fonctionnalités spécifiques aux équipements.
"""

from app.models.amenity import Amenity
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    """
    Repository spécifique pour les équipements.
    Cette classe étend SQLAlchemyRepository pour ajouter des fonctionnalités
    spécifiques à la gestion des équipements.
    """
    
    def __init__(self):
        """
        Initialise le repository avec le modèle Amenity.
        """
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """
        Récupère un équipement par son nom.
        
        :param name: Le nom de l'équipement à rechercher
        :return: L'équipement correspondant ou None s'il n'existe pas
        """
        return self.model.query.filter_by(name=name).first()
    
    def search_amenities_by_name(self, search_term):
        """
        Recherche des équipements dont le nom contient un terme spécifique.
        
        :param search_term: Le terme à rechercher dans le nom des équipements
        :return: Une liste d'équipements dont le nom contient le terme recherché
        """
        return self.model.query.filter(self.model.name.ilike(f'%{search_term}%')).all()
