"""
Ce fichier contient les classes de base pour la persistance des données dans l'application.
Il définit une interface abstraite Repository et une implémentation en mémoire.
"""

from abc import ABC, abstractmethod

class Repository(ABC):
    """
    Interface abstraite définissant les opérations de base pour la persistance des données.
    Toutes les implémentations de repository doivent hériter de cette classe et implémenter ses méthodes.
    """
    @abstractmethod
    def add(self, obj):
        """
        Ajoute un objet au repository.
        
        :param obj: L'objet à ajouter
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Récupère un objet par son identifiant.
        
        :param obj_id: L'identifiant de l'objet à récupérer
        :return: L'objet correspondant à l'identifiant ou None s'il n'existe pas
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Récupère tous les objets du repository.
        
        :return: Une liste contenant tous les objets
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Met à jour un objet dans le repository.
        
        :param obj_id: L'identifiant de l'objet à mettre à jour
        :param data: Les données à mettre à jour
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Supprime un objet du repository.
        
        :param obj_id: L'identifiant de l'objet à supprimer
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Récupère un objet par la valeur d'un de ses attributs.
        
        :param attr_name: Le nom de l'attribut
        :param attr_value: La valeur de l'attribut
        :return: L'objet correspondant ou None s'il n'existe pas
        """
        pass



class InMemoryRepository(Repository):
    """
    Implémentation en mémoire du repository.
    Stocke les objets dans un dictionnaire en mémoire.
    Cette implémentation est principalement utilisée pour les tests et le développement.
    """
    _storage = {}  # Stockage partagé pour toutes les instances

    def add(self, obj):
        """
        Ajoute un objet au repository en mémoire.
        
        :param obj: L'objet à ajouter
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Récupère un objet par son identifiant.
        
        :param obj_id: L'identifiant de l'objet à récupérer
        :return: L'objet correspondant à l'identifiant ou None s'il n'existe pas
        """
        obj = self._storage.get(obj_id)
        return obj

    def get_all(self):
        """
        Récupère tous les objets du repository.
        
        :return: Une liste contenant tous les objets
        """
        all_objects = list(self._storage.values())
        return all_objects

    def update(self, obj_id, obj):
        """
        Met à jour un objet dans le repository.
        
        :param obj_id: L'identifiant de l'objet à mettre à jour
        :param obj: L'objet mis à jour
        """
        if obj_id in self._storage:
            self._storage[obj_id] = obj

    def delete(self, obj_id):
        """
        Supprime un objet du repository.
        
        :param obj_id: L'identifiant de l'objet à supprimer
        """
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """
        Récupère un objet par la valeur d'un de ses attributs.
        
        :param attr_name: Le nom de l'attribut
        :param attr_value: La valeur de l'attribut
        :return: L'objet correspondant ou None s'il n'existe pas
        """
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
