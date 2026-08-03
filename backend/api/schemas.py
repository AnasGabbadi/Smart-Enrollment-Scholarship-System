"""
Schémas de données Pydantic pour validation et sérialisation
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal
from datetime import datetime

# ============================================================================
# MODÈLES POUR SYSTÈME ÉDUCATIF MAROCAIN
# ============================================================================

class DonneesBaccalaureat(BaseModel):
    """Données du Baccalauréat (Marocain)"""
    notes_regionales: float = Field(..., ge=0, le=20, description="Notes régionales du Bac (0-20)")
    note_generale: float = Field(..., ge=0, le=20, description="Note générale du Bac (0-20)")
    option: Literal["Maths", "Physique", "SVT"] = Field(..., description="Option du Bac")

    class Config:
        json_schema_extra = {
            "example": {
                "notes_regionales": 16.5,
                "note_generale": 17.0,
                "option": "Maths"
            }
        }


class DonneesDiplome(BaseModel):
    """Données du Diplôme Bac+2"""
    notes_diplome: float = Field(..., ge=0, le=20, description="Notes du diplôme (0-20)")
    option: str = Field(..., description="Spécialité du diplôme (ex: Informatique, Commerce)")

    class Config:
        json_schema_extra = {
            "example": {
                "notes_diplome": 15.5,
                "option": "Informatique"
            }
        }


# ============================================================================
# MODÈLES D'ENTRÉE - Données reçues du client
# ============================================================================

class DonneesAcademiques(BaseModel):
    """Données académiques de l'étudiant"""
    gpa: float = Field(..., ge=0, le=20, description="Note moyenne (0-20)")
    noteExamen: float = Field(..., ge=0, le=100, description="Note d'examen (0-100)")

    class Config:
        json_schema_extra = {
            "example": {
                "gpa": 16.5,
                "noteExamen": 85
            }
        }


class DonneesFianciales(BaseModel):
    """Données financières de l'étudiant"""
    revenu: float = Field(..., ge=0, description="Revenu familial annuel")
    dependants: int = Field(..., ge=0, le=15, description="Nombre de dépendants")

    class Config:
        json_schema_extra = {
            "example": {
                "revenu": 25000,
                "dependants": 3
            }
        }


class DonneesContextuelles(BaseModel):
    """Données contextuelles / géographiques"""
    distance: float = Field(..., ge=0, description="Distance à l'université (km)")

    class Config:
        json_schema_extra = {
            "example": {
                "distance": 50.5
            }
        }


class RequeteCapaciteFinanciere(BaseModel):
    """Requête de prédiction de capacité financière"""
    donnees_academiques: DonneesAcademiques
    donnees_financieres: DonneesFianciales


class RequeteRecommandationBourse(BaseModel):
    """Requête de recommandation de bourse"""
    donnees_academiques: DonneesAcademiques
    donnees_financieres: DonneesFianciales


class RequeteProabiliteInscription(BaseModel):
    """Requête de prédiction de probabilité d'inscription"""
    donnees_academiques: DonneesAcademiques
    donnees_financieres: DonneesFianciales
    donnees_contextuelles: DonneesContextuelles


class InscriptionEtudiant(BaseModel):
    """Données d'inscription d'un nouvel étudiant"""
    idEtudiant: Optional[str] = None
    prenom: str = Field(..., min_length=1, description="Prénom de l'étudiant")
    nom: str = Field(..., min_length=1, description="Nom de famille de l'étudiant")
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="Email unique de l'étudiant")
    password: str = Field(..., min_length=6, description="Mot de passe (minimum 6 caractères)")
    phone: Optional[str] = None
    address: Optional[str] = None
    annee: int = Field(..., ge=2020, le=2100, description="Année scolaire d'inscription")
    
    # Niveau d'étude
    niveau_etude: Literal["Baccalauréat", "Bac+2", "Bac+3", "Bac+4"] = Field(..., description="Niveau d'études")
    
    # Type de parrainage demandé
    type_sponsorship: Literal["Complète", "Partielle", "Moitié"] = Field(..., description="Type de parrainage demandé")
    
    # Données du Baccalauréat (obligatoire pour tous)
    donnees_baccalaureat: DonneesBaccalaureat
    
    # Données du Diplôme (optionnel pour Bac+2 et plus)
    donnees_diplome: Optional[DonneesDiplome] = None
    
    # Données financières et contextuelles
    donnees_financieres: DonneesFianciales
    donnees_contextuelles: DonneesContextuelles

    class Config:
        json_schema_extra = {
            "example": {
                "prenom": "Ahmed",
                "nom": "Hassan",
                "email": "ahmed@example.com",
                "password": "secure_password_123",
                "phone": "+212612345678",
                "address": "Casablanca, Morocco",
                "annee": 2024,
                "niveau_etude": "Baccalauréat",
                "donnees_baccalaureat": {
                    "notes_regionales": 16.5,
                    "note_generale": 17.0,
                    "option": "Maths"
                },
                "donnees_financieres": {
                    "revenu": 25000,
                    "dependants": 3
                },
                "donnees_contextuelles": {
                    "distance": 50.5
                }
            }
        }


class RequeteConnexionEtudiant(BaseModel):
    """Requête de connexion étudiant"""
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="Email de l'étudiant")
    password: str = Field(..., min_length=1, description="Mot de passe")


class ReponseConnexionEtudiant(BaseModel):
    """Réponse de connexion étudiant"""
    token: str
    etudiant: Dict[str, Any]


# ============================================================================
# MODÈLES DE RÉPONSE - Données retournées au client
# ============================================================================

class ReponseCapaciteFinanciere(BaseModel):
    """Réponse de prédiction de capacité financière"""
    scoreFinancier: float = Field(..., ge=0, le=100)
    message: str
    details: Optional[Dict[str, Any]] = None


class ReponseRecommandationBourse(BaseModel):
    """Réponse de recommandation de bourse"""
    typeBourse: str
    pourcentage: int = Field(..., ge=0, le=100)
    message: str
    details: Optional[Dict[str, Any]] = None


class ReponseProabiliteInscription(BaseModel):
    """Réponse de prédiction de probabilité d'inscription"""
    probabiliteInscription: str
    confiance: float = Field(..., ge=0, le=1)
    message: str
    details: Optional[Dict[str, Any]] = None


class ResultatEtudiant(BaseModel):
    """Résultat complet d'un étudiant"""
    idEtudiant: str
    prenom: str
    nom: str
    email: str
    annee: int
    dateCreation: datetime
    dateModification: datetime
    scoreFinancier: Optional[float] = None
    typeBourse: Optional[str] = None
    pourcentageBourse: Optional[int] = None
    probabiliteInscription: Optional[str] = None
    confianceInscription: Optional[float] = None


class StatistiquesSysteme(BaseModel):
    """Statistiques agrégées du système"""
    totalEtudiants: int
    totalTraites: int
    scoreMoyenFinancier: float
    confianceMoyenneInscription: float
    distributionBourses: Dict[str, int]
    distributionProbabilites: Dict[str, int]
    tauxTraitement: float
