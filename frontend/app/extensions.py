"""
Ce fichier contient les extensions Flask utilisées par l'application.
"""

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Initialisation des extensions
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
