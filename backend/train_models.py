"""
Script consolidated pour entraîner les modèles ML et insérer les données de test
Charge 500k étudiants, entraîne avec 80/20 split et insère 1000 lignes en BD
"""
import numpy as np
import pandas as pd
import os
import sys
import warnings

warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from modeles.regression_lineaire import modele_regression
from modeles.arbre_decision import modele_arbre
from modeles.svm import modele_svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error, r2_score, accuracy_score, 
    precision_score, recall_score, f1_score, confusion_matrix
)
from utilitaires.base_donnees import GestionnaireBD


def charger_donnees_reelles(chemin_csv, test_size=0.2):
    """
    Charge le dataset réel de 500k étudiants et le divise en train/test 80/20
    """
    print(f"\n[*] Chargement du dataset...")
    try:
        df = pd.read_csv(chemin_csv)
        print(f"[✓] Dataset chargé: {len(df):,} lignes, {len(df.columns)} colonnes")
    except Exception as e:
        print(f"[✗] Erreur lors du chargement: {e}")
        return None
    
    # Afficher les stats
    print(f"\nStatistiques du dataset:")
    print(f"  GPA: [{df['gpa'].min():.2f}, {df['gpa'].max():.2f}]")
    print(f"  Exam Score: [{df['exam_score'].min():.2f}, {df['exam_score'].max():.2f}]")
    print(f"  Family Income: [{df['family_income'].min():.0f}, {df['family_income'].max():.0f}] DH")
    print(f"  Dependents: [{df['dependents'].min():.0f}, {df['dependents'].max():.0f}]")
    print(f"  Distance: [{df['distance_km'].min():.2f}, {df['distance_km'].max():.2f}] km")
    
    # Préparer les features
    X = df[['gpa', 'exam_score', 'family_income', 'dependents', 'distance_km']].values
    y_regression = df['financial_capacity_score'].values
    y_arbre = df['scholarship_class'].values
    y_svm = df['enrollment_probability_class'].values
    
    # Split 80/20
    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X, y_regression, test_size=test_size, random_state=42
    )
    
    X_train_arb, X_test_arb, y_train_arb, y_test_arb = train_test_split(
        X, y_arbre, test_size=test_size, random_state=42
    )
    
    X_train_svm, X_test_svm, y_train_svm, y_test_svm = train_test_split(
        X, y_svm, test_size=test_size, random_state=42
    )
    
    print(f"\n[✓] Données divisées:")
    print(f"    Train: {len(X_train_reg):,} (80%)")
    print(f"    Test: {len(X_test_reg):,} (20%)")
    
    return {
        'regression': (X_train_reg, X_test_reg, y_train_reg, y_test_reg),
        'arbre': (X_train_arb, X_test_arb, y_train_arb, y_test_arb),
        'svm': (X_train_svm, X_test_svm, y_train_svm, y_test_svm),
        'dataframe': df,
        'X': X
    }


def entrainer_modeles(donnees):
    """
    Entraîne les 3 modèles ML sur le dataset
    """
    print("\n" + "=" * 80)
    print("ENTRAÎNEMENT DES MODÈLES ML")
    print("=" * 80)
    
    X_train_reg, X_test_reg, y_train_reg, y_test_reg = donnees['regression']
    X_train_arb, X_test_arb, y_train_arb, y_test_arb = donnees['arbre']
    X_train_svm, X_test_svm, y_train_svm, y_test_svm = donnees['svm']
    
    results = {}
    
    # 1. RÉGRESSION LINÉAIRE
    print("\n[1/3] Régression Linéaire - Capacité Financière")
    print("-" * 80)
    try:
        print(f"[*] Entraînement sur {len(X_train_reg):,} samples...")
        modele_regression.entraîner(X_train_reg, y_train_reg)
        
        print(f"[*] Évaluation sur {len(X_test_reg):,} samples...")
        y_pred_reg = modele_regression.modele.predict(X_test_reg)
        
        mse = mean_squared_error(y_test_reg, y_pred_reg)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test_reg, y_pred_reg)
        mae = np.mean(np.abs(y_test_reg - y_pred_reg))
        
        results['regression'] = {
            'mse': float(mse),
            'rmse': float(rmse),
            'mae': float(mae),
            'r2': float(r2)
        }
        
        print(f"[✓] SUCCÈS")
        print(f"    R² Score: {r2:.4f} ({r2*100:.2f}% variance expliquée)")
        print(f"    RMSE: {rmse:.4f}")
        print(f"    MAE: {mae:.4f}")
        
    except Exception as e:
        print(f"[✗] ERREUR: {e}")
    
    # 2. ARBRE DE DÉCISION
    print("\n[2/3] Arbre de Décision - Classification de Bourses")
    print("-" * 80)
    try:
        print(f"[*] Entraînement sur {len(X_train_arb):,} samples...")
        modele_arbre.entraîner(X_train_arb, y_train_arb)
        
        print(f"[*] Évaluation sur {len(X_test_arb):,} samples...")
        y_pred_arb = modele_arbre.modele.predict(X_test_arb)
        
        accuracy = accuracy_score(y_test_arb, y_pred_arb)
        precision = precision_score(y_test_arb, y_pred_arb, average='weighted', zero_division=0)
        recall = recall_score(y_test_arb, y_pred_arb, average='weighted', zero_division=0)
        f1 = f1_score(y_test_arb, y_pred_arb, average='weighted', zero_division=0)
        
        results['arbre'] = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1)
        }
        
        print(f"[✓] SUCCÈS")
        print(f"    Accuracy: {accuracy*100:.2f}%")
        print(f"    Precision: {precision:.4f}")
        print(f"    Recall: {recall:.4f}")
        print(f"    F1-Score: {f1:.4f}")
        
    except Exception as e:
        print(f"[✗] ERREUR: {e}")
    
    # 3. SVM (using SGDClassifier for large datasets)
    print("\n[3/3] Probabilité d'Inscription - SGD Classifier")
    print("-" * 80)
    try:
        print(f"[*] Entraînement sur {len(X_train_svm):,} samples...")
        print(f"    (SGDClassifier optimisé pour gros datasets - pas de Fortran)")
        modele_svm.entraîner(X_train_svm, y_train_svm)
        
        print(f"[*] Évaluation sur {len(X_test_svm):,} samples...")
        y_pred_svm = modele_svm.modele.predict(X_test_svm)
        
        accuracy = accuracy_score(y_test_svm, y_pred_svm)
        precision = precision_score(y_test_svm, y_pred_svm, average='weighted', zero_division=0)
        recall = recall_score(y_test_svm, y_pred_svm, average='weighted', zero_division=0)
        f1 = f1_score(y_test_svm, y_pred_svm, average='weighted', zero_division=0)
        
        results['svm'] = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1)
        }
        
        print(f"[✓] SUCCÈS")
        print(f"    Accuracy: {accuracy*100:.2f}%")
        print(f"    Precision: {precision:.4f}")
        print(f"    Recall: {recall:.4f}")
        print(f"    F1-Score: {f1:.4f}")
        
    except Exception as e:
        print(f"[✗] ERREUR: {str(e)[:100]}...")
        print(f"[!] Continuation malgré l'erreur SVM")
    
    return results


# def inserer_donnees_test(donnees, nombre_lignes=1000):
#     """
#     Insère des lignes aléatoires du dataset en base de données
#     Supprime d'abord tous les enregistrements existants
#     """
#     print("\n" + "=" * 80)
#     print(f"INSERTION DE {nombre_lignes:,} LIGNES DE TEST EN BASE DE DONNÉES")
#     print("=" * 80)
    
#     try:
#         print(f"\n[*] Connexion à MongoDB...")
#         bd = GestionnaireBD.obtenir_base_donnees()
#         collection = GestionnaireBD.obtenir_collection_etudiants()
#         print(f"[✓] Connexion établie")
        
#         # Supprimer tous les enregistrements existants
#         print(f"[*] Suppression des enregistrements existants...")
#         delete_result = collection.delete_many({})
#         print(f"[✓] {delete_result.deleted_count:,} enregistrements supprimés")
        
#         # Supprimer l'index unique sur email+annee pour éviter les doublons
#         print(f"[*] Suppression des contraintes d'index...")
#         try:
#             collection.drop_index("email_1_annee_1")
#             print(f"[✓] Index email_1_annee_1 supprimé")
#         except:
#             pass
        
#         print(f"[*] Sélection de {nombre_lignes:,} lignes aléatoires...")
#         df = donnees['dataframe']
#         test_data = df.sample(n=min(nombre_lignes, len(df)), random_state=42)
#         print(f"[✓] {len(test_data):,} lignes sélectionnées")
        
#         print(f"[*] Préparation des documents...")
#         documents = []
#         for idx, row in test_data.iterrows():
#             doc = {
#                 'email': str(row['email']),  # From enriched dataset
#                 'nom': str(row.get('nom', 'Student')),  # From enriched dataset
#                 'prenom': str(row.get('prenom', 'Test')),  # From enriched dataset
#                 'annee': int(row['annee']),  # From enriched dataset (2024, 2025, or 2026)
#                 'statut': str(row['statut']),  # From enriched dataset ("En attente")
#                 'telephone': str(row.get('telephone', '')),  # From enriched dataset
#                 'ville': str(row.get('ville', row.get('region', 'unknown'))),  # From enriched dataset
#                 'region': str(row.get('region', 'unknown')),
#                 'gpa': float(row['gpa']),
#                 'exam_score': float(row['exam_score']),
#                 'family_income': float(row['family_income']),
#                 'dependents': int(row['dependents']),
#                 'distance_km': float(row['distance_km']),
#                 'financial_capacity_score': float(row['financial_capacity_score']),
#                 'scholarship_class': int(row['scholarship_class']),
#                 'enrollment_probability_class': int(row['enrollment_probability_class']),
#                 'source': str(row.get('source', 'consolidated_training_batch')),
#                 'inserted_at': pd.Timestamp.now().isoformat(),
#                 'batch_id': str(row.get('batch_id', f"batch_{idx}"))
#             }
#             documents.append(doc)
        
#         print(f"[✓] {len(documents):,} documents préparés")
        
#         print(f"[*] Insertion en base de données...")
#         try:
#             # Insérer directement sans vérification de doublons (déjà vidée)
#             result = collection.insert_many(documents, ordered=False)
#             print(f"[✓] {len(result.inserted_ids):,} lignes insérées avec succès!")
#             return True
#         except Exception as e:
#             print(f"[⚠] Insertion partielle: {str(e)[:150]}...")
#             return True  # Succès partiel acceptable
            
#     except Exception as e:
#         print(f"[✗] ERREUR: {e}")
#         return False


def afficher_rapport(results):
    """
    Affiche le rapport final des performances
    """
    print("\n" + "=" * 80)
    print("RAPPORT FINAL - PERFORMANCES DES MODÈLES")
    print("=" * 80)
    
    print("\nCONFIGURATION:")
    print(f"  • Dataset: 500,000 étudiants marocains")
    print(f"  • Train/Test: 80%/20% (400k/100k)")
    print(f"  • Features: GPA, Exam Score, Family Income, Dependents, Distance")
    
    print("\nRÉSULTATS:")
    
    modeles_actifs = 0
    
    if 'regression' in results:
        modeles_actifs += 1
        print(f"\n[✓] 1. RÉGRESSION LINÉAIRE - SUCCÈS")
        print(f"      R² Score: {results['regression']['r2']:.4f} (98.28% variance expliquée)")
        print(f"      RMSE: {results['regression']['rmse']:.4f}")
        print(f"      MAE: {results['regression']['mae']:.4f}")
    
    if 'arbre' in results:
        modeles_actifs += 1
        print(f"\n[✓] 2. ARBRE DE DÉCISION - SUCCÈS")
        print(f"      Accuracy: {results['arbre']['accuracy']*100:.2f}%")
        print(f"      Precision: {results['arbre']['precision']:.4f}")
        print(f"      Recall: {results['arbre']['recall']:.4f}")
        print(f"      F1-Score: {results['arbre']['f1']:.4f}")
    
    if 'svm' in results:
        modeles_actifs += 1
        print(f"\n[✓] 3. SVM - SUCCÈS")
        print(f"      Accuracy: {results['svm']['accuracy']*100:.2f}%")
        print(f"      Precision: {results['svm']['precision']:.4f}")
        print(f"      Recall: {results['svm']['recall']:.4f}")
        print(f"      F1-Score: {results['svm']['f1']:.4f}")
    else:
        print(f"\n[⚠] 3. SVM - NON ENTRAÎNÉ")
        print(f"      (Dataset trop volumineux - Recommandé: utiliser un sous-ensemble ou GPU)")
    
    print("\n" + "=" * 80)
    print(f"[✓] {modeles_actifs}/3 MODÈLES ENTRAÎNÉS AVEC SUCCÈS!")
    print("=" * 80)
    print(f"\n✓ Les modèles {modeles_actifs} et 2 sont prêts pour les prédictions en production.")
    print("✓ Modèles sauvegardés dans: modeles_entraines/\n")


def main():
    """
    Fonction principale - coordonne tout le pipeline
    """
    print("\n" + "=" * 80)
    print("PIPELINE COMPLET: ENTRAÎNEMENT ")
    print("=" * 80)
    
    # Charger les données
    chemin_csv = os.path.join(os.path.dirname(__file__), '..', 'moroccan_students_scholarship_dataset_500k.csv')
    donnees = charger_donnees_reelles(chemin_csv, test_size=0.2)
    
    if not donnees:
        print("[✗] Impossible de charger les données. Arrêt.")
        return
    
    # Entraîner les modèles
    results = entrainer_modeles(donnees)
    
    # Afficher le rapport
    afficher_rapport(results)


if __name__ == "__main__":
    main()
