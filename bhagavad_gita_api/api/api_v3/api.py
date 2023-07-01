from fastapi import APIRouter

from bhagavad_gita_api.api.api_v3.endpoints import gita, social

api_router_v3 = APIRouter()
api_router_v3.include_router(gita.router)
api_router_v3.include_router(social.router, include_in_schema=True)
