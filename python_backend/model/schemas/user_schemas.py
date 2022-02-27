from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    password: str
    profile: str
    
    
class UserLogin(BaseModel):
    email: str
    password: str
    

class Follow(BaseModel):
    user_id_to_follow: int
    
class UnFollow(BaseModel):
    user_id_to_unfollow: int
