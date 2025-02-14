import psycopg2
from pymongo import MongoClient
import logging

# Configuração do Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do MongoDB
MONGO_URI = "mongodb://mongodb:27017/"
MONGO_DB_NAME = "omie_db"

# Configuração do PostgreSQL
PG_HOST = "postgres"
PG_PORT = "5432"
PG_DATABASE = "db_omieoximag"
PG_USER = "omieapi"
PG_PASSWORD = "admin123%"

def connect_mongodb():
    """Conecta ao MongoDB e retorna o banco de dados."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
       
::contentReference[oaicite:0]{index=0}
 
