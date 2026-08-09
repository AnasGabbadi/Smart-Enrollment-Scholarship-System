"""
API routes for managing yearly scholarship quotas
"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from utilitaires.base_donnees import GestionnaireBD
from utilitaires.securite import exiger_role_admin

logger = logging.getLogger(__name__)

routeur_quotas = APIRouter(
    prefix="/api/v1/quotas",
    tags=["Quotas"]
)

@routeur_quotas.get("/")
async def obtenir_tous_quotas():
    """
    Récupérer tous les quotas de bourses par année
    
    Returns:
        dict: Liste de tous les quotas avec année et nombre de bourses
    """
    try:
        collection_quotas = GestionnaireBD.obtenir_collection_quotas()
        quotas = list(collection_quotas.find().sort("annee", -1))
        
        for quota in quotas:
            quota['_id'] = str(quota['_id'])
        
        return {
            "total": len(quotas),
            "quotas": quotas
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la récupération des quotas")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@routeur_quotas.get("/{annee}")
async def obtenir_quota_annee(annee: int):
    """
    Récupérer le quota de bourses pour une année spécifique
    
    Args:
        annee: L'année concernée
        
    Returns:
        dict: Le quota pour l'année spécifiée
    """
    try:
        collection_quotas = GestionnaireBD.obtenir_collection_quotas()
        quota = collection_quotas.find_one({"annee": annee})
        
        if not quota:
            raise HTTPException(
                status_code=404,
                detail=f"Aucun quota trouvé pour l'année {annee}"
            )
        
        quota['_id'] = str(quota['_id'])
        return quota
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la récupération du quota")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@routeur_quotas.post("/{annee}")
async def creer_ou_mettre_a_jour_quota(annee: int, nombre_bourses: int, utilisateur_admin: dict = Depends(exiger_role_admin)):
    """
    Créer ou mettre à jour le quota de bourses pour une année (réservé aux administrateurs)

    Args:
        annee: L'année concernée
        nombre_bourses: Nombre de bourses disponibles

    Returns:
        dict: Le quota créé ou mis à jour

    Raises:
        HTTPException 401: Authentification manquante ou invalide
        HTTPException 403: Utilisateur authentifié mais non admin
    """
    try:
        if nombre_bourses < 0:
            raise HTTPException(
                status_code=400,
                detail="Le nombre de bourses ne peut pas être négatif"
            )
        
        collection_quotas = GestionnaireBD.obtenir_collection_quotas()
        
        # Chercher si le quota existe déjà
        quota_existant = collection_quotas.find_one({"annee": annee})
        
        if quota_existant:
            # Mettre à jour
            result = collection_quotas.update_one(
                {"annee": annee},
                {
                    "$set": {
                        "nombre_bourses": nombre_bourses,
                        "derniere_mise_a_jour": datetime.utcnow()
                    }
                }
            )
            if result.modified_count == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Aucune modification effectuée"
                )
        else:
            # Créer nouveau
            collection_quotas.insert_one({
                "annee": annee,
                "nombre_bourses": nombre_bourses,
                "date_creation": datetime.utcnow(),
                "derniere_mise_a_jour": datetime.utcnow()
            })
        
        # Retourner le quota mis à jour
        quota = collection_quotas.find_one({"annee": annee})
        quota['_id'] = str(quota['_id'])
        
        return {
            "success": True,
            "message": f"Quota pour {annee} mis à jour: {nombre_bourses} bourses",
            "quota": quota
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la création/mise à jour du quota")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@routeur_quotas.delete("/{annee}")
async def supprimer_quota(annee: int, utilisateur_admin: dict = Depends(exiger_role_admin)):
    """
    Supprimer le quota de bourses pour une année (réservé aux administrateurs)

    Args:
        annee: L'année concernée

    Returns:
        dict: Message de confirmation

    Raises:
        HTTPException 401: Authentification manquante ou invalide
        HTTPException 403: Utilisateur authentifié mais non admin
    """
    try:
        collection_quotas = GestionnaireBD.obtenir_collection_quotas()
        result = collection_quotas.delete_one({"annee": annee})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Aucun quota trouvé pour l'année {annee}"
            )
        
        return {
            "success": True,
            "message": f"Quota pour {annee} supprimé avec succès"
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la suppression du quota")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
