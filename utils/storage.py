"""
Storage utilities - JSON load/save functions.
"""
import os
import json
import logging
from typing import Any

log = logging.getLogger("MaftyIntel")


def p(filename: str) -> str:
    """
    Retorna o caminho para um arquivo, garantindo que arquivos de dados (.json) 
    fiquem na pasta 'data/' para persistência (Docker Volumes).
    """
    if filename.endswith(".json") and not filename.startswith("data"):
        data_dir = os.path.join(os.getcwd(), "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
        return os.path.join("data", filename)
        
    return os.path.abspath(filename)


def load_json_safe(filepath: str, default: Any) -> Any:
    """
    Carrega JSON sem derrubar o bot se faltar / vazio / corrompido.
    
    Args:
        filepath: Caminho do arquivo JSON
        default: Valor padrão se falhar
    
    Returns:
        Dados do JSON ou valor padrão
    """
    try:
        if not os.path.exists(filepath):
            log.warning(f"Arquivo '{filepath}' não existe. Usando padrão.")
            return default
        if os.path.getsize(filepath) == 0:
            log.warning(f"Arquivo '{filepath}' está vazio. Usando padrão.")
            return default
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log.error(f"Falha ao carregar '{filepath}': {e}. Usando padrão.")
        return default


def save_json_safe(filepath: str, data: Any) -> None:
    """
    Salva JSON com indentação; em erro, loga e segue.
    
    Args:
        filepath: Caminho do arquivo JSON
        data: Dados a salvar
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        log.error(f"Falha ao salvar '{filepath}': {e}")
