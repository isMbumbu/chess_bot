from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fen: str = Field(index=True)
    status: str = Field(default="in_progress", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Move(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id", index=True)
    move_number: int = Field(index=True)
    uci: str
    san: str
    fen_after: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
