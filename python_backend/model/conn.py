import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def create_engine_session(test: bool = False):
    if not test:
        SQLALCHEMY_DATABASE_URL = os.environ.get('DB_URL')
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL
        )
    else:
        SQLALCHEMY_DATABASE_URL = os.environ.get('TEST_DB_URL')
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL
        )

    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, session_local


engine, session = create_engine_session()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
