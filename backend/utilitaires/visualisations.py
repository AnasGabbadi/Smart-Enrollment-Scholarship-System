"""
Module de visualisation des données et prédictions des modèles ML

Génère des graphiques pour analyser les performances et résultats
des modèles de prédiction du système d'admission
"""
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any
import os
from datetime import datetime
from config.parametres import CHEMIN_DONNEES


class VisualiseurModeles:
    """
    Classe pour générer des visualisations des modèles et données
    """
    
    def __init__(self):
        """Initialiser le visualiseur"""
        self.chemin_graphiques = os.path.join(CHEMIN_DONNEES, "graphiques")
        os.makedirs(self.chemin_graphiques, exist_ok=True)
        # Utiliser un style professionnel
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def visualiser_distribution_capacite_financiere(self, scores: List[float], nom_fichier: str = None) -> str:
        """
        Visualiser la distribution des scores de capacité financière
        
        Args:
            scores: Liste des scores de capacité financière (0-100)
            nom_fichier: Nom du fichier de sortie (optionnel)
            
        Returns:
            str: Chemin du fichier généré
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogramme
        ax1.hist(scores, bins=20, color='steelblue', edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Score de Capacité Financière', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Nombre d\'étudiants', fontsize=12, fontweight='bold')
        ax1.set_title('Distribution des Scores de Capacité Financière', fontsize=14, fontweight='bold')
        ax1.axvline(np.mean(scores), color='red', linestyle='--', linewidth=2, label=f'Moyenne: {np.mean(scores):.2f}')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Boîte à moustaches
        ax2.boxplot(scores, vert=True)
        ax2.set_ylabel('Score de Capacité Financière', fontsize=12, fontweight='bold')
        ax2.set_title('Boîte à Moustaches - Capacité Financière', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Sauvegarder le graphique
        if nom_fichier is None:
            nom_fichier = f"capacite_financiere_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        chemin_fichier = os.path.join(self.chemin_graphiques, nom_fichier)
        plt.savefig(chemin_fichier, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chemin_fichier
    
    def visualiser_distribution_bourses(self, recommandations: Dict[str, int], nom_fichier: str = None) -> str:
        """
        Visualiser la distribution des recommandations de bourses
        
        Args:
            recommandations: Dict avec types de bourses et leurs comptes
            nom_fichier: Nom du fichier de sortie (optionnel)
            
        Returns:
            str: Chemin du fichier généré
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        types = list(recommandations.keys())
        counts = list(recommandations.values())
        couleurs = ['#ff9999', '#ffcc99', '#99ccff', '#99ff99']
        
        # Diagramme circulaire
        ax1.pie(counts, labels=types, autopct='%1.1f%%', startangle=90,
                colors=couleurs[:len(types)], explode=[0.05]*len(types))
        ax1.set_title('Distribution des Recommandations de Bourses', fontsize=14, fontweight='bold')
        
        # Diagramme en barres
        ax2.bar(types, counts, color=couleurs[:len(types)], edgecolor='black', alpha=0.7)
        ax2.set_xlabel('Type de Bourse', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Nombre d\'étudiants', fontsize=12, fontweight='bold')
        ax2.set_title('Nombre d\'étudiants par Type de Bourse', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Sauvegarder le graphique
        if nom_fichier is None:
            nom_fichier = f"distribution_bourses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        chemin_fichier = os.path.join(self.chemin_graphiques, nom_fichier)
        plt.savefig(chemin_fichier, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chemin_fichier
    
    def visualiser_probabilites_inscription(self, probabilites: Dict[str, int], nom_fichier: str = None) -> str:
        """
        Visualiser la distribution des probabilités d'inscription
        
        Args:
            probabilites: Dict avec niveaux (Faible/Moyen/Fort) et comptes
            nom_fichier: Nom du fichier de sortie (optionnel)
            
        Returns:
            str: Chemin du fichier généré
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        niveaux = list(probabilites.keys())
        counts = list(probabilites.values())
        couleurs = ['#ff6b6b', '#ffd93d', '#6bcf7f']
        
        # Diagramme en barres avec gradient
        bars = ax.bar(niveaux, counts, color=couleurs, edgecolor='black', alpha=0.8, linewidth=2)
        
        # Ajouter les valeurs sur les barres
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        ax.set_xlabel('Niveau de Probabilité d\'Inscription', fontsize=12, fontweight='bold')
        ax.set_ylabel('Nombre d\'étudiants', fontsize=12, fontweight='bold')
        ax.set_title('Distribution des Probabilités d\'Inscription', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        # Sauvegarder le graphique
        if nom_fichier is None:
            nom_fichier = f"probabilites_inscription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        chemin_fichier = os.path.join(self.chemin_graphiques, nom_fichier)
        plt.savefig(chemin_fichier, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chemin_fichier
    
    def visualiser_correlation_variables(self, donnees: List[Dict[str, float]], nom_fichier: str = None) -> str:
        """
        Visualiser la corrélation entre les variables académiques et financières
        
        Args:
            donnees: Liste de dictionnaires avec gpa, noteExamen, revenu, dependants
            nom_fichier: Nom du fichier de sortie (optionnel)
            
        Returns:
            str: Chemin du fichier généré
        """
        if not donnees:
            return None
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        gpa_list = [d.get('gpa', 0) for d in donnees]
        notes_list = [d.get('noteExamen', 0) for d in donnees]
        revenu_list = [d.get('revenu', 0) for d in donnees]
        dependants_list = [d.get('dependants', 0) for d in donnees]
        
        # GPA vs Note d'Examen
        axes[0, 0].scatter(gpa_list, notes_list, alpha=0.6, s=50, color='steelblue')
        axes[0, 0].set_xlabel('GPA', fontweight='bold')
        axes[0, 0].set_ylabel('Note d\'Examen', fontweight='bold')
        axes[0, 0].set_title('GPA vs Note d\'Examen', fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # GPA vs Revenu
        axes[0, 1].scatter(gpa_list, revenu_list, alpha=0.6, s=50, color='coral')
        axes[0, 1].set_xlabel('GPA', fontweight='bold')
        axes[0, 1].set_ylabel('Revenu (€)', fontweight='bold')
        axes[0, 1].set_title('GPA vs Revenu', fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Revenu vs Dépendants
        axes[1, 0].scatter(revenu_list, dependants_list, alpha=0.6, s=50, color='mediumseagreen')
        axes[1, 0].set_xlabel('Revenu (€)', fontweight='bold')
        axes[1, 0].set_ylabel('Nombre de Dépendants', fontweight='bold')
        axes[1, 0].set_title('Revenu vs Dépendants', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Distribution des revenus
        axes[1, 1].hist(revenu_list, bins=15, color='mediumpurple', edgecolor='black', alpha=0.7)
        axes[1, 1].set_xlabel('Revenu (€)', fontweight='bold')
        axes[1, 1].set_ylabel('Fréquence', fontweight='bold')
        axes[1, 1].set_title('Distribution des Revenus', fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        # Sauvegarder le graphique
        if nom_fichier is None:
            nom_fichier = f"correlation_variables_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        chemin_fichier = os.path.join(self.chemin_graphiques, nom_fichier)
        plt.savefig(chemin_fichier, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chemin_fichier
    
    def visualiser_performance_modele(self, metriques: Dict[str, float], nom_modele: str, nom_fichier: str = None) -> str:
        """
        Visualiser les métriques de performance d'un modèle
        
        Args:
            metriques: Dict avec noms de métriques et leurs valeurs
            nom_modele: Nom du modèle
            nom_fichier: Nom du fichier de sortie (optionnel)
            
        Returns:
            str: Chemin du fichier généré
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        noms = list(metriques.keys())
        valeurs = list(metriques.values())
        couleurs = plt.cm.viridis(np.linspace(0, 1, len(noms)))
        
        bars = ax.barh(noms, valeurs, color=couleurs, edgecolor='black', alpha=0.8)
        
        # Ajouter les valeurs sur les barres
        for i, bar in enumerate(bars):
            ax.text(valeurs[i], bar.get_y() + bar.get_height()/2.,
                   f'{valeurs[i]:.3f}',
                   ha='left', va='center', fontweight='bold', fontsize=10, 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
        
        ax.set_xlabel('Score', fontsize=12, fontweight='bold')
        ax.set_title(f'Métriques de Performance - {nom_modele}', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 1.1)
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        # Sauvegarder le graphique
        if nom_fichier is None:
            nom_fichier = f"performance_{nom_modele.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        chemin_fichier = os.path.join(self.chemin_graphiques, nom_fichier)
        plt.savefig(chemin_fichier, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chemin_fichier


# Instance globale du visualiseur
visualiseur = VisualiseurModeles()
