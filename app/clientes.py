import requests
import json
import os

# Configuração do diretório de saída
data_dir = "/app/data"
os.makedirs(data_dir, exist_ok=True)

# Configuração da API Omie
URL = "https://app.omie.com.br/api/v1/geral/clientes/"
APP_KEY = "1092958907040"
APP_SECRET = "f89956dec1af07e9334ccca7e2e78710"
REGISTROS_POR_PAGINA = 500  # Máximo suportado pela API

def obter_todos_clientes():
    pagina = 1
    clientes_totais = []

    while True:
        # Configura os parâmetros da requisição
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

        # Faz a requisição à API
        response = requests.post(URL, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            data = response.json()
            clientes = data.get("clientes_cadastro", [])

            if not clientes:
                break  # Sai do loop quando não houver mais clientes

            clientes_totais.extend(clientes)  # Adiciona à lista total
            print(f"Página {pagina} carregada. Total acumulado: {len(clientes_totais)} clientes.")
            pagina += 1  # Passa para a próxima página

        else:
            print(f"Erro ao obter clientes: {response.status_code}")
            break

    return clientes_totais

def salvar_clientes(clientes):
    """Salva os clientes no arquivo JSON"""
    if not clientes:
        print("Nenhum cliente encontrado para salvar.")
        return

    with open(os.path.join(data_dir, "clientes.json"), "w", encoding="utf-8") as json_file:
        json.dump(clientes, json_file, ensure_ascii=False, indent=4)

    print(f"Arquivo 'clientes.json' salvo com sucesso! ({len(clientes)} registros)")

# Chama a função para buscar todos os clientes e salvar
clientes = obter_todos_clientes()
salvar_clientes(clientes)
