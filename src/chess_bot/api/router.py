from fastapi import APIRouter

from chess_bot.api.routes import analysis, games, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
api_router.include_router(games.router, prefix="/api/v1/games", tags=["games"])
