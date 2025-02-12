// Conectando ao banco de dados 'mydatabase'
db = db.getSiblingDB('mydatabase');

// Criação das coleções para os dados que serão inseridos
db.createCollection('clientes');
db.createCollection('pedidos');
db.createCollection('vendedores');

// (Opcional) Criação de índices para facilitar as buscas
db.clientes.createIndex({ "cliente_id": 1 });
db.pedidos.createIndex({ "pedido_id": 1 });
db.vendedores.createIndex({ "vendedor_id": 1 });

print("Banco de dados e coleções configurados com sucesso!");
