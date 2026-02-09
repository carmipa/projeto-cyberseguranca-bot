# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# Obrigatório
TOKEN = os.getenv("DISCORD_TOKEN")
# ID do Dono para comandos restritos (Active Defense)
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Operação (opcional via env)
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")
try:
    LOOP_MINUTES = int(os.getenv("LOOP_MINUTES", "30"))
except ValueError:
    LOOP_MINUTES = 60

# Logging Level (INFO, DEBUG, WARNING, ERROR)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Node-RED Integration
NODE_RED_ENDPOINT = os.getenv("NODE_RED_ENDPOINT", "http://localhost:1880/cyber-intel")
