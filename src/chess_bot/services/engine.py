from dataclasses import dataclass
from random import SystemRandom

import chess

from chess_bot.services.board import BoardService, InvalidPositionError

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20_000,
}


@dataclass(frozen=True)
class EngineMove:
    move: str | None
    san: str | None
    reason: str


class ChessEngine:
    def __init__(self) -> None:
        self._random = SystemRandom()

    async def choose_move(self, fen: str) -> EngineMove:
        board = BoardService.board_from_fen(fen)

        if board.is_game_over():
            return EngineMove(move=None, san=None, reason="game_over")

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return EngineMove(move=None, san=None, reason="no_legal_moves")

        move, reason = self._select_move(board, legal_moves)
        san = board.san(move)
        return EngineMove(move=move.uci(), san=san, reason=reason)

    def _select_move(
        self,
        board: chess.Board,
        legal_moves: list[chess.Move],
    ) -> tuple[chess.Move, str]:
        checkmate = self._find_checkmate(board, legal_moves)
        if checkmate is not None:
            return checkmate, "immediate_checkmate"

        capture = self._best_capture(board, legal_moves)
        if capture is not None:
            return capture, "highest_value_capture"

        return self._random.choice(legal_moves), "random_legal_move"

    @staticmethod
    def _find_checkmate(
        board: chess.Board,
        legal_moves: list[chess.Move],
    ) -> chess.Move | None:
        for move in legal_moves:
            candidate = board.copy(stack=False)
            candidate.push(move)
            if candidate.is_checkmate():
                return move

        return None

    @staticmethod
    def _best_capture(
        board: chess.Board,
        legal_moves: list[chess.Move],
    ) -> chess.Move | None:
        captures = [move for move in legal_moves if board.is_capture(move)]
        if not captures:
            return None

        return max(captures, key=lambda move: ChessEngine._capture_value(board, move))

    @staticmethod
    def _capture_value(board: chess.Board, move: chess.Move) -> int:
        captured_piece = board.piece_at(move.to_square)
        if captured_piece is None and board.is_en_passant(move):
            return PIECE_VALUES[chess.PAWN]
        if captured_piece is None:
            return 0

        return PIECE_VALUES[captured_piece.piece_type]
