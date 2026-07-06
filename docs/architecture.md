# Architecture

Chess Bot starts as a FastAPI service with a deliberately small domain core.

## Layers

- `api`: HTTP routes, request handling, response models, and API errors.
- `schemas`: Pydantic request and response contracts.
- `models`: SQLModel database tables.
- `db`: async database engine and session lifecycle.
- `services`: chess rules, position validation, and engine selection logic.

## Request Flow

1. A route receives a validated Pydantic payload.
2. The route calls a service for chess-specific behavior.
3. The route persists state through an async SQLModel session when needed.
4. The route returns a response schema, not a raw database object.

## Engine Strategy

The first engine is intentionally simple:

- It returns checkmate in one when available.
- It prefers the highest-value capture.
- It otherwise chooses a random legal move.

This gives the API a working legal baseline while leaving room for search,
self-play, neural evaluation, or Stockfish-backed analysis later.

## Platform Integrations

Future integrations should be explicit adapters, for example:

- `integrations/lichess_bot.py` for official Lichess bot accounts.
- `integrations/local_board.py` for local GUI or CLI play.
- `workers/training.py` for background self-play and training jobs.

The project should not contain stealth browser automation for live human
accounts.
