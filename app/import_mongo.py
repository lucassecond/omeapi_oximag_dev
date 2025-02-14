import os
import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DATA_DIR = "/data"
MONGO_DB = "omie_db"
COLLECTIONS = {
    "clientes": "clientes.json",
    "faturamento": "faturamento.json",
    "vendedores": "vendedores.json",
}

logging.info("Aguardando MongoDB iniciar...")
time.sleep(10)

for collection, filename in COLLECTIONS.items():
    json_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(json_path):
        logging.info(f"Importando {filename} para {collection}...")
        subprocess.run(["mongoimport", "--db", MONGO_DB, "--collection", collection, "--file", json_path, "--jsonArray"], check=True)
        logging.info(f"Importação de {collection} concluída!")
    else:
        logging.warning(f"Arquivo {filename} não encontrado.")

logging.info("Importação finalizada.")