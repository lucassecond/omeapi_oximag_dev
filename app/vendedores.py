import requests
import json
import os

# Configuração do diretório de saída
data_dir = "/app/data"
os.makedirs(data_dir, exist_ok=True)

# Configuração da API Omie
URL = "https://app.omie.com.br/api/v1/geral/vendedores/"
APP_KEY = "1092958907040"
APP_SECRET = "f89956dec1af07e9334ccca7e2e78710"
REGISTROS_POR_PAGINA = 100  # Máximo permitido pela API

def obter_vendedores():
    # Configura os parâmetros da requisição
    payload = {
        "call": "ListarVendedores",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": [
            {
                "pagina": 1,
                "registros_por_pagina": REGISTROS_POR_PAGINA,
                "apenas_importado_api": "N"
            }
        ]
    }

    # Faz a requisição à API
    response = requests.post(URL, json=payload, headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        vendedores_data = response.json()
        
        # Verifica se os dados de vendedores estão presentes na resposta
        if 'cadastro' in vendedores_data:
            return vendedores_data['cadastro']
        else:
            print("Erro: Nenhum vendedor encontrado.")
            return []
    else:
        print(f"Erro ao obter vendedores: {response.status_code}")
        return []

def salvar_vendedores(vendedores):
    """Salva os vendedores no arquivo JSON"""
    if not vendedores:
        print("Nenhum vendedor encontrado para salvar.")
        return

    # Salva os vendedores no arquivo JSON
    with open(os.path.join(data_dir, "vendedores.json"), "w", encoding="utf-8") as json_file:
        json.dump(vendedores, json_file, ensure_ascii=False, indent=4)
    
    print("Arquivo 'vendedores.json' salvo com sucesso!")

# Chama a função para obter os vendedores e salvar os dados
vendedores = obter_vendedores()
salvar_vendedores(vendedores)
