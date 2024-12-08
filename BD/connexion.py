import psycopg2
from psycopg2 import pool, sql

# Configuration centralisée de la base de données
DB_CONFIG = {
    "dbname": "Serie_SAE_S5",
    "user": "postgres",
    "password": "$iutinfo",
    "host": "127.0.0.1",
    "port": "5432"
}
class DatabasePool:
    _instance = None
    
    @staticmethod
    def get_instance():
        if DatabasePool._instance is None:
            DatabasePool._instance = DatabasePool()
        return DatabasePool._instance
    
    def __init__(self):
        self.pool = pool.SimpleConnectionPool(
            1,  # minimum de connexions
            5,  # maximum de connexions
            **DB_CONFIG  # Utilisation de la configuration globale
        )
    
    def get_connection(self):
        return self.pool.getconn()
    
    def release_connection(self, conn):
        self.pool.putconn(conn)
        
    def close(self):
        self.pool.closeall()