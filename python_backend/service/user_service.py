import os
import jwt
import bcrypt
from datetime import datetime, timedelta


class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao
        
    def create_new_user(self, user):
        is_created = self.user_dao.insert_user(user)
        return is_created
    
    def login(self, user):
        data = self.user_dao.get_user_id_and_password(user)
        
        if not data:
            return False
        if bcrypt.checkpw(password=user.password.encode('utf-8'),
                          hashed_password=data.hashed_password.encode('utf-8')):
            payload = {'user_id': data.id,
                       'exp': datetime.utcnow() + timedelta(seconds=60 * 60)}
            token = jwt.encode(payload, os.environ['JWT_SECRET_KEY'], 'HS256')
            return token
        else:
            return False
        
    def get_user_by_id(self, user):
        return self.user_dao.get_user_by_id(user)
    
    def follow(self, user_id, user_id_to_follow):
        return self.user_dao.insert_follow(user_id, user_id_to_follow)
    
    def unfollow(self, user_id, user_id_to_unfollow):
        return self.user_dao.delete_follow(user_id, user_id_to_unfollow)
