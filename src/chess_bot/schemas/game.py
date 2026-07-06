from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateGameRequest(BaseModel):
    fen: str = Field(default="startpos")


class GameResponse(BaseModel):
    id: int
    fen: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MoveRequest(BaseModel):
    uci: str = Field(examples=["e2e4"])


class MoveResponse(BaseModel):
    id: int
    game_id: int
    move_number: int
    uci: str
    san: str
    fen_after: str
    status: str
