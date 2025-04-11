"""
Ce fichier contient l'implémentation du repository spécifique pour les lieux.
Il étend le SQLAlchemyRepository pour ajouter des fonctionnalités spécifiques aux lieux.
"""

from app.models.place import Place
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    """
    Repository spécifique pour les lieux.
    Cette classe étend SQLAlchemyRepository pour ajouter des fonctionnalités
    spécifiques à la gestion des lieux.
    """
    
    def __init__(self):
        """
        Initialise le repository avec le modèle Place.
        """
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
        """
        Récupère tous les lieux appartenant à un propriétaire spécifique.
        
        :param owner_id: L'identifiant du propriétaire
        :return: Une liste de lieux appartenant au propriétaire
        """
        return self.model.query.filter_by(owner_id=owner_id).all()
    
    def get_places_by_price_range(self, min_price, max_price):
        """
        Récupère tous les lieux dont le prix est compris dans une fourchette spécifique.
        
        :param min_price: Le prix minimum
        :param max_price: Le prix maximum
        :return: Une liste de lieux dont le prix est compris dans la fourchette
        """
        return self.model.query.filter(
            self.model.price >= min_price,
            self.model.price <= max_price
        ).all()
    
    def get_places_by_location(self, lat, lng, radius):
        """
        Récupère tous les lieux situés dans un rayon spécifique autour d'un point.
        Cette méthode utilise une approximation simple de la distance euclidienne.
        Pour une recherche plus précise, il faudrait utiliser la formule de Haversine.
        
        :param lat: La latitude du point central
        :param lng: La longitude du point central
        :param radius: Le rayon de recherche en degrés (approximativement 111 km par degré)
        :return: Une liste de lieux situés dans le rayon spécifié
        """
        # Cette implémentation est une approximation simple
        # Pour une recherche plus précise, il faudrait utiliser la formule de Haversine
        # ou une extension spatiale de la base de données
        return self.model.query.filter(
            self.model.latitude.between(lat - radius, lat + radius),
            self.model.longitude.between(lng - radius, lng + radius)
        ).all()
