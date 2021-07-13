import graphene
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from starlette.graphql import GraphQLApp

from bhagavad_gita_api.api import deps
from bhagavad_gita_api.api.api_v2.api import api_router
from bhagavad_gita_api.config import settings
from bhagavad_gita_api.crud import get_valid_api_keys
from bhagavad_gita_api.graphql import Query

API_KEY_NAME = "X-API-KEY"
api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(
    db: Session = Depends(deps.get_db),
    api_key_header: str = Security(api_key_header_auth),
) -> None:
    if api_key_header not in get_valid_api_keys(db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key.",
        )


app = FastAPI(
    title="Bhagavad Gita API",
    description="The Bhagavad Gita Application Programming Interface (API) "
    "allows a web or mobile developer to use the Bhagavad Gita text "
    "in their web or mobile application(s). It is a RESTful API that "
    "follows some of the Best Practices for designing a REST API which "
    "makes it easy for developers to use and implement.",
    version="2.0",
    dependencies=[Security(get_api_key, scopes=["openid"])],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))
app.include_router(api_router, prefix=settings.API_V2_STR)


def cli():
    # this function will be called when run from cli
    uvicorn.run(
        "bhagavad_gita_api.main:app",
        host="0.0.0.0",
        port=8081,
        reload=bool(settings.debug),
    )
