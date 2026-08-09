"""
Utilitaires de sécurité : émission et vérification des tokens JWT,
et dépendances FastAPI pour protéger les endpoints d'administration
"""
import logging
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config.parametres import JWT_SECRET_KEY, JWT_ALGORITHME, JWT_DUREE_VALIDITE_MINUTES

logger = logging.getLogger(__name__)

_schema_bearer = HTTPBearer(auto_error=False)


def creer_jeton_acces(sub: str, role: str) -> str:
    """
    Créer un JWT signé pour un utilisateur authentifié

    Args:
        sub: Identifiant du sujet (ici l'email de l'administrateur)
        role: Rôle de l'utilisateur (ex: "admin")

    Returns:
        str: Le token JWT encodé
    """
    expiration = datetime.utcnow() + timedelta(minutes=JWT_DUREE_VALIDITE_MINUTES)
    charge_utile = {"sub": sub, "role": role, "exp": expiration}
    return jwt.encode(charge_utile, JWT_SECRET_KEY, algorithm=JWT_ALGORITHME)


def obtenir_utilisateur_courant(
    identifiants: HTTPAuthorizationCredentials = Depends(_schema_bearer)
) -> dict:
    """
    Dépendance FastAPI : décode et valide le JWT présenté dans l'en-tête
    Authorization: Bearer <token>

    Raises:
        HTTPException 401: Si le token est absent, invalide ou expiré
    """
    if identifiants is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return jwt.decode(identifiants.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHME])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expirée, veuillez vous reconnecter",
        )
    except jwt.InvalidTokenError:
        logger.warning("Tentative d'authentification avec un token JWT invalide")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
        )


def exiger_role_admin(utilisateur: dict = Depends(obtenir_utilisateur_courant)) -> dict:
    """
    Dépendance FastAPI : vérifie que l'utilisateur authentifié a le rôle admin

    Raises:
        HTTPException 401: Hérité de obtenir_utilisateur_courant
        HTTPException 403: Si le token est valide mais le rôle n'est pas admin
    """
    if utilisateur.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs",
        )
    return utilisateur
