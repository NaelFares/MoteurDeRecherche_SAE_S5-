import unittest
import sys
import os
import time  # Importer le module time pour mesurer le temps d'exécution

# Obtenir le chemin absolu du répertoire parent (pour pouvoir importer depuis le dossier BD)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from BD.requete import verify_user, find_best_series, rate_series, create_user, delete_rating, filter_series
from BD.connexion import DatabasePool

class TestDatabaseOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour tous les tests"""
        # Connexion à la base de données de test
        cls.db_pool = DatabasePool.get_instance()
        cls.connection = cls.db_pool.get_connection()
        cls.cursor = cls.connection.cursor()
        
        # Nettoyage des données existantes
        cls.cursor.execute("DELETE FROM regarde;")
        cls.cursor.execute("DELETE FROM utilisateur;")
        
        # Réinitialisation des séquences
        cls.cursor.execute("ALTER SEQUENCE utilisateur_id_utilisateur_seq RESTART WITH 1;")
        cls.cursor.execute("ALTER SEQUENCE serie_id_serie_seq RESTART WITH 1;")

        # Créer les données de test
        cls.cursor.execute("INSERT INTO utilisateur (login, mdp) VALUES ('test_user', 'test_password');")
        cls.cursor.execute("INSERT INTO utilisateur (login, mdp) VALUES ('wrong_user', 'wrong_password');")
        cls.connection.commit()

    @classmethod
    def tearDownClass(cls):    
        cls.db_pool.release_connection(cls.connection)
        
    
    def test_verify_user_success(self):
        """Test de la vérification d'un utilisateur valide"""
        success, user_id = verify_user("test_user", "test_password")

        # Vérifications
        self.assertTrue(success, "L'utilisateur devrait être vérifié avec succès.")
        self.assertEqual(user_id, 1, "L'ID de l'utilisateur devrait être 1.")

    def test_verify_user_fail(self):
        """Test de la vérification d'un utilisateur invalide"""
        success, user_id = verify_user("wrong_user", "mauvais_mdp")

        # Vérifications
        self.assertFalse(success)
        self.assertIsNone(user_id)

    def test_find_best_series(self):
        """Test de la recherche des séries les plus pertinentes à partir des mots clés"""

        results = find_best_series("crash avion île")

        # Vérifications
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0][1], "lost")

    def test_find_best_series_performance(self):
        """Test de la performance"""
        
        start_time = time.time()  # Démarrer le temps
        results = find_best_series("crash avion île")
        execution_time = time.time() - start_time  # Calculer le temps d'exécution

        # Afficher le temps d'exécution
        print(f"Temps d'exécution de find_best_series : {execution_time:.4f} secondes")

        # Vérifications
        self.assertEqual(len(results), 3)
        self.assertLess(execution_time, 0.1, "Le temps d'exécution devrait être inférieur à 100 ms (quelques dixièmes de secondes).")

    def test_rate_series(self):
        """Test de la notation d'une série"""
        success = rate_series(1, 1, 5)  # Noter la série avec ID 1 par l'utilisateur avec ID 1

        # Vérifications
        self.assertTrue(success)

    def test_create_user(self):
        """Test de la création d'un utilisateur"""
        success = create_user("new_user", "new_password")

        # Vérifications
        self.assertTrue(success)
        
    def test_filter_series(self):
        """Test du filtrage des séries"""
        try:
            # Ajout d'une note pour s'assurer qu'elle existe avant le filtrage
            self.cursor.execute("INSERT INTO Regarde (id_serie, id_utilisateur, note) VALUES (1, 1, 5);")
            self.connection.commit()

            # Test avec un terme de recherche
            results = filter_series("24", 1)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][1], "24")  # Vérifie le titre
            self.assertEqual(results[0][2], 5)       # Vérifie la note

            # Test avec une chaîne vide (doit retourner toutes les séries)
            results = filter_series("", 1)
            self.assertEqual(len(results), 127) #Le nombre total de séries

        except Exception as e:
            self.connection.rollback()
            raise e

    def test_delete_rating(self):
        """Test de la suppression d'une note"""
        # Ajout d'une note à supprimer
        self.cursor.execute("INSERT INTO Regarde (id_serie, id_utilisateur, note) VALUES (1, 1, 5);")
        self.connection.commit()

        success = delete_rating(1, 1)  # Supprime la note de la série avec ID 1 pour l'utilisateur avec ID 1

        # Vérifications
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2)  # Exécution des tests avec affichage détaillé 