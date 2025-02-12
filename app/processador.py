import os
import json
import psycopg2
from pymongo import MongoClient

data_dir = "/app/data"

# Conexão MongoDB
mongo_client = MongoClient(f"mongodb://admin:secret@mongodb:27017/mydatabase")
mongo_db = mongo_client["mydatabase"]

# Conexão PostgreSQL
pg_conn = psycopg2.connect(dbname="mydatabase", user="admin", password="secret", host="postgres")
pg_cursor = pg_conn.cursor()

def process_json(filename):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, "r") as file:
        data = json.load(file)

        # Insere no MongoDB
        collection = mongo_db[filename.replace(".json", "")]
        collection.insert_many(data if isinstance(data, list) else [data])
        print(f"{filename} inserido no MongoDB.")

        # Insere no PostgreSQL
        pg_cursor.execute("INSERT INTO dados (json_data) VALUES (%s)", (json.dumps(data),))
        pg_conn.commit()
        print(f"{filename} inserido no PostgreSQL.")

        # Remove o arquivo processado
        os.remove(filepath)

while True:
    for file in os.listdir(data_dir):
        if file.endswith(".json"):
            process_json(file)
