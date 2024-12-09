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


def find_recommendations_from_favorites(id_utilisateur, limit_series=5):
    """
    Trouve des séries recommandées basées sur les mots-clés des séries préférées de l'utilisateur.
    
    :param id_utilisateur: ID de l'utilisateur
    :param limit_series: Nombre de séries à recommander (défaut: 5)
    :return: Liste des séries recommandées (titre, score)
    """
    db_pool = DatabasePool.get_instance()
    conn = None

    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        
        # 1. Récupère les mots-clés les plus pertinents des séries les mieux notées
        query_mots = sql.SQL("""
            WITH series_favorites AS (
                SELECT id_serie
                FROM Regarde
                WHERE id_utilisateur = %s
                AND note >= 4
                ORDER BY note DESC
                LIMIT 5
            ),
            mots_importants AS (
                SELECT DISTINCT ON (sf.id_serie) m.mot, m.score_tf_idf
                FROM series_favorites sf
                JOIN Mot m ON m.id_serie = sf.id_serie
                ORDER BY sf.id_serie, m.score_tf_idf DESC
            )
            SELECT mot FROM mots_importants;
        """)
        
        cursor.execute(query_mots, (id_utilisateur,))
        mots_cles = [row[0] for row in cursor.fetchall()]
        
        if not mots_cles:
            return []
            
        # 2. Trouve les séries correspondant à ces mots-clés
        query_series = sql.SQL("""
            WITH mots_recherches AS (
                SELECT UNNEST(%s) AS word
            )
            SELECT s.titre, SUM(m.score_tf_idf) AS total_score
            FROM Mot m
            JOIN mots_recherches mr ON m.mot = mr.word
            JOIN Serie s ON s.id_serie = m.id_serie
            LEFT JOIN Regarde r ON r.id_serie = s.id_serie AND r.id_utilisateur = %s
            WHERE r.id_serie IS NULL
            GROUP BY s.titre
            ORDER BY total_score DESC
            LIMIT %s;
        """)
        
        cursor.execute(query_series, (mots_cles, id_utilisateur, limit_series))
        results = cursor.fetchall()
        
        return results

    except Exception as e:
        print("Erreur lors de la recommandation :", e)
        return []
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.release_connection(conn)