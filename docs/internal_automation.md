# Internal Automation Pattern

This pattern is for authenticated internal web-app testing. Keep selectors,
URLs, credentials, and account behavior scoped to systems you own or are
authorized to test.

## Install

```bash
pip install -e ".[automation]"
playwright install chromium
```

You also need a local Stockfish binary, for example `/usr/local/bin/stockfish`.

## Modules

- `automation/auth.py`: creates a Playwright context and persists storage state.
- `automation/board_state.py`: reads FEN or piece positions from the DOM.
- `automation/engine.py`: wraps a local UCI engine through `python-chess`.
- `automation/executor.py`: maps UCI moves to coordinate clicks.
- `automation/runner.py`: demonstrates the full flow.

## Expected DOM Contract

The simplest option is to expose a full FEN string:

```html
<div
  data-testid="board"
  data-fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
>
</div>
```

If the app does not expose FEN, each square can expose a coordinate and piece:

```html
<div data-testid="board" data-turn="white">
  <div data-square="e2"><span data-piece="P"></span></div>
  <div data-square="e7"><span data-piece="p"></span></div>
</div>
```

Uppercase pieces are white and lowercase pieces are black, matching
`python-chess` symbols.

## Authentication Persistence

`AuthSessionManager` checks for `.auth/storage-state.json`. If it exists, the
browser context starts already logged in. If it does not exist, the provided
login flow runs once and saves cookies/local storage for future runs.

```python
session = AuthSessionManager(Path(".auth/storage-state.json"))
context = await session.context(browser, "https://internal.example.test", login_flow)
```

## Full Flow

```python
from pathlib import Path

from chess_bot.automation.runner import run_internal_board_test

await run_internal_board_test(
    base_url="https://internal.example.test",
    board_path="/chess-board",
    stockfish_path=Path("/usr/local/bin/stockfish"),
    email="tester@example.test",
    password="change-me",
)
```
