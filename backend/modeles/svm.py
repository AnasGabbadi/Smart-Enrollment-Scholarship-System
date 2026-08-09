"""
Modèle SGD (Stochastic Gradient Descent) pour classification de probabilité d'inscription
Remplace SVM qui a des problèmes de Fortran sur Windows

Classifie les étudiants en 3 catégories de probabilité d'inscription:
- Faible (0): probabilité 0-33%
- Moyenne (1): probabilité 33-67%
- Forte (2): probabilité 67-100%

Avantages du SGDClassifier:
- Pas de dépendances Fortran (compatible Windows)
- Très efficace sur les gros datasets (>100k samples)
- Pas de timeout ou erreur de mémoire
"""
import logging
import os
import pickle
import numpy as np
from sklearn.linear_model import SGDClassifier
from config.parametres import CHEMIN_MODELES_ENTRAINES

logger = logging.getLogger(__name__)


class ModeleSVM:
    """
    Gestionnaire du modèle pour prédiction de probabilité d'inscription
    Utilise SGDClassifier pour efficacité sur gros datasets
    """
    
    def __init__(self):
        """Initialiser le modèle"""
        self.modele = None
        self.nom_fichier = "modele_svm.pkl"
        self.chemin_complet = os.path.join(CHEMIN_MODELES_ENTRAINES, self.nom_fichier)
        self._charger_modele()
    
    def _charger_modele(self):
        """Charger le modèle à partir du fichier"""
        try:
            if os.path.exists(self.chemin_complet):
                with open(self.chemin_complet, 'rb') as f:
                    self.modele = pickle.load(f)
                print(f"[✓] Modèle SGD chargé")
            else:
                print(f"[⚠] Modèle non trouvé: {self.chemin_complet}")
                self._creer_modele_par_defaut()
        except Exception as e:
            print(f"[✗] Erreur lors du chargement du modèle: {e}")
            self._creer_modele_par_defaut()
    
    def _creer_modele_par_defaut(self):
        """Créer un modèle par défaut avec données minimales"""
        self.modele = SGDClassifier(loss='hinge', n_jobs=-1, random_state=42, n_iter_no_change=10, warm_start=False)
        # Données synthétiques pour initialisation avec 5 features: [gpa, note_examen, revenu, dependants, distance]
        X_dummy = np.array([
            [18, 90, 5000, 1, 10],     # Fort, haute proba
            [18, 85, 5000, 0, 20],     # Fort, haute proba
            [12, 70, 30000, 2, 50],    # Moyen, proba moyenne
            [10, 60, 50000, 3, 80],    # Faible, basse proba
            [10, 50, 100000, 5, 100]   # Faible, très basse proba
        ])
        y_dummy = np.array([2, 2, 1, 0, 0])
        try:
            self.modele.fit(X_dummy, y_dummy)
        except Exception as e:
            logger.warning(f"Échec de l'initialisation du modèle SVM par défaut: {e}")
    
    def entraîner(self, X_train, y_train):
        """
        Entraîner le modèle avec SGDClassifier
        
        Args:
            X_train: Données [GPA, NoteExamen, Revenu, Distance]
            y_train: Classes [0, 1, 2]
        """
        try:
            self.modele = SGDClassifier(
                loss='hinge',
                n_jobs=-1,
                random_state=42,
                n_iter_no_change=10,
                warm_start=False
            )
            self.modele.fit(X_train, y_train)
            self._sauvegarder_modele()
            print("[✓] Modèle SGD entraîné avec succès")
        except Exception as e:
            print(f"[✗] Erreur lors de l'entraînement: {e}")
    
    def predire(self, caracteristiques):
        """
        Prédire la probabilité d'inscription
        
        Args:
            caracteristiques: [GPA, NoteExamen, Revenu, Dependants, Distance]
            
        Returns:
            dict: {'classe': int, 'confiance': float}
                - classe: 0=faible, 1=moyen, 2=fort
                - confiance: score de confiance (0-1)
        """
        try:
            if self.modele is None:
                self._creer_modele_par_defaut()
            
            X = np.array(caracteristiques).reshape(1, -1)
            classe = int(self.modele.predict(X)[0])
            
            # Obtenir les probabilités pour calculer la confiance
            if hasattr(self.modele, 'predict_proba'):
                probabilites = self.modele.predict_proba(X)[0]
                confiance = float(np.max(probabilites))
            else:
                # Si probability=False, utiliser une distance relative
                confiance = 0.6
            
            return {
                'classe': max(0, min(2, classe)),
                'confiance': min(1.0, confiance)
            }
        except Exception as e:
            print(f"[✗] Erreur lors de la prédiction: {e}")
            # Heuristique par défaut - accepter 4 ou 5 paramètres
            try:
                if len(caracteristiques) >= 5:
                    gpa, note_exam, revenu, dependants, distance = caracteristiques[:5]
                elif len(caracteristiques) >= 4:
                    gpa, note_exam, revenu, distance = caracteristiques[:4]
                    dependants = 1  # Valeur par défaut
                else:
                    return {'classe': 1, 'confiance': 0.5}
            except Exception as e:
                logger.warning(f"Impossible d'extraire les caractéristiques pour la prédiction de secours: {e}")
                return {'classe': 1, 'confiance': 0.5}
            
            score_complet = (gpa/20) * 40 + (note_exam/100) * 30 - (revenu/100000) * 20 - (distance/200) * 10
            
            if score_complet >= 60:
                return {'classe': 2, 'confiance': 0.8}
            elif score_complet >= 40:
                return {'classe': 1, 'confiance': 0.65}
            else:
                return {'classe': 0, 'confiance': 0.5}
    
    def _sauvegarder_modele(self):
        """Sauvegarder le modèle"""
        try:
            with open(self.chemin_complet, 'wb') as f:
                pickle.dump(self.modele, f)
            print(f"[✓] Modèle sauvegardé: {self.chemin_complet}")
        except Exception as e:
            print(f"[✗] Erreur lors de la sauvegarde: {e}")
    
    def obtenir_vecteurs_support(self):
        """Retourner le nombre de vecteurs de support"""
        if self.modele and hasattr(self.modele, 'n_support_'):
            return int(np.sum(self.modele.n_support_))
        return None


# Instance globale du modèle
modele_svm = ModeleSVM()
