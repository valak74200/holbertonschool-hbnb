"""
Ce fichier contient la classe Amenity qui représente un équipement dans l'application.
"""

from sqlalchemy.orm import relationship
from .base_model import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    """
    Classe représentant un équipement dans l'application.
    Hérite de BaseModel pour les fonctionnalités communes.
    """
    __tablename__ = 'amenities'

    _name = db.Column('name', db.String(50), nullable=False)

    def __init__(self, name: str):
        """
        Initialise un nouvel équipement.

        :param name: Nom de l'équipement
        """
        super().__init__()
        self.name = name

    @property
    def name(self) -> str:
        """Getter pour le nom de l'équipement."""
        return self._name

    @name.setter
    def name(self, value: str):
        """
        Setter pour le nom de l'équipement.
        Vérifie que le nom n'est pas vide et ne dépasse pas 50 caractères.
        """
        if not value or len(value) > 50:
            raise ValueError("Le nom de l'équipement est requis et ne doit pas dépasser 50 caractères.")
        self._name = value

    def __str__(self):
        """Retourne une représentation en chaîne de caractères de l'équipement."""
        return f"Amenity(id={self.id}, name={self.name})"
