"""
Ce fichier contient l'implémentation du repository spécifique pour les avis.
Il étend le SQLAlchemyRepository pour ajouter des fonctionnalités spécifiques aux avis.
"""

from app.models.review import Review
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    """
    Repository spécifique pour les avis.
    Cette classe étend SQLAlchemyRepository pour ajouter des fonctionnalités
    spécifiques à la gestion des avis.
    """
    
    def __init__(self):
        """
        Initialise le repository avec le modèle Review.
        """
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        """
        Récupère tous les avis pour un lieu spécifique.
        
        :param place_id: L'identifiant du lieu
        :return: Une liste d'avis pour le lieu
        """
        return self.model.query.filter_by(place_id=place_id).all()
    
    def get_reviews_by_user(self, user_id):
        """
        Récupère tous les avis laissés par un utilisateur spécifique.
        
        :param user_id: L'identifiant de l'utilisateur
        :return: Une liste d'avis laissés par l'utilisateur
        """
        return self.model.query.filter_by(user_id=user_id).all()
    
    def get_reviews_by_rating(self, rating):
        """
        Récupère tous les avis ayant une note spécifique.
        
        :param rating: La note à rechercher (entre 1 et 5)
        :return: Une liste d'avis ayant la note spécifiée
        """
        return self.model.query.filter_by(rating=rating).all()
    
    def get_average_rating_for_place(self, place_id):
        """
        Calcule la note moyenne pour un lieu spécifique.
        
        :param place_id: L'identifiant du lieu
        :return: La note moyenne ou None si le lieu n'a pas d'avis
        """
        from sqlalchemy import func
        result = self.model.query.with_entities(
            func.avg(self.model.rating).label('average')
        ).filter_by(place_id=place_id).first()
        
        return result.average if result and result.average else None
