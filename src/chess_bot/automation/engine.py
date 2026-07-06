from __future__ import annotations

import asyncio
from pathlib import Path

import chess
import chess.engine


class StockfishEngine:
    """Async context manager for a local UCI-compatible Stockfish binary."""

    def __init__(self, binary_path: Path, think_time_seconds: float = 0.1) -> None:
        self.binary_path = binary_path
        self.think_time_seconds = think_time_seconds
        self._transport: asyncio.SubprocessTransport | None = None
        self._engine: chess.engine.UciProtocol | None = None

    async def __aenter__(self) -> "StockfishEngine":
        transport, engine = await chess.engine.popen_uci(str(self.binary_path))
        self._transport = transport
        self._engine = engine
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: object | None,
    ) -> None:
        if self._engine is not None:
            await self._engine.quit()
        if self._transport is not None:
            self._transport.close()

    async def best_move(self, board: chess.Board) -> chess.Move:
        if self._engine is None:
            raise RuntimeError("StockfishEngine must be used as an async context manager")

        result = await self._engine.play(
            board,
            chess.engine.Limit(time=self.think_time_seconds),
        )
        if result.move is None:
            raise RuntimeError("Engine did not return a move")

        return result.move
