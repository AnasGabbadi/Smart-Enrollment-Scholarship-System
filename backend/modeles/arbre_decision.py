"""
Modèle Arbre de Décision pour recommandation de bourse

Classe les étudiants dans 4 catégories de bourses basées sur
leurs performances académiques et situation financière
"""
import logging
import os
import pickle
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from config.parametres import CHEMIN_MODELES_ENTRAINES

logger = logging.getLogger(__name__)


class ModeleArbreDecision:
    """
    Gestionnaire du modèle d'arbre de décision
    Recommande un type de bourse (0-3) basé sur les critères
    """
    
    def __init__(self):
        """Initialiser le modèle"""
        self.modele = None
        self.nom_fichier = "modele_arbre_decision.pkl"
        self.chemin_complet = os.path.join(CHEMIN_MODELES_ENTRAINES, self.nom_fichier)
        self._charger_modele()
    
    def _charger_modele(self):
        """Charger le modèle à partir du fichier"""
        try:
            if os.path.exists(self.chemin_complet):
                with open(self.chemin_complet, 'rb') as f:
                    self.modele = pickle.load(f)
                print(f"[✓] Modèle d'arbre de décision chargé")
            else:
                print(f"[⚠] Modèle non trouvé: {self.chemin_complet}")
                self._creer_modele_par_defaut()
        except Exception as e:
            print(f"[✗] Erreur lors du chargement du modèle: {e}")
            self._creer_modele_par_defaut()
    
    def _creer_modele_par_defaut(self):
        """Créer un modèle par défaut avec règles heuristiques"""
        self.modele = DecisionTreeClassifier(max_depth=3, random_state=42)
        # Créer des données synthétiques minimales pour initialiser
        X_dummy = np.array([
            [10, 50, 10000, 0, 20],      # GPA moyen, note_examen moyen, revenu moyen, pas de dépendants, distance faible
            [18, 80, 5000, 3, 50],       # Bon GPA, bonne note, revenu faible, plusieurs dépendants, distance moyenne
            [12, 60, 50000, 2, 10],      # GPA faible, note moyen, revenu élevé, dépendants, distance faible
            [15, 70, 15000, 1, 60]       # Bon GPA, bonne note, revenu moyen, dépendant, distance élevée
        ])
        y_dummy = np.array([1, 3, 0, 2])  # Classes
        try:
            self.modele.fit(X_dummy, y_dummy)
        except Exception as e:
            logger.warning(f"Échec de l'initialisation du modèle d'arbre de décision par défaut: {e}")
    
    def entraîner(self, X_train, y_train):
        """
        Entraîner le modèle
        
        Args:
            X_train: Données [GPA, Revenu, Dépendants]
            y_train: Classes [0, 1, 2, 3]
        """
        try:
            self.modele = DecisionTreeClassifier(max_depth=5, min_samples_split=10, min_samples_leaf=5)
            self.modele.fit(X_train, y_train)
            self._sauvegarder_modele()
            print("[✓] Modèle d'arbre de décision entraîné avec succès")
        except Exception as e:
            print(f"[✗] Erreur lors de l'entraînement: {e}")
    
    def predire(self, caracteristiques):
        """
        Prédire le type de bourse
        
        Args:
            caracteristiques: [GPA, NoteExamen, Revenu, Dépendants, Distance]
            
        Returns:
            int: Classe de bourse (0=aucune, 1=25%, 2=50%, 3=100%)
        """
        try:
            if self.modele is None:
                self._creer_modele_par_defaut()
            
            X = np.array(caracteristiques).reshape(1, -1)
            prediction = int(self.modele.predict(X)[0])
            
            # Constraindre entre 0 et 3
            return max(0, min(3, prediction))
        except Exception as e:
            print(f"[✗] Erreur lors de la prédiction: {e}")
            # Heuristique par défaut : GPA bon + revenu faible = bourse complète
            # Accepter 3 à 5 paramètres pour compatibilité
            try:
                if len(caracteristiques) >= 5:
                    gpa, note_examen, revenu, dependants, distance = caracteristiques[:5]
                elif len(caracteristiques) >= 3:
                    gpa = caracteristiques[0]
                    revenu = caracteristiques[1]
                    dependants = caracteristiques[2]
                    note_examen = 75  # Valeur par défaut
                    distance = 50  # Valeur par défaut
                else:
                    return 0  # Pas de bourse si données insuffisantes
            except Exception as e:
                logger.warning(f"Impossible d'extraire les caractéristiques pour la prédiction de secours: {e}")
                return 0
            
            # Logique de décision basée sur les critères académiques et financiers
            # Priorité: GPA élevé + revenu faible + dépendants = bourse complète
            gpa_score = (gpa / 20.0) * 100  # Normaliser GPA 0-20 à 0-100
            
            # Facteur financier: revenu plus bas = plus de besoin (plus haut score)
            financial_factor = max(0, (50000 - revenu) / 50000 * 100)
            
            # Facteur dépendants
            dependant_factor = min(dependants * 15, 60)
            
            # Score composite: 50% académique, 30% financier, 20% dépendants
            composite_score = (gpa_score * 0.50) + (financial_factor * 0.30) + (dependant_factor * 0.20)
            
            # Décision basée sur score composite
            if composite_score >= 80:
                return 3  # Bourse complète (100%)
            elif composite_score >= 60:
                return 2  # Bourse partielle (50%)
            elif composite_score >= 40:
                return 1  # Bourse réduite (25%)
            else:
                return 0  # Pas de bourse
    
    def _sauvegarder_modele(self):
        """Sauvegarder le modèle"""
        try:
            with open(self.chemin_complet, 'wb') as f:
                pickle.dump(self.modele, f)
            print(f"[✓] Modèle sauvegardé: {self.chemin_complet}")
        except Exception as e:
            print(f"[✗] Erreur lors de la sauvegarde: {e}")
    
    def obtenir_regles(self):
        """Extraire les règles du modèle"""
        try:
            from sklearn.tree import export_text
            if self.modele:
                return export_text(self.modele)
        except Exception as e:
            logger.warning(f"Impossible d'extraire les règles du modèle: {e}")
            return None


# Instance globale du modèle
modele_arbre = ModeleArbreDecision()
