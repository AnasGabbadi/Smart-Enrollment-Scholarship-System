"""
Endpoints API pour la gestion des étudiants
Permet l'enregistrement et la récupération des informations des étudiants
"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import uuid
from datetime import datetime
from api.schemas import InscriptionEtudiant, ResultatEtudiant, RequeteConnexionEtudiant
from utilitaires.base_donnees import GestionnaireBD
from utilitaires.securite import exiger_role_admin
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

# Configuration pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Projection MongoDB à appliquer sur toute lecture d'étudiant destinée à être
# renvoyée au client : le hash bcrypt du mot de passe ne doit jamais sortir de l'API.
PROJECTION_SANS_MOT_DE_PASSE = {"motDePasse": 0}

# Créer le routeur avec le préfixe /api/v1/etudiants
routeur_etudiants = APIRouter(
    prefix="/api/v1/etudiants",
    tags=["Gestion des Étudiants"],
    responses={404: {"description": "Étudiant non trouvé"}}
)


@routeur_etudiants.post("/enregistrer", response_model=ResultatEtudiant)
async def enregistrer_etudiant(etudiant: InscriptionEtudiant):
    """
    Enregistrer un nouvel étudiant dans le système
    
    Crée un identifiant unique pour l'étudiant et stocke ses informations
    dans la base de données MongoDB.
    
    Validations:
    - L'email doit être unique (pas de doublon dans la même année)
    - Un étudiant ne peut s'inscrire qu'une fois par année
    - Les données académiques et financières sont obligatoires
    
    Args:
        etudiant: Données complètes de l'étudiant (prénom, nom, email, année, données académiques/financières)
        
    Returns:
        ResultatEtudiant: Informations de l'étudiant créé avec ID et dates
        
    Raises:
        HTTPException 400: Email déjà utilisé cette année
        HTTPException 400: Données invalides
        HTTPException 500: Erreur serveur lors de l'enregistrement
    """
    try:
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        
        # Vérifier si l'email existe déjà pour cette année
        inscription_existante = collection_etudiants.find_one({
            "email": etudiant.email,
            "annee": etudiant.annee
        })
        
        if inscription_existante:
            raise HTTPException(
                status_code=400,
                detail=f"Un étudiant avec cet email ({etudiant.email}) est déjà inscrit pour l'année {etudiant.annee}. Un seul enregistrement par année et par email est permis."
            )
        
        # Générer un ID unique si pas fourni
        id_etudiant = etudiant.idEtudiant or str(uuid.uuid4())
        maintenant = datetime.utcnow()
        
        # Hacher le mot de passe avant le stockage
        mot_de_passe_hache = pwd_context.hash(etudiant.password)
        
        # Préparer le document pour MongoDB
        document_etudiant = {
            "idEtudiant": id_etudiant,
            "prenom": etudiant.prenom,
            "nom": etudiant.nom,
            "email": etudiant.email,
            "phone": etudiant.phone,
            "address": etudiant.address,
            "motDePasse": mot_de_passe_hache,
            "annee": etudiant.annee,
            "niveau_etude": etudiant.niveau_etude,
            "donnees_baccalaureat": etudiant.donnees_baccalaureat.dict(),
            "donnees_diplome": etudiant.donnees_diplome.dict() if etudiant.donnees_diplome else None,
            "donnees_financieres": etudiant.donnees_financieres.dict(),
            "donnees_contextuelles": etudiant.donnees_contextuelles.dict(),
            "type_sponsorship": etudiant.type_sponsorship,
            "statut": "En attente",
            "dateCreation": maintenant,
            "dateModification": maintenant
        }
        
        # Insérer dans la collection etudiants
        collection_etudiants.insert_one(document_etudiant)
        
        return {
            "idEtudiant": id_etudiant,
            "prenom": etudiant.prenom,
            "nom": etudiant.nom,
            "email": etudiant.email,
            "phone": etudiant.phone,
            "address": etudiant.address,
            "annee": etudiant.annee,
            "niveau_etude": etudiant.niveau_etude,
            "donnees_baccalaureat": etudiant.donnees_baccalaureat.dict(),
            "donnees_diplome": etudiant.donnees_diplome.dict() if etudiant.donnees_diplome else None,
            "donnees_financieres": etudiant.donnees_financieres.dict(),
            "donnees_contextuelles": etudiant.donnees_contextuelles.dict(),
            "type_sponsorship": etudiant.type_sponsorship,
            "statut": "En attente",
            "dateCreation": maintenant,
            "dateModification": maintenant
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de l'enregistrement de l'étudiant")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_etudiants.get("/")
async def lister_etudiants(saut: int = 0, limite: int = 10):
    """
    Récupérer la liste des étudiants enregistrés
    
    Retourne une liste paginée des étudiants avec leurs informations de base
    
    Args:
        saut: Nombre de documents à ignorer (offset)
        limite: Nombre maximum de documents à retourner
        
    Returns:
        dict: Contient le nombre total, le saut, la limite et la liste des étudiants
        
    Raises:
        HTTPException: En cas d'erreur lors de la récupération
    """
    try:
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        
        # Récupérer les étudiants avec pagination
        etudiants = list(
            collection_etudiants.find({}, PROJECTION_SANS_MOT_DE_PASSE)
        )
        
        # Convertir les _id MongoDB en string
        for etudiant in etudiants:
            etudiant['_id'] = str(etudiant['_id'])
        
        return {
            "total": collection_etudiants.count_documents({}),
            "saut": saut,
            "limite": limite,
            "etudiants": etudiants
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la récupération des étudiants")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_etudiants.post("/connexion")
async def connexion_etudiant(requete: RequeteConnexionEtudiant):
    """
    Connecter un étudiant avec email et mot de passe
    
    Args:
        requete: Email et mot de passe de l'étudiant
        
    Returns:
        dict: Token et données de l'étudiant
        
    Raises:
        HTTPException 401: Identifiants invalides
        HTTPException 500: Erreur serveur
    """
    try:
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        
        # Chercher l'étudiant par email
        etudiant = collection_etudiants.find_one({"email": requete.email})
        
        if not etudiant:
            raise HTTPException(
                status_code=401,
                detail="Email ou mot de passe incorrect"
            )
        
        # Vérifier le mot de passe contre le hash bcrypt stocké
        if not pwd_context.verify(requete.password, etudiant.get("motDePasse", "")):
            raise HTTPException(
                status_code=401,
                detail="Email ou mot de passe incorrect"
            )

        # Générer un token simple (en prod, utiliser JWT avec secret)
        token = "student-token-" + str(uuid.uuid4())

        # Préparer la réponse - ne jamais renvoyer le hash du mot de passe
        etudiant['_id'] = str(etudiant['_id'])
        etudiant.pop("motDePasse", None)

        return {
            "token": token,
            "etudiant": etudiant
        }
        
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la connexion")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_etudiants.get("/connexion/verifier/{email}")
async def verifier_etudiant(email: str):
    """
    Vérifier si un étudiant existe par email
    
    Args:
        email: Email de l'étudiant
        
    Returns:
        dict: Données de l'étudiant ou error 404
    """
    try:
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        
        etudiant = collection_etudiants.find_one({"email": email}, PROJECTION_SANS_MOT_DE_PASSE)

        if not etudiant:
            raise HTTPException(
                status_code=404,
                detail="Étudiant non trouvé"
            )

        etudiant['_id'] = str(etudiant['_id'])
        return etudiant

    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la vérification")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")



@routeur_etudiants.get("/{id_etudiant}")
async def recuperer_etudiant(id_etudiant: str):
    """
    Récupérer les informations d'un étudiant spécifique
    
    Args:
        id_etudiant: Identifiant unique de l'étudiant
        
    Returns:
        dict: Informations complètes de l'étudiant
        
    Raises:
        HTTPException: Si l'étudiant n'existe pas ou en cas d'erreur
    """
    try:
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        etudiant = collection_etudiants.find_one({"idEtudiant": id_etudiant}, PROJECTION_SANS_MOT_DE_PASSE)

        if not etudiant:
            raise HTTPException(
                status_code=404,
                detail="Étudiant non trouvé"
            )

        etudiant['_id'] = str(etudiant['_id'])
        return etudiant
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la récupération de l'étudiant")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@routeur_etudiants.put("/{id_etudiant}")
async def mettre_a_jour_etudiant(id_etudiant: str, donnees: dict):
    """
    Mettre à jour les informations d'un étudiant
    
    Args:
        id_etudiant: Identifiant unique de l'étudiant
        donnees: Données à mettre à jour
        
    Returns:
        dict: Étudiant mis à jour
        
    Raises:
        HTTPException: Si l'étudiant n'existe pas ou en cas d'erreur
    """
    try:
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        
        # Vérifier que l'étudiant existe
        etudiant = collection_etudiants.find_one({"idEtudiant": id_etudiant})
        if not etudiant:
            raise HTTPException(
                status_code=404,
                detail="Étudiant non trouvé"
            )
        
        # Préparer les données à mettre à jour
        donnees["dateModification"] = datetime.utcnow()
        
        # Effectuer la mise à jour
        result = collection_etudiants.update_one(
            {"idEtudiant": id_etudiant},
            {"$set": donnees}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=400,
                detail="Aucune modification effectuée"
            )
        
        # Retourner l'étudiant mis à jour
        etudiant_mis_a_jour = collection_etudiants.find_one({"idEtudiant": id_etudiant}, PROJECTION_SANS_MOT_DE_PASSE)
        etudiant_mis_a_jour['_id'] = str(etudiant_mis_a_jour['_id'])
        return etudiant_mis_a_jour
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la mise à jour de l'étudiant")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_etudiants.delete("/{id_etudiant}")
async def supprimer_etudiant(id_etudiant: str, utilisateur_admin: dict = Depends(exiger_role_admin)):
    """
    Supprimer un étudiant du système (réservé aux administrateurs)

    Args:
        id_etudiant: Identifiant unique de l'étudiant

    Returns:
        dict: Message de confirmation

    Raises:
        HTTPException 401: Authentification manquante ou invalide
        HTTPException 403: Utilisateur authentifié mais non admin
        HTTPException: Si l'étudiant n'existe pas ou en cas d'erreur
    """
    try:
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        
        result = collection_etudiants.delete_one({"idEtudiant": id_etudiant})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Étudiant non trouvé"
            )
        
        return {"message": "Étudiant supprimé avec succès"}
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la suppression de l'étudiant")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_etudiants.patch("/{id_etudiant}/approuver")
async def approuver_etudiant(id_etudiant: str, utilisateur_admin: dict = Depends(exiger_role_admin)):
    """
    Approuver un étudiant (réservé aux administrateurs)

    Args:
        id_etudiant: Identifiant unique de l'étudiant

    Returns:
        dict: Étudiant approuvé

    Raises:
        HTTPException 401: Authentification manquante ou invalide
        HTTPException 403: Utilisateur authentifié mais non admin
        HTTPException: Si l'étudiant n'existe pas
    """
    try:
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        
        result = collection_etudiants.update_one(
            {"idEtudiant": id_etudiant},
            {
                "$set": {
                    "statut": "Approuvé",
                    "dateModification": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Étudiant non trouvé"
            )
        
        etudiant = collection_etudiants.find_one({"idEtudiant": id_etudiant}, PROJECTION_SANS_MOT_DE_PASSE)
        etudiant['_id'] = str(etudiant['_id'])
        return etudiant
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de l'approbation")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_etudiants.patch("/{id_etudiant}/rejeter")
async def rejeter_etudiant(id_etudiant: str, utilisateur_admin: dict = Depends(exiger_role_admin)):
    """
    Rejeter un étudiant (réservé aux administrateurs)

    Args:
        id_etudiant: Identifiant unique de l'étudiant

    Returns:
        dict: Étudiant rejeté

    Raises:
        HTTPException 401: Authentification manquante ou invalide
        HTTPException 403: Utilisateur authentifié mais non admin
        HTTPException: Si l'étudiant n'existe pas
    """
    try:
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        
        result = collection_etudiants.update_one(
            {"idEtudiant": id_etudiant},
            {
                "$set": {
                    "statut": "Rejeté",
                    "dateModification": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Étudiant non trouvé"
            )
        
        etudiant = collection_etudiants.find_one({"idEtudiant": id_etudiant}, PROJECTION_SANS_MOT_DE_PASSE)
        etudiant['_id'] = str(etudiant['_id'])
        return etudiant
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors du rejet")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")