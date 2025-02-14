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
    client = MongoClient(MONGO_URI)
    return client[MONGO_DB_NAME]

def connect_postgresql():
    """Conecta ao PostgreSQL e retorna a conexão."""
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT, database=PG_DATABASE, user=PG_USER, password=PG_PASSWORD
    )

def import_data_mongo_to_postgres():
    """Importa todas as collections do MongoDB para PostgreSQL."""
    db_mongo = connect_mongodb()
    conn_pg = connect_postgresql()

    collections = ["clientes", "faturamento", "vendedores"]
    
    with conn_pg.cursor() as cursor:
        for collection in collections:
            logging.info(f"Importando dados de {collection}...")
            for doc in db_mongo[collection].find():
                cursor.execute(
                    f"INSERT INTO {collection} (data) VALUES (%s)",
                    [json.dumps(doc)]
                )
    
    conn_pg.commit()
    conn_pg.close()
    logging.info("Importação concluída com sucesso!")

if __name__ == "__main__":
    import_data_mongo_to_postgres()
