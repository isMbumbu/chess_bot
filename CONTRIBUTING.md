# Contributing

Thanks for helping make Chess Bot better.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

## Quality Checks

Run these before opening a pull request:

```bash
ruff check .
ruff format --check .
mypy src
pytest
```

## Code Style

- Keep functions small and typed.
- Prefer async interfaces for I/O boundaries.
- Put chess rules and engine behavior in services, not route handlers.
- Keep route handlers focused on HTTP validation, errors, and orchestration.
- Add tests for engine behavior, board validation, and API responses.

## Fair Play

Do not contribute code that secretly controls a human chess account or plays
against unsuspecting opponents. Platform integrations must use official APIs,
approved bot accounts, or local/offline play modes.
