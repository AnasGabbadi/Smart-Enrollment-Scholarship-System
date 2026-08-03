# 📚 DOCUMENTATION - Système Intelligent d'Admission et d'Attribution de Bourses

**Version**: 1.0  
**Date**: Janvier 2026  
**Langue**: Français

---

## 📑 Table des Matières

1. [Architecture Générale](#1-architecture-générale)
2. [Flux de Données](#2-flux-de-données)
3. [Diagrammes des Modèles IA](#3-diagrammes-des-modèles-ia)
4. [Diagrammes de Cas d'Utilisation](#4-diagrammes-de-cas-dutilisation)
5. [Diagrammes de Séquence](#5-diagrammes-de-séquence)
6. [Diagrammes d'Activités](#6-diagrammes-dactivités)

---

## 1. Architecture Générale

### Diagramme Architecture Système

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SYSTÈME COMPLET                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────────┐         ┌──────────────────────┐          │
│  │   FRONTEND REACT     │         │   BACKEND FASTAPI    │          │
│  │  (Port 3000)         │◄────────│  (Port 8000)         │          │
│  │                      │         │                      │          │
│  │ • Admin Dashboard    │         │ • API REST           │          │
│  │ • Student Portal     │         │ • Logique Métier     │          │
│  │ • Visualisations     │         │ • ML Ranking         │          │
│  └──────────────────────┘         └──────┬───────────────┘          │
│                                           │                          │
│                                    ┌──────▼────────┐                │
│                                    │   MONGODB     │                │
│                                    │ Base de Données
│                                    │               │                │
│                                    └───────────────┘                │
│                                                                       │
│  ┌─────────────────────────────────────────────────┐                │
│  │         MOTEUR ML (3 MODÈLES)                  │                │
│  ├─────────────────────────────────────────────────┤                │
│  │ • Régression Linéaire                           │                │
│  │ • Arbre de Décision                             │                │
│  │ • Support Vector Machine (SVM)                  │                │
│  └─────────────────────────────────────────────────┘                │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Flux de Données

### Processus de Classement des Étudiants

```
┌──────────────────────────────────────────────────────────────────┐
│                    ÉTUDIANT CANDIDAT                              │
│            (Status = "En attente")                                │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
         ┌──────────────────────────┐
         │  EXTRACTION DES FEATURES │
         ├──────────────────────────┤
         │ • GPA                    │
         │ • Note Examen            │
         │ • Revenu Mensuel         │
         │ • Nombre Dépendants      │
         │ • Distance Université    │
         └────────┬─────────────────┘
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
    ┌───────┐ ┌────────┐ ┌─────┐
    │Model1 │ │Model 2 │ │Model│
    │RegLin │ │Arbre   │ │SVM  │
    └───┬───┘ └───┬────┘ └──┬──┘
        │         │         │
        ▼         ▼         ▼
    Score1    Score2    Score3
    (0-100)   (0-100)   (0-100)
        │         │         │
        └─────────┼─────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │  CONSENSUS CHECK            │
    │  (Tous 3 modèles d'accord?) │
    └─────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
    Consensus          Non-Consensus
    (Haute confiance)  (Score moyen)
        │                   │
        └─────────┬─────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │  CLASSEMENT FUSIONNÉ        │
    │  (Score moyen des 3 modèles)│
    │  Respectant QUOTA annuel    │
    └─────────────────────────────┘
                  │
                  ▼
         ┌────────────────────┐
         │ RÉSULTATS FINAUX   │
         │ • Top N candidats  │
         │ • Consensus List   │
         │ • All Rankings     │
         └────────────────────┘
```

---

## 3. Fonctionnement Détaillé des Modèles IA

### 3.1 Comment les Modèles Apprennent

#### Données d'Entraînement

Chaque modèle apprend à partir de **données historiques** des étudiants:

```
DONNÉES D'ENTRAÎNEMENT
│
├─ Features (Caractéristiques d'Entrée)
│  ├─ GPA (Note Générale)
│  ├─ Note Examen
│  ├─ Revenu Mensuel (DH)
│  ├─ Nombre de Dépendants
│  └─ Distance Université (km)
│
└─ Target (Objectif d'Apprentissage)
   ├─ Régression Linéaire → Score continu (0-100)
   ├─ Arbre de Décision → Classe bourse (0, 1, 2, 3)
   └─ SVM → Probabilité inscription (0, 1, 2)
```

#### Processus d'Apprentissage Général

```python
# ÉTAPE 1: Charger les données historiques
données = récupérer_étudiants_approuvés_et_rejetés()

# ÉTAPE 2: Diviser en entraînement et test
X_train (70%) = Features des données d'entraînement
y_train (70%) = Résultats réels (approuvé/rejeté)

X_test (30%) = Features des données de test
y_test (30%) = Résultats réels de test

# ÉTAPE 3: Normaliser les données
X_train = normaliser(X_train)  # Mettre toutes les features entre 0-1
X_test = normaliser(X_test)

# ÉTAPE 4: Créer et entraîner le modèle
modele = ModeleML()
modele.fit(X_train, y_train)

# ÉTAPE 5: Évaluer la performance
precision = modele.évaluer(X_test, y_test)
print(f"Précision du modèle: {precision}%")

# ÉTAPE 6: Sauvegarder le modèle entraîné
sauvegarder(modele, "modele_entrainé.pkl")
```

---

### 3.2 MODÈLE 1: RÉGRESSION LINÉAIRE

#### Concept Fondamental

La régression linéaire cherche une **relation linéaire** entre les features et le résultat:

```
Score = w₁×GPA + w₂×NoteExamen + w₃×Revenu + w₄×Dépendants + w₅×Distance + b

Où:
- w₁, w₂, w₃, w₄, w₅ = Poids appris automatiquement
- b = Biais (valeur initiale)
```

#### Comment ça Apprend

```
ITÉRATION 1:
─────────────
Supposons les poids initiaux: w = [1, 1, 1, 1, 1], b = 50

Étudiant 1: GPA=15, Note=75, Revenu=10000, Dépendants=2, Distance=30
Prédiction = 1×15 + 1×75 + 1×10000 + 1×2 + 1×30 + 50 = 10172 ❌
Résultat réel = 85 (approuvé)
Erreur = 10172 - 85 = 10087 (ÉNORME ERREUR!)

AJUSTEMENT DES POIDS:
Le modèle calcule: "J'ai trop surestimé le Revenu!"
Nouveau w₃ = 0.00001 (beaucoup plus petit)

ITÉRATION 2:
─────────────
Même étudiant avec nouveaux poids
Prédiction = 1×15 + 1×75 + 0.00001×10000 + 1×2 + 1×30 + 50 = 172.1
Résultat réel = 85
Erreur = 172.1 - 85 = 87.1 (mieux!)

ITÉRATION 3, 4, 5... (répété 1000 fois):
Chaque itération ajuste les poids pour réduire l'erreur
Jusqu'à atteindre la convergence
```

#### Formule Mathématique Complète

```
Score = w₁·GPA + w₂·NoteExamen + w₃·Revenu + w₄·Dépendants + w₅·Distance + b

Exemple de poids APPRIS (après entraînement):
- w₁ (GPA) = 5.0          → GPA impact fortement (+5 par point)
- w₂ (NoteExamen) = 0.3   → NoteExamen impact faiblement (+0.3 par point)
- w₃ (Revenu) = -0.0001   → Plus de revenu = MOINS besoin bourse
- w₄ (Dépendants) = -3.0  → Plus de dépendants = PLUS besoin bourse
- w₅ (Distance) = -0.05   → Distance éloignée = légèrement MOINS besoin
- b (Biais) = 40.0        → Score de base

Prédiction pour un étudiant:
GPA=16, Note=80, Revenu=8000, Dépendants=3, Distance=40km

Score = (5.0×16) + (0.3×80) + (-0.0001×8000) + (-3.0×3) + (-0.05×40) + 40
      = 80 + 24 + (-0.8) + (-9) + (-2) + 40
      = 132.2 → CLAMPED à 100 (max)
```

#### Avantages et Limitations

```
✓ AVANTAGES:
  • Rapide à entraîner (quelques millisecondes)
  • Résultats très interprétables
  • Bon pour relationss linéaires
  • Peu d'overfitting

✗ LIMITATIONS:
  • Suppose que tout est linéaire
  • Sensible aux valeurs extrêmes (outliers)
  • Ne capture pas les interactions complexes
  • Exemple: Si GPA>15 ET Revenu<5000 → cas spécial non capturé
```

---

### 3.3 MODÈLE 2: ARBRE DE DÉCISION

#### Concept Fondamental

L'arbre de décision pose une **série de questions** pour classer les étudiants:

```
                    ┌─────────────────┐
                    │   GPA > 14?     │
                    └────┬────┬───────┘
                    OUI /      \ NON
                    /            \
            ┌───────▼────┐    ┌───▼──────┐
            │Revenu >    │    │Distance >│
            │8000 DH?    │    │50 km?    │
            └──┬────┬───┘    └──┬────┬──┘
              /      \         /      \
           OUI       NON      OUI     NON
           /           \       /        \
       ┌──▼──┐    ┌────▼─┐ ┌──▼──┐  ┌──▼──┐
       │ 100%│    │ 50%  │ │ 75% │  │ 25% │
       └─────┘    └──────┘ └─────┘  └─────┘
```

#### Comment ça Apprend

```
ÉTAPE 1: ANALYSE DE LA PREMIÈRE FEATURE
─────────────────────────────────────────
Le modèle teste TOUTES les features pour trouver le meilleur split:

GPA comme split?
   Si GPA > 10: Classes = [✓✓✓✗✗]  (3 approuvés, 2 rejetés)
   Gain d'info = Bon ✓

NoteExamen comme split?
   Si NoteExamen > 70: Classes = [✓✓✗✓✗]  (3 approuvés, 2 rejetés)
   Gain d'info = Moyen

→ GPA est choisi comme première condition (meilleur gain d'info)

ÉTAPE 2: SPLIT RÉCURSIF
──────────────────────
Pour la branche GPA > 10 (3 approuvés, 2 rejetés):
  Tester Revenu > 5000:
    Si Revenu > 5000: Classes = [✓✓✗]  Meilleur!
    Gain = Très bon
  → Ajouter question "Revenu > 5000?" à cette branche

Pour la branche GPA ≤ 10 (2 rejetés, 0 approuvés):
  Tous rejetés → FEUILLE TERMINALE (pas besoin de continuer)

ÉTAPE 3: ARRÊT
──────────────
Max profondeur atteinte (max_depth=5)
OU Pas assez d'échantillons (min_samples_leaf=5)
OU Classes pures (tous approuvés ou rejetés)

RÉSULTAT: Arbre avec règles explicites
```

#### Mathématique: Gain d'Information

```
Entropy AVANT split:
E = -[p(✓)·log(p(✓)) + p(✗)·log(p(✗))]

Exemple: 3 approuvés, 2 rejetés
p(✓) = 3/5 = 0.6
p(✗) = 2/5 = 0.4
E = -[0.6·log(0.6) + 0.4·log(0.4)] = 0.971

APRÈS split par GPA > 10:
Gauche: 3 approuvés, 0 rejetés → E_gauche = 0
Droit: 0 approuvés, 2 rejetés → E_droit = 0

Gain = E_avant - [5/5 × 0 + 2/5 × 0] = 0.971

(Plus grand gain = meilleur split)
```

#### Avantages et Limitations

```
✓ AVANTAGES:
  • Capture relations NON-linéaires
  • Très facile à interpréter (on voit les règles)
  • Robuste aux outliers
  • Pas besoin de normalisation

✗ LIMITATIONS:
  • Tend à overfitter (mémoriser plutôt que généraliser)
  • Instable: petits changements → grand changement d'arbre
  • Sensible à l'ordre des données
  • Peut créer des règles trop spécifiques
```

---

### 3.4 MODÈLE 3: SUPPORT VECTOR MACHINE (SVM)

#### Concept Fondamental

SVM cherche l'**hyperplan optimal** qui sépare les deux classes avec la **plus grande marge**:

```
ESPACE 2D SIMPLIFIÉ (GPA vs Revenu):

       GPA
        │
        │ Classe: Approuvé (●)
        │  ●●
        │ ●●  ╱─ Hyperplan
        │ ●  ╱
    ────┼────────── Marge (vide!)
        │ ╲ ○○
        │  ╲○○  Classe: Rejeté (○)
        │   ○
        └──────────── Revenu

→ Maximiser la distance VIDE entre les deux classes
→ Meilleure généralisation sur données nouvelles
```

#### Comment ça Apprend

```
ÉTAPE 1: TRANSFORMER EN ESPACE HAUTE DIMENSION
───────────────────────────────────────────────
Nos 5 features: [GPA, NoteExamen, Revenu, Dépendants, Distance]

Le kernel RBF transforme ces 5 dimensions en 1000+ dimensions:

Feature originale:  GPA=15, Revenu=8000
Feature transformée: [1.0, 15.0, 8000.0, 15², 8000², 15×8000, sin(15), cos(8000), ...]
                     (1000+ dimensions!)

POURQUOI? Parce qu'en haute dimension, les données deviennent souvent séparables!

ÉTAPE 2: TROUVER L'HYPERPLAN OPTIMAL
────────────────────────────────────
Tester millions de positions d'hyperplan:

Position 1: Marge = 2.5 unités
Position 2: Marge = 3.1 unités  ← Meilleur!
Position 3: Marge = 2.8 unités

Garder position 2 (marge maximale)

ÉTAPE 3: IDENTIFIER LES SUPPORT VECTORS
──────────────────────────────────────
Support Vectors = Points les plus proches de l'hyperplan

Seulement ~10-20% des points d'entraînement sont "support vectors"
Le reste ? Ignorés! (Efficace pour généralisation)

ÉTAPE 4: PRÉDICTION SUR NOUVEAU POINT
─────────────────────────────────────
Nouvel étudiant: GPA=16, Note=78, Revenu=9000, Dépendants=2, Distance=35

1. Transformer en espace haute dimension
2. Mesurer distance à l'hyperplan
3. Si distance > 0 → Classe Approuvé
   Si distance < 0 → Classe Rejeté
   Distance absolue = Confiance
```

#### Exemple Mathématique Concret

```
Hyperplan SVM en 5D:
w₁·GPA + w₂·NoteExamen + w₃·Revenu + w₄·Dépendants + w₅·Distance + b = 0

Exemple de poids APPRIS:
w₁ = 0.8   (GPA important)
w₂ = 0.3   (NoteExamen peu important)
w₃ = -0.001 (Revenu inversé)
w₄ = 0.6   (Dépendants important)
w₅ = 0.2
b = -5.0

Score = 0.8×16 + 0.3×78 - 0.001×9000 + 0.6×2 + 0.2×35 - 5.0
      = 12.8 + 23.4 - 9 + 1.2 + 7 - 5
      = 30.4 (positif → APPROUVÉ)

Confiance = sigmoid(30.4) = 99.9% → Très confiant!
```

#### Avantages et Limitations

```
✓ AVANTAGES:
  • Très efficace en haute dimension
  • Robuste: peu affecté par outliers
  • Généralize bien (peu d'overfitting)
  • Marges maximales = meilleure séparation

✗ LIMITATIONS:
  • Moins interprétable que arbres
  • Plus lent à entraîner que régression
  • Hyperparamètres complexes (C, gamma, kernel)
  • Ne fournit pas les "règles" directes
```

---

### 3.5 Tableau Comparatif d'Apprentissage

```
╔════════════════════╦═══════════════╦═══════════════╦═══════════════╗
║ ASPECT             ║ RÉGRESSION    ║ ARBRE         ║ SVM           ║
║                    ║ LINÉAIRE      ║ DÉCISION      ║               ║
╠════════════════════╬═══════════════╬═══════════════╬═══════════════╣
║ TEMPS APPRENTISSAGE║ ~10ms         ║ ~50ms         ║ ~200ms        ║
╠════════════════════╬═══════════════╬═══════════════╬═══════════════╣
║ COMPLEXITÉ         ║ Simple        ║ Moyenne       ║ Haute         ║
║ OPÉRATIONS         ║ (Multiplication║ (Comparaisons)║ (Noyau RBF)   ║
╠════════════════════╬═══════════════╬═══════════════╬═══════════════╣
║ DONNÉES REQUISES   ║ 30-50         ║ 50-100        ║ 100+          ║
╠════════════════════╬═══════════════╬═══════════════╬═══════════════╣
║ INTERPRÉTABILITÉ   ║ ✓✓✓ Excellent ║ ✓✓ Bon        ║ ✓ Acceptable  ║
╠════════════════════╬═══════════════╬═══════════════╬═══════════════╣
║ OVERFITTING        ║ Bas           ║ Haut (risque) ║ Bas           ║
╠════════════════════╬═══════════════╬═══════════════╬═══════════════╣
║ OUTLIERS           ║ Sensible      ║ Robuste       ║ Robuste       ║
╠════════════════════╬═══════════════╬═══════════════╬═══════════════╣
║ NON-LINÉARITÉ      ║ Mauvais       ║ Excellent     ║ Excellent     ║
╚════════════════════╩═══════════════╩═══════════════╩═══════════════╝
```

---

### 3.6 Diagrammes des Modèles IA

```
╔════════════════════════════════════════════════════════════════════╗
║                      MODÈLE 1: RÉGRESSION LINÉAIRE                ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Features Input              Processing              Score Output ║
║  ┌────────────────┐        ┌──────────┐           ┌─────────────┐║
║  │ GPA            │        │ Poids    │           │  Score      ║
║  │ Note Examen    │───────▶│ Linéaires│──────────▶│ Continu     ║
║  │ Revenu         │        │          │           │ (0-100)     ║
║  │ Dépendants     │        └──────────┘           │             ║
║  │ Distance       │                               │ Interprétable║
║  └────────────────┘                               └─────────────┘║
║                                                                    ║
║  Formule: Score = w₁·GPA + w₂·Note + w₃·Revenu + ... + b         ║
║                                                                    ║
║  ✓ Rapide  ✓ Simple  ✓ Explicable                                ║
║  ✗ Suppose linéarité  ✗ Sensible outliers                        ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

#### Diagramme 3: Arbre de Décision
📄 **Fichier**: `04_arbre_decision.png`
```
                    GPA > 14?
                   /          \
              OUI /            \ NON
                 /              \
            Revenu >8000?    Distance >50?
            /        \        /         \
          85%       50%     75%        25%

✓ Non-linéaire  ✓ Robuste outliers  ✓ Interprétable
✗ Risque overfitting  ✗ Instable
```

#### Diagramme 4: Support Vector Machine (SVM)
📄 **Fichier**: `05_svm.png`
```
        Classe Éligible (●)
              ●●  ╱
             ●●  ╱  Marge Maximale
            ●●  ╱
    ─ ─ ─ ─ ─ ─ ─ Hyperplan Optimal
                ╲  ○○
                 ╲ ○○  Classe Non-Éligible (○)
                  ╲ ○○

✓ Efficace complexité  ✓ Robuste  ✓ Haute dimension
✗ Moins interprétable  ✗ Lent grandes données
```

### Processus d'Entraînement des Modèles

```
┌──────────────────────────────────────────────────┐
│        DONNÉES D'ENTRAÎNEMENT HISTORIQUES       │
│  (Étudiants approuvés/rejetés + leurs scores)  │
└──────────────┬───────────────────────────────────┘
               │
       ┌───────┼───────┐
       │       │       │
       ▼       ▼       ▼
   ┌─────┐ ┌─────┐ ┌─────┐
   │ ML1 │ │ ML2 │ │ ML3 │
   └──┬──┘ └──┬──┘ └──┬──┘
      │       │       │
      ▼       ▼       ▼
  ┌─────────────────────────┐
  │ EVALUATION PERFORMANCE  │
  │ Precision / Recall / F1 │
  └──────────┬──────────────┘
             │
             ▼
     ┌──────────────────┐
     │ MODÈLES PRÊTS    │
     │ (Sauvegardés)    │
     └──────────────────┘
```

---

## 4. Diagrammes des Cas d'Utilisation

📄 **Fichier**: `06_cas_utilisation.png`

Le système supporte deux types d'utilisateurs avec différents cas d'utilisation:

### Cas d'Utilisation Étudiant
- ✅ S'authentifier
- ✅ Consulter son profil
- ✅ S'enregistrer avec infos académiques/financières
- ✅ Télécharger sa prédiction IA

### Cas d'Utilisation Admin
- ✅ Ajouter/modifier/supprimer des étudiants
- ✅ Voir les classements ML par année
- ✅ Gérer les quotas de bourses
- ✅ Consulter les statistiques globales
- ✅ Exporter les données

---

## 5. Diagrammes de Séquence

### Scénario 1: Authentification Étudiant

📄 **Fichier**: `07_sequence_login.png`

```
Étudiant        Frontend        Backend        MongoDB
   │               │              │              │
   │─ Clic Login─►│              │              │
   │              │─ POST /login─►│              │
   │              │              │              │
   │              │              │─ Vérifier ──►│
   │              │              │  Identifiants│
   │              │              │◄─ Token ────│
   │              │◄─ Token ─────│              │
   │◄─ Redirection─              │              │
   │              │              │              │
   │─ Clic Profil─►              │              │
   │              │─ GET /profile┬─token─►     │
   │              │              │              │
   │              │              │─ Récupérer ─►│
   │              │              │  Données     │
   │              │              │◄─ Données ──│
   │              │◄─ Profil ────│              │
   │◄─ Afficher ──│              │              │
│   Profil     │              │              │
```

---

## 6. Diagrammes d'Activités

### Processus d'Admission Complet

📄 **Fichier**: `08_activite_admission.png`

```
         Début Processus Admission
                     │
                     ▼
           Étudiant S'enregistre
                     │
                     ▼
           Status = "En attente"
                     │
                     ▼
           Admin demande Classement IA
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
    Calcul Features      Vérifier Quota
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ML Ranking (3 Modèles)
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
     Consensus            Non-Consensus
     (Tous d'accord)     (Scores mixtes)
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         Merge Scores + Respect Quota
                     │
                     ▼
         Résultats Finaux
                     │
                     ▼
         Fin Processus Admission
```

### Processus Entraînement des Modèles

📄 **Fichier**: `09_comparaison_modeles.png` (Comparatif complet)

```
┌─────────────────────────────────────┐
│   COLLECTE DONNÉES HISTORIQUES      │
│   Étudiants Approuvés/Rejetés       │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   PREPROCESSING                     │
│   • Normalisation Features          │
│   • Traitement Valeurs Manquantes   │
│   • Balancing Data                  │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐      ┌──────────┐
│ 70% Train│      │ 30% Test │
└────┬────┘      └────┬─────┘
     │                │
     ▼                ▼
┌──────────────────────────────┐
│ ENTRAÎNER 3 MODÈLES         │
├──────────────────────────────┤
│ 1. Régression Linéaire      │
│ 2. Arbre de Décision        │
│ 3. Support Vector Machine   │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ ÉVALUER PERFORMANCE          │
│ (Precision/Recall/F1/ROC)   │
└──────────┬───────────────────┘
           │
      ┌────┴─────┐
      │           │
      ▼           ▼
  Résultats  Ajuster
  OK?        Hyperparams
  │              │
  │         ┌────┘
  │         │
  └────┬────┘
       │
       ▼
┌──────────────────────────────┐
│ SAUVEGARDER MODÈLES ENTRAÎNÉS│
│ (modeles_entraines/)         │
└──────────────────────────────┘
```

---

## 📊 Tableau Récapitulatif des Diagrammes

| # | Nom du Fichier | Contenu | Utilité |
|---|---|---|---|
| 1 | `01_architecture_system.png` | Architecture globale Frontend/Backend/DB | Vue d'ensemble du système |
| 2 | `02_flux_donnees.png` | Flux complet de classement | Processus étudiant |
| 3 | `03_regression_lineaire.png` | Modèle 1 détaillé | Comprendre la régression |
| 4 | `04_arbre_decision.png` | Modèle 2 avec arbre visuel | Comprendre les règles |
| 5 | `05_svm.png` | Modèle 3 avec hyperplan | Comprendre la séparation |
| 6 | `06_cas_utilisation.png` | Interactions utilisateurs | Cas d'usage système |
| 7 | `07_sequence_login.png` | Flux d'authentification | Interactions détaillées |
| 8 | `08_activite_admission.png` | Processus admission complet | Workflow global |
| 9 | `09_comparaison_modeles.png` | Comparatif 3 modèles | Performances relatives |

| Aspect | Détail |
|--------|--------|
| **Frontend** | React 18, Tailwind CSS, Axios |
| **Backend** | FastAPI, Python 3.11+ |
| **Base de Données** | MongoDB |
| **Modèles IA** | Scikit-learn (3 modèles) |
| **Authentification** | JWT + Bcrypt |
| **Port Frontend** | 3000 |
| **Port Backend** | 8000 |

---

**📞 Support**: Contact administrateur système  
**📅 Mise à jour**: Janvier 2026
