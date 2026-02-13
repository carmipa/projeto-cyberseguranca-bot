"""
Utilitário para limpeza e gerenciamento do state.json.
Previne crescimento excessivo do arquivo que pode causar problemas de performance.
"""
import os
import logging
import time
from typing import Dict, Any, Tuple
from utils.storage import p, load_json_safe, save_json_safe

log = logging.getLogger("CyberIntel")

# Limites de tamanho
MAX_STATE_SIZE = 10 * 1024 * 1024  # 10 MB - limite crítico
WARN_STATE_SIZE = 5 * 1024 * 1024  # 5 MB - aviso e limpeza parcial
CLEANUP_INTERVAL = 604800  # 7 dias em segundos

# Limites de itens por seção
MAX_DEDUP_ITEMS = 2000  # Máximo de itens de deduplicação por feed
MAX_CACHE_ITEMS = 1000  # Máximo de itens de cache HTTP
MAX_HASHES_ITEMS = 100  # Máximo de hashes HTML


def get_state_size(state_file: str) -> int:
    """Retorna o tamanho do arquivo state.json em bytes."""
    try:
        return os.path.getsize(state_file) if os.path.exists(state_file) else 0
    except Exception as e:
        log.debug(f"Erro ao verificar tamanho de {state_file}: {e}")
        return 0


def cleanup_state(state: Dict[str, Any], reason: str = "Manual") -> Tuple[Dict[str, Any], Dict[str, int]]:
    """
    Limpa o state.json removendo dados antigos e excessivos.
    
    Args:
        state: Estado atual carregado
        reason: Motivo da limpeza (para logs)
    
    Returns:
        Tuple (state_cleaned, stats) onde stats contém contadores antes/depois
    """
    stats_before = {
        "dedup": len(state.get("dedup", {})),
        "http_cache": len(state.get("http_cache", {})),
        "html_hashes": len(state.get("html_hashes", {}))
    }
    
    # Limpa dedup (mais crítico - pode crescer muito)
    dedup = state.get("dedup", {})
    if isinstance(dedup, dict):
        dedup_count = sum(len(v) if isinstance(v, (list, dict)) else 1 for v in dedup.values())
        if dedup_count > MAX_DEDUP_ITEMS:
            log.info(f"🧹 Limpando dedup: {dedup_count} itens -> 0")
            state["dedup"] = {}
        else:
            # Limpa feeds individuais que têm muitos itens
            cleaned_feeds = 0
            for feed_url, items in list(dedup.items()):
                if isinstance(items, list) and len(items) > 500:
                    dedup[feed_url] = items[-500:]  # Mantém últimos 500
                    cleaned_feeds += 1
            if cleaned_feeds > 0:
                log.info(f"🧹 Limpeza parcial de {cleaned_feeds} feeds no dedup")
    
    # Limpa http_cache
    http_cache = state.get("http_cache", {})
    if isinstance(http_cache, dict) and len(http_cache) > MAX_CACHE_ITEMS:
        log.info(f"🧹 Limpando http_cache: {len(http_cache)} itens -> 0")
        state["http_cache"] = {}
    
    # Limpa html_hashes (menos crítico, mas pode crescer)
    html_hashes = state.get("html_hashes", {})
    if isinstance(html_hashes, dict) and len(html_hashes) > MAX_HASHES_ITEMS:
        log.info(f"🧹 Limpando html_hashes: {len(html_hashes)} itens -> 0")
        state["html_hashes"] = {}
    
    stats_after = {
        "dedup": len(state.get("dedup", {})) if isinstance(state.get("dedup"), dict) else 0,
        "http_cache": len(state.get("http_cache", {})),
        "html_hashes": len(state.get("html_hashes", {}))
    }
    
    state["last_cleanup"] = time.time()
    
    log.info(f"✅ Limpeza concluída ({reason}). Antes: {stats_before}, Depois: {stats_after}")
    
    return state, {"before": stats_before, "after": stats_after}


def should_cleanup_by_time(state: Dict[str, Any]) -> bool:
    """Verifica se deve fazer limpeza baseado no tempo (7 dias)."""
    last_clean = state.get("last_cleanup", 0)
    now_ts = time.time()
    return (now_ts - last_clean) > CLEANUP_INTERVAL


def should_cleanup_by_size(state_file: str) -> Tuple[bool, str]:
    """
    Verifica se deve fazer limpeza baseado no tamanho do arquivo.
    
    Returns:
        Tuple (should_cleanup, reason)
    """
    file_size = get_state_size(state_file)
    
    if file_size > MAX_STATE_SIZE:
        return True, f"Tamanho crítico ({file_size / 1024 / 1024:.2f} MB > {MAX_STATE_SIZE / 1024 / 1024:.2f} MB)"
    elif file_size > WARN_STATE_SIZE:
        return True, f"Tamanho grande ({file_size / 1024 / 1024:.2f} MB > {WARN_STATE_SIZE / 1024 / 1024:.2f} MB)"
    
    return False, ""


def check_and_cleanup_state(force: bool = False) -> Dict[str, Any]:
    """
    Verifica e limpa o state.json se necessário.
    
    Args:
        force: Se True, força limpeza mesmo se não necessário
    
    Returns:
        Estado limpo
    """
    state_file = p("state.json")
    state = load_json_safe(state_file, {})
    
    state.setdefault("dedup", {})
    state.setdefault("http_cache", {})
    state.setdefault("html_hashes", {})
    state.setdefault("last_cleanup", 0)
    
    cleanup_reason = ""
    should_clean = force
    
    if not should_clean:
        # Verifica por tempo
        if should_cleanup_by_time(state):
            should_clean = True
            cleanup_reason = "Ciclo de 7 dias"
        
        # Verifica por tamanho
        if not should_clean:
            should_clean, size_reason = should_cleanup_by_size(state_file)
            if should_clean:
                cleanup_reason = size_reason
    
    if should_clean:
        state, stats = cleanup_state(state, cleanup_reason)
        save_json_safe(state_file, state, atomic=True)
        
        # Log do tamanho após limpeza
        new_size = get_state_size(state_file)
        log.info(f"📊 state.json após limpeza: {new_size / 1024 / 1024:.2f} MB")
    
    return state
