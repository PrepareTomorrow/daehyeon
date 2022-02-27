import bcrypt

from ..tables import Users, UsersFollowList
from ..schemas.user_schemas import *

from sqlalchemy import exc, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import exc as oexc
        

class UserDao:
    def __init__(self, engine):
        self.engine = engine
        self.user_table = Users
        self.follow_table = UsersFollowList
        
    def insert_user(self, user: UserBase):
        db = sessionmaker(bind=self.engine)()
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'),
                                        bcrypt.gensalt())
        
        query = Users(name=user.name,
                      email=user.email,
                      profile=user.profile,
                      hashed_password=hashed_password)
        try:
            db.add(query)
            db.commit()
            return True
        except exc.IntegrityError:
            return False
        finally:
            db.close()
        
    def get_user_id_and_password(self, user: UserLogin):
        db = sessionmaker(bind=self.engine)()
        try:
            data = db.query(self.user_table.id, self.user_table.hashed_password)\
                .filter(self.user_table.email == user.email).first()
        finally:
            db.close()
            
        if data is None:
            return False
        else:
            return data
        
    def get_user_by_id(self,
                       user_id: int):
        db = sessionmaker(bind=self.engine)()
        try:
            query = db.query(self.user_table).filter(self.user_table.id == user_id).first()
        finally:
            db.close()
        
        if query is None:
            return False
        else:
            return True
        
    def insert_follow(self,
                      user_id: int,
                      user_id_to_follow: int):
        db = sessionmaker(bind=self.engine)()
        
        try:
            query = self.follow_table(user_id=user_id,
                                      follow_user_id=user_id_to_follow)
        finally:
            db.close()
        
        try:
            db.add(query)
            db.commit()
            return True
        except exc.IntegrityError as e:
            return False
        finally:
            db.close()
        
    def delete_follow(self,
                      user_id: int,
                      user_id_to_unfollow: int):
        db = sessionmaker(bind=self.engine)()
        
        try:
            query = db.query(self.follow_table)\
                .filter(and_(self.follow_table.user_id == user_id,
                            self.follow_table.follow_user_id == user_id_to_unfollow)).first()
        finally:
            db.close()
            
        if query is None:
            return False
        
        try:
            db.delete(query)
            db.commit()
            return True
        except oexc.UnmappedInstanceError:
            return False
        finally:
            db.close()
