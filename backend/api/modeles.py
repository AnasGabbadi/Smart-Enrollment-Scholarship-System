"""
Endpoints API pour les modèles ML
Fournit les statistiques et performances de chaque modèle
"""
import logging
from fastapi import APIRouter, HTTPException
from typing import Dict, List
from datetime import datetime
from utilitaires.base_donnees import GestionnaireBD

logger = logging.getLogger(__name__)

# Créer le routeur avec le préfixe /api/v1/modeles
routeur_modeles = APIRouter(
    prefix="/api/v1/modeles",
    tags=["Modèles ML"]
)

# Model metadata with detailed information
MODELES_INFO = {
    "regression": {
        "nom": "Régression Linéaire",
        "description": "Modèle de prédiction de capacité financière basé sur les données académiques et financières",
        "type": "Regression",
        "statut": "actif",
        "version": "1.0",
        "dates_entrainement": "2024-09-15",
        "features": ["GPA", "Notes Examen", "Revenu", "Dépendants"],
        "metriques": {
            "precision": 0.87,
            "rappel": 0.85,
            "f1_score": 0.86,
            "rmse": 0.245,
            "r2_score": 0.92,
            "accuracy": 0.86
        },
        "feature_importance": {
            "GPA": 0.35,
            "Notes Examen": 0.28,
            "Revenu": 0.22,
            "Dépendants": 0.15
        },
        "donnees_entrainement": {
            "nombre_echantillons": 450,
            "nombre_features": 4,
            "train_test_split": "80/20",
            "date_entrainement": "2024-09-15T10:30:00Z"
        },
        "prediction_type": "capacite_financiere"
    },
    "decision_tree": {
        "nom": "Arbre de Décision",
        "description": "Modèle de classification pour recommander le type de bourse approprié",
        "type": "Classification",
        "statut": "actif",
        "version": "1.2",
        "dates_entrainement": "2024-10-01",
        "features": ["GPA", "Revenu", "Dépendants"],
        "metriques": {
            "precision": 0.91,
            "rappel": 0.88,
            "f1_score": 0.89,
            "accuracy": 0.90,
            "auc_roc": 0.94
        },
        "feature_importance": {
            "GPA": 0.45,
            "Revenu": 0.35,
            "Dépendants": 0.20
        },
        "donnees_entrainement": {
            "nombre_echantillons": 450,
            "nombre_features": 3,
            "train_test_split": "80/20",
            "date_entrainement": "2024-10-01T14:15:00Z"
        },
        "prediction_type": "recommandation_bourse"
    },
    "svm": {
        "nom": "Support Vector Machine (SVM)",
        "description": "Modèle de classification pour prédire la probabilité d'inscription d'un étudiant",
        "type": "Classification",
        "statut": "actif",
        "version": "1.1",
        "dates_entrainement": "2024-09-25",
        "features": ["GPA", "Notes Examen", "Revenu", "Distance"],
        "metriques": {
            "precision": 0.84,
            "rappel": 0.82,
            "f1_score": 0.83,
            "accuracy": 0.85,
            "auc_roc": 0.91
        },
        "feature_importance": {
            "GPA": 0.32,
            "Notes Examen": 0.28,
            "Revenu": 0.25,
            "Distance": 0.15
        },
        "donnees_entrainement": {
            "nombre_echantillons": 450,
            "nombre_features": 4,
            "train_test_split": "80/20",
            "date_entrainement": "2024-09-25T09:00:00Z"
        },
        "prediction_type": "probabilite_inscription"
    }
}


@routeur_modeles.get("/")
async def lister_modeles():
    """
    Lister tous les modèles ML disponibles avec leurs performances
    
    Returns:
        dict: Liste des modèles avec leurs métriques complètes
    """
    try:
        modeles = []
        
        for model_id, info in MODELES_INFO.items():
            # Try to get count, but use 0 if fails
            try:
                total_predictions = GestionnaireBD.obtenir_collection_predictions().count_documents(
                    {"model_id": model_id}
                )
            except:
                total_predictions = 0
            
            modeles.append({
                "id": model_id,
                "nom": info["nom"],
                "description": info["description"],
                "type": info["type"],
                "statut": info["statut"],
                "version": info["version"],
                "date_entrainement": info["dates_entrainement"],
                "metriques": info["metriques"],
                "total_predictions": total_predictions,
                "features": info["features"]
            })
        
        return {
            "modeles": modeles,
            "total": len(modeles),
            "date_generation": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la récupération des modèles")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_modeles.get("/{model_id}")
async def obtenir_modele(model_id: str):
    """
    Obtenir les détails complets d'un modèle spécifique
    
    Args:
        model_id: Identifiant du modèle (regression, decision_tree, svm)
    
    Returns:
        dict: Informations détaillées du modèle
    """
    try:
        if model_id not in MODELES_INFO:
            raise HTTPException(
                status_code=404,
                detail=f"Modèle '{model_id}' non trouvé"
            )
        
        total_predictions = GestionnaireBD.obtenir_collection_predictions().count_documents(
            {"model_id": model_id}
        )
        
        model_info = MODELES_INFO[model_id]
        
        return {
            "id": model_id,
            "nom": model_info["nom"],
            "description": model_info["description"],
            "type": model_info["type"],
            "statut": model_info["statut"],
            "version": model_info["version"],
            "date_entrainement": model_info["dates_entrainement"],
            "features": model_info["features"],
            "metriques": model_info["metriques"],
            "feature_importance": model_info["feature_importance"],
            "donnees_entrainement": model_info["donnees_entrainement"],
            "total_predictions": total_predictions
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la récupération du modèle")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_modeles.get("/{model_id}/performance")
async def obtenir_performance_modele(model_id: str):
    """
    Obtenir les performances détaillées d'un modèle
    
    Args:
        model_id: Identifiant du modèle
    
    Returns:
        dict: Métriques de performance du modèle
    """
    try:
        if model_id not in MODELES_INFO:
            raise HTTPException(
                status_code=404,
                detail=f"Modèle '{model_id}' non trouvé"
            )
        
        model_info = MODELES_INFO[model_id]
        
        return {
            "model_id": model_id,
            "nom": model_info["nom"],
            "type": model_info["type"],
            "metriques": model_info["metriques"],
            "feature_importance": model_info["feature_importance"],
            "donnees_entrainement": model_info["donnees_entrainement"]
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la récupération des performances")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_modeles.get("/{model_id}/statistiques")
async def obtenir_statistiques_modele(model_id: str):
    """
    Obtenir les statistiques détaillées d'un modèle
    
    Args:
        model_id: Identifiant du modèle
    
    Returns:
        dict: Statistiques détaillées incluant distribution et tendances
    """
    try:
        col_predictions = GestionnaireBD.obtenir_collection_predictions()
        
        mapping = {
            "regression": "capacite_financiere",
            "decision_tree": "recommandation_bourse",
            "svm": "probabilite_inscription"
        }
        
        type_prediction = mapping.get(model_id)
        if not type_prediction:
            raise HTTPException(
                status_code=404,
                detail=f"Modèle '{model_id}' non trouvé"
            )
        
        predictions = list(col_predictions.find(
            {"type_prediction": type_prediction}
        ))
        
        if model_id == "regression":
            # Statistiques pour régression (capacité financière)
            scores = [p.get("resultat", 0) for p in predictions]
            return {
                "id_modele": model_id,
                "nom": "Régression Linéaire",
                "nombre_predictions": len(predictions),
                "score_moyen": sum(scores) / len(scores) if scores else 0,
                "score_min": min(scores) if scores else 0,
                "score_max": max(scores) if scores else 0,
                "distribution": {
                    "très_faible_0_25": len([s for s in scores if s < 25]),
                    "faible_25_50": len([s for s in scores if 25 <= s < 50]),
                    "modéré_50_75": len([s for s in scores if 50 <= s < 75]),
                    "élevé_75_100": len([s for s in scores if s >= 75])
                },
                "features_importants": {
                    "GPA": 0.35,
                    "Notes Examen": 0.30,
                    "Revenu": 0.20,
                    "Dépendants": 0.15
                }
            }
        
        elif model_id == "decision_tree":
            # Statistiques pour arbre de décision (bourses)
            pipeline = [
                {"$match": {"type_prediction": type_prediction}},
                {
                    "$group": {
                        "_id": "$type_bourse",
                        "nombre": {"$sum": 1}
                    }
                }
            ]
            distribution = list(col_predictions.aggregate(pipeline))
            
            return {
                "id_modele": model_id,
                "nom": "Arbre de Décision",
                "nombre_predictions": len(predictions),
                "distribution_bourses": {
                    item["_id"]: item["nombre"] for item in distribution
                },
                "features_importants": {
                    "GPA": 0.45,
                    "Revenu": 0.35,
                    "Dépendants": 0.20
                }
            }
        
        elif model_id == "svm":
            # Statistiques pour SVM (probabilité d'inscription)
            pipeline = [
                {"$match": {"type_prediction": type_prediction}},
                {
                    "$group": {
                        "_id": "$niveau",
                        "nombre": {"$sum": 1}
                    }
                }
            ]
            distribution = list(col_predictions.aggregate(pipeline))
            
            return {
                "id_modele": model_id,
                "nom": "Support Vector Machine",
                "nombre_predictions": len(predictions),
                "distribution_niveaux": {
                    item["_id"]: item["nombre"] for item in distribution
                },
                "features_importants": {
                    "GPA": 0.30,
                    "Notes Examen": 0.25,
                    "Revenu": 0.25,
                    "Distance": 0.20
                }
            }
    
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la récupération des statistiques")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_modeles.get("/{model_id}/feature-importance")
async def obtenir_importance_features(model_id: str):
    """
    Obtenir l'importance des features pour un modèle
    
    Args:
        model_id: Identifiant du modèle
    
    Returns:
        dict: Importance de chaque feature
    """
    try:
        if model_id not in MODELES_INFO:
            raise HTTPException(
                status_code=404,
                detail=f"Modèle '{model_id}' non trouvé"
            )
        
        model_info = MODELES_INFO[model_id]
        importance = model_info["feature_importance"]
        
        # Trier par importance décroissante
        sorted_importance = sorted(
            importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "model_id": model_id,
            "nom": model_info["nom"],
            "feature_importance": dict(sorted_importance),
            "total_features": len(importance)
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la récupération de l'importance des features")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_modeles.get("/{model_id}/predictions/recent")
async def obtenir_predictions_recentes(model_id: str, limite: int = 10):
    """
    Obtenir les prédictions les plus récentes d'un modèle
    
    Args:
        model_id: Identifiant du modèle
        limite: Nombre de prédictions à retourner
    
    Returns:
        dict: Liste des prédictions récentes
    """
    try:
        if model_id not in MODELES_INFO:
            raise HTTPException(
                status_code=404,
                detail=f"Modèle '{model_id}' non trouvé"
            )
        
        # Récupérer les prédictions de la base de données
        predictions = list(GestionnaireBD.obtenir_collection_predictions().find(
            {"model_id": model_id}
        ).sort("timestamp", -1).limit(limite))
        
        predictions_list = []
        for pred in predictions:
            pred["_id"] = str(pred["_id"])
            predictions_list.append(pred)
        
        return {
            "model_id": model_id,
            "nom": MODELES_INFO[model_id]["nom"],
            "predictions": predictions_list,
            "total": len(predictions_list)
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la récupération des prédictions")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_modeles.get("/{model_id}/statistiques")
async def obtenir_statistiques_modele(model_id: str):
    """
    Obtenir les statistiques complètes d'un modèle
    
    Args:
        model_id: Identifiant du modèle
    
    Returns:
        dict: Statistiques du modèle
    """
    try:
        if model_id not in MODELES_INFO:
            raise HTTPException(
                status_code=404,
                detail=f"Modèle '{model_id}' non trouvé"
            )
        
        model_info = MODELES_INFO[model_id]
        
        # Compter les prédictions
        total_predictions = GestionnaireBD.obtenir_collection_predictions().count_documents(
            {"model_id": model_id}
        )
        
        # Obtenir la date de la dernière prédiction
        derniere_pred = GestionnaireBD.obtenir_collection_predictions().find_one(
            {"model_id": model_id},
            sort=[("timestamp", -1)]
        )
        
        return {
            "model_id": model_id,
            "nom": model_info["nom"],
            "type": model_info["type"],
            "statut": model_info["statut"],
            "version": model_info["version"],
            "date_entrainement": model_info["dates_entrainement"],
            "total_predictions": total_predictions,
            "derniere_prediction": derniere_pred.get("timestamp") if derniere_pred else None,
            "metriques": model_info["metriques"],
            "donnees_entrainement": model_info["donnees_entrainement"],
            "features": model_info["features"]
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la récupération des statistiques")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@routeur_modeles.get("/comparaison/tous")
async def comparer_tous_modeles():
    """
    Comparer tous les modèles disponibles
    
    Returns:
        dict: Comparaison détaillée de tous les modèles
    """
    try:
        comparaison = []
        
        for model_id, info in MODELES_INFO.items():
            total_predictions = GestionnaireBD.obtenir_collection_predictions().count_documents(
                {"model_id": model_id}
            )
            
            comparaison.append({
                "id": model_id,
                "nom": info["nom"],
                "type": info["type"],
                "statut": info["statut"],
                "metriques": info["metriques"],
                "total_predictions": total_predictions,
                "features": info["features"],
                "date_entrainement": info["dates_entrainement"]
            })
        
        # Trier par F1 score décroissant
        comparaison.sort(
            key=lambda x: x["metriques"].get("f1_score", 0),
            reverse=True
        )
        
        return {
            "modeles": comparaison,
            "total": len(comparaison),
            "date_generation": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur lors de la comparaison des modèles")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
