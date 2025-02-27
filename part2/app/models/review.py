"""
Ce fichier contient la classe Review qui représente un avis dans l'application.
"""

from .base_model import BaseModel
from .user import User

class Review(BaseModel):
    """
    Classe représentant un avis dans l'application.
    Hérite de BaseModel pour les fonctionnalités communes.
    """

    def __init__(self, text: str, rating: int, place, user: User):
        """
        Initialise un nouvel avis.

        :param text: Texte de l'avis
        :param rating: Note donnée (entre 1 et 5)
        :param place: Lieu concerné par l'avis (instance de Place)
        :param user: Utilisateur ayant laissé l'avis (instance de User)
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self) -> str:
        """Getter pour le texte de l'avis."""
        return self._text

    @text.setter
    def text(self, value: str):
        """
        Setter pour le texte de l'avis.
        Vérifie que le texte n'est pas vide.
        """
        if not value:
            raise ValueError("Le texte de l'avis est requis.")
        self._text = value

    @property
    def rating(self) -> int:
        """Getter pour la note de l'avis."""
        return self._rating

    @rating.setter
    def rating(self, value: int):
        """
        Setter pour la note de l'avis.
        Vérifie que la note est comprise entre 1 et 5.
        """
        if not 1 <= value <= 5:
            raise ValueError("La note doit être comprise entre 1 et 5.")
        self._rating = value

    @property
    def place(self):
        """Getter pour le lieu concerné par l'avis."""
        return self._place

    @place.setter
    def place(self, value):
        """
        Setter pour le lieu concerné par l'avis.
        Vérifie que le lieu est une instance de la classe Place.
        """
        from .place import Place  # Import local pour éviter l'import circulaire
        if not isinstance(value, Place):
            raise ValueError("Le lieu doit être une instance de la classe Place.")
        self._place = value

    @property
    def user(self) -> User:
        """Getter pour l'utilisateur ayant laissé l'avis."""
        return self._user

    @user.setter
    def user(self, value: User):
        """
        Setter pour l'utilisateur ayant laissé l'avis.
        Vérifie que l'utilisateur est une instance de la classe User.
        """
        if not isinstance(value, User):
            raise ValueError("L'utilisateur doit être une instance de la classe User.")
        self._user = value

    def __str__(self):
        """Retourne une représentation en chaîne de caractères de l'avis."""
        return f"Review(id={self.id}, rating={self.rating}, user={self.user.id}, place={self.place.id})"
