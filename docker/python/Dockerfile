# Usa uma imagem base do Python
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY app/ /app/

# Instala dependências do projeto
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir requests pymongo psycopg2-binary

# Define o comando padrão para rodar o contêiner
CMD ["python", "/app/main.py"]
