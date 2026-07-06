# Chess Bot

An open-source Python service for experimenting with chess engines, training
loops, and analysis APIs.

This project is intentionally designed for ethical chess automation. It can
analyze positions, choose legal moves, store games, and support future engine
training work. It should not be used to secretly play on a human account on
chess.com, Lichess, or similar platforms. If platform play is added later, use
official bot accounts and follow each platform's fair-play and API rules.

## Features

- FastAPI application with async routes.
- Pydantic settings and request/response schemas.
- SQLModel persistence with async SQLAlchemy sessions.
- `python-chess` move validation and board state handling.
- Docker and Docker Compose for local development.
- Ruff, mypy, and pytest configuration for open-source quality.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn chess_bot.main:app --reload
```

Open the API docs at <http://127.0.0.1:8000/docs>.

## Docker

```bash
docker compose up --build
```

Docker stores the SQLite database in a named volume at `/data/chess_bot.db`.
You do not need a local `.env` file unless you want to override settings.

## Example Requests

Create a game:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/games \
  -H "Content-Type: application/json" \
  -d '{}'
```

Ask the engine for a move from the starting position:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/analysis/move \
  -H "Content-Type: application/json" \
  -d '{"fen":"startpos"}'
```

Make a move:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/games/1/moves \
  -H "Content-Type: application/json" \
  -d '{"uci":"e2e4"}'
```

## Development

```bash
ruff check .
ruff format --check .
mypy src
pytest
```

More detail:

- [API reference](docs/api.md)
- [Architecture](docs/architecture.md)
- [Internal automation pattern](docs/internal_automation.md)
- [Contributing](CONTRIBUTING.md)

## Roadmap

- Add stronger engine search and evaluation.
- Add self-play training jobs.
- Add PGN import/export.
- Add a compliant Lichess bot integration for approved bot accounts.
- Add background workers for training and game analysis.
