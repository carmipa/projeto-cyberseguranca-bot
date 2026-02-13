"""
Padrão de ícones e cores para logs do CyberIntel SOC Bot.
Centraliza todos os ícones para consistência e fácil manutenção.
"""

# =========================================================
# ÍCONES POR CATEGORIA
# =========================================================

class LogIcons:
    """Ícones padronizados para logs."""
    
    # Status Geral
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    DEBUG = "🐛"
    CRITICAL = "🔥"
    
    # Operações do Bot
    BOT_CONNECTED = "✅"
    BOT_DISCONNECTED = "🛑"
    BOT_STARTING = "🚀"
    BOT_READY = "🟢"
    
    # Scanner e Inteligência
    SCAN_START = "🔎"
    SCAN_COMPLETE = "✅"
    SCAN_SKIP = "⏭️"
    SCAN_WAIT = "⏳"
    INTEL_MATCH = "✨"
    INTEL_BLOCKED = "🛡️"
    INTEL_ALERT = "🚨"
    
    # APIs e Serviços
    API_NVD = "🛡️"
    API_OTX = "🛸"
    API_URLSCAN = "🔍"
    API_VT = "🦠"
    API_NODERED = "📡"
    API_SUCCESS = "✅"
    API_ERROR = "❌"
    
    # Cache e Performance
    CACHE_HIT = "📦"
    CACHE_MISS = "📭"
    PERFORMANCE = "⚡"
    
    # Backup e Storage
    BACKUP_CREATED = "📦"
    BACKUP_RESTORED = "✅"
    BACKUP_CLEANUP = "🧹"
    STORAGE_SAVED = "💾"
    STORAGE_LOADED = "📂"
    
    # Segurança
    SECURITY_ALERT = "🚨"
    SECURITY_BLOCK = "🛡️"
    SECURITY_INTRUSION = "⛔"
    SECURITY_AUTH = "🔐"
    
    # Notificações
    NOTIFICATION_SENT = "📢"
    NOTIFICATION_FAILED = "❌"
    NEWS_POSTED = "📰"
    
    # Sistema
    SYSTEM_UPDATE = "🔄"
    SYSTEM_CLEANUP = "🧹"
    SYSTEM_ERROR = "🔥"
    SYSTEM_INFO = "📊"
    
    # Cold Start
    COLD_START = "❄️"
    
    # Filtros
    FILTER_BLOCK = "🛑"
    FILTER_ALLOW = "✅"
    
    # HTML Monitor
    HTML_CHANGE = "🔄"
    HTML_INIT = "📄"
    
    # Discord
    DISCORD_SYNC = "🔄"
    DISCORD_COG_LOADED = "🧩"
    DISCORD_CHANNEL = "📺"
    
    # Web Server
    WEB_STARTED = "🌍"
    WEB_INTRUSION = "⛔"
    
    # Testes
    TEST_START = "🧪"
    TEST_SUCCESS = "✅"
    TEST_FAIL = "❌"


# =========================================================
# CORES POR SEVERIDADE (para Discord Embeds)
# =========================================================

class LogColors:
    """Cores padronizadas para Discord embeds e logs."""
    
    # Cores Discord (hex)
    SUCCESS = 0x00FF00      # Verde
    ERROR = 0xFF0000        # Vermelho
    WARNING = 0xFFFF00      # Amarelo
    INFO = 0x00FFFF         # Cyan
    CRITICAL = 0x000000     # Preto (máxima severidade)
    
    # Cores específicas do CyberIntel
    INTEL_UPDATE = 0x00FFCC  # Cyan claro
    THREAT_ALERT = 0xFF0000  # Vermelho
    VULNERABILITY = 0xFF8C00 # Laranja
    SECURITY = 0x00FF00     # Verde
    SYSTEM = 0x808080       # Cinza


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def format_log(icon: str, message: str) -> str:
    """
    Formata mensagem de log com ícone.
    
    Args:
        icon: Ícone da mensagem
        message: Mensagem a ser logada
    
    Returns:
        String formatada com ícone
    """
    return f"{icon} {message}"


def get_severity_icon(severity: str) -> str:
    """
    Retorna ícone baseado na severidade.
    
    Args:
        severity: 'success', 'error', 'warning', 'info', 'critical'
    
    Returns:
        Ícone correspondente
    """
    severity_map = {
        'success': LogIcons.SUCCESS,
        'error': LogIcons.ERROR,
        'warning': LogIcons.WARNING,
        'info': LogIcons.INFO,
        'critical': LogIcons.CRITICAL,
        'debug': LogIcons.DEBUG
    }
    return severity_map.get(severity.lower(), LogIcons.INFO)


def get_severity_color(severity: str) -> int:
    """
    Retorna cor Discord baseada na severidade.
    
    Args:
        severity: 'success', 'error', 'warning', 'info', 'critical'
    
    Returns:
        Cor hex correspondente
    """
    severity_map = {
        'success': LogColors.SUCCESS,
        'error': LogColors.ERROR,
        'warning': LogColors.WARNING,
        'info': LogColors.INFO,
        'critical': LogColors.CRITICAL
    }
    return severity_map.get(severity.lower(), LogColors.INFO)
