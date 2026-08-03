"""
Modèle de Régression Linéaire pour prédiction de capacité financière

Prédit un score numérique (0-100) représentant la capacité financière
de l'étudiant basé sur ses informations académiques et financières
"""
import os
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from config.parametres import CHEMIN_MODELES_ENTRAINES


class ModeleRegressionLineaire:
    """
    Gestionnaire du modèle de régression linéaire
    Entraîne et utilise le modèle pour prédire la capacité financière
    """
    
    def __init__(self):
        """Initialiser le modèle"""
        self.modele = None
        self.nom_fichier = "modele_regression_lineaire.pkl"
        self.chemin_complet = os.path.join(CHEMIN_MODELES_ENTRAINES, self.nom_fichier)
        self._charger_modele()
    
    def _charger_modele(self):
        """
        Charger le modèle à partir du fichier de sauvegarde
        Si le fichier n'existe pas, créer un modèle par défaut
        """
        try:
            if os.path.exists(self.chemin_complet):
                with open(self.chemin_complet, 'rb') as f:
                    self.modele = pickle.load(f)
                print(f"[✓] Modèle de régression linéaire chargé")
            else:
                print(f"[⚠] Modèle non trouvé: {self.chemin_complet}")
                self._creer_modele_par_defaut()
        except Exception as e:
            print(f"[✗] Erreur lors du chargement du modèle: {e}")
            self._creer_modele_par_defaut()
    
    def _creer_modele_par_defaut(self):
        """Créer un modèle par défaut avec des coefficients simples"""
        self.modele = LinearRegression()
        # Coefficients arbitraires pour les prédictions en l'absence d'entraînement
        # Pour 5 features: [GPA, NoteExamen, Revenu, Dépendants, Distance]
        self.modele.coef_ = np.array([5.0, 0.3, -0.0001, -3.0, -0.05])
        self.modele.intercept_ = 40.0
    
    def entraîner(self, X_train, y_train):
        """
        Entraîner le modèle avec des données
        
        Args:
            X_train: Données d'entraînement (caractéristiques)
            y_train: Cibles d'entraînement (scores)
        """
        try:
            self.modele = LinearRegression()
            self.modele.fit(X_train, y_train)
            self._sauvegarder_modele()
            print("[✓] Modèle de régression linéaire entraîné avec succès")
        except Exception as e:
            print(f"[✗] Erreur lors de l'entraînement: {e}")
    
    def predire(self, caracteristiques):
        """
        Prédire la capacité financière
        
        Args:
            caracteristiques: Liste [GPA, NoteExamen, Revenu, Dépendants, Distance]
            
        Returns:
            float: Score entre 0 et 100
        """
        try:
            if self.modele is None:
                self._creer_modele_par_defaut()
            
            # Transformer en array et redimensionner
            X = np.array(caracteristiques).reshape(1, -1)
            prediction = self.modele.predict(X)[0]
            
            # Constraindre la prédiction entre 0 et 100
            return max(0, min(100, prediction))
        except Exception as e:
            print(f"[✗] Erreur lors de la prédiction: {e}")
            return 50.0  # Valeur par défaut
    
    def _sauvegarder_modele(self):
        """Sauvegarder le modèle dans un fichier"""
        try:
            with open(self.chemin_complet, 'wb') as f:
                pickle.dump(self.modele, f)
            print(f"[✓] Modèle sauvegardé: {self.chemin_complet}")
        except Exception as e:
            print(f"[✗] Erreur lors de la sauvegarde: {e}")
    
    def obtenir_coefficients(self):
        """Retourner les coefficients du modèle"""
        if self.modele:
            return {
                "coefficients": self.modele.coef_.tolist(),
                "intercept": float(self.modele.intercept_)
            }
        return None


# Instance globale du modèle
modele_regression = ModeleRegressionLineaire()
