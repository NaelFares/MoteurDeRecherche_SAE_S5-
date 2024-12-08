from requete import find_best_series
from connexion import DatabasePool

def test_recherche_series():
    """
    Fonction de test pour la recherche de séries
    """
    print("=== Test de recherche de séries ===")
    
    # Test avec différents mots-clés
    tests = [
        "crash avion île",
        "voisines secret",
        "amour drame",
    ]

    for test_input in tests:
        print(f"\nRecherche pour : '{test_input}'")
        try:
            resultats = find_best_series(test_input)
            if resultats:
                print("Séries trouvées :")
                for titre, score in resultats:
                    # Affichage direct du score sans conversion
                    print(f"- {titre:<40} (score: {score})")
            else:
                print("Aucune série trouvée")
        except Exception as e:
            print(f"Erreur lors du test : {e}")

def main():
    try:
        # Test de la connexion à la base de données
        print("Test de connexion à la base de données...")
        db_pool = DatabasePool.get_instance()
        conn = db_pool.get_connection()
        if conn:
            print("✓ Connexion à la base de données réussie")
            db_pool.release_connection(conn)
        
        # Exécution des tests de recherche
        test_recherche_series()
        
    except Exception as e:
        print(f"Erreur critique : {e}")
    finally:
        # Fermeture propre du pool de connexions
        DatabasePool.get_instance().close()

if __name__ == "__main__":
    main() 