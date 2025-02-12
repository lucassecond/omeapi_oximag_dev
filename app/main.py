import json
import os
import tempfile
import logging
import requests

# Configuração básica do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

def write_json_atomic(data, target_path):
    """
    Escreve dados JSON de forma atômica para evitar a leitura de arquivos parcialmente gravados.
    """
    dir_name = os.path.dirname(target_path)
    with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False, suffix=".tmp") as tmp_file:
        json.dump(data, tmp_file, indent=4)
        temp_path = tmp_file.name
    os.rename(temp_path, target_path)

def generate_clientes():
    """
    Consulta a API Omie para obter a lista de clientes, paginando os resultados,
    e gera o arquivo JSON 'clientes.json' na pasta /data.
    """
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

        try:
            response = requests.post(
                URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                if "clientes_cadastro" in data and data["clientes_cadastro"]:
                    clientes_totais.extend(data["clientes_cadastro"])
                    logging.info("Página %s carregada. Total acumulado: %d clientes.", pagina, len(clientes_totais))
                    pagina += 1
                else:
                    logging.info("Nenhum dado adicional encontrado na página %s.", pagina)
                    break
            else:
                logging.error("Erro ao obter clientes: status code %s", response.status_code)
                break
        except Exception as e:
            logging.error("Erro na consulta de clientes: %s", e)
            break

    data_dir = '/data'
    os.makedirs(data_dir, exist_ok=True)
    target_path = os.path.join(data_dir, "clientes.json")
    write_json_atomic(clientes_totais, target_path)
    logging.info("Arquivo '%s' gerado com sucesso.", target_path)

def generate_faturamento():
    """
    Consulta a API Omie para listar pedidos faturados e gera o arquivo JSON 'faturamento.json' na pasta /data.
    """
    url = "https://app.omie.com.br/api/v1/produtos/pedido/#ListarPedidos"
    headers = {"Content-Type": "application/json"}
    payload = {
        "call": "ListarPedidos",
        "app_key": "1092958907040",
        "app_secret": "f89956dec1af07e9334ccca7e2e78710",
        "param": [
            {
                "pagina": 1,
                "registros_por_pagina": 99999999999,
                "apenas_importado_api": "N",
                "status_pedido": "FATURADO",
                "data_faturamento_de": "11/02/2025",
                "data_faturamento_ate": "11/02/2025"
            }
        ]
    }

    logging.info("Consultando API de faturamento...")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            data_dir = '/data'
            os.makedirs(data_dir, exist_ok=True)
            target_path = os.path.join(data_dir, "faturamento.json")
            write_json_atomic(data, target_path)
            logging.info("Arquivo '%s' gerado com sucesso.", target_path)
        else:
            logging.error("Erro na consulta de faturamento: status code %s", response.status_code)
    except Exception as e:
        logging.error("Erro na consulta de faturamento: %s", e)

def generate_vendedores():
    """
    Consulta a API Omie para obter a lista de vendedores e gera o arquivo JSON 'vendedores.json' na pasta /data.
    """
    url_vendedores = "https://app.omie.com.br/api/v1/geral/vendedores/"
    payload_vendedores = {
        "call": "ListarVendedores",
        "app_key": "1092958907040",
        "app_secret": "f89956dec1af07e9334ccca7e2e78710",
        "param": [
            {
                "pagina": 1,
                "registros_por_pagina": 100,
                "apenas_importado_api": "N"
            }
        ]
    }

    logging.info("Consultando API de vendedores...")
    try:
        response = requests.post(
            url_vendedores,
            json=payload_vendedores,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        if response.status_code == 200:
            vendedores_data = response.json()
            if 'cadastro' in vendedores_data:
                vendedores = vendedores_data['cadastro']
                data_dir = '/data'
                os.makedirs(data_dir, exist_ok=True)
                target_path = os.path.join(data_dir, "vendedores.json")
                write_json_atomic(vendedores, target_path)
                logging.info("Arquivo '%s' gerado com sucesso.", target_path)
            else:
                logging.error("Erro: Nenhum vendedor encontrado na resposta.")
        else:
            logging.error("Erro ao obter vendedores: status code %s", response.status_code)
    except Exception as e:
        logging.error("Erro na consulta de vendedores: %s", e)

def main():
    logging.info("Iniciando a consulta à API e geração dos arquivos JSON...")
    generate_clientes()
    generate_faturamento()
    generate_vendedores()

    # Cria um arquivo de flag para sinalizar que a geração foi concluída
    data_dir = '/data'
    os.makedirs(data_dir, exist_ok=True)
    flag_path = os.path.join(data_dir, "done.flag")
    try:
        with open(flag_path, 'w') as f:
            f.write("done")
        logging.info("Geração dos arquivos concluída com sucesso. Flag criada em: %s", flag_path)
    except Exception as e:
        logging.error("Erro ao criar flag de conclusão: %s", e)

if __name__ == "__main__":
    main()
