from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from chess_bot.db.session import get_session
from chess_bot.models.game import Game, Move
from chess_bot.schemas.game import (
    CreateGameRequest,
    GameResponse,
    MoveRequest,
    MoveResponse,
)
from chess_bot.services.board import (
    BoardService,
    GameNotInProgressError,
    IllegalMoveError,
    InvalidPositionError,
)

router = APIRouter()


def require_persisted_id(value: int | None, resource: str) -> int:
    if value is None:
        raise RuntimeError(f"{resource} was not persisted")

    return value


@router.post("", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
async def create_game(
    payload: CreateGameRequest,
    session: AsyncSession = Depends(get_session),
) -> GameResponse:
    try:
        fen = BoardService.normalize_fen(payload.fen)
    except InvalidPositionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    game = Game(fen=fen, status=BoardService.status_for_fen(fen))
    session.add(game)
    await session.commit()
    await session.refresh(game)
    return GameResponse.model_validate(game)


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: int,
    session: AsyncSession = Depends(get_session),
) -> GameResponse:
    game = await session.get(Game, game_id)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    return GameResponse.model_validate(game)


@router.post("/{game_id}/moves", response_model=MoveResponse)
async def make_move(
    game_id: int,
    payload: MoveRequest,
    session: AsyncSession = Depends(get_session),
) -> MoveResponse:
    game = await session.get(Game, game_id)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    try:
        result = BoardService.apply_move(game.fen, payload.uci)
    except (GameNotInProgressError, IllegalMoveError, InvalidPositionError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    latest_move = await session.scalar(
        select(Move).where(Move.game_id == game_id).order_by(Move.id.desc())
    )
    move_number = 1 if latest_move is None else latest_move.move_number + 1

    game.fen = result.fen
    game.status = result.status
    game.updated_at = datetime.now(UTC)
    move = Move(
        game_id=require_persisted_id(game.id, "Game"),
        move_number=move_number,
        uci=payload.uci,
        san=result.san,
        fen_after=result.fen,
    )

    session.add(game)
    session.add(move)
    await session.commit()
    await session.refresh(move)

    return MoveResponse(
        id=require_persisted_id(move.id, "Move"),
        game_id=require_persisted_id(game.id, "Game"),
        move_number=move.move_number,
        uci=move.uci,
        san=move.san,
        fen_after=move.fen_after,
        status=game.status,
    )
