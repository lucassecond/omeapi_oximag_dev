import os
import time
import subprocess
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Diretório onde os JSONs estão armazenados
DATA_DIR = "/data"

# Banco de dados e collections
MONGO_DB = "omie_db"
COLLECTIONS = {
    "clientes": "clientes.json",
    "faturamento": "faturamento.json",
    "vendedores": "vendedores.json",
}

# Aguardar o MongoDB ficar pronto
logging.info("Aguardando MongoDB iniciar...")
time.sleep(10)

# Verifica se os arquivos JSON existem e importa para o MongoDB
for collection, filename in COLLECTIONS.items():
    json_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(json_path):
        logging.info(f"Importando {filename} para a coleção {collection}...")
        try:
            subprocess.run(
                [
                    "mongoimport",
                    "--db", MONGO_DB,
                    "--collection", collection,
                    "--file", json_path,
                    "--jsonArray"
                ],
                check=True
            )
            logging.info(f"Importação de {collection} concluída com sucesso!")
        except subprocess.CalledProcessError as e:
            logging.error(f"Erro ao importar {collection}: {e}")
    else:
        logging.warning(f"Arquivo {filename} não encontrado. Pulando importação.")

logging.info("Importação de JSONs concluída.")
