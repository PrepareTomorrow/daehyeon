from pydantic import BaseModel

class TweetBase(BaseModel):
    tweet: str