from fastapi import APIRouter, HTTPException, status

from chess_bot.schemas.analysis import MoveAnalysisRequest, MoveAnalysisResponse
from chess_bot.services.engine import ChessEngine, InvalidPositionError

router = APIRouter()


@router.post("/move", response_model=MoveAnalysisResponse)
async def choose_move(payload: MoveAnalysisRequest) -> MoveAnalysisResponse:
    engine = ChessEngine()

    try:
        result = await engine.choose_move(payload.normalized_fen)
    except InvalidPositionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return MoveAnalysisResponse(
        fen=payload.normalized_fen,
        move=result.move,
        san=result.san,
        reason=result.reason,
    )
