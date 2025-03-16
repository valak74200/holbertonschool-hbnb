"""
Ce fichier contient la classe de base pour tous les modèles de l'application.
Il fournit des attributs et des méthodes communs à tous les modèles.
"""

import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    """
    Classe de base pour tous les modèles de l'application.
    Elle fournit un identifiant unique, des horodatages de création et de mise à jour,
    ainsi que des méthodes pour sauvegarder et mettre à jour les objets.
    """
    __abstract__ = True  # Cela garantit que SQLAlchemy ne crée pas de table pour BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def update(self, data):
        """
        Met à jour les attributs de l'objet en fonction du dictionnaire fourni.
        
        :param data: Un dictionnaire contenant les nouvelles valeurs des attributs.
        """
        if not isinstance(data, dict):
            raise ValueError("L'argument 'data' doit être un dictionnaire")
        
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
