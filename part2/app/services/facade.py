"""
Ce fichier contient la classe HBnBFacade qui sert d'interface entre les contrôleurs API
et la couche de persistance. Elle encapsule toute la logique métier de l'application.
"""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    """
    Façade qui fournit une interface unifiée pour toutes les opérations de l'application.
    Cette classe implémente le pattern Façade pour simplifier l'interface du système
    et masquer la complexité de la couche de persistance aux contrôleurs API.
    """
    def __init__(self):
        """
        Initialise une nouvelle instance de HBnBFacade avec un repository en mémoire.
        """
        self.repository = InMemoryRepository()

    def create_user(self, user_data):
        """
        Crée un nouvel utilisateur.
        
        :param user_data: Dictionnaire contenant les données de l'utilisateur
        :return: L'objet utilisateur créé
        :raises ValueError: Si des champs requis sont manquants
        """
        # Vérifie que tous les champs requis sont présents
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Champ requis manquant: {field}")
        
        user = User(**user_data)
        self.repository.add(user)
        return user

    def get_user(self, user_id):
        """
        Récupère un utilisateur par son identifiant.
        
        :param user_id: L'identifiant de l'utilisateur à récupérer
        :return: L'objet utilisateur correspondant ou None s'il n'existe pas
        """
        return self.repository.get(user_id)

    def get_user_by_email(self, email):
        """
        Récupère un utilisateur par son adresse email.
        
        :param email: L'adresse email de l'utilisateur à récupérer
        :return: L'objet utilisateur correspondant ou None s'il n'existe pas
        """
        return next((u for u in self.repository.get_all() if isinstance(u, User) and u.email == email), None)

    def get_all_users(self):
        """
        Récupère tous les utilisateurs.
        
        :return: Une liste contenant tous les objets utilisateur
        """
        return [u for u in self.repository.get_all() if isinstance(u, User)]

    def update_user(self, user_id, user_data):
        """
        Met à jour un utilisateur existant.
        
        :param user_id: L'identifiant de l'utilisateur à mettre à jour
        :param user_data: Dictionnaire contenant les nouvelles données de l'utilisateur
        :return: L'objet utilisateur mis à jour ou None s'il n'existe pas
        """
        user = self.repository.get(user_id)
        if user and isinstance(user, User):
            user.update(user_data)
            self.repository.update(user_id, user)
        return user

    def create_amenity(self, amenity_data):
        """
        Crée un nouvel équipement.
        
        :param amenity_data: Dictionnaire contenant les données de l'équipement
        :return: L'objet équipement créé
        :raises ValueError: Si le nom de l'équipement est manquant
        """
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Le nom de l'équipement est requis")
        amenity = Amenity(**amenity_data)
        self.repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Récupère un équipement par son identifiant.
        
        :param amenity_id: L'identifiant de l'équipement à récupérer
        :return: L'objet équipement correspondant
        :raises ValueError: Si l'équipement n'existe pas
        """
        amenity = self.repository.get(amenity_id)
        if not amenity or not isinstance(amenity, Amenity):
            raise ValueError(f"Équipement avec l'id {amenity_id} non trouvé")
        return amenity

    def get_all_amenities(self):
        """
        Récupère tous les équipements.
        
        :return: Une liste contenant tous les objets équipement
        """
        return [a for a in self.repository.get_all() if isinstance(a, Amenity)]

    def update_amenity(self, amenity_id, amenity_data):
        """
        Met à jour un équipement existant.
        
        :param amenity_id: L'identifiant de l'équipement à mettre à jour
        :param amenity_data: Dictionnaire contenant les nouvelles données de l'équipement
        :return: L'objet équipement mis à jour ou None s'il n'existe pas
        :raises ValueError: Si le nom de l'équipement est manquant
        """
        amenity = self.repository.get(amenity_id)
        if amenity and isinstance(amenity, Amenity):
            if 'name' not in amenity_data or not amenity_data['name']:
                raise ValueError("Le nom de l'équipement est requis")
            amenity.update(amenity_data)
            self.repository.update(amenity_id, amenity)
        return amenity

    def get_place(self, place_id):
        """
        Récupère un lieu par son identifiant.
        
        :param place_id: L'identifiant du lieu à récupérer
        :return: L'objet lieu correspondant
        :raises ValueError: Si le lieu n'existe pas
        """
        place = self.repository.get(place_id)
        if not place or not isinstance(place, Place):
            raise ValueError(f"Lieu avec l'id {place_id} non trouvé")
        return place

    def create_place(self, place_data):
        """
        Crée un nouveau lieu.
        
        :param place_data: Dictionnaire contenant les données du lieu
        :return: L'objet lieu créé
        :raises ValueError: Si des champs requis sont manquants ou invalides
        """
        # Valide les champs requis
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"Champ requis manquant: {field}")

        # Valide le prix, la latitude et la longitude
        if float(place_data['price']) < 0:
            raise ValueError("Le prix doit être positif ou nul")
        if not -90 <= float(place_data['latitude']) <= 90:
            raise ValueError("La latitude doit être comprise entre -90 et 90")
        if not -180 <= float(place_data['longitude']) <= 180:
            raise ValueError("La longitude doit être comprise entre -180 et 180")

        # Vérifie si le propriétaire existe
        owner = self.repository.get(place_data['owner_id'])
        if not owner or not isinstance(owner, User):
            raise ValueError(f"Propriétaire avec l'id {place_data['owner_id']} non trouvé")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=float(place_data['price']),
            latitude=float(place_data['latitude']),
            longitude=float(place_data['longitude']),
            owner_id=place_data['owner_id']
        )
        self.repository.add(place)
        return place

    def get_all_places(self):
        """
        Récupère tous les lieux.
        
        :return: Une liste contenant tous les objets lieu
        """
        return [p for p in self.repository.get_all() if isinstance(p, Place)]

    def update_place(self, place_id, place_data):
        """
        Met à jour un lieu existant.
        
        :param place_id: L'identifiant du lieu à mettre à jour
        :param place_data: Dictionnaire contenant les nouvelles données du lieu
        :return: L'objet lieu mis à jour
        :raises ValueError: Si le lieu n'existe pas ou si les données sont invalides
        """
        place = self.repository.get(place_id)
        if not place or not isinstance(place, Place):
            raise ValueError(f"Lieu avec l'id {place_id} non trouvé")

        # Vérifie que place_data est un dictionnaire
        if not isinstance(place_data, dict):
            raise ValueError(f"Entrée invalide: dictionnaire attendu, reçu {type(place_data)}")

        # Met à jour les attributs du lieu
        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)
            elif key == 'title':
                place.title = value
            elif key == 'description':
                place.description = value
            elif key == 'price':
                place.price = float(value)
            elif key == 'latitude':
                place.latitude = float(value)
            elif key == 'longitude':
                place.longitude = float(value)
            elif key == 'owner_id':
                place.owner_id = value

        # Met à jour le lieu dans le repository
        place.save()  # Met à jour l'horodatage de dernière modification
        self.repository.update(place_id, place)
        return place
        
    def create_review(self, review_data):
        """
        Crée un nouvel avis.
        
        :param review_data: Dictionnaire contenant les données de l'avis
        :return: L'objet avis créé
        :raises ValueError: Si des champs requis sont manquants ou invalides
        """
        # Valide les champs requis
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Champ requis manquant: {field}")
        
        # Valide la note
        try:
            rating = int(review_data['rating'])
            if not 1 <= rating <= 5:
                raise ValueError("La note doit être comprise entre 1 et 5")
        except (ValueError, TypeError):
            raise ValueError("La note doit être un entier compris entre 1 et 5")
        
        # Vérifie si l'utilisateur existe
        user = self.repository.get(review_data['user_id'])
        if not user or not isinstance(user, User):
            raise ValueError(f"Utilisateur avec l'id {review_data['user_id']} non trouvé")
        
        # Vérifie si le lieu existe
        place = self.repository.get(review_data['place_id'])
        if not place or not isinstance(place, Place):
            raise ValueError(f"Lieu avec l'id {review_data['place_id']} non trouvé")
        
        # Crée l'avis
        review = Review(
            text=review_data['text'],
            rating=rating,
            place=place,
            user=user
        )
        
        # Ajoute l'avis au repository
        self.repository.add(review)
        
        # Ajoute l'avis à la liste des avis du lieu
        place.add_review(review)
        self.repository.update(place.id, place)
        
        return review
    
    def get_review(self, review_id):
        """
        Récupère un avis par son identifiant.
        
        :param review_id: L'identifiant de l'avis à récupérer
        :return: L'objet avis correspondant
        :raises ValueError: Si l'avis n'existe pas
        """
        review = self.repository.get(review_id)
        if not review or not isinstance(review, Review):
            raise ValueError(f"Avis avec l'id {review_id} non trouvé")
        return review
    
    def get_all_reviews(self):
        """
        Récupère tous les avis.
        
        :return: Une liste contenant tous les objets avis
        """
        return [r for r in self.repository.get_all() if isinstance(r, Review)]
    
    def get_reviews_by_place(self, place_id):
        """
        Récupère tous les avis pour un lieu spécifique.
        
        :param place_id: L'identifiant du lieu pour lequel récupérer les avis
        :return: Une liste d'objets avis pour le lieu
        :raises ValueError: Si le lieu n'existe pas
        """
        # Vérifie si le lieu existe
        place = self.repository.get(place_id)
        if not place or not isinstance(place, Place):
            raise ValueError(f"Lieu avec l'id {place_id} non trouvé")
        
        # Retourne tous les avis pour le lieu
        return [r for r in self.repository.get_all() 
                if isinstance(r, Review) and r.place.id == place_id]
    
    def update_review(self, review_id, review_data):
        """
        Met à jour un avis existant.
        
        :param review_id: L'identifiant de l'avis à mettre à jour
        :param review_data: Dictionnaire contenant les nouvelles données de l'avis
        :return: L'objet avis mis à jour
        :raises ValueError: Si l'avis n'existe pas ou si les données sont invalides
        """
        # Vérifie si l'avis existe
        review = self.repository.get(review_id)
        if not review or not isinstance(review, Review):
            raise ValueError(f"Avis avec l'id {review_id} non trouvé")
        
        # Met à jour les attributs de l'avis
        if 'text' in review_data:
            review.text = review_data['text']
        
        if 'rating' in review_data:
            try:
                rating = int(review_data['rating'])
                if not 1 <= rating <= 5:
                    raise ValueError("La note doit être comprise entre 1 et 5")
                review.rating = rating
            except (ValueError, TypeError):
                raise ValueError("La note doit être un entier compris entre 1 et 5")
        
        # Met à jour l'avis dans le repository
        review.save()  # Met à jour l'horodatage de dernière modification
        self.repository.update(review_id, review)
        
        return review
    
    def delete_review(self, review_id):
        """
        Supprime un avis.
        
        :param review_id: L'identifiant de l'avis à supprimer
        :return: True si la suppression a réussi, False sinon
        :raises ValueError: Si l'avis n'existe pas
        """
        # Vérifie si l'avis existe
        review = self.repository.get(review_id)
        if not review or not isinstance(review, Review):
            raise ValueError(f"Avis avec l'id {review_id} non trouvé")
        
        # Supprime l'avis de la liste des avis du lieu
        place = review.place
        if place and hasattr(place, 'reviews'):
            place.reviews = [r for r in place.reviews if r.id != review_id]
            self.repository.update(place.id, place)
        
        # Supprime l'avis du repository
        self.repository.delete(review_id)
        
        return True

facade = HBnBFacade()
