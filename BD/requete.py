from psycopg2 import sql
from .connexion import DatabasePool
#from connexion import DatabasePool

def find_best_series(user_input):
    """
    Trouve les 3 séries les plus pertinentes en fonction des mots-clés saisis par l'utilisateur.
    
    :param user_input: Chaîne de mots-clés (par exemple : "avion crash mystère").
    :return: Liste des 3 séries les plus probables (titre, total_score).
    """
    # Vérifie l'entrée utilisateur
    if not user_input.strip():
        print("Erreur : L'entrée utilisateur est vide ou invalide.")
        return []

    # Obtient l'instance du pool
    db_pool = DatabasePool.get_instance()
    conn = None

    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        
        user_words = user_input.split()
        query = sql.SQL("""
            WITH mots_recherches AS (
                SELECT UNNEST(%s) AS word
            )
            SELECT s.titre, SUM(m.score_tf_idf) AS total_score
            FROM Mot m
            JOIN mots_recherches mr ON m.mot = mr.word
            JOIN Serie s ON s.id_serie = m.id_serie
            GROUP BY s.titre
            ORDER BY total_score DESC
            LIMIT 3;
        """)
        
        cursor.execute(query, (user_words,))
        results = cursor.fetchall()
        conn.commit()
        
        return results

    except Exception as e:
        print("Erreur lors de l'exécution de la requête :", e)
        return []
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.release_connection(conn)
