"""
Ce fichier contient la classe Place qui représente un lieu dans l'application.
"""

from typing import Optional, List
from .base_model import BaseModel
from .user import User

class Place(BaseModel):
    """
    Classe représentant un lieu dans l'application.
    Hérite de BaseModel pour les fonctionnalités communes.
    """

    def __init__(self, title: str, description: Optional[str], price: float,
                 latitude: float, longitude: float, owner_id: str):
        """
        Initialise un nouveau lieu.

        :param title: Titre du lieu
        :param description: Description du lieu (optionnel)
        :param price: Prix par nuit
        :param latitude: Latitude du lieu
        :param longitude: Longitude du lieu
        :param owner_id: ID du propriétaire du lieu
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

    def update(self, data: dict):
        """
        Met à jour les attributs de l'objet en fonction du dictionnaire fourni.
        
        :param data: Un dictionnaire contenant les nouvelles valeurs des attributs.
        """
        if not isinstance(data, dict):
            raise ValueError(f"L'argument 'data' doit être un dictionnaire. Reçu: {type(data)}")
        
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Met à jour l'horodatage de dernière modification

    @property
    def title(self) -> str:
        """Getter pour le titre du lieu."""
        return self._title

    @title.setter
    def title(self, value: str):
        """
        Setter pour le titre du lieu.
        Vérifie que le titre n'est pas vide et ne dépasse pas 100 caractères.
        """
        if not value or len(value) > 100:
            raise ValueError("Le titre est requis et ne doit pas dépasser 100 caractères.")
        self._title = value

    @property
    def price(self) -> float:
        """Getter pour le prix du lieu."""
        return self._price

    @price.setter
    def price(self, value: float):
        """
        Setter pour le prix du lieu.
        Vérifie que le prix est une valeur positive.
        """
        if value <= 0:
            raise ValueError("Le prix doit être une valeur positive.")
        self._price = value

    @property
    def latitude(self) -> float:
        """Getter pour la latitude du lieu."""
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        """
        Setter pour la latitude du lieu.
        Vérifie que la latitude est comprise entre -90.0 et 90.0.
        """
        if not -90.0 <= value <= 90.0:
            raise ValueError("La latitude doit être comprise entre -90.0 et 90.0.")
        self._latitude = value

    @property
    def longitude(self) -> float:
        """Getter pour la longitude du lieu."""
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        """
        Setter pour la longitude du lieu.
        Vérifie que la longitude est comprise entre -180.0 et 180.0.
        """
        if not -180.0 <= value <= 180.0:
            raise ValueError("La longitude doit être comprise entre -180.0 et 180.0.")
        self._longitude = value

    @property
    def owner_id(self) -> str:
        """Getter pour l'ID du propriétaire du lieu."""
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        """
        Setter pour l'ID du propriétaire du lieu.
        Vérifie que l'ID du propriétaire n'est pas vide.
        """
        if not value:
            raise ValueError("L'ID du propriétaire ne peut pas être vide.")
        self._owner_id = value

    def add_review(self, review):
        """Ajoute un avis au lieu."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Ajoute un équipement au lieu."""
        self.amenities.append(amenity)

    def __str__(self):
        """Retourne une représentation en chaîne de caractères du lieu."""
        return f"Place(id={self.id}, title={self.title}, price={self.price}, owner_id={self.owner_id})"
