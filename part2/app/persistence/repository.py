from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    _storage = {}  # Shared storage for all instances

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        obj = self._storage.get(obj_id)
        return obj

    def get_all(self):
        all_objects = list(self._storage.values())
        return all_objects

    def update(self, obj_id, obj):
        """
        Update an object in the repository.
        
        :param obj_id: The ID of the object to update
        :param obj: The updated object
        """
        if obj_id in self._storage:
            self._storage[obj_id] = obj

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
