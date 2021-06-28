from fastapi import APIRouter

from .endpoints import gita

api_router = APIRouter()
api_router.include_router(gita.router)
