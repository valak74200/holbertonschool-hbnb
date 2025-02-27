"""
Ce fichier contient les configurations de l'application.
Il définit différentes classes de configuration pour les différents environnements
(développement, production, test, etc.).
"""

import os

class Config:
    """
    Classe de base pour la configuration de l'application.
    Contient les paramètres communs à tous les environnements.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    """
    Configuration pour l'environnement de développement.
    Active le mode debug pour faciliter le développement.
    """
    DEBUG = True

# Dictionnaire des configurations disponibles
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
