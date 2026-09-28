# EKTGC — Educational Knowledge & Telegram Group Analytics

A self-hosted Python tool for analyzing message readership in Telegram groups.
EKTGC collects messages from a teacher, determines which participants have read
each message and when, and stores the results in an Excel spreadsheet for
further analysis. The report refreshes automatically every hour.

![Python](https://img.shields.io/badge/python-3.x-3776AB)
![Telethon](https://img.shields.io/badge/telethon-1.x-2CA5E0)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Tool](#running-the-tool)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Output Format](#output-format)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Automatic message collection** — retrieves the latest messages sent by the teacher in the target group.
- **Reader tracking** — resolves which participants have read each message and the exact read timestamp.
- **Excel export** — writes results to `analytics.xlsx` with deduplication of existing records.
- **Hourly refresh** — reruns the analysis loop every 3600 seconds.
- **Persistent data** — the spreadsheet is preserved between runs and appended to, not overwritten.
- **Simple configuration** — sensitive values are stored in a `.env` file.
- **Lightweight** — no external services, no paid hosting, runs locally.

---

## Tech Stack

| Component   | Technology      |
|-------------|-----------------|
| Language    | Python 3.x      |
| Telegram API| Telethon        |
| Excel       | openpyxl        |
| Config      | python-dotenv   |
| Package mgr | pip             |

---

## Requirements

- Python **3.x**
- Telegram API credentials (`API_ID`, `API_HASH`) from [my.telegram.org](https://my.telegram.org)
- A Telegram account authorized to read the target group
- The teacher's Telegram **user ID**
- The target group's **chat ID** (set in `config.py`)
- Permission to call `GetMessageReadParticipantsRequest` (works in groups, not channels)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/EKTGC.git
   cd EKTGC
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv

   # Linux / macOS
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install telethon openpyxl python-dotenv
   ```

---

## Configuration

Create a `.env` file in the project root:

```env
API_ID=your_api_id
API_HASH=your_api_hash
TEACHER_ID=your_teacher_id
```

| Variable     | Description                                          | Required |
|--------------|------------------------------------------------------|----------|
| `API_ID`     | Telegram API ID from my.telegram.org                 | Yes      |
| `API_HASH`   | Telegram API hash from my.telegram.org               | Yes      |
| `TEACHER_ID` | Telegram user ID of the teacher whose messages are analyzed | Yes |

> **Note:** the target `GROUP_ID` is defined directly in `config.py`.

---

## Running the Tool

```bash
python main.py
```

On first launch, Telethon will prompt for Telegram authorization (phone number
and confirmation code). The `analytics.xlsx` file is created automatically on
the first write.

---

## How It Works

EKTGC runs a **continuous hourly loop** that collects messages, resolves
readership, and persists the results.

### Stage 1 — Message collection

- `get_teacher_messages(limit=10)` fetches the most recent messages in the group.
- Messages are filtered by `message.sender_id == TEACHER_ID`.
- Only messages authored by the teacher are kept for analysis.

### Stage 2 — Reader resolution

- For each teacher message, `get_readers(message_id)` calls
  `GetMessageReadParticipantsRequest` to obtain the list of participants who read it.
- The full group participant list is fetched once and indexed by `user.id` into a
  dictionary for O(1) lookup.
- Each reader is expanded into a record with `user_id`, `first_name`,
  `last_name`, and `read_at` (the read timestamp).

### Stage 3 — Excel persistence

- `save_readings(message, readers)` loads `analytics.xlsx` (or creates it with
  headers if missing).
- Existing `(message_id, user_id)` pairs are loaded into a set for deduplication.
- Only new reader records are appended; duplicates are skipped.
- The workbook is saved back to disk.

The full pipeline: `get_teacher_messages → get_readers → save_readings → sleep(3600)`,
with data persisted in `analytics.xlsx`.

---

## Project Structure

```
EKTGC/
├── config.py            # Loads .env, defines API_ID, API_HASH, TEACHER_ID, GROUP_ID
├── telegram_client.py   # Initializes the Telethon client
├── messages.py          # Message collection and reader resolution
├── excel.py             # Excel read/write with deduplication
├── main.py              # Entry point and hourly loop
├── .env                 # Environment variables (not committed)
└── analytics.xlsx       # Generated report
```

---

## Output Format

`analytics.xlsx` contains a single sheet named **"Прочтения"** with the following columns:

| Column            | Description                       |
|-------------------|-----------------------------------|
| ID сообщения      | Unique message identifier         |
| Дата сообщения    | Date and time the message was sent|
| ID пользователя   | Telegram ID of the reader         |
| Имя               | Reader's first name               |
| Фамилия           | Reader's last name                |
| Время прочтения   | Date and time the message was read|

Duplicate `(message_id, user_id)` pairs are automatically skipped.

---

## Contributing

Contributions are welcome. To keep things clean:

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
2. Follow **PEP 8** and keep functions small and focused.
3. Test your changes against a private Telegram group before opening a PR.
4. Open a pull request with a clear description of what changed and why.

For bug reports, please include:
- Python version
- Telethon version
- Steps to reproduce
- Relevant console output

---

## License

MIT — see [LICENSE](LICENSE) for details.
