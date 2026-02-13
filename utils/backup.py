"""
Sistema de Backup Automático para arquivos JSON.
Mantém histórico auditável para compliance e GRC.
"""
import os
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from utils.storage import p, load_json_safe, save_json_safe

log = logging.getLogger("CyberIntel_Backup")

# Configuração de backup
BACKUP_DIR = "data/backups"
MAX_BACKUPS_PER_FILE = 30  # Mantém últimos 30 backups por arquivo
BACKUP_RETENTION_DAYS = 90  # Mantém backups por 90 dias


def ensure_backup_dir():
    """Garante que diretório de backup existe."""
    backup_path = Path(BACKUP_DIR)
    backup_path.mkdir(parents=True, exist_ok=True)
    return backup_path


def create_backup(filepath: str, label: Optional[str] = None) -> Optional[str]:
    """
    Cria backup de um arquivo JSON com timestamp.
    
    Args:
        filepath: Caminho do arquivo a fazer backup
        label: Label opcional para identificar o backup (ex: "pre_update")
    
    Returns:
        Caminho do backup criado ou None se falhar
    """
    try:
        if not os.path.exists(filepath):
            log.warning(f"Arquivo não existe para backup: {filepath}")
            return None
        
        backup_dir = ensure_backup_dir()
        filename = os.path.basename(filepath)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Nome do backup: filename_YYYYMMDD_HHMMSS[_label].json.backup
        backup_name = f"{filename}_{timestamp}"
        if label:
            backup_name += f"_{label}"
        backup_name += ".json.backup"
        
        backup_path = backup_dir / backup_name
        
        # Copia arquivo
        shutil.copy2(filepath, backup_path)
        
        log.info(f"✅ Backup criado: {backup_path}")
        return str(backup_path)
        
    except Exception as e:
        log.error(f"Erro ao criar backup de {filepath}: {e}")
        return None


def cleanup_old_backups(filepath: Optional[str] = None):
    """
    Remove backups antigos baseado em retenção.
    
    Args:
        filepath: Se fornecido, limpa backups apenas deste arquivo.
                  Se None, limpa todos os backups.
    """
    try:
        backup_dir = ensure_backup_dir()
        now = datetime.now()
        
        backups_to_check = []
        if filepath:
            # Backups de um arquivo específico
            filename = os.path.basename(filepath)
            backups_to_check = list(backup_dir.glob(f"{filename}_*.json.backup"))
        else:
            # Todos os backups
            backups_to_check = list(backup_dir.glob("*.json.backup"))
        
        backups_to_check.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        
        removed_count = 0
        for backup_path in backups_to_check:
            # Remove por idade
            backup_age = now.timestamp() - backup_path.stat().st_mtime
            if backup_age > (BACKUP_RETENTION_DAYS * 24 * 3600):
                try:
                    backup_path.unlink()
                    removed_count += 1
                    log.debug(f"Backup antigo removido: {backup_path.name}")
                except Exception as e:
                    log.warning(f"Erro ao remover backup {backup_path}: {e}")
            
            # Remove por quantidade (mantém apenas os N mais recentes)
            if backups_to_check.index(backup_path) >= MAX_BACKUPS_PER_FILE:
                try:
                    backup_path.unlink()
                    removed_count += 1
                    log.debug(f"Backup excedente removido: {backup_path.name}")
                except Exception as e:
                    log.warning(f"Erro ao remover backup {backup_path}: {e}")
        
        if removed_count > 0:
            log.info(f"🧹 Limpeza de backups: {removed_count} arquivos removidos")
            
    except Exception as e:
        log.error(f"Erro na limpeza de backups: {e}")


def list_backups(filepath: str) -> List[dict]:
    """
    Lista backups disponíveis para um arquivo.
    
    Args:
        filepath: Caminho do arquivo original
    
    Returns:
        Lista de dicts com informações dos backups
    """
    try:
        backup_dir = ensure_backup_dir()
        filename = os.path.basename(filepath)
        backups = list(backup_dir.glob(f"{filename}_*.json.backup"))
        
        backup_info = []
        for backup_path in sorted(backups, key=lambda p: p.stat().st_mtime, reverse=True):
            stat = backup_path.stat()
            backup_info.append({
                "path": str(backup_path),
                "name": backup_path.name,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "age_days": (datetime.now().timestamp() - stat.st_mtime) / (24 * 3600)
            })
        
        return backup_info
        
    except Exception as e:
        log.error(f"Erro ao listar backups: {e}")
        return []


def restore_backup(filepath: str, backup_path: Optional[str] = None) -> bool:
    """
    Restaura um arquivo de um backup.
    
    Args:
        filepath: Caminho do arquivo a restaurar
        backup_path: Caminho do backup específico. Se None, usa o mais recente.
    
    Returns:
        True se restauração bem-sucedida
    """
    try:
        if backup_path is None:
            # Usa backup mais recente
            backups = list_backups(filepath)
            if not backups:
                log.error(f"Nenhum backup encontrado para {filepath}")
                return False
            backup_path = backups[0]["path"]
        
        if not os.path.exists(backup_path):
            log.error(f"Backup não existe: {backup_path}")
            return False
        
        # Cria backup do arquivo atual antes de restaurar
        create_backup(filepath, label="pre_restore")
        
        # Restaura
        shutil.copy2(backup_path, filepath)
        log.info(f"✅ Arquivo restaurado: {filepath} <- {backup_path}")
        return True
        
    except Exception as e:
        log.error(f"Erro ao restaurar backup: {e}")
        return False


def auto_backup_critical_files():
    """
    Cria backups automáticos dos arquivos críticos do sistema.
    Deve ser chamado periodicamente (ex: antes de operações importantes).
    """
    critical_files = [
        "config.json",
        "state.json",
        "history.json",
        "data/database.json"
    ]
    
    backed_up = 0
    for filename in critical_files:
        filepath = p(filename)
        if os.path.exists(filepath):
            if create_backup(filepath, label="auto"):
                backed_up += 1
    
    if backed_up > 0:
        log.info(f"📦 Backup automático concluído: {backed_up} arquivos")
    
    # Limpa backups antigos
    cleanup_old_backups()
