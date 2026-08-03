"""
Module de gestion de la base de données MongoDB
Gère les connexions et les collections
"""
from pymongo import MongoClient
import os
from config.parametres import URL_MONGODB, NOM_BASE_DONNEES

class GestionnaireBD:
    """
    Gestionnaire centralisé pour les connexions MongoDB
    Utilise le pattern Singleton pour une seule instance
    """
    _client = None
    _base_donnees = None

    @classmethod
    def connecter(cls):
        """
        Établit la connexion à MongoDB
        Lance une exception si la connexion échoue
        """
        try:
            cls._client = MongoClient(URL_MONGODB)
            cls._base_donnees = cls._client[NOM_BASE_DONNEES]
            # Vérifier la connexion avec une commande ping
            cls._base_donnees.command('ping')
            print("[✓] Connecté à MongoDB avec succès")
            return True
        except Exception as e:
            print(f"[✗] Échec de la connexion à MongoDB: {e}")
            raise

    @classmethod
    def deconnecter(cls):
        """Ferme la connexion à MongoDB"""
        if cls._client:
            cls._client.close()
            print("[✓] Déconnecté de MongoDB")

    @classmethod
    def obtenir_base_donnees(cls):
        """
        Retourne l'instance de la base de données
        Établit la connexion si elle n'existe pas
        """
        if cls._base_donnees is None:
            cls.connecter()
        return cls._base_donnees

    @classmethod
    def obtenir_collection_etudiants(cls):
        """Retourne la collection des étudiants"""
        bd = cls.obtenir_base_donnees()
        return bd["etudiants"]

    @classmethod
    def obtenir_collection_predictions(cls):
        """Retourne la collection des résultats de prédiction"""
        bd = cls.obtenir_base_donnees()
        return bd["predictions"]

    @classmethod
    def obtenir_collection_statistiques(cls):
        """Retourne la collection des statistiques agrégées"""
        bd = cls.obtenir_base_donnees()
        return bd["statistiques"]

    @classmethod
    def obtenir_collection_quotas(cls):
        """Retourne la collection des quotas de bourses par année"""
        bd = cls.obtenir_base_donnees()
        return bd["quotas_bourses"]

    @classmethod
    def initialiser_indices(cls):
        """Crée les indices de la base de données pour optimiser les requêtes"""
        try:
            collection = cls.obtenir_collection_etudiants()
            
            # Vérifier et nettoyer les anciens indices
            indices_existants = collection.list_indexes()
            for index_info in indices_existants:
                if index_info['name'] != '_id_':
                    try:
                        collection.drop_index(index_info['name'])
                    except:
                        pass
            
            # Index compound sur email + année (permet même email dans années différentes)
            collection.create_index([("email", 1), ("annee", 1)], unique=True)
            
            # Index sur la date de création
            cls.obtenir_collection_predictions().create_index("dateCreation")
            print("[✓] Indices de la base de données créés")
        except Exception as e:
            print(f"[⚠] Avertissement lors de la création des indices: {e}")


def initialiser_bd():
    """Initialise la connexion à la base de données"""
    GestionnaireBD.connecter()
    GestionnaireBD.initialiser_indices()


def fermer_bd():
    """Ferme la connexion à la base de données"""
    GestionnaireBD.deconnecter()
