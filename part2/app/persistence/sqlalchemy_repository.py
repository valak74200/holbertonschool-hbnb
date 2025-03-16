"""
Ce fichier contient l'implémentation du repository SQLAlchemy pour la persistance des données.
Il implémente l'interface Repository définie dans repository.py.
"""

from app.persistence.repository import Repository
from app.extensions import db

class SQLAlchemyRepository(Repository):
    """
    Implémentation SQLAlchemy du repository.
    Cette classe utilise SQLAlchemy pour effectuer les opérations CRUD sur la base de données.
    """
    
    def __init__(self, model):
        """
        Initialise le repository avec un modèle SQLAlchemy.
        
        :param model: La classe du modèle SQLAlchemy à utiliser
        """
        self.model = model

    def add(self, obj):
        """
        Ajoute un objet à la base de données.
        
        :param obj: L'objet à ajouter
        """
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """
        Récupère un objet par son identifiant.
        
        :param obj_id: L'identifiant de l'objet à récupérer
        :return: L'objet correspondant à l'identifiant ou None s'il n'existe pas
        """
        return self.model.query.get(obj_id)

    def get_all(self):
        """
        Récupère tous les objets du repository.
        
        :return: Une liste contenant tous les objets
        """
        return self.model.query.all()

    def update(self, obj_id, data):
        """
        Met à jour un objet dans la base de données.
        
        :param obj_id: L'identifiant de l'objet à mettre à jour
        :param data: Un dictionnaire contenant les attributs à mettre à jour et leurs nouvelles valeurs
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """
        Supprime un objet de la base de données.
        
        :param obj_id: L'identifiant de l'objet à supprimer
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """
        Récupère un objet par la valeur d'un de ses attributs.
        
        :param attr_name: Le nom de l'attribut
        :param attr_value: La valeur de l'attribut
        :return: L'objet correspondant ou None s'il n'existe pas
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
