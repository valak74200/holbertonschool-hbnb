"""
Ce fichier contient la classe User qui représente un utilisateur dans l'application.
"""

from typing import Optional
import re
from .base_model import BaseModel

class User(BaseModel):
    """
    Classe représentant un utilisateur dans l'application.
    Hérite de BaseModel pour les fonctionnalités communes.
    """

    def __init__(self, first_name: str, last_name: str, email: str, 
                 password: str, is_admin: bool = False):
        """
        Initialise un nouvel utilisateur.

        :param first_name: Prénom de l'utilisateur
        :param last_name: Nom de famille de l'utilisateur
        :param email: Adresse email de l'utilisateur
        :param password: Mot de passe de l'utilisateur
        :param is_admin: Indique si l'utilisateur est un administrateur (par défaut False)
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    @property
    def password(self) -> str:
        """Getter pour le mot de passe de l'utilisateur."""
        return self._password

    @password.setter
    def password(self, value: str):
        """
        Setter pour le mot de passe de l'utilisateur.
        Vérifie que le mot de passe n'est pas vide et a au moins 8 caractères.
        """
        if not value or len(value) < 8:
            raise ValueError("Le mot de passe est requis et doit avoir au moins 8 caractères.")
        self._password = value

    @property
    def first_name(self) -> str:
        """Getter pour le prénom de l'utilisateur."""
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        """
        Setter pour le prénom de l'utilisateur.
        Vérifie que le prénom n'est pas vide et ne dépasse pas 50 caractères.
        """
        if not value or len(value) > 50:
            raise ValueError("Le prénom est requis et ne doit pas dépasser 50 caractères.")
        self._first_name = value

    @property
    def last_name(self) -> str:
        """Getter pour le nom de famille de l'utilisateur."""
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        """
        Setter pour le nom de famille de l'utilisateur.
        Vérifie que le nom n'est pas vide et ne dépasse pas 50 caractères.
        """
        if not value or len(value) > 50:
            raise ValueError("Le nom de famille est requis et ne doit pas dépasser 50 caractères.")
        self._last_name = value

    @property
    def email(self) -> str:
        """Getter pour l'adresse email de l'utilisateur."""
        return self._email

    @email.setter
    def email(self, value: str):
        """
        Setter pour l'adresse email de l'utilisateur.
        Vérifie que l'email est valide selon un format simple.
        """
        if not value or not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Format d'email invalide.")
        self._email = value

    def __str__(self):
        """Retourne une représentation en chaîne de caractères de l'utilisateur."""
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, is_admin={self.is_admin})"
