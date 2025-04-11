"""
Ce module initialise les modèles de l'application.
Il importe toutes les classes de modèles pour faciliter leur utilisation dans d'autres parties de l'application.
"""

from .base_model import BaseModel
from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity

__all__ = ['BaseModel', 'User', 'Place', 'Review', 'Amenity']
