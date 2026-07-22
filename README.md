# Telegram AntiSpam Bot

Telegram AntiSpam Bot is a moderation bot built with **Aiogram 3** and **SQLAlchemy**.  
It automatically detects spam messages, removes them, logs incidents and provides moderation tools for administrators.

## Features

- 🔍 Keyword spam detection
- 🔗 Link detection
- 😀 Emoji spam detection
- 🚀 Flood protection
- ✅ Whitelist support
- 🚫 Blacklist support
- 📝 Spam logging
- 🗑 Automatic deletion of moderator notifications
- 💾 SQLite database via SQLAlchemy

## Project structure

```
app/
├── database/
├── filters/
├── handlers/
├── models/
├── repositories/
├── services/
└── utils/
```

Architecture:

```
Handler
    ↓
Management Service
    ↓
Service
    ↓
Repository
    ↓
SQLAlchemy
```

## Tech Stack

- Python 3.13
- Aiogram 3
- SQLAlchemy
- SQLite

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd TelegramAntiSpamBot
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` or configure `config.py` with your bot token.

Run the bot:

```bash
python bot.py
```

## Current filters

| Filter | Status |
|--------|--------|
| Keyword filter | ✅ |
| Link filter | ✅ |
| Flood filter | ✅ |
| Emoji filter | ✅ |
| Whitelist | ✅ |
| Blacklist | ✅ |

## Roadmap

- [ ] Configurable filter settings
- [ ] Admin panel
- [ ] More advanced spam heuristics
- [ ] Docker deployment
- [ ] CI/CD

## License

MIT