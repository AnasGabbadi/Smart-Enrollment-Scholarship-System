"""
Endpoints d'authentification administrateur

Vérifie les identifiants côté serveur (contre ADMIN_EMAIL / ADMIN_PASSWORD
définis dans l'environnement) et émet un JWT signé en cas de succès.
"""
import secrets

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from config.parametres import ADMIN_EMAIL, ADMIN_PASSWORD, JWT_DUREE_VALIDITE_MINUTES
from utilitaires.securite import creer_jeton_acces

routeur_auth = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentification"]
)


class RequeteConnexionAdmin(BaseModel):
    """Requête de connexion administrateur"""
    email: str = Field(..., description="Email administrateur")
    password: str = Field(..., description="Mot de passe administrateur")


class ReponseConnexionAdmin(BaseModel):
    """Réponse de connexion administrateur"""
    token: str
    token_type: str = "bearer"
    role: str = "admin"
    expire_dans_minutes: int


@routeur_auth.post("/connexion", response_model=ReponseConnexionAdmin)
async def connexion_admin(requete: RequeteConnexionAdmin):
    """
    Authentifier un administrateur

    Compare les identifiants soumis à ADMIN_EMAIL / ADMIN_PASSWORD (variables
    d'environnement) avec une comparaison à temps constant, puis émet un JWT
    signé valable JWT_DUREE_VALIDITE_MINUTES minutes.

    Raises:
        HTTPException 401: Identifiants invalides ou non configurés
    """
    identifiants_configures = bool(ADMIN_EMAIL) and bool(ADMIN_PASSWORD)
    email_correct = identifiants_configures and secrets.compare_digest(requete.email, ADMIN_EMAIL)
    mot_de_passe_correct = identifiants_configures and secrets.compare_digest(requete.password, ADMIN_PASSWORD)

    if not (email_correct and mot_de_passe_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    token = creer_jeton_acces(sub=requete.email, role="admin")

    return ReponseConnexionAdmin(
        token=token,
        expire_dans_minutes=JWT_DUREE_VALIDITE_MINUTES
    )
