# 🔐 CyberIntel Bot — Sistema de Inteligência em Cibersegurança

<p align="center">
  <img alt="CyberIntel Bot" src="./icon.png" width="200">
</p>

<p align="center">
  <a href="https://github.com/carmipa/cyberintel-discord"><img src="https://img.shields.io/badge/Discord-Bot-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord Bot" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" /></a>
  <img src="https://img.shields.io/badge/Status-Seguro-success?style=for-the-badge&logo=security-scorecard&logoColor=white" alt="Status" />
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=open-source-initiative&logoColor=white" alt="License MIT" /></a>
</p>

<p align="center">
  <b>Monitoramento Inteligente de Feeds de Cibersegurança (RSS/Atom/YouTube)</b><br>
  Filtragem Cirúrgica • Dashboard Interativo • Postagem Automática no Discord • Persistência de Dados
</p>

---

## 📋 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [🧱 Arquitetura](#-arquitetura)
- [🚀 Instalação](#-instalação)
- [⚙️ Configuração](#️-configuração)
- [🧰 Comandos](#-comandos)
- [🎛️ Dashboard](#️-dashboard)
- [🧠 Sistema de Filtros](#-sistema-de-filtros)
- [🖥️ Deploy](#️-deploy)
- [📜 Licença](#-licença)

---

## ✨ Funcionalidades

| Recurso | Descrição |
|---------|-----------|
| 📡 **Scanner Periódico** | Varredura de feeds RSS/Atom/YouTube a cada 30 minutos (configurável). |
| 🕵️ **HTML Watcher** | Monitora sites oficiais sem RSS (ex: CISA, NIST) detectando mudanças visuais. |
| 🎛️ **Dashboard Persistente** | Painel interativo com botões que funciona mesmo após reinicialização. |
| 🎯 **Filtros por Categoria** | Malware, Ransomware, Vulnerabilidade, Exploit + opção "TUDO". |
| 🛡️ **Anti-Spam** | Blacklist para bloquear notícias genéricas ou irrelevantes. |
| 🔄 **Deduplicação Inteligente** | Nunca repete notícias (histórico em `history.json` e `database.json`). |
| 💾 **Persistência de Dados** | Monitoramento de envio de notícias com base de dados local (`data/database.json`). |
| 🌐 **Integração Node-RED** | Envio de notificações para dashboards externos via webhook. |
| 🎨 **Embeds Ricos** | Estilo visual Premium (Verde Matrix, thumbnails, timestamps). |
| 🎞️ **Player Nativo** | Vídeos do YouTube/Twitch tocam direto no chat. |
| 🌍 **Multi-Idioma** | Suporte a EN, PT, ES, IT, JA (detecção automática + `/setlang`). |
| 🔐 **SSL Seguro** | Conexões verificadas com certifi (proteção contra MITM). |

---

## 🧱 Arquitetura

O sistema é composto por módulos integrados para coleta, processamento, filtragem e distribuição de inteligência.

```mermaid
graph TD
    subgraph Sources
        RSS[RSS Feeds]
        YT[YouTube Channels]
        HTML[Official Sites]
    end

    subgraph Core System
        Scanner[Scanner Loop (30m)]
        HTMLMonitor[HTML Monitor]
        NewsService[News Service (External)]
        DBService[DB Service (Persistence)]
        
        Scanner -->|Fetch| RSS
        Scanner -->|Fetch| YT
        HTMLMonitor -->|Check Hash| HTML
        
        Scanner -->|Raw Data| Filters{Filters & Logic}
        HTMLMonitor -->|Changes| Filters
    end

    subgraph Data & State
        Config[config.json]
        History[history.json]
        State[state.json]
        Database[database.json]
        
        Filters -->|Check| Config
        Filters -->|Deduplicate| History
        Filters -->|Deduplicate| Database
        Scanner -->|Update| State
    end

    subgraph Output
        Discord[Discord Bot]
        NodeRED[Node-RED Dashboard]
        
        Filters -->|Approved| Discord
        Discord -->|Commands| Config
        DBService -->|Notify| NodeRED
    end

    Scanner -->|Save| History
    Scanner -->|Save| Database
    NewsService -->|Fetch| RSS
    MonitorCog[Monitor Cog] -->|Poll| NewsService
    MonitorCog -->|Save/Check| DBService
    DBService -->|Persist| Database
```

---

## 🚀 Instalação

### Pré-requisitos

- **Python 3.10+**
- **Token do Bot Discord** ([Portal de Desenvolvedores](https://discord.com/developers/applications))

### Início Rápido

```bash
# 1. Clonar repositório
git clone https://github.com/carmipa/cyberintel-discord.git
cd cyberintel-discord

# 2. Criar ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar ambiente
cp .env.example .env
# Edite o .env com seu token
```

---

## ⚙️ Configuração

### Variáveis de Ambiente (`.env`)

```env
DISCORD_TOKEN=seu_token_aqui
COMMAND_PREFIX=!
LOOP_MINUTES=30
LOG_LEVEL=INFO
DISCORD_NEWS_CHANNEL_ID=seu_canal_id
NODE_RED_ENDPOINT=http://nodered:1880/cyber-intel
```

### Fontes de Feeds (`sources.json`)

Customize suas fontes de inteligência:

```json
{
  "rss_feeds": [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/"
  ],
  "youtube_feeds": [
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC9-y-6csu5WGm29I7JiwpnA"
  ],
   "official_sites_reference_(not_rss)": [
    "https://www.cisa.gov/cybersecurity-alerts-and-advisories"
  ]
}
```

---

## 🧰 Comandos

| Comando | Tipo | Descrição |
|---------|------|-----------|
| `/dashboard` | Slash | Abre painel de configuração de filtros (Admin) |
| `/setlang` | Slash | Define o idioma do bot para o servidor (Admin) |
| `/forcecheck` | Slash | Força uma varredura imediata (Admin) |
| `/status` | Slash | Mostra estatísticas do bot (Uptime, Scans) |
| `/feeds` | Slash | Lista todas as fontes monitoradas |

---

## 🎛️ Dashboard

O painel interativo permite configurar quais categorias monitorar em tempo real:

- 🦠 **Malware**
- 🔒 **Ransomware**
- 🛡️ **Vulnerabilidade**
- 💥 **Exploit**
- 🕵️ **Zero-Day**

As configurações são salvas por servidor e persistem após reinicialização do bot.

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License**.

---

<p align="center">
  🔐 <i>Sistema CyberIntel — Proteja a rede. Proteja o futuro.</i>
</p>
