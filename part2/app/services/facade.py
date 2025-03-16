"""
Ce fichier contient la classe HBnBFacade qui sert d'interface entre les contrôleurs API
et la couche de persistance. Elle encapsule toute la logique métier de l'application.
"""

from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
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
        Initialise une nouvelle instance de HBnBFacade avec des repositories spécifiques.
        """
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

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
        
        # Crée l'utilisateur sans le mot de passe pour éviter la validation automatique
        password = user_data.pop('password')
        user = User(**user_data)
        
        # Hache le mot de passe avant de sauvegarder l'utilisateur
        user.hash_password(password)
        
        # Ajoute l'utilisateur au repository
        self.user_repo.add(user)
        
        return user

    def get_user(self, user_id):
        """
        Récupère un utilisateur par son identifiant.
        
        :param user_id: L'identifiant de l'utilisateur à récupérer
        :return: L'objet utilisateur correspondant ou None s'il n'existe pas
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Récupère un utilisateur par son adresse email.
        
        :param email: L'adresse email de l'utilisateur à récupérer
        :return: L'objet utilisateur correspondant ou None s'il n'existe pas
        """
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """
        Récupère tous les utilisateurs.
        
        :return: Une liste contenant tous les objets utilisateur
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Met à jour un utilisateur existant.
        
        :param user_id: L'identifiant de l'utilisateur à mettre à jour
        :param user_data: Dictionnaire contenant les nouvelles données de l'utilisateur
        :return: L'objet utilisateur mis à jour ou None s'il n'existe pas
        """
        user = self.user_repo.get(user_id)
        if user:
            # Traite le mot de passe séparément s'il est présent
            if 'password' in user_data:
                password = user_data.pop('password')
                user.hash_password(password)
            
            # Met à jour les autres attributs
            for key, value in user_data.items():
                setattr(user, key, value)
                
            # Sauvegarde les modifications
            self.user_repo.update(user_id, user_data)
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
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Récupère un équipement par son identifiant.
        
        :param amenity_id: L'identifiant de l'équipement à récupérer
        :return: L'objet équipement correspondant
        :raises ValueError: Si l'équipement n'existe pas
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError(f"Équipement avec l'id {amenity_id} non trouvé")
        return amenity

    def get_all_amenities(self):
        """
        Récupère tous les équipements.
        
        :return: Une liste contenant tous les objets équipement
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Met à jour un équipement existant.
        
        :param amenity_id: L'identifiant de l'équipement à mettre à jour
        :param amenity_data: Dictionnaire contenant les nouvelles données de l'équipement
        :return: L'objet équipement mis à jour ou None s'il n'existe pas
        :raises ValueError: Si le nom de l'équipement est manquant
        """
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            if 'name' not in amenity_data or not amenity_data['name']:
                raise ValueError("Le nom de l'équipement est requis")
            for key, value in amenity_data.items():
                setattr(amenity, key, value)
            self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    def get_place(self, place_id):
        """
        Récupère un lieu par son identifiant.
        
        :param place_id: L'identifiant du lieu à récupérer
        :return: L'objet lieu correspondant
        :raises ValueError: Si le lieu n'existe pas
        """
        place = self.place_repo.get(place_id)
        if not place:
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
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError(f"Propriétaire avec l'id {place_data['owner_id']} non trouvé")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=float(place_data['price']),
            latitude=float(place_data['latitude']),
            longitude=float(place_data['longitude']),
            owner_id=place_data['owner_id']
        )
        
        # Ajoute les équipements au lieu si présents
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_id in place_data['amenities']:
                try:
                    amenity = self.get_amenity(amenity_id)
                    place.add_amenity(amenity)
                except ValueError:
                    # Si l'équipement n'existe pas, on l'ignore
                    pass
        
        self.place_repo.add(place)
        return place

    def get_all_places(self):
        """
        Récupère tous les lieux.
        
        :return: Une liste contenant tous les objets lieu
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Met à jour un lieu existant.
        
        :param place_id: L'identifiant du lieu à mettre à jour
        :param place_data: Dictionnaire contenant les nouvelles données du lieu
        :return: L'objet lieu mis à jour
        :raises ValueError: Si le lieu n'existe pas ou si les données sont invalides
        """
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Lieu avec l'id {place_id} non trouvé")

        # Vérifie que place_data est un dictionnaire
        if not isinstance(place_data, dict):
            raise ValueError(f"Entrée invalide: dictionnaire attendu, reçu {type(place_data)}")

        # Traite les équipements séparément s'ils sont présents
        if 'amenities' in place_data:
            # Récupère les IDs des équipements
            amenity_ids = place_data.pop('amenities')
            
            # Supprime tous les équipements existants
            place.amenities = []
            
            # Ajoute les nouveaux équipements
            for amenity_id in amenity_ids:
                try:
                    amenity = self.get_amenity(amenity_id)
                    place.add_amenity(amenity)
                except ValueError:
                    # Si l'équipement n'existe pas, on l'ignore
                    pass

        # Met à jour les attributs du lieu
        for key, value in place_data.items():
            if key == 'price':
                setattr(place, key, float(value))
            elif key == 'latitude':
                setattr(place, key, float(value))
            elif key == 'longitude':
                setattr(place, key, float(value))
            else:
                setattr(place, key, value)

        # Met à jour le lieu dans le repository
        self.place_repo.update(place_id, place_data)
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
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError(f"Utilisateur avec l'id {review_data['user_id']} non trouvé")
        
        # Vérifie si le lieu existe
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError(f"Lieu avec l'id {review_data['place_id']} non trouvé")
        
        # Crée l'avis
        review = Review(
            text=review_data['text'],
            rating=rating,
            place=place,
            user=user
        )
        
        # Ajoute l'avis au repository
        self.review_repo.add(review)
        
        return review
    
    def get_review(self, review_id):
        """
        Récupère un avis par son identifiant.
        
        :param review_id: L'identifiant de l'avis à récupérer
        :return: L'objet avis correspondant
        :raises ValueError: Si l'avis n'existe pas
        """
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Avis avec l'id {review_id} non trouvé")
        return review
    
    def get_all_reviews(self):
        """
        Récupère tous les avis.
        
        :return: Une liste contenant tous les objets avis
        """
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        """
        Récupère tous les avis pour un lieu spécifique.
        
        :param place_id: L'identifiant du lieu pour lequel récupérer les avis
        :return: Une liste d'objets avis pour le lieu
        :raises ValueError: Si le lieu n'existe pas
        """
        # Vérifie si le lieu existe
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Lieu avec l'id {place_id} non trouvé")
        
        # Retourne tous les avis pour le lieu
        return self.review_repo.get_reviews_by_place(place_id)
    
    def update_review(self, review_id, review_data):
        """
        Met à jour un avis existant.
        
        :param review_id: L'identifiant de l'avis à mettre à jour
        :param review_data: Dictionnaire contenant les nouvelles données de l'avis
        :return: L'objet avis mis à jour
        :raises ValueError: Si l'avis n'existe pas ou si les données sont invalides
        """
        # Vérifie si l'avis existe
        review = self.review_repo.get(review_id)
        if not review:
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
        self.review_repo.update(review_id, review_data)
        
        return review
    
    def delete_review(self, review_id):
        """
        Supprime un avis.
        
        :param review_id: L'identifiant de l'avis à supprimer
        :return: True si la suppression a réussi, False sinon
        :raises ValueError: Si l'avis n'existe pas
        """
        # Vérifie si l'avis existe
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Avis avec l'id {review_id} non trouvé")
        
        # Supprime l'avis du repository
        self.review_repo.delete(review_id)
        
        return True
    
    def delete_place(self, place_id):
        """
        Supprime un lieu.
        
        :param place_id: L'identifiant du lieu à supprimer
        :return: True si la suppression a réussi, False sinon
        :raises ValueError: Si le lieu n'existe pas
        """
        # Vérifie si le lieu existe
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Lieu avec l'id {place_id} non trouvé")
        
        # Supprime d'abord tous les avis associés à ce lieu
        reviews = self.review_repo.get_reviews_by_place(place_id)
        for review in reviews:
            self.review_repo.delete(review.id)
        
        # Supprime le lieu du repository
        self.place_repo.delete(place_id)
        
        return True
    
    def delete_user(self, user_id):
        """
        Supprime un utilisateur.
        
        :param user_id: L'identifiant de l'utilisateur à supprimer
        :return: True si la suppression a réussi, False sinon
        :raises ValueError: Si l'utilisateur n'existe pas
        """
        # Vérifie si l'utilisateur existe
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError(f"Utilisateur avec l'id {user_id} non trouvé")
        
        # Supprime d'abord tous les avis écrits par cet utilisateur
        reviews = self.review_repo.get_reviews_by_user(user_id)
        for review in reviews:
            self.review_repo.delete(review.id)
        
        # Supprime tous les lieux appartenant à cet utilisateur
        places = self.place_repo.get_places_by_owner(user_id)
        for place in places:
            self.delete_place(place.id)
        
        # Supprime l'utilisateur du repository
        self.user_repo.delete(user_id)
        
        return True
    
    def delete_amenity(self, amenity_id):
        """
        Supprime un équipement.
        
        :param amenity_id: L'identifiant de l'équipement à supprimer
        :return: True si la suppression a réussi, False sinon
        :raises ValueError: Si l'équipement n'existe pas
        """
        # Vérifie si l'équipement existe
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError(f"Équipement avec l'id {amenity_id} non trouvé")
        
        # Supprime l'équipement du repository
        self.amenity_repo.delete(amenity_id)
        
        return True

facade = HBnBFacade()
