# 🔐 CyberIntel Bot — Cybersecurity Intelligence System

<p align="center">
  <img alt="CyberIntel Bot" src="./icon.png" width="200">
</p>

<p align="center">
  <a href="https://github.com/carmipa/cyberintel-discord"><img src="https://img.shields.io/badge/Discord-Bot-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord Bot" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" /></a>
  <img src="https://img.shields.io/badge/Status-Secure-success?style=for-the-badge&logo=security-scorecard&logoColor=white" alt="Status" />
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=open-source-initiative&logoColor=white" alt="License MIT" /></a>
</p>

<p align="center">
  <b>Intelligent Cybersecurity Feed Monitoring (RSS/Atom/YouTube)</b><br>
  Surgical Filtering • Interactive Dashboard • Auto-posting to Discord • Data Persistence
</p>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🧱 Architecture](#-architecture)
- [🚀 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🧰 Commands](#-commands)
- [🎛️ Dashboard](#️-dashboard)
- [🧠 Filter System](#-filter-system)
- [🖥️ Deploy](#️-deploy)
- [📜 License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-----------|
| 📡 **Periodic Scanner** | Scans RSS/Atom/YouTube feeds every 30 minutes (configurable). |
| 🕵️ **HTML Watcher** | Monitors official non-RSS sites (e.g., CISA, NIST) for visual changes. |
| 🎛️ **Persistent Dashboard** | Interactive panel with buttons that work even after restart. |
| 🎯 **Category Filters** | Malware, Ransomware, Vulnerability, Exploit + "ALL" option. |
| 🛡️ **Anti-Spam** | Blacklist to block generic or irrelevant news. |
| 🔄 **Smart Deduplication** | Never repeats news (history in `history.json` and `database.json`). |
| 💾 **Data Persistence** | Tracks sent news with a local database (`data/database.json`). |
| 🌐 **Node-RED Integration** | Sends notifications to external dashboards via webhook. |
| 🎨 **Rich Embeds** | Premium visual style (Matrix Green, thumbnails, timestamps). |
| 🎞️ **Native Player** | YouTube/Twitch videos play directly in chat. |
| 🌍 **Multi-Language** | Support for EN, PT, ES, IT, JA (auto-detect + `/setlang`). |
| 🔐 **Secure SSL** | Verified connections with certifi (MITM protection). |

---

## 🧱 Architecture

The system consists of integrated modules for intelligence collection, processing, filtering, and distribution.

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

## 🚀 Installation

### Prerequisites

- **Python 3.10+**
- **Discord Bot Token** ([Developer Portal](https://discord.com/developers/applications))

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/carmipa/cyberintel-discord.git
cd cyberintel-discord

# 2. Create virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your token
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```env
DISCORD_TOKEN=your_token_here
COMMAND_PREFIX=!
LOOP_MINUTES=30
LOG_LEVEL=INFO
DISCORD_NEWS_CHANNEL_ID=your_channel_id
NODE_RED_ENDPOINT=http://nodered:1880/cyber-intel
```

### Feed Sources (`sources.json`)

Customize your intelligence sources:

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

## 🧰 Commands

| Command | Type | Description |
|---------|------|-----------|
| `/dashboard` | Slash | Opens filter configuration panel (Admin) |
| `/setlang` | Slash | Sets bot language for the server (Admin) |
| `/forcecheck` | Slash | Forces immediate scan (Admin) |
| `/status` | Slash | Shows bot statistics (Uptime, Scans) |
| `/feeds` | Slash | Lists all monitored sources |

---

## 🎛️ Dashboard

The interactive panel allows configuring which categories to monitor in real-time:

- 🦠 **Malware**
- 🔒 **Ransomware**
- 🛡️ **Vulnerability**
- 💥 **Exploit**
- 🕵️ **Zero-Day**

Configurations are saved per server and persist after bot restart.

---

## 📜 License

This project is licensed under the **MIT License**.

---

<p align="center">
  🔐 <i>CyberIntel System — Secure the network. Secure the future.</i>
</p>
