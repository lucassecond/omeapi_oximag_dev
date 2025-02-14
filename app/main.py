import json
import os
import tempfile
import logging
import requests
from datetime import datetime

# Configuração básica do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

def write_json_atomic(data, target_path):
    """Escreve dados JSON de forma atômica para evitar a leitura de arquivos parcialmente gravados."""
    dir_name = os.path.dirname(target_path)
    os.makedirs(dir_name, exist_ok=True)
    
    with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False, suffix=".tmp") as tmp_file:
        json.dump(data, tmp_file, indent=4, ensure_ascii=False)
        temp_path = tmp_file.name
    
    os.rename(temp_path, target_path)
    logging.info("Arquivo '%s' gerado com sucesso.", target_path)

def consulta_api(url, payload):
    """Realiza uma requisição POST na API da Omie."""
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error("Erro na consulta à API (%s): %s", url, e)
        return None

def generate_clientes():
    """Consulta a API Omie para obter a lista de clientes e gera 'clientes.json'."""
    APP_KEY = "1092958907040"
    APP_SECRET = "f89956dec1af07e9334ccca7e2e78710"
    URL = "https://app.omie.com.br/api/v1/geral/clientes/"
    REGISTROS_POR_PAGINA = 500

    pagina = 1
    clientes_totais = []
    logging.info("Iniciando consulta de clientes...")

    while True:
        payload = {
            "call": "ListarClientes",
            "app_key": APP_KEY,
            "app_secret": APP_SECRET,
            "param": [
                {
                    "pagina": pagina,
                    "registros_por_pagina": REGISTROS_POR_PAGINA,
                    "apenas_importado_api": "N"
                }
            ]
        }

        data = consulta_api(URL, payload)
        if data and "clientes_cadastro" in data and data["clientes_cadastro"]:
            clientes_totais.extend(data["clientes_cadastro"])
            logging.info("Página %s carregada. Total acumulado: %d clientes.", pagina, len(clientes_totais))
            pagina += 1
        else:
            logging.info("Nenhum dado adicional encontrado na página %s.", pagina)
            break

    write_json_atomic(clientes_totais, "/data/clientes.json")

def generate_faturamento():
    """Consulta a API Omie para listar pedidos faturados e gera 'faturamento.json'."""
    APP_KEY = "1092958907040"
    APP_SECRET = "f89956dec1af07e9334ccca7e2e78710"
    URL = "https://app.omie.com.br/api/v1/produtos/pedido/"
    REGISTROS_POR_PAGINA = 500

    data_inicio = "01/01/2020"
    data_fim = datetime.now().strftime("%d/%m/%Y")

    pagina = 1
    pedidos_totais = []
    logging.info(f"Consultando API de faturamento de {data_inicio} até {data_fim}...")

    while True:
        payload = {
            "call": "ListarPedidos",
            "app_key": APP_KEY,
            "app_secret": APP_SECRET,
            "param": [
                {
                    "pagina": pagina,
                    "registros_por_pagina": REGISTROS_POR_PAGINA,
                    "apenas_importado_api": "N",
                    "status_pedido": "FATURADO",
                    "data_faturamento_de": data_inicio,
                    "data_faturamento_ate": data_fim
                }
            ]
        }

        data = consulta_api(URL, payload)
        if data and "pedido_cadastro" in data and data["pedido_cadastro"]:
            pedidos_totais.extend(data["pedido_cadastro"])
            logging.info("Página %s carregada. Total acumulado: %d pedidos.", pagina, len(pedidos_totais))
            pagina += 1
        else:
            logging.info("Nenhum dado adicional encontrado na página %s.", pagina)
            break

    write_json_atomic(pedidos_totais, "/data/faturamento.json")

def generate_vendedores():
    """Consulta a API Omie para obter a lista de vendedores e gera 'vendedores.json'."""
    APP_KEY = "1092958907040"
    APP_SECRET = "f89956dec1af07e9334ccca7e2e78710"
    URL = "https://app.omie.com.br/api/v1/geral/vendedores/"
    REGISTROS_POR_PAGINA = 500

    pagina = 1
    vendedores_totais = []
    logging.info("Iniciando consulta de vendedores...")

    while True:
        payload = {
            "call": "ListarVendedores",
            "app_key": APP_KEY,
            "app_secret": APP_SECRET,
            "param": [
                {
                    "pagina": pagina,
                    "registros_por_pagina": REGISTROS_POR_PAGINA,
                    "apenas_importado_api": "N"
                }
            ]
        }

        data = consulta_api(URL, payload)
        if data and "cadastro" in data and data["cadastro"]:
            vendedores_totais.extend(data["cadastro"])
            logging.info("Página %s carregada. Total acumulado: %d vendedores.", pagina, len(vendedores_totais))
            pagina += 1
        else:
            logging.info("Nenhum dado adicional encontrado na página %s.", pagina)
            break

    write_json_atomic(vendedores_totais, "/data/vendedores.json")

def main():
    logging.info("Iniciando a consulta à API e geração dos arquivos JSON...")
    
    generate_clientes()
    generate_faturamento()
    generate_vendedores()

    # Criando flag para indicar que a geração foi concluída
    flag_path = "/data/done.flag"
    try:
        with open(flag_path, 'w') as f:
            f.write("done")
        logging.info("Geração dos arquivos concluída com sucesso. Flag criada em: %s", flag_path)
    except Exception as e:
        logging.error("Erro ao criar flag de conclusão: %s", e)

if __name__ == "__main__":
    main()
