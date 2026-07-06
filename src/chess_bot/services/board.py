from dataclasses import dataclass

import chess


class InvalidPositionError(ValueError):
    """Raised when a FEN string cannot be loaded as a chess position."""


class IllegalMoveError(ValueError):
    """Raised when a requested move is not legal in the current position."""


class GameNotInProgressError(ValueError):
    """Raised when a move is requested after the game has ended."""


@dataclass(frozen=True)
class AppliedMove:
    fen: str
    san: str
    status: str


class BoardService:
    @staticmethod
    def normalize_fen(fen: str) -> str:
        if fen == "startpos":
            return chess.STARTING_FEN

        try:
            board = chess.Board(fen)
        except ValueError as exc:
            raise InvalidPositionError("Invalid FEN position") from exc

        return board.fen()

    @staticmethod
    def status_for_fen(fen: str) -> str:
        board = BoardService.board_from_fen(fen)

        if board.is_checkmate():
            return "checkmate"
        if board.is_stalemate():
            return "stalemate"
        if board.is_insufficient_material():
            return "draw_insufficient_material"
        if board.can_claim_fifty_moves():
            return "draw_fifty_move_claim_available"
        if board.can_claim_threefold_repetition():
            return "draw_threefold_claim_available"

        return "in_progress"

    @staticmethod
    def apply_move(fen: str, uci: str) -> AppliedMove:
        if BoardService.status_for_fen(fen) != "in_progress":
            raise GameNotInProgressError("Game is not in progress")

        board = BoardService.board_from_fen(fen)

        try:
            move = chess.Move.from_uci(uci)
        except ValueError as exc:
            raise IllegalMoveError("Move must be valid UCI notation") from exc

        if move not in board.legal_moves:
            raise IllegalMoveError("Move is not legal in the current position")

        san = board.san(move)
        board.push(move)
        next_fen = board.fen()

        return AppliedMove(
            fen=next_fen,
            san=san,
            status=BoardService.status_for_fen(next_fen),
        )

    @staticmethod
    def board_from_fen(fen: str) -> chess.Board:
        try:
            return chess.Board(BoardService.normalize_fen(fen))
        except ValueError as exc:
            raise InvalidPositionError("Invalid FEN position") from exc
