-- Criação do banco de dados
CREATE DATABASE mydatabase;

-- Criação da tabela para armazenar os dados JSON
CREATE TABLE dados (
    id SERIAL PRIMARY KEY,
    json_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exemplo de índice, se necessário
CREATE INDEX idx_json_data ON dados USING gin (json_data);

-- Confirma que a tabela foi criada corretamente
SELECT * FROM dados;
