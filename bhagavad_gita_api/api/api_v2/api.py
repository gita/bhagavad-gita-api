from fastapi import APIRouter

from bhagavad_gita_api.api.api_v2.endpoints import gita, social

api_router = APIRouter()
api_router.include_router(gita.router)
api_router.include_router(social.router, include_in_schema=True)
