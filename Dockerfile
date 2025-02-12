# Usando a imagem oficial do Python como base
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os requisitos (se você estiver usando um arquivo requirements.txt)
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para o contêiner
COPY . /app/

# Comando padrão para rodar sua aplicação (ajuste conforme necessário)
CMD ["python3", "/app/consulta_omie.py"]
