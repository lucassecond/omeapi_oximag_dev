import requests
import json
import os

# Configuração do diretório de saída
data_dir = "/app/data"
os.makedirs(data_dir, exist_ok=True)

# Configuração da API Omie
URL = "https://app.omie.com.br/api/v1/produtos/pedido/#ListarPedidos"
APP_KEY = "1092958907040"
APP_SECRET = "f89956dec1af07e9334ccca7e2e78710"
REGISTROS_POR_PAGINA = 500  # Ajustável conforme necessário

def obter_todos_pedidos():
    pagina = 1
    pedidos_totais = []

    while True:
        # Configura os parâmetros da requisição
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
                    "data_faturamento_de": "11/02/2025",
                    "data_faturamento_ate": "11/02/2025"
                }
            ]
        }

        # Faz a requisição à API
        response = requests.post(URL, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            data = response.json()
            pedidos = data.get("pedidos", [])  # Ajuste conforme a estrutura do JSON da API

            if not pedidos:
                break  # Sai do loop quando não houver mais pedidos

            pedidos_totais.extend(pedidos)  # Adiciona os pedidos à lista total
            print(f"Página {pagina} carregada. Total acumulado: {len(pedidos_totais)} pedidos.")
            pagina += 1  # Passa para a próxima página

        else:
            print(f"Erro ao obter pedidos: {response.status_code}")
            break

    return pedidos_totais

def salvar_pedidos(pedidos):
    """Salva os pedidos no arquivo JSON"""
    if not pedidos:
        print("Nenhum pedido encontrado para salvar.")
        return

    with open(os.path.join(data_dir, "faturamento.json"), "w", encoding="utf-8") as json_file:
        json.dump(pedidos, json_file, ensure_ascii=False, indent=4)

    print(f"Arquivo 'faturamento.json' salvo com sucesso! ({len(pedidos)} registros)")

# Chama a função para buscar todos os pedidos e salvar
pedidos = obter_todos_pedidos()
salvar_pedidos(pedidos)
