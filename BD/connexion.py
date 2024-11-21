import psycopg2
from psycopg2 import sql

def connect_to_db(db_config):
    """
    Établit une connexion à la base de données PostgreSQL.
    
    :param db_config: Dictionnaire contenant les informations de connexion à la base de données.
    :return: Connexion et curseur à la base de données.
    """
    try:
        conn = psycopg2.connect(
            dbname=db_config["dbname"],
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"]
        )
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print("Erreur de connexion à la base de données :", e)
        raise