import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from .models import gitaChapterModel
from .database import db_session

db = db_session.session_factory()

class Query(graphene.ObjectType):
    chapters = graphene.List(gitaChapterModel)

    @staticmethod
    def resolve_chapters(parent, info):
        query = gitaChapterModel.get_query(info)  # SQLAlchemy query
        return query.all()

app = FastAPI()
app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))