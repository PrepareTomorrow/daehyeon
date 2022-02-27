from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model.conn import Base, engine, session
from model.dao import UserDao, TweetDao
from model.schemas import user_schemas, tweet_schemas
from service import UserService, TweetService

from view import create_endpoints
import uvicorn


class Services:
    def __init__(self, engine):
        self.user_service = UserService(UserDao(engine))
        self.tweet_service = TweetService(TweetDao(engine))
        
class Schemas:
    def __init__(self):
        self.user_schemas = user_schemas
        self.tweet_schemas = tweet_schemas


def create_app(engine_):
    app_ = FastAPI()

    Base.metadata.create_all(bind=engine_)

    origins = [
        "http://localhost:5000",
        "http://127.0.0.1:5000"
    ]

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app_


if __name__ == '__main__':
    services = Services(engine)
    schemas = Schemas()
    app = create_app(engine)
    create_endpoints(app, services, schemas)
    uvicorn.run(app)
