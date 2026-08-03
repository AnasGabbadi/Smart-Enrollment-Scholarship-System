"""
Endpoints API pour les prédictions ML
Fournit les prédictions de capacité financière, bourse et probabilité d'inscription
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
from typing import Dict, Any
from api.schemas import (
    RequeteCapaciteFinanciere, ReponseCapaciteFinanciere,
    RequeteRecommandationBourse, ReponseRecommandationBourse,
    RequeteProabiliteInscription, ReponseProabiliteInscription
)
from modeles.regression_lineaire import modele_regression
from modeles.arbre_decision import modele_arbre
from modeles.svm import modele_svm
from utilitaires.base_donnees import GestionnaireBD

# Créer le routeur avec le préfixe /api/v1/predictions
routeur_predictions = APIRouter(
    prefix="/api/v1/predictions",
    tags=["Prédictions ML"]
)


@routeur_predictions.post("/capacite-financiere", response_model=ReponseCapaciteFinanciere)
async def predire_capacite_financiere(requete: RequeteCapaciteFinanciere):
    """
    Prédire la capacité financière d'un étudiant
    
    Utilise un modèle de régression linéaire entraîné pour estimer
    la capacité financière de l'étudiant sur une échelle 0-100
    
    Args:
        requete: Données académiques et financières de l'étudiant
        
    Returns:
        ReponseCapaciteFinanciere: Score (0-100) et message explicatif
        
    Raises:
        HTTPException: En cas d'erreur de prédiction
    """
    try:
        # Préparer les données pour le modèle (extraire des objets imbriqués)
        caracteristiques = [
            requete.donnees_academiques.gpa,
            requete.donnees_academiques.noteExamen,
            requete.donnees_financieres.revenu,
            requete.donnees_financieres.dependants
        ]
        
        # Faire la prédiction
        score = modele_regression.predire(caracteristiques)
        
        # Générer un message explicatif basé sur le score
        if score >= 75:
            message = "Capacité financière élevée - Excellente situation"
        elif score >= 50:
            message = "Capacité financière modérée - Situation stable"
        elif score >= 25:
            message = "Capacité financière limitée - Nécessite du soutien"
        else:
            message = "Capacité financière très faible - Soutien prioritaire recommandé"
        
        # Enregistrer la prédiction dans la base de données
        try:
            collection_predictions = GestionnaireBD.obtenir_collection_predictions()
            collection_predictions.insert_one({
                "id_prediction": str(uuid.uuid4()),
                "type_prediction": "capacite_financiere",
                "donnees_entree": requete.dict(),
                "resultat": score,
                "message": message,
                "date_creation": datetime.utcnow()
            })
        except:
            pass  # Ne pas bloquer la réponse si l'enregistrement échoue
        
        return {
            "scoreFinancier": round(score, 2),
            "message": message,
            "details": {
                "gpa": requete.donnees_academiques.gpa,
                "noteExamen": requete.donnees_academiques.noteExamen,
                "revenu": requete.donnees_financieres.revenu,
                "dependants": requete.donnees_financieres.dependants
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la prédiction de capacité financière: {str(e)}"
        )


@routeur_predictions.post("/recommandation-bourse", response_model=ReponseRecommandationBourse)
async def predire_recommandation_bourse(requete: RequeteRecommandationBourse):
    """
    Recommander un type et montant de bourse
    
    Utilise un modèle d'arbre de décision pour recommander le type
    et le pourcentage de bourse basé sur les performances et situation financière
    
    Args:
        requete: Données de l'étudiant
        
    Returns:
        ReponseRecommandationBourse: Type de bourse et pourcentage
        
    Raises:
        HTTPException: En cas d'erreur de prédiction
    """
    try:
        # Préparer les données pour le modèle (extraire des objets imbriqués)
        caracteristiques = [
            requete.donnees_academiques.gpa,
            requete.donnees_financieres.revenu,
            requete.donnees_financieres.dependants
        ]
        
        # Faire la prédiction
        classe_bourse = modele_arbre.predire(caracteristiques)
        
        # Mapper les classes aux types de bourses
        types_bourses = {
            0: {"nom": "Pas de réduction", "pourcentage": 0},
            1: {"nom": "Réduction 25%", "pourcentage": 25},
            2: {"nom": "Bourse 50%", "pourcentage": 50},
            3: {"nom": "Bourse complète", "pourcentage": 100}
        }
        
        recommandation = types_bourses.get(classe_bourse, types_bourses[0])
        
        message = f"Recommandation: {recommandation['nom']} basée sur GPA ({requete.donnees_academiques.gpa}), revenu ({requete.donnees_financieres.revenu}€) et dépendants ({requete.donnees_financieres.dependants})"
        
        # Enregistrer la prédiction
        try:
            collection_predictions = GestionnaireBD.obtenir_collection_predictions()
            collection_predictions.insert_one({
                "id_prediction": str(uuid.uuid4()),
                "type_prediction": "recommandation_bourse",
                "donnees_entree": requete.dict(),
                "type_bourse": recommandation['nom'],
                "pourcentage": recommandation['pourcentage'],
                "date_creation": datetime.utcnow()
            })
        except:
            pass
        
        return {
            "typeBourse": recommandation['nom'],
            "pourcentage": recommandation['pourcentage'],
            "message": message,
            "details": {
                "gpa": requete.donnees_academiques.gpa,
                "revenu": requete.donnees_financieres.revenu,
                "dependants": requete.donnees_financieres.dependants
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la recommandation de bourse: {str(e)}"
        )


@routeur_predictions.post("/probabilite-inscription", response_model=ReponseProabiliteInscription)
async def predire_probabilite_inscription(requete: RequeteProabiliteInscription):
    """
    Prédire la probabilité que l'étudiant s'inscrive
    
    Utilise un modèle SVM pour classer la probabilité d'inscription
    de l'étudiant (faible, moyenne, forte)
    
    Args:
        requete: Données académiques et contextuelles
        
    Returns:
        ReponseProabiliteInscription: Niveau de probabilité et confiance
        
    Raises:
        HTTPException: En cas d'erreur de prédiction
    """
    try:
        # Préparer les données pour le modèle (extraire des objets imbriqués)
        caracteristiques = [
            requete.donnees_academiques.gpa,
            requete.donnees_academiques.noteExamen,
            requete.donnees_financieres.revenu,
            requete.donnees_contextuelles.distance
        ]
        
        # Faire la prédiction
        prediction = modele_svm.predire(caracteristiques)
        
        # Mapper les niveaux de probabilité
        niveaux = {
            0: "Faible probabilité",
            1: "Probabilité moyenne",
            2: "Forte probabilité"
        }
        
        niveau = niveaux.get(prediction['classe'], "Probabilité inconnue")
        confiance = prediction.get('confiance', 0.5)
        
        message = f"Prédiction d'inscription avec confiance {confiance*100:.1f}%"
        
        # Enregistrer la prédiction
        try:
            collection_predictions = GestionnaireBD.obtenir_collection_predictions()
            collection_predictions.insert_one({
                "id_prediction": str(uuid.uuid4()),
                "type_prediction": "probabilite_inscription",
                "donnees_entree": requete.dict(),
                "niveau": niveau,
                "confiance": confiance,
                "date_creation": datetime.utcnow()
            })
        except:
            pass
        
        return {
            "probabiliteInscription": niveau,
            "confiance": round(confiance, 3),
            "message": message,
            "details": {
                "gpa": requete.donnees_academiques.gpa,
                "noteExamen": requete.donnees_academiques.noteExamen,
                "revenu": requete.donnees_financieres.revenu,
                "distance": requete.donnees_contextuelles.distance
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la prédiction de probabilité d'inscription: {str(e)}"
        )


@routeur_predictions.get("/etudiant/{id_etudiant}/recommandations")
async def obtenir_recommandations_etudiant(id_etudiant: str) -> Dict[str, Any]:
    """
    Obtenir toutes les recommandations IA pour un étudiant spécifique
    
    Récupère les données de l'étudiant et exécute tous les modèles ML
    pour fournir une recommandation complète sur l'attribution de bourse
    
    Args:
        id_etudiant: Identifiant unique de l'étudiant
        
    Returns:
        Dict contenant:
        - capacite_financiere: Score et message
        - recommandation_bourse: Type de bourse et montant suggéré
        - probabilite_inscription: Probabilité d'inscription
        - recommandation_globale: Synthèse et décision finale
        
    Raises:
        HTTPException 404: Étudiant non trouvé
        HTTPException 500: Erreur lors de la prédiction
    """
    try:
        # Récupérer l'étudiant de la base de données
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        etudiant = collection_etudiants.find_one({"idEtudiant": id_etudiant})
        
        if not etudiant:
            raise HTTPException(
                status_code=404,
                detail=f"Étudiant avec ID {id_etudiant} non trouvé"
            )
        
        # Extraire les données nécessaires avec conversion robuste
        # Support pour le nouveau système marocain (baccalauréat/diplôme)
        # AND support pour l'ancienne structure plate (données enrichies)
        
        # Essayer d'abord la structure imbriquée (new registration system)
        donnees_baccalaureat = etudiant.get("donnees_baccalaureat", {})
        donnees_diplome = etudiant.get("donnees_diplome", {})
        donnees_financieres = etudiant.get("donnees_financieres", {})
        donnees_contextuelles = etudiant.get("donnees_contextuelles", {})
        
        # Extraire les notes académiques du nouveau système marocain
        # Convertir en float avec valeurs par défaut
        if donnees_baccalaureat:
            # Structure imbriquée (new registration)
            note_regionale = float(donnees_baccalaureat.get("notes_regionales", 0) or 0)
            note_generale = float(donnees_baccalaureat.get("note_generale", 0) or 0)
            note_diplome = float(donnees_diplome.get("notes_diplome", 0) or 0) if donnees_diplome else 0
        else:
            # Structure plate (enriched data from insert_data.py)
            note_regionale = float(etudiant.get("notes_regionales", 0) or 0)
            note_generale = float(etudiant.get("note_generale", 0) or 0)
            note_diplome = float(etudiant.get("notes_diplome", 0) or 0)
        
        # Utiliser la moyenne des notes du baccalauréat comme base pour GPA (converti en échelle 0-20)
        gpa = (note_regionale + note_generale) / 2  # Moyenne des deux notes Bac
        
        # Utiliser la note diplôme si disponible sinon utiliser la note générale
        note_examen = note_diplome if note_diplome > 0 else note_generale
        
        # Extraire les données financières (support pour les deux structures)
        if donnees_financieres:
            # Structure imbriquée (new registration)
            revenu = float(donnees_financieres.get("revenu", 0) or 0)
            dependants = int(donnees_financieres.get("dependants", 0) or 0)
        else:
            # Structure plate (enriched data)
            revenu = float(etudiant.get("revenu", 0) or 0)
            dependants = int(etudiant.get("dependants", 0) or 0)
        
        # Extraire la distance (support pour les deux structures)
        if donnees_contextuelles:
            distance = float(donnees_contextuelles.get("distance", 0) or 0)
        else:
            distance = float(etudiant.get("distance", 0) or 0)
        
        
        # 1. Prédiction de capacité financière
        caracteristiques_financieres = [gpa, note_examen, revenu, dependants, distance]
        score_financier = modele_regression.predire(caracteristiques_financieres)
        
        niveaux_capacite = {
            (0, 30): ("Capacité Faible", "L'étudiant a besoin d'un soutien financier important"),
            (30, 60): ("Capacité Moyenne", "L'étudiant pourrait bénéficier d'une aide partielle"),
            (60, 100): ("Capacité Élevée", "L'étudiant a une bonne capacité financière")
        }
        
        niveau_capacite = "Capacité Moyenne"
        message_capacite = "Capacité financière standard"
        for (min_val, max_val), (niveau, msg) in niveaux_capacite.items():
            if min_val <= score_financier < max_val:
                niveau_capacite = niveau
                message_capacite = msg
                break
        
        # 2. Prédiction de recommandation de bourse
        caracteristiques_bourse = [gpa, note_examen, revenu, dependants, distance]
        prediction_bourse = modele_arbre.predire(caracteristiques_bourse)
        
        types_bourse = {
            0: ("Aucune", 0, "Performance ou situation financière ne justifie pas de bourse"),
            1: ("Partielle", 2500, "Bourse partielle (25%) recommandée pour soutien minimal"),
            2: ("Partielle", 5000, "Bourse partielle (50%) recommandée pour soutien modéré"),
            3: ("Complète", 10000, "Bourse complète (100%) recommandée - cas prioritaire")
        }
        
        type_bourse, montant_bourse, message_bourse = types_bourse.get(
            prediction_bourse,
            ("Aucune", 0, "Type de bourse non déterminé")
        )
        
        # 3. Prédiction de probabilité d'inscription
        caracteristiques_inscription = [gpa, note_examen, revenu, dependants, distance]
        resultat_svm = modele_svm.predire(caracteristiques_inscription)
        prediction_inscription = resultat_svm['classe']
        confiance_inscription = resultat_svm['confiance']
        
        niveaux_proba = {
            0: "Faible (< 50%)",
            1: "Moyenne (50-75%)",
            2: "Élevée (> 75%)"
        }
        
        niveau_inscription = niveaux_proba.get(prediction_inscription, "Probabilité inconnue")
        
        # 4. Recommandation globale synthétisée
        score_global = (score_financier / 100) * 0.3 + (prediction_bourse / 3) * 0.4 + (prediction_inscription / 2) * 0.3
        
        if score_global >= 0.7 and type_bourse == "Complète":
            decision_globale = "Bourse Complète Recommandée"
            couleur_decision = "green"
            justification = f"Excellent profil académique (GPA: {gpa:.2f}), besoin financier important et forte probabilité d'inscription. Priorité élevée."
        elif score_global >= 0.5 or type_bourse == "Partielle":
            decision_globale = "Bourse Partielle Recommandée"
            couleur_decision = "yellow"
            justification = f"Bon profil (GPA: {gpa:.2f}) avec besoin modéré de soutien financier. Bourse partielle appropriée."
        else:
            decision_globale = "Pas de Bourse Recommandée"
            couleur_decision = "red"
            justification = f"Capacité financière suffisante (Score: {score_financier:.0f}/100) ou performance académique ne justifiant pas de bourse pour l'instant."
        
        # Construire la réponse complète
        return {
            "idEtudiant": id_etudiant,
            "nomComplet": f"{etudiant.get('prenom', '')} {etudiant.get('nom', '')}",
            "capaciteFinanciere": {
                "score": round(score_financier, 1),
                "niveau": niveau_capacite,
                "message": message_capacite
            },
            "recommandationBourse": {
                "type": type_bourse,
                "montant": montant_bourse,
                "message": message_bourse
            },
            "probabiliteInscription": {
                "niveau": niveau_inscription,
                "confiance": round(confiance_inscription * 100, 1),
                "prediction": int(prediction_inscription)
            },
            "recommandationGlobale": {
                "decision": decision_globale,
                "couleur": couleur_decision,
                "justification": justification,
                "scoreGlobal": round(score_global * 100, 1)
            },
            "details": {
                "gpa": gpa,
                "noteExamen": note_examen,
                "revenu": revenu,
                "dependants": dependants,
                "distance": distance
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Erreur dans obtenir_recommandations_etudiant: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération des recommandations: {str(e)}"
        )
