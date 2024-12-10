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
            
def filter_series(user_input):
    """
    Trouve la série en fonction de l'entrée dans la barre de recherche dans la fenetre "Noter"
    
    :return: Liste des séries les plus probables.
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
        
        # Normalisation de l'entrée utilisateur : minuscules et suppression des espaces
        normalized_input = f"%{user_input.lower().replace(' ', '')}%"
        
        query = sql.SQL("""
            SELECT s.titre
            FROM Serie s 
            WHERE LOWER(REPLACE(s.titre, ' ', '')) ILIKE %s
            LIMIT 3;
        """)
        
        cursor.execute(query, (normalized_input,))
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
            
            
            
def create_user(login, mdp):
    """
    Crée un nouvel utilisateur dans la base de données.
    
    :param login: Login de l'utilisateur
    :param mdp: Mot de passe de l'utilisateur
    :return: True si la création est réussie, False sinon
    """
    db_pool = DatabasePool.get_instance()
    conn = None

    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        
        query = sql.SQL("""
            INSERT INTO Utilisateur (login, mdp)
            VALUES (%s, %s)
            RETURNING id_utilisateur;
        """)
        
        cursor.execute(query, (login, mdp))
        id_utilisateur = cursor.fetchone()[0]
        conn.commit()
        
        return True

    except Exception as e:
        print("Erreur lors de la création de l'utilisateur :", e)
        conn.rollback()
        return False
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.release_connection(conn)
            
            
def verify_user(login, mdp):
    """
    Vérifie si l'utilisateur existe et si le mot de passe correspond.
    
    :param login: Login de l'utilisateur
    :param mdp: Mot de passe de l'utilisateur
    :return: (bool, int) - (True et id_utilisateur si connexion réussie, False et None sinon)
    """
    db_pool = DatabasePool.get_instance()
    conn = None

    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        
        query = sql.SQL("""
            SELECT id_utilisateur
            FROM Utilisateur
            WHERE login = %s AND mdp = %s;
        """)
        
        cursor.execute(query, (login, mdp))
        result = cursor.fetchone()
        
        if result:
            return True, result[0]  # Retourne True et l'id_utilisateur
        return False, None  # Retourne False et None si l'utilisateur n'existe pas

    except Exception as e:
        print("Erreur lors de la vérification de l'utilisateur :", e)
        return False, None
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.release_connection(conn)