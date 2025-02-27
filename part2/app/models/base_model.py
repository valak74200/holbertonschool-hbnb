"""
Ce fichier contient la classe de base pour tous les modèles de l'application.
Il fournit des attributs et des méthodes communs à tous les modèles.
"""

import uuid
from datetime import datetime

class BaseModel:
    """
    Classe de base pour tous les modèles de l'application.
    Elle fournit un identifiant unique, des horodatages de création et de mise à jour,
    ainsi que des méthodes pour sauvegarder et mettre à jour les objets.
    """
    def __init__(self):
        """
        Initialise un nouvel objet avec un ID unique et des horodatages.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Met à jour l'horodatage de dernière modification chaque fois que l'objet est modifié.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Met à jour les attributs de l'objet en fonction du dictionnaire fourni.
        
        :param data: Un dictionnaire contenant les nouvelles valeurs des attributs.
        """
        if not isinstance(data, dict):
            raise ValueError("L'argument 'data' doit être un dictionnaire")
        
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Met à jour l'horodatage de dernière modification
