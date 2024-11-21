import psycopg2
from psycopg2 import sql
from connexion import connect_to_db

def find_best_series(user_input):
    """
    Trouve les 3 séries les plus pertinentes en fonction des mots-clés saisis par l'utilisateur.
    
    :param user_input: Chaîne de mots-clés (par exemple : "avion crash mystère").
    :return: Liste des 3 séries les plus probables (id_serie, total_score).
    """
    # Configuration de la base de données
    db_config = {
        "dbname": "Serie_SAE_S5",
        "user": "postgres",
        "password": "$iutinfo",
        "host": "127.0.0.1",  # ou "localhost"
        "port": "5432"
    }
    
    # Vérifie l'entrée utilisateur
    if not user_input.strip():
        print("Erreur : L'entrée utilisateur est vide ou invalide.")
        return []

    try:
        # Utilisation du gestionnaire de contexte pour gérer la connexion et le curseur
        with connect_to_db(db_config) as (conn, cursor):
            # Préparation de l'entrée utilisateur : éclate les mots en liste
            user_words = user_input.split()

            # Prépare la requête SQL
            query = sql.SQL("""
                WITH mots_recherches AS (
                    SELECT UNNEST(%s) AS word
                )
                SELECT s.titre , SUM(m.score_tf_idf) AS total_score
                FROM Mot m
                JOIN mots_recherches mr ON m.mot = mr.word
                JOIN Serie s ON s.id_serie = m.id_serie
                GROUP BY s.titre
                ORDER BY total_score DESC
                LIMIT 3;
            """)

            # Exécution de la requête
            cursor.execute(query, (user_words,))
            
            # Récupère les résultats
            results = cursor.fetchall()
            
            return results

    except Exception as e:
        print("Erreur lors de l'exécution de la requête ou de la connexion :", e)
        return []
