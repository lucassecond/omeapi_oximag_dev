import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import tempfile
from app.main import write_json_atomic

def test_write_json_atomic(tmp_path):
    data = {"teste": True}
    target_file = tmp_path / "arquivo.json"
    write_json_atomic(data, str(target_file))
    
    # Verifica se o arquivo foi criado
    assert os.path.exists(target_file)
    
    # Verifica se o conteúdo do arquivo é o esperado
    with open(target_file) as f:
        conteudo = json.load(f)
    assert conteudo == data
