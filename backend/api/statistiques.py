"""
Endpoints API pour les statistiques et visualisations

Fournit les statistiques agrégées du système et génère des visualisations
des prédictions et données des modèles ML
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from datetime import datetime
from utilitaires.base_donnees import GestionnaireBD
from utilitaires.visualisations import visualiseur
from config.parametres import CHEMIN_DONNEES
import os


# Créer le routeur avec le préfixe /api/v1/statistiques
routeur_statistiques = APIRouter(
    prefix="/api/v1/statistiques",
    tags=["Statistiques et Visualisations"]
)


@routeur_statistiques.get("/resume")
async def obtenir_resume_statistiques():
    """
    Obtenir un résumé des statistiques du système
    
    Retourne le nombre total d'étudiants, de prédictions et des statistiques
    agrégées sur les capacités financières et probabilités d'inscription
    
    Returns:
        dict: Statistiques globales du système
        
    Raises:
        HTTPException: En cas d'erreur lors de la récupération
    """
    try:
        col_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        col_predictions = GestionnaireBD.obtenir_collection_predictions()
        
        total_etudiants = col_etudiants.count_documents({})
        total_predictions = col_predictions.count_documents({})
        
        # Récupérer les statistiques des prédictions
        pipeline = [
            {
                "$group": {
                    "_id": "$type_prediction",
                    "nombre": {"$sum": 1}
                }
            }
        ]
        predictions_par_type = list(col_predictions.aggregate(pipeline))
        
        return {
            "total_etudiants": total_etudiants,
            "total_predictions": total_predictions,
            "predictions_par_type": {
                p["_id"]: p["nombre"] for p in predictions_par_type
            },
            "date_generation": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des statistiques: {str(e)}"
        )


@routeur_statistiques.get("/etudiants-par-annee")
async def obtenir_etudiants_par_annee():
    """
    Obtenir le nombre d'étudiants par année scolaire
    
    Returns:
        dict: Distribution des étudiants par année
        
    Raises:
        HTTPException: En cas d'erreur
    """
    try:
        col_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        
        pipeline = [
            {
                "$group": {
                    "_id": "$annee",
                    "nombre": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id": -1}
            }
        ]
        
        resultats = list(col_etudiants.aggregate(pipeline))
        
        return {
            "etudiants_par_annee": {
                str(r["_id"]): r["nombre"] for r in resultats
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération: {str(e)}"
        )


@routeur_statistiques.post("/generer-graphique-capacite")
async def generer_graphique_capacite_financiere():
    """
    Générer un graphique de distribution de capacité financière
    
    Récupère tous les scores de capacité financière et crée une visualisation
    
    Returns:
        dict: Chemin du fichier généré et URL d'accès
        
    Raises:
        HTTPException: En cas d'erreur de génération
    """
    try:
        col_predictions = GestionnaireBD.obtenir_collection_predictions()
        
        # Récupérer tous les scores de capacité financière
        predictions = list(col_predictions.find(
            {"type_prediction": "capacite_financiere"},
            {"donnees_sortie.scoreFinancier": 1}
        ))
        
        if not predictions:
            return {
                "message": "Aucune prédiction de capacité financière disponible",
                "chemin": None
            }
        
        scores = [p.get("donnees_sortie", {}).get("scoreFinancier", 0) 
                 for p in predictions]
        
        # Générer le graphique
        chemin = visualiseur.visualiser_distribution_capacite_financiere(scores)
        
        return {
            "message": "Graphique généré avec succès",
            "chemin": chemin,
            "nombre_predictions": len(predictions),
            "score_moyen": sum(scores) / len(scores) if scores else 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du graphique: {str(e)}"
        )


@routeur_statistiques.post("/generer-graphique-bourses")
async def generer_graphique_distribution_bourses():
    """
    Générer un graphique de distribution des bourses recommandées
    
    Returns:
        dict: Chemin du fichier généré et statistiques
        
    Raises:
        HTTPException: En cas d'erreur de génération
    """
    try:
        col_predictions = GestionnaireBD.obtenir_collection_predictions()
        
        # Récupérer les recommandations de bourses
        pipeline = [
            {"$match": {"type_prediction": "recommandation_bourse"}},
            {
                "$group": {
                    "_id": "$donnees_sortie.type_bourse",
                    "nombre": {"$sum": 1}
                }
            }
        ]
        
        resultats = list(col_predictions.aggregate(pipeline))
        distribution = {r["_id"]: r["nombre"] for r in resultats}
        
        if not distribution:
            return {
                "message": "Aucune recommandation de bourse disponible",
                "chemin": None
            }
        
        # Générer le graphique
        chemin = visualiseur.visualiser_distribution_bourses(distribution)
        
        return {
            "message": "Graphique généré avec succès",
            "chemin": chemin,
            "distribution": distribution,
            "total_recommendations": sum(distribution.values())
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du graphique: {str(e)}"
        )


@routeur_statistiques.post("/generer-graphique-inscriptions")
async def generer_graphique_probabilites_inscription():
    """
    Générer un graphique de distribution des probabilités d'inscription
    
    Returns:
        dict: Chemin du fichier généré et statistiques
        
    Raises:
        HTTPException: En cas d'erreur de génération
    """
    try:
        col_predictions = GestionnaireBD.obtenir_collection_predictions()
        
        # Récupérer les probabilités d'inscription
        pipeline = [
            {"$match": {"type_prediction": "probabilite_inscription"}},
            {
                "$group": {
                    "_id": "$donnees_sortie.niveau",
                    "nombre": {"$sum": 1}
                }
            }
        ]
        
        resultats = list(col_predictions.aggregate(pipeline))
        distribution = {r["_id"]: r["nombre"] for r in resultats}
        
        if not distribution:
            return {
                "message": "Aucune prédiction d'inscription disponible",
                "chemin": None
            }
        
        # Générer le graphique
        chemin = visualiseur.visualiser_probabilites_inscription(distribution)
        
        return {
            "message": "Graphique généré avec succès",
            "chemin": chemin,
            "distribution": distribution,
            "total_predictions": sum(distribution.values())
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du graphique: {str(e)}"
        )


@routeur_statistiques.get("/telech/graphiques")
async def lister_graphiques_disponibles():
    """
    Lister tous les graphiques générés disponibles
    
    Returns:
        dict: Liste des graphiques avec leurs chemins
        
    Raises:
        HTTPException: En cas d'erreur
    """
    try:
        chemin_graphiques = os.path.join(CHEMIN_DONNEES, "graphiques")
        
        if not os.path.exists(chemin_graphiques):
            return {"graphiques": [], "total": 0}
        
        graphiques = []
        for fichier in os.listdir(chemin_graphiques):
            if fichier.endswith('.png'):
                chemin_complet = os.path.join(chemin_graphiques, fichier)
                graphiques.append({
                    "nom": fichier,
                    "chemin": chemin_complet,
                    "date_creation": datetime.fromtimestamp(
                        os.path.getmtime(chemin_complet)
                    ).isoformat(),
                    "taille_kb": os.path.getsize(chemin_complet) / 1024
                })
        
        # Trier par date décroissante
        graphiques.sort(key=lambda x: x["date_creation"], reverse=True)
        
        return {
            "graphiques": graphiques,
            "total": len(graphiques)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des graphiques: {str(e)}"
        )
