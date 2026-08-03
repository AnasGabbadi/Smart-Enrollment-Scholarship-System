"""
Générateur de Diagrammes PNG pour la Documentation
Crée tous les diagrammes du système en format PNG
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
import numpy as np
import os

# Configuration de style
plt.style.use('seaborn-v0_8-darkgrid')
OUTPUT_DIR = "diagrammes"

def save_figure(filename, fig, dpi=300):
    """Sauvegarder une figure en PNG"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f"✓ Diagramme créé: {filename}")
    plt.close(fig)

# ============================================================================
# 1. ARCHITECTURE GÉNÉRALE DU SYSTÈME
# ============================================================================
def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Titre
    ax.text(5, 9.5, 'Architecture Système Complet', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Frontend
    frontend_box = FancyBboxPatch((0.5, 6.5), 2.5, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  edgecolor='#2E86AB', facecolor='#A7C6DA', linewidth=2)
    ax.add_patch(frontend_box)
    ax.text(1.75, 7.5, 'Frontend React', fontsize=12, fontweight='bold', ha='center')
    ax.text(1.75, 7.15, 'Port 3000', fontsize=10, ha='center')
    ax.text(1.75, 6.85, '• Admin Dashboard\n• Student Portal', fontsize=8, ha='center')
    
    # Backend
    backend_box = FancyBboxPatch((4, 6.5), 2.5, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 edgecolor='#A23B72', facecolor='#F18F01', linewidth=2)
    ax.add_patch(backend_box)
    ax.text(5.25, 7.5, 'Backend FastAPI', fontsize=12, fontweight='bold', ha='center')
    ax.text(5.25, 7.15, 'Port 8000', fontsize=10, ha='center')
    ax.text(5.25, 6.85, '• API REST\n• ML Ranking', fontsize=8, ha='center')
    
    # MongoDB
    db_box = FancyBboxPatch((7.5, 6.5), 2, 1.5, 
                           boxstyle="round,pad=0.1", 
                           edgecolor='#13A538', facecolor='#90EE90', linewidth=2)
    ax.add_patch(db_box)
    ax.text(8.5, 7.5, 'MongoDB', fontsize=12, fontweight='bold', ha='center')
    ax.text(8.5, 7.15, 'Base Données', fontsize=10, ha='center')
    ax.text(8.5, 6.85, '• Students\n• Rankings', fontsize=8, ha='center')
    
    # Flèches
    arrow1 = FancyArrowPatch((3, 7.25), (4, 7.25), 
                            arrowstyle='<->', mutation_scale=30, 
                            color='black', linewidth=2)
    ax.add_patch(arrow1)
    
    arrow2 = FancyArrowPatch((6.5, 7.25), (7.5, 7.25), 
                            arrowstyle='<->', mutation_scale=30, 
                            color='black', linewidth=2)
    ax.add_patch(arrow2)
    
    # ML Models
    ml_box = FancyBboxPatch((1.5, 4), 7, 1.8, 
                           boxstyle="round,pad=0.1", 
                           edgecolor='#6A4C93', facecolor='#D7BFF4', linewidth=2)
    ax.add_patch(ml_box)
    ax.text(5, 5.4, 'Moteur ML (3 Modèles)', fontsize=12, fontweight='bold', ha='center')
    ax.text(5, 4.9, 'Régression Linéaire  •  Arbre de Décision  •  SVM', 
            fontsize=9, ha='center')
    ax.text(5, 4.5, 'Classement & Prédictions', fontsize=9, ha='center', style='italic')
    
    # Flèche Backend vers ML
    arrow3 = FancyArrowPatch((5.25, 6.5), (5.25, 5.8), 
                            arrowstyle='<->', mutation_scale=25, 
                            color='black', linewidth=2)
    ax.add_patch(arrow3)
    
    # Processus de traitement
    ax.text(5, 3.2, 'Flux de Données', fontsize=11, fontweight='bold', ha='center')
    
    steps = [
        '1. Extraction Features',
        '2. Score 3 Modèles',
        '3. Identification Consensus',
        '4. Classement Fusionné',
        '5. Respect Quota'
    ]
    
    y_pos = 2.8
    for step in steps:
        ax.text(5, y_pos, step, fontsize=9, ha='center', 
               bbox=dict(boxstyle='round', facecolor='#FFE5B4', alpha=0.7))
        y_pos -= 0.35
    
    save_figure('01_architecture_system.png', fig)

# ============================================================================
# 2. FLUX DE DONNÉES - CLASSEMENT ÉTUDIANTS
# ============================================================================
def create_data_flow_diagram():
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    ax.text(5, 13.5, 'Flux de Données - Classement Étudiants', 
            fontsize=16, fontweight='bold', ha='center')
    
    boxes = [
        (5, 12.5, 'Étudiant Candidat\n(Status = En attente)', '#FFB6C1'),
        (5, 11.3, 'Extraction des Features\n(GPA, Note, Revenu, Dépendants, Distance)', '#FFE5B4'),
        (2, 10, 'Modèle 1\nRégression Linéaire', '#A7C6DA'),
        (5, 10, 'Modèle 2\nArbre de Décision', '#F18F01'),
        (8, 10, 'Modèle 3\nSVM', '#D7BFF4'),
        (2, 8.5, 'Score 1\n(0-100)', '#A7C6DA'),
        (5, 8.5, 'Score 2\n(0-100)', '#F18F01'),
        (8, 8.5, 'Score 3\n(0-100)', '#D7BFF4'),
        (5, 7.2, 'Vérification Consensus\n(Les 3 modèles sont d\'accord?)', '#FFE5B4'),
        (3, 5.8, 'Consensus\n(Haute confiance)', '#90EE90'),
        (7, 5.8, 'Non-Consensus\n(Score moyen)', '#FFA07A'),
        (5, 4.5, 'Classement Fusionné\n(Score moyen des 3 modèles)\nRespect Quota annuel', '#FFE5B4'),
        (5, 2.8, 'Résultats Finaux\nTop N candidats + Consensus List', '#90EE90'),
    ]
    
    for x, y, label, color in boxes:
        width = 2.5 if len(label) < 15 else 3
        height = 0.8
        box = FancyBboxPatch((x-width/2, y-height/2), width, height, 
                            boxstyle="round,pad=0.05", 
                            edgecolor='black', facecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Flèches de connexion
    arrows = [
        (5, 12.1, 5, 11.7),  # Étudiant vers Features
        (5, 10.9, 2, 10.4),  # Features vers Model1
        (5, 10.9, 5, 10.4),  # Features vers Model2
        (5, 10.9, 8, 10.4),  # Features vers Model3
        (2, 9.6, 2, 8.9),    # Model1 vers Score1
        (5, 9.6, 5, 8.9),    # Model2 vers Score2
        (8, 9.6, 8, 8.9),    # Model3 vers Score3
        (2, 8.1, 4, 7.6),    # Score1 vers Consensus
        (5, 8.1, 5, 7.6),    # Score2 vers Consensus
        (8, 8.1, 6, 7.6),    # Score3 vers Consensus
        (4, 6.8, 3, 6.2),    # Consensus vers branches
        (6, 6.8, 7, 6.2),    # Consensus vers branches
        (3, 5.4, 5, 4.9),    # Consensus vers Fusion
        (7, 5.4, 5, 4.9),    # Non-Consensus vers Fusion
        (5, 4.1, 5, 3.2),    # Fusion vers Résultats
    ]
    
    for x1, y1, x2, y2 in arrows:
        arrow = FancyArrowPatch((x1, y1), (x2, y2), 
                               arrowstyle='->', mutation_scale=20, 
                               color='black', linewidth=1.5)
        ax.add_patch(arrow)
    
    save_figure('02_flux_donnees.png', fig)

# ============================================================================
# 3. RÉGRESSION LINÉAIRE
# ============================================================================
def create_linear_regression_diagram():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(7, 9.5, 'Modèle 1: Régression Linéaire', 
            fontsize=16, fontweight='bold', ha='center')
    
    # Input Features
    features = ['GPA', 'Note\nExamen', 'Revenu', 'Dépendants', 'Distance']
    x_start = 1
    for i, feature in enumerate(features):
        circle = Circle((x_start + i*2, 8), 0.4, color='#A7C6DA', ec='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x_start + i*2, 8, feature, fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Processing box
    process_box = FancyBboxPatch((2, 5.5), 10, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 edgecolor='#6A4C93', facecolor='#D7BFF4', linewidth=2)
    ax.add_patch(process_box)
    ax.text(7, 6.5, 'Poids Appris', fontsize=11, fontweight='bold', ha='center')
    ax.text(7, 6.05, 'w₁=5.0  w₂=0.3  w₃=-0.0001  w₄=-3.0  w₅=-0.05  b=40.0', 
            fontsize=9, ha='center', family='monospace')
    
    # Arrows from inputs
    for i in range(5):
        arrow = FancyArrowPatch((x_start + i*2, 7.6), (7, 7), 
                               arrowstyle='->', mutation_scale=15, 
                               color='gray', linewidth=1.5)
        ax.add_patch(arrow)
    
    # Formula box
    formula_box = FancyBboxPatch((1, 3.8), 12, 1.2, 
                                 boxstyle="round,pad=0.1", 
                                 edgecolor='black', facecolor='#FFE5B4', linewidth=2)
    ax.add_patch(formula_box)
    ax.text(7, 4.7, 'Score = w₁·GPA + w₂·NoteExamen + w₃·Revenu + w₄·Dépendants + w₅·Distance + b', 
            fontsize=10, ha='center', family='monospace', fontweight='bold')
    ax.text(7, 4.1, 'Score = 5×GPA + 0.3×Note - 0.0001×Revenu - 3×Dépendants - 0.05×Distance + 40', 
            fontsize=9, ha='center', family='monospace')
    
    # Example
    example_box = FancyBboxPatch((1, 1.8), 12, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 edgecolor='#13A538', facecolor='#90EE90', linewidth=2)
    ax.add_patch(example_box)
    ax.text(7, 3, 'Exemple: GPA=16, Note=80, Revenu=8000, Dépendants=3, Distance=40', 
            fontsize=9, ha='center', family='monospace')
    ax.text(7, 2.5, 'Score = 5×16 + 0.3×80 - 0.0001×8000 - 3×3 - 0.05×40 + 40', 
            fontsize=9, ha='center', family='monospace')
    ax.text(7, 2, 'Score = 80 + 24 - 0.8 - 9 - 2 + 40 = 132.2 → CLAMPED à 100', 
            fontsize=9, ha='center', family='monospace', fontweight='bold')
    
    # Arrow to output
    arrow_output = FancyArrowPatch((7, 3.8), (7, 3.3), 
                                  arrowstyle='->', mutation_scale=20, 
                                  color='black', linewidth=2)
    ax.add_patch(arrow_output)
    
    # Output
    output_circle = Circle((7, 0.5), 0.5, color='#90EE90', ec='black', linewidth=2)
    ax.add_patch(output_circle)
    ax.text(7, 0.5, 'Score\n(0-100)', fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Advantages and limitations
    ax.text(2, 0.1, '✓ Rapide  ✓ Interprétable  ✗ Suppose linéarité  ✗ Sensible outliers', 
            fontsize=8, ha='left', style='italic')
    
    save_figure('03_regression_lineaire.png', fig)

# ============================================================================
# 4. ARBRE DE DÉCISION
# ============================================================================
def create_decision_tree_diagram():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(7, 9.5, 'Modèle 2: Arbre de Décision', 
            fontsize=16, fontweight='bold', ha='center')
    
    # Root node
    root = FancyBboxPatch((6, 8), 2, 0.6, boxstyle="round,pad=0.05", 
                          edgecolor='black', facecolor='#FFE5B4', linewidth=2)
    ax.add_patch(root)
    ax.text(7, 8.3, 'GPA > 14?', fontsize=10, ha='center', fontweight='bold')
    
    # Left branch (GPA > 14)
    left_node = FancyBboxPatch((1.5, 6.2), 2, 0.6, boxstyle="round,pad=0.05", 
                               edgecolor='black', facecolor='#FFE5B4', linewidth=2)
    ax.add_patch(left_node)
    ax.text(2.5, 6.5, 'Revenu >8000?', fontsize=9, ha='center', fontweight='bold')
    
    # Right branch (GPA ≤ 14)
    right_node = FancyBboxPatch((10.5, 6.2), 2, 0.6, boxstyle="round,pad=0.05", 
                                edgecolor='black', facecolor='#FFE5B4', linewidth=2)
    ax.add_patch(right_node)
    ax.text(11.5, 6.5, 'Distance >50?', fontsize=9, ha='center', fontweight='bold')
    
    # Arrows from root
    arrow_left = FancyArrowPatch((6.5, 8), (3.5, 6.8), 
                                arrowstyle='->', mutation_scale=20, color='black', linewidth=1.5)
    ax.add_patch(arrow_left)
    ax.text(4.5, 7.5, 'OUI', fontsize=9, ha='center', fontweight='bold', color='green')
    
    arrow_right = FancyArrowPatch((7.5, 8), (10.5, 6.8), 
                                 arrowstyle='->', mutation_scale=20, color='black', linewidth=1.5)
    ax.add_patch(arrow_right)
    ax.text(9.5, 7.5, 'NON', fontsize=9, ha='center', fontweight='bold', color='red')
    
    # Leaf nodes - Left branch
    leaves_left = [
        (0.5, 4, '100%', '#90EE90'),
        (4.5, 4, '50%', '#FFB6C1'),
    ]
    
    for i, (x, y, label, color) in enumerate(leaves_left):
        box = FancyBboxPatch((x-0.6, y-0.3), 1.2, 0.6, boxstyle="round,pad=0.05", 
                            edgecolor='black', facecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, label, fontsize=10, ha='center', va='center', fontweight='bold')
        
        # Arrows
        if i == 0:
            arrow = FancyArrowPatch((1.5, 6.2), (0.5, 4.3), 
                                   arrowstyle='->', mutation_scale=15, color='green', linewidth=1.5)
            ax.text(0.8, 5.2, 'OUI', fontsize=8, fontweight='bold', color='green')
        else:
            arrow = FancyArrowPatch((3.5, 6.2), (4.5, 4.3), 
                                   arrowstyle='->', mutation_scale=15, color='red', linewidth=1.5)
            ax.text(4.2, 5.2, 'NON', fontsize=8, fontweight='bold', color='red')
        ax.add_patch(arrow)
    
    # Leaf nodes - Right branch
    leaves_right = [
        (10, 4, '75%', '#FFE5B4'),
        (13, 4, '25%', '#FFA07A'),
    ]
    
    for i, (x, y, label, color) in enumerate(leaves_right):
        box = FancyBboxPatch((x-0.6, y-0.3), 1.2, 0.6, boxstyle="round,pad=0.05", 
                            edgecolor='black', facecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, label, fontsize=10, ha='center', va='center', fontweight='bold')
        
        # Arrows
        if i == 0:
            arrow = FancyArrowPatch((10.5, 6.2), (10, 4.3), 
                                   arrowstyle='->', mutation_scale=15, color='green', linewidth=1.5)
            ax.text(10.8, 5.2, 'OUI', fontsize=8, fontweight='bold', color='green')
        else:
            arrow = FancyArrowPatch((12.5, 6.2), (13, 4.3), 
                                   arrowstyle='->', mutation_scale=15, color='red', linewidth=1.5)
            ax.text(12.2, 5.2, 'NON', fontsize=8, fontweight='bold', color='red')
        ax.add_patch(arrow)
    
    # Info box
    info_text = 'Avantages: Non-linéaire, Robuste outliers, Interprétable\nLimitations: Overfitting, Instable'
    ax.text(7, 0.5, info_text, fontsize=9, ha='center', 
           bbox=dict(boxstyle='round', facecolor='#D7BFF4', alpha=0.8))
    
    save_figure('04_arbre_decision.png', fig)

# ============================================================================
# 5. SUPPORT VECTOR MACHINE (SVM)
# ============================================================================
def create_svm_diagram():
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(6, 9.5, 'Modèle 3: Support Vector Machine (SVM)', 
            fontsize=16, fontweight='bold', ha='center')
    
    # Create scatter plot area
    ax.set_xlim(1, 11)
    ax.set_ylim(2, 8)
    
    # Plot data points
    np.random.seed(42)
    # Class 1 (Approuvé)
    class1_x = np.random.normal(3, 0.8, 15)
    class1_y = np.random.normal(6, 0.8, 15)
    ax.scatter(class1_x, class1_y, c='green', s=150, marker='o', 
              edgecolors='darkgreen', linewidth=2, label='Approuvé', zorder=3)
    
    # Class 2 (Rejeté)
    class2_x = np.random.normal(9, 0.8, 15)
    class2_y = np.random.normal(4, 0.8, 15)
    ax.scatter(class2_x, class2_y, c='red', s=150, marker='x', 
              linewidth=2, label='Rejeté', zorder=3)
    
    # Hyperplan optimal
    x_line = np.array([1, 11])
    y_line = -0.6 * x_line + 10.5
    ax.plot(x_line, y_line, 'b-', linewidth=3, label='Hyperplan Optimal', zorder=2)
    
    # Marges
    y_line_up = -0.6 * x_line + 11.5
    y_line_down = -0.6 * x_line + 9.5
    ax.plot(x_line, y_line_up, 'b--', linewidth=1.5, alpha=0.5, label='Marges')
    ax.plot(x_line, y_line_down, 'b--', linewidth=1.5, alpha=0.5)
    
    # Margin area
    ax.fill_between(x_line, y_line_down, y_line_up, alpha=0.1, color='blue')
    
    # Add text annotations
    ax.text(1.5, 3, 'Classe:\nRejeté', fontsize=10, fontweight='bold', 
           bbox=dict(boxstyle='round', facecolor='#FFA07A', alpha=0.7))
    ax.text(9.5, 7, 'Classe:\nApprouvé', fontsize=10, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='#90EE90', alpha=0.7))
    
    ax.text(6, 1.3, 'Marge Maximale = Meilleure Généralisation', 
           fontsize=11, ha='center', fontweight='bold', style='italic')
    
    ax.legend(loc='upper left', fontsize=9)
    ax.set_xlabel('Feature 1 (GPA)', fontsize=10)
    ax.set_ylabel('Feature 2 (Revenu)', fontsize=10)
    
    # Info box below
    info_text = 'Avantages: Haute dimension, Robuste, Peu d\'overfitting\nLimitations: Moins interprétable, Lent sur grands datasets'
    ax.text(6, 0.5, info_text, fontsize=9, ha='center',
           bbox=dict(boxstyle='round', facecolor='#D7BFF4', alpha=0.8))
    
    save_figure('05_svm.png', fig)

# ============================================================================
# 6. DIAGRAMME DE CAS D'UTILISATION
# ============================================================================
def create_usecase_diagram():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(7, 9.5, 'Diagramme de Cas d\'Utilisation', 
            fontsize=16, fontweight='bold', ha='center')
    
    # Acteurs
    # Étudiant
    student_circle = Circle((1.5, 5), 0.4, color='#FFE5B4', ec='black', linewidth=2)
    ax.add_patch(student_circle)
    ax.text(1.5, 4.3, 'Étudiant', fontsize=10, ha='center', fontweight='bold')
    
    # Admin
    admin_circle = Circle((12.5, 5), 0.4, color='#FFE5B4', ec='black', linewidth=2)
    ax.add_patch(admin_circle)
    ax.text(12.5, 4.3, 'Admin', fontsize=10, ha='center', fontweight='bold')
    
    # Système boundary
    boundary = FancyBboxPatch((3, 1), 8.5, 8, boxstyle="round,pad=0.1", 
                             edgecolor='black', facecolor='#E6F3FF', 
                             linewidth=2, linestyle='dashed')
    ax.add_patch(boundary)
    ax.text(7, 8.7, 'Système d\'Admission et de Bourses', 
           fontsize=11, ha='center', fontweight='bold')
    
    # Use cases - Étudiant
    student_usecases = [
        (4, 7, 'S\'authentifier'),
        (4, 6, 'Consulter Profil'),
        (4, 5, 'S\'enregistrer'),
    ]
    
    for x, y, label in student_usecases:
        oval = FancyBboxPatch((x-0.7, y-0.25), 1.4, 0.5, boxstyle="round,pad=0.05", 
                             edgecolor='black', facecolor='#FFE5B4', linewidth=1.5)
        ax.add_patch(oval)
        ax.text(x, y, label, fontsize=8, ha='center', va='center')
        
        arrow = FancyArrowPatch((2, 5), (x-0.7, y), 
                               arrowstyle='->', mutation_scale=15, color='gray', linewidth=1)
        ax.add_patch(arrow)
    
    # Use cases - Admin
    admin_usecases = [
        (10, 7.5, 'Ajouter Étudiant'),
        (10, 6.5, 'Voir Classements'),
        (10, 5.5, 'Gérer Quotas'),
        (10, 4.5, 'Consulter Stats'),
    ]
    
    for x, y, label in admin_usecases:
        oval = FancyBboxPatch((x-0.7, y-0.25), 1.4, 0.5, boxstyle="round,pad=0.05", 
                             edgecolor='black', facecolor='#FFE5B4', linewidth=1.5)
        ax.add_patch(oval)
        ax.text(x, y, label, fontsize=8, ha='center', va='center')
        
        arrow = FancyArrowPatch((12, 5), (x+0.7, y), 
                               arrowstyle='->', mutation_scale=15, color='gray', linewidth=1)
        ax.add_patch(arrow)
    
    save_figure('06_cas_utilisation.png', fig)

# ============================================================================
# 7. DIAGRAMME DE SÉQUENCE - LOGIN
# ============================================================================
def create_sequence_login_diagram():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(7, 9.5, 'Diagramme de Séquence - Authentification Étudiant', 
            fontsize=14, fontweight='bold', ha='center')
    
    # Actors
    actors = ['Étudiant', 'Frontend', 'Backend', 'MongoDB']
    actor_x = [2, 5.5, 9, 12.5]
    
    for x, actor in zip(actor_x, actors):
        # Actor box
        box = FancyBboxPatch((x-0.6, 8.5), 1.2, 0.4, boxstyle="round,pad=0.05", 
                            edgecolor='black', facecolor='#A7C6DA', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, 8.7, actor, fontsize=9, ha='center', fontweight='bold')
        
        # Lifeline
        ax.plot([x, x], [8.5, 1], 'k--', linewidth=1, alpha=0.5)
    
    # Interactions
    interactions = [
        (2, 7.8, 5.5, 7.6, 'Clic Login'),
        (5.5, 7.4, 9, 7.2, 'POST /login'),
        (9, 6.8, 12.5, 6.6, 'Vérifier Email'),
        (12.5, 6.2, 9, 6, 'Token'),
        (9, 5.6, 5.5, 5.4, 'Token'),
        (5.5, 5, 2, 4.8, 'Redirection Dashboard'),
        (2, 4.4, 5.5, 4.2, 'GET /profile'),
        (5.5, 3.8, 9, 3.6, 'Récupérer Données'),
        (9, 3.2, 12.5, 3, 'Query'),
        (12.5, 2.6, 9, 2.4, 'Données'),
        (9, 2, 5.5, 1.8, 'Profile JSON'),
        (5.5, 1.4, 2, 1.2, 'Afficher Profil'),
    ]
    
    for x1, y1, x2, y2, label in interactions:
        if x1 < x2:
            arrow = FancyArrowPatch((x1, y1), (x2, y2), 
                                   arrowstyle='->', mutation_scale=15, 
                                   color='black', linewidth=1.5)
        else:
            arrow = FancyArrowPatch((x1, y1), (x2, y2), 
                                   arrowstyle='<-', mutation_scale=15, 
                                   color='black', linewidth=1.5)
        ax.add_patch(arrow)
        
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y + 0.15, label, fontsize=8, ha='center', style='italic')
    
    save_figure('07_sequence_login.png', fig)

# ============================================================================
# 8. DIAGRAMME D'ACTIVITÉ - PROCESSUS ADMISSION
# ============================================================================
def create_activity_admission_diagram():
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    ax.text(5, 13.5, 'Diagramme d\'Activité - Processus Admission', 
            fontsize=14, fontweight='bold', ha='center')
    
    # Define activity boxes
    activities = [
        (5, 12.5, 'Début\nProcessus Admission', '#FFE5B4'),
        (5, 11.5, 'Étudiant\nS\'enregistre', '#A7C6DA'),
        (5, 10.3, 'Status = "En attente"\nSaved', '#FFE5B4'),
        (5, 9.1, 'Admin demande\nClassement IA', '#A7C6DA'),
        (2.5, 7.5, 'Calcul\nFeatures', '#A7C6DA'),
        (7.5, 7.5, 'Vérifier\nQuota Année', '#A7C6DA'),
        (5, 5.8, 'ML Ranking\n(3 Modèles)', '#F18F01'),
        (2.5, 4.2, 'Consensus\n(All 3 agree)', '#90EE90'),
        (7.5, 4.2, 'Non-Consensus\n(Mixed)', '#FFA07A'),
        (5, 2.7, 'Merge Scores\nRespect Quota', '#FFE5B4'),
        (5, 1.3, 'Résultats Finaux\nFin Processus', '#90EE90'),
    ]
    
    for x, y, label, color in activities:
        if 'Début' in label or 'Fin' in label:
            circle = Circle((x, y), 0.35, color=color, ec='black', linewidth=2)
            ax.add_patch(circle)
        else:
            box = FancyBboxPatch((x-0.8, y-0.35), 1.6, 0.7, boxstyle="round,pad=0.05", 
                                edgecolor='black', facecolor=color, linewidth=1.5)
            ax.add_patch(box)
        ax.text(x, y, label, fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Arrows
    arrow_sequence = [
        (5, 12.15, 5, 11.85),
        (5, 11.15, 5, 10.65),
        (5, 9.95, 5, 9.45),
        (5, 8.75, 3.5, 7.85),
        (5, 8.75, 6.5, 7.85),
        (2.5, 7.15, 4, 6.2),
        (7.5, 7.15, 6, 6.2),
        (5, 5.45, 3.5, 4.55),
        (5, 5.45, 6.5, 4.55),
        (3.5, 3.9, 4.5, 3.05),
        (6.5, 3.9, 5.5, 3.05),
        (5, 2.35, 5, 1.65),
    ]
    
    for x1, y1, x2, y2 in arrow_sequence:
        arrow = FancyArrowPatch((x1, y1), (x2, y2), 
                               arrowstyle='->', mutation_scale=18, 
                               color='black', linewidth=1.5)
        ax.add_patch(arrow)
    
    save_figure('08_activite_admission.png', fig)

# ============================================================================
# 9. COMPARAISON DES 3 MODÈLES
# ============================================================================
def create_models_comparison():
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Data
    models = ['Régression\nLinéaire', 'Arbre de\nDécision', 'SVM']
    train_time = [10, 50, 200]
    complexity = [1, 3, 5]
    data_needed = [30, 70, 120]
    interpretability = [9, 7, 5]
    overfitting_risk = [2, 8, 3]
    
    x = np.arange(len(models))
    width = 0.15
    
    # Create bars
    bars1 = ax.bar(x - 2*width, train_time, width, label='Temps Entraînement (ms)', color='#A7C6DA')
    bars2 = ax.bar(x - width, complexity, width, label='Complexité (1-5)', color='#F18F01')
    bars3 = ax.bar(x, data_needed, width, label='Données Requises', color='#D7BFF4')
    bars4 = ax.bar(x + width, interpretability, width, label='Interprétabilité (0-10)', color='#90EE90')
    bars5 = ax.bar(x + 2*width, overfitting_risk, width, label='Risque Overfitting (1-10)', color='#FFA07A')
    
    ax.set_ylabel('Valeurs', fontsize=12, fontweight='bold')
    ax.set_title('Comparaison des 3 Modèles ML', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=11, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2, bars3, bars4, bars5]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=8)
    
    save_figure('09_comparaison_modeles.png', fig)

# ============================================================================
# EXÉCUTION PRINCIPALE
# ============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Génération des Diagrammes PNG")
    print("=" * 60)
    
    create_architecture_diagram()
    create_data_flow_diagram()
    create_linear_regression_diagram()
    create_decision_tree_diagram()
    create_svm_diagram()
    create_usecase_diagram()
    create_sequence_login_diagram()
    create_activity_admission_diagram()
    create_models_comparison()
    
    print("=" * 60)
    print("✓ Tous les diagrammes ont été générés avec succès!")
    print(f"✓ Dossier de destination: {OUTPUT_DIR}/")
    print("=" * 60)
