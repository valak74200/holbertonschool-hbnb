"""
Ce fichier est le point d'entrée principal de l'application.
Il initialise et démarre le serveur Flask pour l'API HBnB.
"""

from app import create_app
import sys

print("Démarrage de l'application...")

try:
    # Création de l'instance de l'application Flask avec la configuration de développement
    app = create_app("config.DevelopmentConfig")
    print("Application créée avec succès.")
except Exception as e:
    # Gestion des erreurs lors de l'initialisation de l'application
    print(f"Erreur lors de la création de l'application: {e}", file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    """
    Exécute l'application si ce fichier est exécuté directement.
    Le mode debug est activé pour faciliter le développement.
    Le rechargement automatique est désactivé pour éviter les problèmes avec les threads.
    """
    print("Exécution de l'application...")
    app.run(debug=True, use_reloader=False)
