"""
Génère un dataset synthétique reproductible d'étudiants marocains pour
l'entraînement des 3 modèles ML (régression, arbre de décision, SGD/SVM).

Le dataset original (500k lignes) utilisé pour ce projet a été perdu et n'a
jamais été versionné (voir README, section "Dataset"). Ce script le remplace
par des données synthétiques générées avec une seed fixe : reproductible,
inspectable, et volontairement plus petit (défaut 30 000 lignes) pour rester
rapide à régénérer/entraîner sur la machine de quiconque clone le repo.

Les relations entre features et cibles sont volontairement bruitées (ajout de
bruit gaussien avant seuillage/coupure) pour simuler un vrai problème de
prédiction : un signal réel mais imparfait, pas une règle déterministe qui
donnerait des métriques irréalistes (accuracy/R² proches de 1.0).
"""
import os
import sys

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SEED = 42

REGIONS = [
    "Casablanca-Settat",
    "Rabat-Salé-Kénitra",
    "Marrakech-Safi",
    "Fès-Meknès",
    "Tanger-Tétouan-Al Hoceïma",
    "Souss-Massa",
    "Béni Mellal-Khénifra",
    "Oriental",
    "Drâa-Tafilalet",
    "Guelmim-Oued Noun",
    "Laâyoune-Sakia El Hamra",
    "Dakhla-Oued Ed-Dahab",
]
# Poids approximatifs (répartition de population, ordre de grandeur réel du Maroc)
REGION_WEIGHTS = [0.20, 0.13, 0.11, 0.11, 0.10, 0.08, 0.07, 0.06, 0.05, 0.03, 0.03, 0.03]


def generer_dataset(n_lignes: int = 30_000, seed: int = SEED) -> pd.DataFrame:
    """
    Génère n_lignes d'étudiants synthétiques avec features académiques,
    financières et géographiques, plus 3 cibles bruitées pour les 3 modèles.
    """
    rng = np.random.default_rng(seed)

    # ------------------------------------------------------------------
    # Features
    # ------------------------------------------------------------------
    gpa = np.clip(rng.normal(12.5, 2.5, n_lignes), 4.0, 20.0)

    # Corrélé au GPA mais avec un bruit propre (deux examens distincts)
    exam_score = np.clip(
        0.5 * (gpa / 20.0 * 100.0) + 0.5 * rng.normal(55, 18, n_lignes),
        0.0, 100.0,
    )

    # Revenu mensuel du foyer en MAD, distribution log-normale (asymétrique,
    # réaliste pour un revenu : beaucoup de foyers modestes, longue traîne)
    family_income = np.clip(rng.lognormal(mean=np.log(6000), sigma=0.65, size=n_lignes), 1200, 90_000)

    dependents = np.clip(rng.poisson(2.2, n_lignes), 0, 8)

    distance_km = np.clip(rng.exponential(scale=25, size=n_lignes), 0.5, 250.0)

    region = rng.choice(REGIONS, size=n_lignes, p=REGION_WEIGHTS)

    # ------------------------------------------------------------------
    # Cible 1 — financial_capacity_score (régression, 0-100)
    # "Capacité financière" = capacité du foyer à assumer les frais, donc
    # positivement liée au revenu, négativement aux dépendants ; un peu de
    # mérite académique est mélangé (design existant de l'app : score
    # combinant mérite + besoin pour prioriser les bourses).
    # ------------------------------------------------------------------
    signal_financier = (
        20.0
        + 1.2 * gpa
        + 0.15 * exam_score
        + 0.9 * (family_income / 1000.0)
        - 3.0 * dependents
    )
    bruit_financier = rng.normal(0, 12, n_lignes)
    financial_capacity_score = np.clip(signal_financier + bruit_financier, 0.0, 100.0)

    # ------------------------------------------------------------------
    # Cible 2 — scholarship_class (classification, 0-3)
    # Composite mérite (GPA) + besoin financier (revenu bas, dépendants
    # nombreux), bruité avant seuillage pour éviter une séparation parfaite.
    # ------------------------------------------------------------------
    facteur_revenu = np.clip((20_000 - family_income) / 20_000 * 100.0, 0.0, 100.0)
    facteur_dependants = np.clip(dependents * 12.0, 0.0, 100.0)
    composite_bourse = (
        0.5 * (gpa / 20.0 * 100.0)
        + 0.3 * facteur_revenu
        + 0.2 * facteur_dependants
        + rng.normal(0, 15, n_lignes)
    )
    scholarship_class = np.select(
        [composite_bourse >= 75, composite_bourse >= 55, composite_bourse >= 35],
        [3, 2, 1],
        default=0,
    )

    # ------------------------------------------------------------------
    # Cible 3 — enrollment_probability_class (classification, 0-2)
    # Mérite académique + revenu (capacité à assumer les coûts indirects)
    # moins la distance (contrainte logistique), bruité avant seuillage.
    # ------------------------------------------------------------------
    facteur_revenu_inscription = np.clip(family_income / 30_000 * 100.0, 0.0, 100.0)
    facteur_distance = np.clip(distance_km / 150.0 * 100.0, 0.0, 100.0)
    composite_inscription = (
        0.30 * (gpa / 20.0 * 100.0)
        + 0.30 * exam_score
        + 0.20 * facteur_revenu_inscription
        - 0.20 * facteur_distance
        + rng.normal(0, 15, n_lignes)
    )
    enrollment_probability_class = np.select(
        [composite_inscription >= 45, composite_inscription >= 25],
        [2, 1],
        default=0,
    )

    return pd.DataFrame({
        "gpa": gpa.round(2),
        "exam_score": exam_score.round(2),
        "family_income": family_income.round(2),
        "dependents": dependents.astype(int),
        "distance_km": distance_km.round(2),
        "region": region,
        "financial_capacity_score": financial_capacity_score.round(2),
        "scholarship_class": scholarship_class.astype(int),
        "enrollment_probability_class": enrollment_probability_class.astype(int),
    })


def main():
    n_lignes = int(os.environ.get("N_LIGNES_DATASET", 30_000))
    print(f"[*] Génération de {n_lignes:,} étudiants synthétiques (seed={SEED})...")
    df = generer_dataset(n_lignes, SEED)

    chemin_csv = os.path.join(os.path.dirname(__file__), "..", "moroccan_students_scholarship_dataset.csv")
    chemin_csv = os.path.abspath(chemin_csv)
    df.to_csv(chemin_csv, index=False)

    print(f"[✓] Dataset écrit: {chemin_csv}")
    print(f"    {len(df):,} lignes, {len(df.columns)} colonnes")
    print("\nRépartition scholarship_class:")
    print(df["scholarship_class"].value_counts(normalize=True).sort_index().round(3))
    print("\nRépartition enrollment_probability_class:")
    print(df["enrollment_probability_class"].value_counts(normalize=True).sort_index().round(3))


if __name__ == "__main__":
    main()
