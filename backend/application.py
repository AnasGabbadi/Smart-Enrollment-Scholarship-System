"""
Application principale FastAPI pour le système d'admission intelligent

Ce module initialise et configure l'application FastAPI avec :
- Les middlewares CORS pour la communication avec le frontend
- Les routeurs API pour les endpoints
- La gestion de la base de données MongoDB
- Les événements de démarrage et arrêt
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.parametres import (
    NOM_APP, VERSION_APP, DESCRIPTION_APP, ORIGINES_AUTORISEES,
    NIVEAU_JOURNAL, FORMAT_JOURNAL
)
from utilitaires.base_donnees import initialiser_bd, fermer_bd

# ============================================================================
# CONFIGURATION DE LA JOURNALISATION
# ============================================================================
# Sans ceci, les logger.exception(...) des modules api/* ne seraient visibles
# qu'via le handler de secours par défaut de Python (format minimal, pas de
# contrôle du niveau). On applique ici le niveau et le format définis dans
# config/parametres.py à toute l'application.
logging.basicConfig(level=NIVEAU_JOURNAL, format=FORMAT_JOURNAL)

# ============================================================================
# INITIALISATION DE L'APPLICATION FASTAPI
# ============================================================================
application = FastAPI(
    title=NOM_APP,
    description=DESCRIPTION_APP,
    version=VERSION_APP,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ============================================================================
# CONFIGURATION CORS - Middleware pour les requêtes cross-origin
# ============================================================================
application.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINES_AUTORISEES,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "Content-Length", "X-Request-ID"],
    max_age=600,
)

# ============================================================================
# ÉVÉNEMENTS DE CYCLE DE VIE DE L'APPLICATION
# ============================================================================

@application.on_event("startup")
async def evenement_demarrage():
    """
    Événement déclenché au démarrage de l'application
    Initialise la base de données et charge les modèles ML
    """
    print("[▶] Démarrage du Système Intelligent d'Admission et d'Attribution de Bourses...")
    try:
        initialiser_bd()
        print("[✓] Système complètement opérationnel!")
    except Exception as e:
        print(f"[⚠] Avertissement au démarrage: {e}")


@application.on_event("shutdown")
async def evenement_arret():
    """
    Événement déclenché à l'arrêt de l'application
    Ferme la connexion à la base de données et libère les ressources
    """
    print("[◼] Arrêt du système...")
    fermer_bd()
    print("[✓] Système arrêté proprement")


# ============================================================================
# ENDPOINTS RACINE ET SANTÉ
# ============================================================================

@application.get("/")
async def racine():
    """
    Point d'accès racine de l'API
    Retourne les informations générales du système et les points d'accès disponibles
    """
    return {
        "nom": NOM_APP,
        "version": VERSION_APP,
        "statut": "opérationnel",
        "documentation": "/docs",
        "documentation_alternative": "/redoc",
        "points_acces": {
            "etudiants": "/api/v1/etudiants",
            "predictions": "/api/v1/predictions",
            "statistiques": "/api/v1/statistiques"
        }
    }


@application.get("/sante")
async def verifier_sante():
    """
    Endpoint de vérification de santé
    Utilisé par les équilibreurs de charge et les systèmes de monitoring
    """
    return {
        "statut": "sain",
        "service": NOM_APP,
        "version": VERSION_APP,
        "api_disponible": True
    }


# ============================================================================
# INCLURE LES ROUTEURS DES ENDPOINTS
# ============================================================================

from api.auth import routeur_auth
from api.etudiants import routeur_etudiants
from api.predictions import routeur_predictions
from api.statistiques import routeur_statistiques
from api.modeles import routeur_modeles
from api.quotas import routeur_quotas
from api.ml_ranking import routeur_ml_ranking

# Inclure tous les routeurs dans l'application
application.include_router(routeur_auth)
application.include_router(routeur_etudiants)
application.include_router(routeur_predictions)
application.include_router(routeur_statistiques)
application.include_router(routeur_modeles)
application.include_router(routeur_quotas)
application.include_router(routeur_ml_ranking)

# ============================================================================
# POINT D'ENTRÉE POUR EXÉCUTION DIRECTE
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        application,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
