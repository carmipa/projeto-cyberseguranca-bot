import logging
import sys

# Define color codes
class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"

class CustomFormatter(logging.Formatter):
    """
    Formatter personalizado com cores e ícones para o console.
    Suporta detecção de ícones já presentes na mensagem para não duplicar.
    """
    
    # Format: [TIME] [LEVEL] MESSAGE
    format_str = "%(asctime)s - %(levelname)s - %(message)s"
    
    # Ícones padrão por nível
    LEVEL_ICONS = {
        logging.DEBUG:    "🐛",
        logging.INFO:     "ℹ️ ",
        logging.WARNING:  "⚠️ ",
        logging.ERROR:    "❌",
        logging.CRITICAL: "🔥"
    }

    FORMATS = {
        logging.DEBUG:    Colors.CYAN + format_str + Colors.RESET,
        logging.INFO:     Colors.GREEN + format_str + Colors.RESET,
        logging.WARNING:  Colors.YELLOW + format_str + Colors.RESET,
        logging.ERROR:    Colors.RED + format_str + Colors.RESET,
        logging.CRITICAL: Colors.RED + Colors.BOLD + format_str + Colors.RESET
    }
    
    def format(self, record):
        # Se a mensagem já tem ícone, não adiciona outro
        msg = record.getMessage()
        level_icon = self.LEVEL_ICONS.get(record.levelno, "")
        
        # Verifica se já tem ícone comum no início da mensagem
        common_icons = ["✅", "❌", "⚠️", "🔎", "📊", "🚨", "✨", "🛡️", "📡", "🧹", 
                       "📦", "🔐", "💥", "🔄", "⏳", "⏭️", "🔥", "🛑", "📢", "🌟",
                       "🦠", "🔒", "🆔", "📂", "🕵️", "📺", "🔗", "🌍", "⛔", "🐛",
                       "ℹ️", "🚀", "⚡", "🛸", "👴", "❄️"]
        
        has_icon = any(msg.startswith(icon) for icon in common_icons)
        
        # Se não tem ícone, adiciona o padrão do nível
        if not has_icon and level_icon:
            record.msg = level_icon + " " + msg
            record.args = ()
        
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def setup_logger(level="INFO"):
    """
    Configura o logger raiz com handlers coloridos para console
    e arquivo padrão (sem cores) para logs/bot.log.
    """
    
    # Cria diretório de logs se não existir
    import os
    os.makedirs("logs", exist_ok=True)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove handlers existentes para não duplicar
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 1. Console Handler (Colorido)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    root_logger.addHandler(console_handler)
    
    # 2. File Handler (Texto Puro / JSON compatible-ish)
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        "logs/bot.log", 
        maxBytes=5*1024*1024, 
        backupCount=3, 
        encoding="utf-8"
    )
    # No arquivo, usamos formato padrão sem ansi codes
    file_fmt = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s - %(message)s")
    file_handler.setFormatter(file_fmt)
    root_logger.addHandler(file_handler)

    return root_logger
