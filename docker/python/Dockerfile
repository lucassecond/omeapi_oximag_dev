# docker/python/Dockerfile
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências e instala os pacotes
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY app/ .

# Define a variável de ambiente para produção
ENV PYTHON_ENV=production

# Executa o script principal
CMD ["python", "main.py"]
