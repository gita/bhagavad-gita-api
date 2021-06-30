from fastapi import APIRouter

from bhagavad_gita_api.api.api_v2.endpoints import gita

api_router = APIRouter()
api_router.include_router(gita.router)
