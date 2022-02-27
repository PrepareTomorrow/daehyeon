from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, ForeignKeyConstraint
from sqlalchemy.sql import func

from .conn import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(255), nullable=False, unique=True)
    hashed_password = Column(VARCHAR(255), nullable=False)
    profile = Column(VARCHAR(2000), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class UsersFollowList(Base):
    __tablename__ = 'users_follow_list'

    user_id = Column(Integer, nullable=False, primary_key=True)
    follow_user_id = Column(Integer, nullable=False, primary_key=True, )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    ForeignKeyConstraint(('user_id', 'follow_user_id'),
                         ('users.id', 'users.id'))


class Tweets(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    tweet = Column(VARCHAR(300), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    ForeignKeyConstraint(('user_id',), ('users.id',))
