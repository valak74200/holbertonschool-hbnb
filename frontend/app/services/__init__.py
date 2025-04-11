"""
Ce module initialise les services de l'application.
Il crée une instance de la façade HBnB qui sert d'interface entre les contrôleurs API
et la couche de persistance.
"""

from app.services.facade import HBnBFacade

# Création d'une instance unique de la façade pour toute l'application
# Cette instance sera importée par les contrôleurs API pour accéder aux fonctionnalités
facade = HBnBFacade()
