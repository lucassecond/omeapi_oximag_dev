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
        logging.info("Conectado ao MongoDB!")
        return db
    except Exception as e:
        logging.error(f"Erro ao conectar ao MongoDB: {e}")
        return None

def connect_postgresql():
    """Conecta ao PostgreSQL e retorna a conexão."""
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            database=PG_DATABASE,
            user=PG_USER,
            password=PG_PASSWORD
        )
        logging.info("Conectado ao PostgreSQL!")
        return conn
    except Exception as e:
        logging.error(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

def create_tables(conn):
    """Cria as tabelas no PostgreSQL, se não existirem."""
    queries = [
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nome TEXT,
            email TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS faturamento (
            id SERIAL PRIMARY KEY,
            pedido_id TEXT,
            valor_total NUMERIC
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS vendedores (
            id SERIAL PRIMARY KEY,
            nome TEXT,
            comissao NUMERIC
        );
        """
    ]

    try:
        with conn.cursor() as cursor:
            for query in queries:
                cursor.execute(query)
        conn.commit()
        logging.info("Tabelas verificadas/criadas com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao criar tabelas: {e}")

def import_data_mongo_to_postgres():
    """Extrai os dados do MongoDB e insere no PostgreSQL."""
    db_mongo = connect_mongodb()
    conn_pg = connect_postgresql()

    if db_mongo is None or conn_pg is None:
        logging.error("Falha ao conectar aos bancos. Abortando...")
        return

    create_tables(conn_pg)

    collections = {
        "clientes": "clientes",
        "faturamento": "faturamento",
        "vendedores": "vendedores"
    }

    try:
        with conn_pg.cursor() as cursor:
            for mongo_collection, postgres_table in collections.items():
                logging.info(f"Importando dados de {mongo_collection} para {postgres_table}...")

                mongo_data = list(db_mongo[mongo_collection].find())

                if not mongo_data:
                    logging.warning(f"Nenhum dado encontrado na coleção {mongo_collection}. Pulando...")
                    continue

                for doc in mongo_data:
                    if mongo_collection == "clientes":
                        cursor.execute(
                            "INSERT INTO clientes (nome, email) VALUES (%s, %s)",
                            (doc.get("nome"), doc.get("email"))
                        )
                    elif mongo_collection == "faturamento":
                        cursor.execute(
                            "INSERT INTO faturamento (pedido_id, valor_total) VALUES (%s, %s)",
                            (doc.get("pedido_id"), doc.get("valor_total"))
                        )
                    elif mongo_collection == "vendedores":
                        cursor.execute(
                            "INSERT INTO vendedores (nome, comissao) VALUES (%s, %s)",
                            (doc.get("nome"), doc.get("comissao"))
                        )

            conn_pg.commit()
            logging.info("Dados importados com sucesso!")

    except Exception as e:
        logging.error(f"Erro ao importar dados: {e}")
    finally:
        conn_pg.close()

if __name__ == "__main__":
    import_data_mongo_to_postgres()
