#!/bin/bash

# Script pour lancer les deux serveurs nécessaires pour l'application HBnB
# 1. Le serveur API Flask sur le port 5000
# 2. Le serveur HTTP Python pour le frontend sur le port 8000

# Définir les couleurs pour une meilleure lisibilité
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Fonction pour vérifier si un port est libre
is_port_free() {
    local port=$1
    # Utiliser nc (netcat) pour vérifier si le port est libre
    nc -z localhost $port >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        # Port est utilisé
        return 1
    else
        # Port est libre
        return 0
    fi
}

# Fonction pour tuer les processus utilisant un port spécifique
kill_port() {
    local port=$1
    local max_attempts=3
    local attempt=1
    
    echo -e "${YELLOW}Nettoyage agressif du port $port...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        echo -e "${YELLOW}Tentative $attempt/$max_attempts de libération du port $port...${NC}"
        
        # Méthode 1: Utiliser lsof pour trouver et tuer les processus
        local pid=$(lsof -ti:$port)
        if [ -n "$pid" ]; then
            echo -e "${YELLOW}Processus trouvé sur le port $port (PID: $pid). Arrêt en cours...${NC}"
            kill -9 $pid 2>/dev/null || true
        fi
        
        # Méthode 2: Utiliser fuser pour tuer les processus (plus agressif)
        echo -e "${YELLOW}Utilisation de fuser pour tuer les processus sur le port $port...${NC}"
        fuser -k $port/tcp 2>/dev/null || true
        
        # Méthode 3: Utiliser netstat et grep pour trouver des processus
        local netstat_pid=$(netstat -tulpn 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d'/' -f1)
        if [ -n "$netstat_pid" ] && [ "$netstat_pid" != "" ]; then
            echo -e "${YELLOW}Processus supplémentaire trouvé sur le port $port (PID: $netstat_pid). Arrêt en cours...${NC}"
            kill -9 $netstat_pid 2>/dev/null || true
        fi
        
        # Méthode 4: Utiliser ss pour trouver des processus (alternative à netstat)
        local ss_pid=$(ss -lptn "sport = :$port" 2>/dev/null | grep -oP '(?<=pid=)[0-9]+')
        if [ -n "$ss_pid" ]; then
            echo -e "${YELLOW}Processus trouvé avec ss sur le port $port (PID: $ss_pid). Arrêt en cours...${NC}"
            kill -9 $ss_pid 2>/dev/null || true
        fi
        
        # Méthode 5: Tuer tous les processus Python qui pourraient utiliser ce port
        if [ $port -eq 8000 ]; then
            echo -e "${YELLOW}Recherche de processus Python pouvant utiliser le port $port...${NC}"
            pkill -f "python -m http.server" 2>/dev/null || true
            pkill -f "SimpleHTTPServer" 2>/dev/null || true
        fi
        
        if [ $port -eq 5000 ]; then
            echo -e "${YELLOW}Recherche de processus Flask pouvant utiliser le port $port...${NC}"
            pkill -f "flask run" 2>/dev/null || true
            pkill -f "python run.py" 2>/dev/null || true
        fi
        
        # Attendre plus longtemps pour s'assurer que le port est libéré
        echo -e "${YELLOW}Attente de la libération du port $port...${NC}"
        sleep 3
        
        # Vérifier si le port est maintenant libre
        if is_port_free $port; then
            echo -e "${GREEN}Port $port libéré avec succès.${NC}"
            return 0
        else
            echo -e "${RED}Le port $port est toujours utilisé après la tentative $attempt.${NC}"
            attempt=$((attempt+1))
        fi
    done
    
    echo -e "${RED}ÉCHEC: Impossible de libérer le port $port après $max_attempts tentatives.${NC}"
    return 1
}

# Fonction pour arrêter les serveurs
stop_servers() {
    echo -e "${RED}Arrêt des serveurs...${NC}"
    # Tuer tous les processus spécifiques
    echo -e "${YELLOW}Arrêt des processus spécifiques...${NC}"
    pkill -f "python run.py" 2>/dev/null || true
    pkill -f "python -m http.server" 2>/dev/null || true
    
    # Attendre que les processus se terminent
    sleep 2
    # Tuer tous les processus sur les ports 5000 et 8000
    kill_port 5000
    kill_port 8000
    echo -e "${GREEN}Serveurs arrêtés.${NC}"
    exit 0
}

# Configurer le gestionnaire de signal pour Ctrl+C
trap stop_servers INT

# Tuer tous les processus existants sur les ports 5000 et 8000
echo -e "${BLUE}Nettoyage agressif des ports avant de démarrer les serveurs...${NC}"
kill_port 5000
kill_port 8000

# Vérifier si nous sommes dans le répertoire racine du projet
if [ ! -d "frontend" ]; then
    echo -e "${RED}Erreur: Ce script doit être exécuté depuis le répertoire racine du projet.${NC}"
    echo -e "${RED}Assurez-vous que le répertoire 'frontend' existe dans le répertoire courant.${NC}"
    exit 1
fi

# Fonction pour démarrer le serveur Flask
start_flask_server() {
    echo -e "${BLUE}Démarrage du serveur API Flask sur le port 5000...${NC}"
    cd frontend && python run.py &
    FLASK_PID=$!
    
    # Attendre que le serveur Flask démarre
    sleep 3
    
    # Vérifier si le serveur Flask a démarré correctement
    if ! ps -p $FLASK_PID > /dev/null; then
        echo -e "${RED}Erreur: Le serveur Flask n'a pas pu démarrer.${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Serveur API Flask démarré avec succès (PID: $FLASK_PID).${NC}"
    echo -e "${GREEN}L'API est accessible à l'adresse: http://localhost:5000${NC}"
    return 0
}

# Fonction pour démarrer le serveur HTTP Python
start_http_server() {
    local port=$1
    echo -e "${BLUE}Démarrage du serveur HTTP Python pour le frontend sur le port $port...${NC}"
    
    # Utiliser une approche différente pour démarrer le serveur HTTP
    # Changer de répertoire et démarrer le serveur
    cd frontend && python -m http.server $port &
    HTTP_PID=$!
    
    # Attendre que le serveur HTTP démarre
    sleep 3
    
    # Vérifier si le serveur HTTP a démarré correctement
    if ! ps -p $HTTP_PID > /dev/null; then
        echo -e "${RED}Erreur: Le serveur HTTP Python n'a pas pu démarrer sur le port $port.${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Serveur HTTP Python démarré avec succès (PID: $HTTP_PID) sur le port $port.${NC}"
    echo -e "${GREEN}Le frontend est accessible à l'adresse: http://localhost:$port/templates/index.html${NC}"
    return 0
}

# Fonction pour trouver un port disponible
find_available_port() {
    local start_port=$1
    local max_port=$2
    
    for port in $(seq $start_port $max_port); do
        echo -e "${BLUE}Vérification de la disponibilité du port $port...${NC}"
        if is_port_free $port; then
            echo -e "${GREEN}Port $port est disponible.${NC}"
            return $port
        else
            echo -e "${YELLOW}Port $port est déjà utilisé, essai du port suivant.${NC}"
        fi
    done
    
    echo -e "${RED}Aucun port disponible trouvé entre $start_port et $max_port.${NC}"
    return 1
}

# Démarrer les serveurs avec des tentatives en cas d'échec
max_attempts=3

# Démarrer le serveur Flask
echo -e "${BLUE}Démarrage du serveur Flask...${NC}"
attempt=1
while [ $attempt -le $max_attempts ]; do
    echo -e "${BLUE}Tentative $attempt/$max_attempts de démarrage du serveur Flask...${NC}"
    if start_flask_server; then
        break
    else
        if [ $attempt -eq $max_attempts ]; then
            echo -e "${RED}Échec du démarrage du serveur Flask après $max_attempts tentatives.${NC}"
            stop_servers
            exit 1
        fi
        echo -e "${YELLOW}Nouvelle tentative de nettoyage du port 5000...${NC}"
        kill_port 5000
        attempt=$((attempt+1))
    fi
done

# Démarrer le serveur HTTP avec ports alternatifs si nécessaire
echo -e "${BLUE}Démarrage du serveur HTTP...${NC}"

# Essayer d'abord le port 8000
if is_port_free 8000; then
    HTTP_PORT=8000
else
    echo -e "${YELLOW}Port 8000 est déjà utilisé et ne peut pas être libéré.${NC}"
    echo -e "${YELLOW}Recherche d'un port alternatif...${NC}"
    
    # Essayer de trouver un port disponible entre 8001 et 8020
    for port in $(seq 8001 8020); do
        if is_port_free $port; then
            HTTP_PORT=$port
            echo -e "${GREEN}Port alternatif trouvé: $HTTP_PORT${NC}"
            break
        fi
    done
    
    # Vérifier si un port a été trouvé
    if [ -z "$HTTP_PORT" ]; then
        echo -e "${RED}Aucun port disponible trouvé entre 8001 et 8020.${NC}"
        echo -e "${RED}Arrêt des serveurs...${NC}"
        stop_servers
        exit 1
    fi
fi

# Démarrer le serveur HTTP sur le port choisi
attempt=1
while [ $attempt -le $max_attempts ]; do
    echo -e "${BLUE}Tentative $attempt/$max_attempts de démarrage du serveur HTTP sur le port $HTTP_PORT...${NC}"
    if start_http_server $HTTP_PORT; then
        break
    else
        if [ $attempt -eq $max_attempts ]; then
            echo -e "${RED}Échec du démarrage du serveur HTTP après $max_attempts tentatives.${NC}"
            stop_servers
            exit 1
        fi
        echo -e "${YELLOW}Nouvelle tentative de nettoyage du port $HTTP_PORT...${NC}"
        kill_port $HTTP_PORT
        attempt=$((attempt+1))
    fi
done

echo -e "${GREEN}Serveur HTTP Python démarré avec succès (PID: $HTTP_PID).${NC}"
echo -e "${GREEN}Le frontend est accessible à l'adresse: http://localhost:$HTTP_PORT/templates/index.html${NC}"

echo -e "${BLUE}Les deux serveurs sont maintenant en cours d'exécution.${NC}"
echo -e "${BLUE}Appuyez sur Ctrl+C pour arrêter les deux serveurs.${NC}"

# Garder le script en cours d'exécution pour pouvoir arrêter les serveurs avec Ctrl+C
while true; do
    sleep 1
done