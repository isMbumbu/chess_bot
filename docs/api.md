# API Reference

Run the app and open `/docs` for the interactive OpenAPI UI.

## Health

```http
GET /health
```

Returns:

```json
{"status": "ok"}
```

## Create Game

```http
POST /api/v1/games
```

Body:

```json
{"fen": "startpos"}
```

`fen` may be a full FEN string or `startpos`.

## Get Game

```http
GET /api/v1/games/{game_id}
```

Returns the stored game position and status.

## Make Move

```http
POST /api/v1/games/{game_id}/moves
```

Body:

```json
{"uci": "e2e4"}
```

The move must be legal in the current position.

## Analyze Move

```http
POST /api/v1/analysis/move
```

Body:

```json
{"fen": "startpos"}
```

Returns one legal move and the reason it was selected.
