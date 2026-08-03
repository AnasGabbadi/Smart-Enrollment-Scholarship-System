"""
API endpoints for ML-based student ranking and recommendations
Ranks pending students by merit for scholarship allocation respecting yearly quotas
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Dict, Any
from modeles.regression_lineaire import modele_regression
from modeles.arbre_decision import modele_arbre
from modeles.svm import modele_svm
from utilitaires.base_donnees import GestionnaireBD

routeur_ml_ranking = APIRouter(
    prefix="/api/v1/ml-ranking",
    tags=["ML Ranking & Recommendations"]
)

# Model information and explanations
MODEL_EXPLANATIONS = {
    "regression_lineaire": {
        "nom": "Régression Linéaire",
        "description": "Modèle de régression linéaire pour prédiction continue",
        "fonctionnement": "Apprend une relation linéaire entre les caractéristiques académiques/financières et la capacité financière",
        "capacite": "Prédit un score continu (0-100) basé sur une combinaison linéaire de features",
        "forces": ["Rapide", "Interprétable", "Bon pour relations linéaires"],
        "limites": ["Suppose une relation linéaire", "Sensible aux outliers"],
        "features_utilisees": ["GPA", "Note Examen", "Revenu", "Dépendants", "Distance"]
    },
    "arbre_decision": {
        "nom": "Arbre de Décision",
        "description": "Arbre de décision pour classification hiérarchique",
        "fonctionnement": "Apprend une série de règles de décision en analysant les seuils des features",
        "capacite": "Classe les étudiants en catégories basées sur des règles de seuil découvertes automatiquement",
        "forces": ["Non-linéaire", "Robuste aux outliers", "Facile à interpréter"],
        "limites": ["Peut surfit", "Sensible aux changements de données"],
        "features_utilisees": ["GPA", "Note Examen", "Revenu", "Dépendants", "Distance"]
    },
    "svm": {
        "nom": "Support Vector Machine (SVM)",
        "description": "Machine à vecteurs de support pour classification",
        "fonctionnement": "Apprend un hyperplan séparant les étudiants aptes des inaptes à recevoir une bourse",
        "capacite": "Classe les étudiants de manière discriminante avec probabilité d'acceptation",
        "forces": ["Très efficace en haute dimension", "Robuste", "Bon pour données complexes"],
        "limites": ["Moins interprétable", "Lent sur grandes données"],
        "features_utilisees": ["GPA", "Note Examen", "Revenu", "Dépendants", "Distance"]
    }
}


def extraire_features_etudiant(student: Dict[str, Any]) -> List[float]:
    """
    Extract ML features from student data
    Features: [GPA, NoteExamen, Revenu, Dépendants, Distance]
    
    Handles both nested structure (from registration form) and flat structure (from database)
    
    Args:
        student: Student document from MongoDB
        
    Returns:
        List of 5 features for ML models
    """
    try:
        # Handle None student
        if not student:
            print("Error extracting features: student is None")
            return [0, 0, 0, 0, 0]
        
        # Try to get GPA from nested structure first, then try flat fields
        gpa = None
        
        # Check nested structure (from registration form)
        donnees_bac = student.get('donnees_baccalaureat')
        if donnees_bac and isinstance(donnees_bac, dict):
            gpa = (donnees_bac.get('notes_regionales', 0) + donnees_bac.get('note_generale', 0)) / 2
        
        # Check flat fields (from database)
        if not gpa or gpa == 0:
            notes_regionales = student.get('notes_regionales', 0)
            note_generale = student.get('note_generale', 0)
            if notes_regionales or note_generale:
                gpa = (float(notes_regionales) + float(note_generale)) / 2
        
        # Check if GPA is already calculated
        if not gpa or gpa == 0:
            gpa_field = student.get('gpa', 0)
            if gpa_field:
                gpa = float(gpa_field)
        
        gpa = float(gpa) if gpa else 0
        
        # Get exam score (note d'examen)
        note_examen = None
        
        # Check nested diplôme
        donnees_diplome = student.get('donnees_diplome')
        if donnees_diplome and isinstance(donnees_diplome, dict):
            note_examen = donnees_diplome.get('notes_diplome')
        
        # Check flat fields
        if not note_examen or note_examen == 0:
            note_examen = student.get('notes_diplome')
        
        # Check exam_score field
        if not note_examen or note_examen == 0:
            note_examen = student.get('exam_score')
        
        # Default to GPA if no exam score
        if not note_examen or note_examen == 0:
            note_examen = gpa
        
        note_examen = float(note_examen) if note_examen else 0
        
        # Get financial data - check nested first, then flat
        revenu = 0
        dependants = 0
        
        donnees_financieres = student.get('donnees_financieres')
        if donnees_financieres and isinstance(donnees_financieres, dict):
            revenu = donnees_financieres.get('revenu', 0)
            dependants = donnees_financieres.get('dependants', 0)
        else:
            # Try flat fields
            revenu = student.get('revenu', 0)
            dependants = student.get('dependants', 0)
        
        revenu = float(revenu) if revenu else 0
        dependants = float(dependants) if dependants else 0
        
        # Get distance - check nested first, then flat
        distance = 0
        
        donnees_contextuelles = student.get('donnees_contextuelles')
        if donnees_contextuelles and isinstance(donnees_contextuelles, dict):
            distance = donnees_contextuelles.get('distance', 0)
        else:
            # Try flat field
            distance = student.get('distance', 0)
        
        distance = float(distance) if distance else 0
        
        return [gpa, note_examen, revenu, dependants, distance]
    
    except Exception as e:
        print(f"Error extracting features: {str(e)}")
        return [0, 0, 0, 0, 0]


@routeur_ml_ranking.get("/models-info")
async def obtenir_info_modeles():
    """
    Get information about all ML models
    Returns how each model learns, its capacity, and features
    """
    try:
        return {
            "models": MODEL_EXPLANATIONS,
            "total_features": 5,
            "feature_names": ["GPA", "Note Examen", "Revenu", "Dépendants", "Distance"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving model information: {str(e)}"
        )


@routeur_ml_ranking.get("/models-statistics")
async def obtenir_stats_modeles():
    """
    Get detailed statistics about ML models including training info and performance
    Shows how models learn, what they've learned, and their prediction capacity
    """
    try:
        # Get total students in database for training context
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        total_students = collection_etudiants.count_documents({})
        approved_students = collection_etudiants.count_documents({"statut": "Approuvé"})
        rejected_students = collection_etudiants.count_documents({"statut": "Rejeté"})
        pending_students = collection_etudiants.count_documents({"statut": "En attente"})
        
        return {
            "training_data": {
                "total_etudiants": total_students,
                "etudiants_approuves": approved_students,
                "etudiants_rejetes": rejected_students,
                "etudiants_en_attente": pending_students,
                "contexte": "Les modèles ont été entraînés sur des données d'étudiants marocains avec normes académiques marocaines"
            },
            "models": {
                "regression_lineaire": {
                    **MODEL_EXPLANATIONS["regression_lineaire"],
                    "type": "Régression",
                    "output": "Score continu 0-100",
                    "apprentissage": "Minimise l'erreur quadratique entre prédictions et résultats réels",
                    "capacite_prediction": "Estime un score basé sur relation linéaire entre features et résultat"
                },
                "arbre_decision": {
                    **MODEL_EXPLANATIONS["arbre_decision"],
                    "type": "Classification",
                    "output": "Classe binaire (Approuvé/Rejeté) ou score 0-100",
                    "apprentissage": "Apprend des règles de décision en divisant les données par seuils de features",
                    "capacite_prediction": "Classe les étudiants via une hiérarchie de questions sur leurs features"
                },
                "svm": {
                    **MODEL_EXPLANATIONS["svm"],
                    "type": "Classification",
                    "output": "Classe binaire avec probabilité",
                    "apprentissage": "Apprend un hyperplan optimal pour séparer les classes en espace transformé",
                    "capacite_prediction": "Classe les étudiants de manière robuste en haute dimension"
                }
            },
            "ensemble_strategy": {
                "description": "Les 3 modèles votent pour chaque étudiant",
                "methode": "Moyenne des scores + consensus voting",
                "consensus": "Étudiant recommandé par les 3 modèles (confiance élevée)",
                "robustesse": "L'ensemble réduit le risque de surfit d'un modèle unique"
            },
            "features_explanation": {
                "GPA": "Score académique (notes_regionales + note_generale) / 2 - indicateur de réussite académique",
                "Note Examen": "Notes d'examen ou diplôme - indicateur de performance complémentaire",
                "Revenu": "Revenu familial annuel en Dirham (DH) - indicateur de besoin financier",
                "Dépendants": "Nombre de dépendants - indicateur de responsabilité financière",
                "Distance": "Distance du domicile à l'établissement - indicateur de mobilité"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving model statistics: {str(e)}"
        )


@routeur_ml_ranking.get("/rank-students/{year}")
async def ranger_etudiants_par_annee(year: int):
    """
    Rank pending students for a given year using all 3 ML models
    Respects the yearly quota and returns top candidates
    
    Args:
        year: Academic year to rank students for
        
    Returns:
        Dict with rankings from each model, respecting quota
    """
    try:
        # Get quota for the year
        collection_quotas = GestionnaireBD.obtenir_collection_quotas()
        quota = collection_quotas.find_one({"annee": year})
        
        if not quota:
            raise HTTPException(
                status_code=404,
                detail=f"No quota defined for year {year}. Please set quota first."
            )
        
        quota_nombre = quota.get("nombre_bourses", 0)
        
        # Get pending students for the year
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        pending_students = list(collection_etudiants.find({
            "statut": "En attente",
            "annee": year
        }))
        
        if not pending_students:
            return {
                "annee": year,
                "quota": quota_nombre,
                "total_etudiants_en_attente": 0,
                "regression_lineaire": {
                    "nom": "Régression Linéaire",
                    "top_candidates": [],
                    "scores": []
                },
                "arbre_decision": {
                    "nom": "Arbre de Décision",
                    "top_candidates": [],
                    "scores": []
                },
                "svm": {
                    "nom": "Support Vector Machine",
                    "top_candidates": [],
                    "scores": []
                },
                "consensus": {
                    "description": "Students recommended by all 3 models",
                    "candidates": []
                }
            }
        
        # Score students with each model
        students_with_scores = []
        
        for student in pending_students:
            # Skip if student is None
            if not student:
                continue
                
            features = extraire_features_etudiant(student)
            
            # Get predictions from each model
            try:
                score_regression = modele_regression.predire(features)
                # Handle case where response is a dict
                if isinstance(score_regression, dict):
                    score_regression = score_regression.get('prediction', score_regression.get('score', 50.0))
                score_regression = float(score_regression)
            except:
                score_regression = 50.0
            
            try:
                score_arbre = modele_arbre.predire(features)
                # Decision tree returns 0-3 (scholarship class), convert to 0-100 score
                if isinstance(score_arbre, dict):
                    score_arbre = score_arbre.get('prediction', score_arbre.get('score', 50.0))
                score_arbre = float(score_arbre)
                # Convert from 0-3 to 0-100: map 0->0, 1->33, 2->67, 3->100
                score_arbre = (score_arbre / 3.0) * 100
            except:
                score_arbre = 50.0
            
            try:
                score_svm = modele_svm.predire(features)
                # SVM returns dict with 'classe' and 'confiance' or 0-2 classification
                if isinstance(score_svm, dict):
                    # Use both class (0-2) and confidence to create 0-100 score
                    classe = score_svm.get('classe', 1)
                    confiance = score_svm.get('confiance', 0.5)
                    # Score = (classe/2 * 80) + (confiance * 20)
                    # This gives: classe importance 80%, confiance 20%
                    score_svm = ((classe / 2.0) * 80) + (confiance * 20)
                else:
                    # Raw classification value 0-2, convert to 0-100
                    score_svm = float(score_svm)
                    score_svm = (score_svm / 2.0) * 100
                score_svm = float(score_svm)
            except:
                score_svm = 50.0
            
            # Average score across models
            avg_score = (score_regression + score_arbre + score_svm) / 3
            
            # Calculate financial need index (0-100, where higher = more need)
            # Lower income = higher need, more dependents = higher need
            max_revenu = 50000
            
            # Get revenu from flat or nested structure
            student_revenu = student.get('revenu') if student.get('revenu') else student.get('donnees_financieres', {}).get('revenu', 0)
            student_dependants = student.get('dependants') if student.get('dependants') else student.get('donnees_financieres', {}).get('dependants', 0)
            
            financial_need = min(100, (max_revenu - float(student_revenu or 0)) / max_revenu * 100)
            dependant_factor = float(student_dependants or 0) * 5
            financial_need = min(100, financial_need + dependant_factor)
            
            # Calculate GPA (0-20 scale) - handle both flat and nested
            gpa_bac = student.get('gpa')
            if not gpa_bac:
                notes_reg = student.get('notes_regionales') or student.get('donnees_baccalaureat', {}).get('notes_regionales', 0)
                note_gen = student.get('note_generale') or student.get('donnees_baccalaureat', {}).get('note_generale', 0)
                gpa = (float(notes_reg or 0) + float(note_gen or 0)) / 2
            else:
                gpa = float(gpa_bac)
            
            # Normalize GPA to 0-100 scale
            gpa_score = (gpa / 20) * 100
            
            # Combined priority score: 60% GPA + 40% Financial Need
            # This prioritizes high-performing students WITH financial need
            priority_score = (gpa_score * 0.60) + (financial_need * 0.40)
            
            # Recommend sponsorship type based on financial need
            if financial_need > 70:
                recommended_sponsorship = "Complète"
            elif financial_need > 40:
                recommended_sponsorship = "Moitié"
            else:
                recommended_sponsorship = "Partielle"
            
            # Extract GPA and financial data - handle both flat and nested structures
            # Flat structure (from database)
            gpa_flat = student.get('gpa')
            revenu_flat = student.get('revenu', 0)
            dependants_flat = student.get('dependants', 0)
            distance_flat = student.get('distance', 0)
            
            # Use flat if available, otherwise use calculated values
            final_gpa = gpa_flat if gpa_flat else gpa
            final_revenu = revenu_flat if revenu_flat else student.get('donnees_financieres', {}).get('revenu', 0)
            final_dependants = dependants_flat if dependants_flat else student.get('donnees_financieres', {}).get('dependants', 0)
            final_distance = distance_flat if distance_flat else student.get('donnees_contextuelles', {}).get('distance', 0)
            
            students_with_scores.append({
                "idEtudiant": str(student.get("idEtudiant", student.get("_id"))),
                "prenom": student.get("prenom"),
                "nom": student.get("nom"),
                "email": student.get("email"),
                "gpa": round(final_gpa, 2) if final_gpa else 0,
                "revenu": round(final_revenu, 2) if final_revenu else 0,
                "dependants": int(final_dependants) if final_dependants else 0,
                "distance": round(final_distance, 2) if final_distance else 0,
                "type_sponsorship": student.get('type_sponsorship', 'Complète'),
                "recommended_sponsorship": recommended_sponsorship,
                "financial_need": round(financial_need, 2),
                "priority_score": round(priority_score, 2),
                "score_regression": round(score_regression, 2),
                "score_arbre": round(score_arbre, 2),
                "score_svm": round(score_svm, 2),
                "average_score": round(avg_score, 2)
            })
        
        # Sort by priority score (financial need + high grades first)
        # This ensures: Low income + High grades > Medium income + High grades > High income + High grades
        students_with_scores.sort(key=lambda x: (-x['priority_score'], -x['average_score']))
        
        # Get top candidates according to quota
        top_candidates = students_with_scores[:quota_nombre]
        
        # Get consensus candidates (recommended by all 3 models)
        # A student is in consensus if they're in top candidates of all models
        regression_top_ids = {s['idEtudiant'] for s in sorted(
            students_with_scores, 
            key=lambda x: x['score_regression'], 
            reverse=True
        )[:quota_nombre]}
        
        arbre_top_ids = {s['idEtudiant'] for s in sorted(
            students_with_scores, 
            key=lambda x: x['score_arbre'], 
            reverse=True
        )[:quota_nombre]}
        
        svm_top_ids = {s['idEtudiant'] for s in sorted(
            students_with_scores, 
            key=lambda x: x['score_svm'], 
            reverse=True
        )[:quota_nombre]}
        
        consensus_ids = regression_top_ids & arbre_top_ids & svm_top_ids
        consensus_candidates = [s for s in students_with_scores if s['idEtudiant'] in consensus_ids]
        
        return {
            "annee": year,
            "quota": quota_nombre,
            "total_etudiants_en_attente": len(pending_students),
            "regression_lineaire": {
                "nom": "Régression Linéaire",
                "description": MODEL_EXPLANATIONS["regression_lineaire"]["description"],
                "fonctionnement": MODEL_EXPLANATIONS["regression_lineaire"]["fonctionnement"],
                "capacite": MODEL_EXPLANATIONS["regression_lineaire"]["capacite"],
                "top_candidates": sorted(
                    students_with_scores,
                    key=lambda x: x['score_regression'],
                    reverse=True
                )[:quota_nombre]
            },
            "arbre_decision": {
                "nom": "Arbre de Décision",
                "description": MODEL_EXPLANATIONS["arbre_decision"]["description"],
                "fonctionnement": MODEL_EXPLANATIONS["arbre_decision"]["fonctionnement"],
                "capacite": MODEL_EXPLANATIONS["arbre_decision"]["capacite"],
                "top_candidates": sorted(
                    students_with_scores,
                    key=lambda x: x['score_arbre'],
                    reverse=True
                )[:quota_nombre]
            },
            "svm": {
                "nom": "Support Vector Machine",
                "description": MODEL_EXPLANATIONS["svm"]["description"],
                "fonctionnement": MODEL_EXPLANATIONS["svm"]["fonctionnement"],
                "capacite": MODEL_EXPLANATIONS["svm"]["capacite"],
                "top_candidates": sorted(
                    students_with_scores,
                    key=lambda x: x['score_svm'],
                    reverse=True
                )[:quota_nombre]
            },
            "consensus": {
                "description": "Students recommended by all 3 models (high confidence)",
                "candidates": consensus_candidates,
                "count": len(consensus_candidates)
            },
            "merged_ranking": {
                "description": "All students ranked by average score across models",
                "top_candidates": top_candidates,
                "remaining_candidates": students_with_scores[quota_nombre:] if quota_nombre < len(students_with_scores) else []
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error ranking students: {str(e)}"
        )


@routeur_ml_ranking.get("/rank-summary/{year}")
async def obtenir_resume_rangement(year: int):
    """
    Get a summary of student rankings for quick view
    Shows consensus candidates and quota status
    """
    try:
        ranking_data = await ranger_etudiants_par_annee(year)
        
        # Count actually approved students
        collection_etudiants = GestionnaireBD.obtenir_collection_etudiants()
        approved_count = collection_etudiants.count_documents({"statut": "Approuvé"})
        
        return {
            "annee": year,
            "quota": ranking_data["quota"],
            "total_etudiants": ranking_data["total_etudiants_en_attente"],
            "approved_count": approved_count,
            "consensus_count": ranking_data["consensus"]["count"],
            "consensus_candidates": ranking_data["consensus"]["candidates"][:5],  # Top 5
            "top_merged": ranking_data["merged_ranking"]["top_candidates"][:ranking_data["quota"]],
            "quota_remaining": max(0, ranking_data["quota"] - approved_count)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating ranking summary: {str(e)}"
        )
