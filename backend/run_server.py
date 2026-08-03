#!/usr/bin/env python
"""
Script de démarrage du serveur FastAPI

Lance le serveur FastAPI du Système Intelligent d'Admission
en mode production (sans rechargement automatique)
"""
import uvicorn
import sys

if __name__ == "__main__":
    print("=" * 70)
    print("Demarrage du Systeme Intelligent d'Admission et d'Attribution de Bourses")
    print("=" * 70)
    print("Documentation: http://localhost:8000/docs")
    print("ReDoc: http://localhost:8000/redoc")
    print("=" * 70)
    print()
    
    try:
        # Lancer le serveur uvicorn SANS rechargement automatique
        uvicorn.run(
            "application:application",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\nArrêt du serveur...")
        sys.exit(0)
    except Exception as e:
        print(f"\nErreur lors du démarrage du serveur: {e}")
        sys.exit(1)

