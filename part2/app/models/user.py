"""
Ce fichier contient la classe User qui représente un utilisateur dans l'application.
"""

from typing import Optional
import re
from sqlalchemy.orm import validates, relationship
from .base_model import BaseModel
from app.extensions import bcrypt, db

# Définition des rôles utilisateur
class UserRole:
    USER = "user"
    ADMIN = "admin"

class User(BaseModel):
    """
    Classe représentant un utilisateur dans l'application.
    Hérite de BaseModel pour les fonctionnalités communes.
    """
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default=UserRole.USER)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Define one-to-many relationship with Place (a user can own many places)
    # Note: backref is defined in the Place model
    owned_places = db.relationship('Place', lazy=True, foreign_keys='Place._owner_id')
    
    # Define one-to-many relationship with Place (a user can be associated with many places)
    # Note: backref is defined in the Place model
    places = db.relationship('Place', lazy=True, foreign_keys='Place.user_id')
    
    # Define one-to-many relationship with Review (a user can write many reviews)
    # Note: backref is defined in the Review model
    reviews = db.relationship('Review', lazy=True, foreign_keys='Review.user_id')

    @validates('first_name')
    def validate_first_name(self, key, value):
        """Valide le prénom de l'utilisateur."""
        if not value or len(value) > 50:
            raise ValueError("Le prénom est requis et ne doit pas dépasser 50 caractères.")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        """Valide le nom de famille de l'utilisateur."""
        if not value or len(value) > 50:
            raise ValueError("Le nom de famille est requis et ne doit pas dépasser 50 caractères.")
        return value

    @validates('email')
    def validate_email(self, key, value):
        """Valide l'adresse email de l'utilisateur."""
        if not value or not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Format d'email invalide.")
        return value

    @validates('password')
    def validate_password(self, key, value):
        """Valide le mot de passe de l'utilisateur."""
        if not value or len(value) < 8:
            raise ValueError("Le mot de passe est requis et doit avoir au moins 8 caractères.")
        return value

    def hash_password(self, password: str):
        """
        Hashes the password before storing it.
        
        :param password: The plaintext password to hash
        """
        if not password or len(password) < 8:
            raise ValueError("Le mot de passe est requis et doit avoir au moins 8 caractères.")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def verify_password(self, password: str) -> bool:
        """
        Verifies if the provided password matches the hashed password.
        
        :param password: The plaintext password to verify
        :return: True if the password matches, False otherwise
        """
        return bcrypt.check_password_hash(self.password, password)

    def __str__(self):
        """Retourne une représentation en chaîne de caractères de l'utilisateur."""
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, role={self.role}, is_admin={self.is_admin})"
