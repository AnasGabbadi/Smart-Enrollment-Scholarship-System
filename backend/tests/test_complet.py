"""
Script de test complet pour le système d'admission
Teste tous les endpoints et affiche un rapport détaillé
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
COULEURS = {
    'SUCCES': '\033[92m',      # Vert
    'ERREUR': '\033[91m',      # Rouge
    'AVERTISSEMENT': '\033[93m', # Jaune
    'INFO': '\033[94m',        # Bleu
    'RESET': '\033[0m'         # Reset
}

def afficher(message, type_msg='INFO'):
    """Afficher un message avec couleur"""
    couleur = COULEURS.get(type_msg, COULEURS['INFO'])
    print(f"{couleur}{message}{COULEURS['RESET']}")

class TesteurAPI:
    """Testeur pour tous les endpoints de l'API"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.resultats = []
        self.debut = time.time()
    
    def test_endpoint(self, nom, methode, endpoint, data=None, code_attendu=200):
        """
        Tester un endpoint
        
        Args:
            nom: Nom du test
            methode: GET, POST, etc.
            endpoint: Chemin de l'endpoint
            data: Données (pour POST)
            code_attendu: Code HTTP attendu
        """
        try:
            url = f"{self.base_url}{endpoint}"
            
            if methode == "GET":
                response = requests.get(url)
            elif methode == "POST":
                response = requests.post(url, json=data)
            else:
                raise ValueError(f"Méthode inconnue: {methode}")
            
            succes = response.status_code == code_attendu
            
            self.resultats.append({
                'nom': nom,
                'succes': succes,
                'status': response.status_code,
                'attendu': code_attendu,
                'temps': response.elapsed.total_seconds() * 1000
            })
            
            couleur = 'SUCCES' if succes else 'ERREUR'
            emoji = '✓' if succes else '✗'
            afficher(f"  {emoji} {nom}: {response.status_code}", couleur)
            
            return response
        except Exception as e:
            self.resultats.append({
                'nom': nom,
                'succes': False,
                'erreur': str(e)
            })
            afficher(f"  ✗ {nom}: EXCEPTION - {e}", 'ERREUR')
            return None
    
    def afficher_rapport(self):
        """Afficher le rapport final des tests"""
        total = len(self.resultats)
        reussis = sum(1 for r in self.resultats if r['succes'])
        echoues = total - reussis
        temps_total = time.time() - self.debut
        
        print("\n" + "=" * 70)
        afficher("RAPPORT DES TESTS", 'INFO')
        print("=" * 70)
        
        afficher(f"\nDate: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 'INFO')
        afficher(f"Durée totale: {temps_total:.2f}s", 'INFO')
        
        print(f"\nRésumé:")
        afficher(f"  Total: {total}", 'INFO')
        afficher(f"  Réussis: {reussis}", 'SUCCES')
        if echoues > 0:
            afficher(f"  Échoués: {echoues}", 'ERREUR')
        
        if echoues == 0 and total > 0:
            afficher(f"\n✓ TOUS LES TESTS SONT PASSÉS!", 'SUCCES')
        else:
            afficher(f"\n✗ {echoues} test(s) ont échoué", 'ERREUR')
        
        print("\nDétails par test:")
        for r in self.resultats:
            if 'temps' in r:
                status_ligne = f"[{r['status']}] ({r['temps']:.2f}ms)"
            else:
                status_ligne = "[ERREUR]"
            
            couleur = 'SUCCES' if r['succes'] else 'ERREUR'
            afficher(f"  {r['nom']}: {status_ligne}", couleur)
        
        print("\n" + "=" * 70)
        return echoues == 0


def main():
    """Exécuter la suite de tests complète"""
    
    print("=" * 70)
    afficher("TESTS COMPLETS - SYSTÈME D'ADMISSION INTELLIGENT", 'INFO')
    print("=" * 70)
    
    testeur = TesteurAPI(BASE_URL)
    
    # ========================================================================
    # TESTS DES ENDPOINTS DE BASE
    # ========================================================================
    
    print("\n[SECTION 1] Endpoints de base")
    print("-" * 70)
    
    testeur.test_endpoint(
        "Endpoint racine",
        "GET",
        "/",
        code_attendu=200
    )
    
    testeur.test_endpoint(
        "Vérification santé",
        "GET",
        "/sante",
        code_attendu=200
    )
    
    # ========================================================================
    # TESTS DES PRÉDICTIONS
    # ========================================================================
    
    print("\n[SECTION 2] Prédictions ML")
    print("-" * 70)
    
    # Prédiction capacité financière
    testeur.test_endpoint(
        "Capacité financière",
        "POST",
        "/api/v1/predictions/capacite-financiere",
        {
            "gpa": 16,
            "examScore": 85,
            "income": 2500,
            "dependents": 2
        },
        code_attendu=200
    )
    
    # Recommandation bourse
    testeur.test_endpoint(
        "Recommandation bourse",
        "POST",
        "/api/v1/predictions/recommandation-bourse",
        {
            "gpa": 16,
            "examScore": 85,
            "income": 2500,
            "dependents": 2,
            "distance": 50
        },
        code_attendu=200
    )
    
    # Probabilité inscription
    testeur.test_endpoint(
        "Probabilité inscription",
        "POST",
        "/api/v1/predictions/probabilite-inscription",
        {
            "gpa": 16,
            "examScore": 85,
            "income": 2500,
            "dependents": 2,
            "distanceToSchool": 50
        },
        code_attendu=200
    )
    
    # ========================================================================
    # TESTS DE GESTION DES ÉTUDIANTS
    # ========================================================================
    
    print("\n[SECTION 3] Gestion des étudiants")
    print("-" * 70)
    
    # Lister les étudiants
    testeur.test_endpoint(
        "Lister étudiants",
        "GET",
        "/api/v1/etudiants",
        code_attendu=200
    )
    
    # Enregistrer un étudiant
    response = testeur.test_endpoint(
        "Enregistrer étudiant",
        "POST",
        "/api/v1/etudiants/enregistrer",
        {
            "prenom": "Test",
            "nom": "Étudiant",
            "email": "test@example.com",
            "donnees_academiques": {
                "gpa": 15,
                "noteExamen": 80
            },
            "donnees_financieres": {
                "revenu": 30000,
                "dependants": 2
            },
            "donnees_contextuelles": {
                "distance": 45
            }
        },
        code_attendu=200
    )
    
    # ========================================================================
    # TESTS DES ERREURS DE VALIDATION
    # ========================================================================
    
    print("\n[SECTION 4] Validation des données")
    print("-" * 70)
    
    # GPA invalide
    testeur.test_endpoint(
        "GPA invalide (>20)",
        "POST",
        "/api/v1/predictions/capacite-financiere",
        {
            "gpa": 25,  # Invalide
            "examScore": 85,
            "income": 2500,
            "dependents": 2
        },
        code_attendu=422
    )
    
    # Paramètres manquants
    testeur.test_endpoint(
        "Paramètres manquants",
        "POST",
        "/api/v1/predictions/capacite-financiere",
        {
            "gpa": 16
            # Manquent: examScore, income, dependents
        },
        code_attendu=422
    )
    
    # ========================================================================
    # AFFICHER LE RAPPORT
    # ========================================================================
    
    succes = testeur.afficher_rapport()
    
    return 0 if succes else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
