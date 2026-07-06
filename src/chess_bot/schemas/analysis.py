from pydantic import BaseModel, Field

from chess_bot.services.board import BoardService


class MoveAnalysisRequest(BaseModel):
    fen: str = Field(
        default="startpos",
        description="FEN string, or 'startpos' for the standard starting position.",
    )

    @property
    def normalized_fen(self) -> str:
        return BoardService.normalize_fen(self.fen)


class MoveAnalysisResponse(BaseModel):
    fen: str
    move: str | None
    san: str | None
    reason: str
