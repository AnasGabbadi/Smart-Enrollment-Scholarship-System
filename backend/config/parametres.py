"""
Paramètres de configuration centralisés pour l'application
Contient toutes les constantes, variables d'environnement et configurations
"""
import os
import secrets
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# ============================================================================
# CONFIGURATION DE LA BASE DE DONNÉES
# ============================================================================
URL_MONGODB = os.getenv("URL_MONGODB", "mongodb://localhost:27017")
NOM_BASE_DONNEES = os.getenv("NOM_BASE_DONNEES", "admission_intelligente")

# ============================================================================
# CONFIGURATION DE L'API FastAPI
# ============================================================================
HOTE_API = os.getenv("HOTE_API", "0.0.0.0")
PORT_API = int(os.getenv("PORT_API", 8000))
ENVIRONNEMENT_FASTAPI = os.getenv("ENVIRONNEMENT_FASTAPI", "developpement")
RECHARGER_SERVEUR = ENVIRONNEMENT_FASTAPI == "developpement"

# ============================================================================
# CHEMINS DES FICHIERS
# ============================================================================
# REPERTOIRE_RACINE pointe vers le dossier backend
REPERTOIRE_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHEMIN_MODELES_ENTRAINES = os.path.join(REPERTOIRE_RACINE, "modeles_entraines")
CHEMIN_DONNEES = os.path.join(REPERTOIRE_RACINE, "donnees")

# Créer les répertoires s'ils n'existent pas
os.makedirs(CHEMIN_MODELES_ENTRAINES, exist_ok=True)
os.makedirs(CHEMIN_DONNEES, exist_ok=True)

# ============================================================================
# CONFIGURATION CORS - Autoriser la communication avec le frontend
# ============================================================================
# Liste blanche explicite - ne jamais ajouter "*" ici, surtout avec
# allow_credentials=True (cf. application.py), sous peine d'autoriser
# n'importe quel site à appeler l'API avec les identifiants de l'utilisateur.
ORIGINES_AUTORISEES = [
    "http://localhost:3000",      # React dev server
    "http://localhost:8080",      # Alternative port
    "http://localhost:5000",      # Flask/autre backend
    "http://127.0.0.1:3000",      # Localhost variant
]

# En production, définir CORS_ORIGINES_SUPPLEMENTAIRES dans l'environnement
# avec la ou les origines réelles du frontend déployé (liste séparée par des
# virgules, ex: "https://mon-app.exemple.com,https://admin.mon-app.exemple.com")
_origines_supplementaires = os.getenv("CORS_ORIGINES_SUPPLEMENTAIRES", "")
if _origines_supplementaires:
    ORIGINES_AUTORISEES.extend(
        origine.strip() for origine in _origines_supplementaires.split(",") if origine.strip()
    )

# ============================================================================
# CONFIGURATION AUTHENTIFICATION ADMIN ET JWT
# ============================================================================
# Identifiants admin : définis uniquement via l'environnement, jamais en dur
# dans le code. Si absents, la connexion admin est désactivée (401 systématique).
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
if not ADMIN_EMAIL or not ADMIN_PASSWORD:
    print(
        "[⚠] ADMIN_EMAIL / ADMIN_PASSWORD non définis dans l'environnement : "
        "la connexion administrateur est désactivée tant qu'ils ne sont pas configurés."
    )

JWT_ALGORITHME = "HS256"
JWT_DUREE_VALIDITE_MINUTES = 480  # 8 heures

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    JWT_SECRET_KEY = secrets.token_hex(32)
    print(
        "[⚠] JWT_SECRET_KEY non défini dans l'environnement : une clé temporaire a été "
        "générée pour cette exécution. Tous les tokens émis seront invalidés au prochain "
        "redémarrage. Définissez JWT_SECRET_KEY dans .env avant un déploiement en production."
    )

# ============================================================================
# CONFIGURATION DE LA PAGINATION
# ============================================================================
SAUT_PAR_DEFAUT = 0              # Offset par défaut
LIMITE_PAR_DEFAUT = 10            # Items par page par défaut
LIMITE_MAX = 100                  # Limite maximale d'items retournables

# ============================================================================
# CONFIGURATION DE LA JOURNALISATION
# ============================================================================
NIVEAU_JOURNAL = os.getenv("NIVEAU_JOURNAL", "INFO")
FORMAT_JOURNAL = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# MÉTADONNÉES DE L'APPLICATION
# ============================================================================
NOM_APP = "Système Intelligent d'Admission et d'Attribution de Bourses"
VERSION_APP = "1.0.0"
DESCRIPTION_APP = "Système intelligent d'admission utilisant l'apprentissage automatique pour prédire la capacité financière, recommander des bourses et évaluer la probabilité d'inscription"

# ============================================================================
# CONFIGURATION DES MODÈLES DE MACHINE LEARNING
# ============================================================================

# Régression Linéaire - Prédiction de la capacité financière
CONFIG_REGRESSION_LINEAIRE = {
    "nom_modele": "Régression Linéaire",
    "description": "Prédiction de la capacité financière de l'étudiant",
    "caracteristiques_entree": ["GPA", "Note Examen", "Revenu Familial", "Dépendants"],
    "plage_sortie": (0, 100),
    "unite_sortie": "score",
    "metrique_precision": "RMSE",
    "fichier_modele": "modele_regression_lineaire.pkl"
}

# Arbre de Décision - Recommandation de bourse
CONFIG_ARBRE_DECISION = {
    "nom_modele": "Arbre de Décision",
    "description": "Recommandation de type et pourcentage de bourse",
    "caracteristiques_entree": ["GPA", "Revenu Familial", "Dépendants"],
    "profondeur_max": 5,
    "echantillons_min_division": 10,
    "echantillons_min_feuille": 5,
    "classes_sortie": {
        0: {"nom": "Pas de réduction", "pourcentage": 0},
        1: {"nom": "Réduction 25%", "pourcentage": 25},
        2: {"nom": "Bourse 50%", "pourcentage": 50},
        3: {"nom": "Bourse complète", "pourcentage": 100}
    },
    "metrique_precision": "Précision (Accuracy)",
    "fichier_modele": "modele_arbre_decision.pkl"
}

# Machine à Vecteurs de Support - Classification probabilité d'inscription
CONFIG_SVM = {
    "nom_modele": "Machine à Vecteurs de Support (SVM)",
    "description": "Prédiction de la probabilité d'inscription de l'étudiant",
    "caracteristiques_entree": ["GPA", "Note Examen", "Revenu Familial", "Distance Université"],
    "noyau": "rbf",  # Radial Basis Function kernel
    "gamma": "scale",
    "classes_sortie": {
        0: {"nom": "Faible probabilité", "intervalle": (0.0, 0.33)},
        1: {"nom": "Probabilité moyenne", "intervalle": (0.33, 0.67)},
        2: {"nom": "Forte probabilité", "intervalle": (0.67, 1.0)}
    },
    "metrique_precision": "Précision (Accuracy)",
    "fichier_modele": "modele_svm.pkl"
}

# ============================================================================
# VALIDATION DES DONNÉES
# ============================================================================
VALIDATION_GPA = {
    "min": 0.0,
    "max": 20.0,
    "description": "Note scolaire (GPA) entre 0 et 20"
}

VALIDATION_EXAMEN = {
    "min": 0,
    "max": 100,
    "description": "Note d'examen entre 0 et 100"
}

VALIDATION_REVENU = {
    "min": 0,
    "description": "Revenu familial (doit être positif)"
}

VALIDATION_DEPENDANTS = {
    "min": 0,
    "max": 15,
    "description": "Nombre de dépendants (0 à 15)"
}

VALIDATION_DISTANCE = {
    "min": 0,
    "description": "Distance à l'université en km (doit être positive)"
}

# ============================================================================
# MESSAGES ET RÉPONSES
# ============================================================================
MESSAGES_SUCCES = {
    "modele_charge": "Modèle ML chargé avec succès",
    "prediction_complete": "Prédiction générée avec succès",
    "etudiant_enregistre": "Étudiant enregistré avec succès",
    "base_donnees_connectee": "Connecté à la base de données MongoDB"
}

MESSAGES_ERREUR = {
    "modele_non_charge": "Le modèle ML n'a pas pu être chargé",
    "parametres_invalides": "Paramètres d'entrée invalides",
    "base_donnees_indisponible": "La base de données est indisponible",
    "etudiant_non_trouve": "Étudiant non trouvé",
    "erreur_interne": "Erreur interne du serveur"
}
