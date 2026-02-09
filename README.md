# 🛡️ Projeto Cyberseguranca Bot

![Bot Logo](icon.png)

Bot de Discord focado em **Threat Intelligence**, notícias em tempo real e monitoramento de vulnerabilidades (CVEs).
CLOG_LEVEL=INFO
DISCORD_NEWS_CHANNEL_ID=123456789012345678
Desenvolvido como parte dos estudos de Cybersecurity na **FIAP**.

## 🚀 Funcionalidades Atuais

- [x] Integração com Discord API.
- [x] Feed automático de notícias (The Hacker News / BleepingComputer) via comando `/news`.
- [ ] Consulta de CVEs via API do MITRE.
- [ ] Análise de links suspeitos (VirusTotal).
- [ ] Monitoramento contínuo de feeds RSS.

## 🛠️ Tecnologias

- Python 3.10+
- Discord.py
- Feedparser (RSS)
- Docker & Docker Compose

## 📦 Instalação

### Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Edite o .env com seu Token

# Rodar
python main.py
```

### Docker

```bash
# Subir container
docker-compose up -d --build
```

## 📝 Comandos

- `/news` - Busca as últimas notícias de Cyber Segurança.
