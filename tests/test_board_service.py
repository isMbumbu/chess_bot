import pytest

from chess_bot.services.board import BoardService, IllegalMoveError


def test_startpos_normalizes_to_starting_fen() -> None:
    assert BoardService.normalize_fen("startpos").startswith(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    )


def test_apply_move_updates_position() -> None:
    result = BoardService.apply_move("startpos", "e2e4")

    assert result.san == "e4"
    assert result.status == "in_progress"
    assert "4P3" in result.fen


def test_apply_move_rejects_illegal_move() -> None:
    with pytest.raises(IllegalMoveError):
        BoardService.apply_move("startpos", "e2e5")
