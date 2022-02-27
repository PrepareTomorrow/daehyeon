from ..tables import Tweets, UsersFollowList

from ..schemas.tweet_schemas import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_


class TweetDao:
    def __init__(self, engine):
        self.engine = engine
        self.tweet_table = Tweets
        self.follow_table = UsersFollowList
        
    def insert_tweet(self,
                     user_id: int,
                     tweet_content: str):
        db = sessionmaker(bind=self.engine)()
        query = self.tweet_table(user_id=user_id,
                                 tweet=tweet_content)
        try:
            db.add(query)
            db.commit()
            return True
        except:
            return False
        finally:
            db.close()
        
    def get_timeline(self,
                     user_id: int):
        db = sessionmaker(bind=self.engine)()
        try:
            data = db.query(self.tweet_table)\
                .join(self.follow_table,
                    self.follow_table.user_id == user_id, isouter=True)\
                .filter(or_(self.tweet_table.user_id == user_id,
                            self.tweet_table.user_id == self.follow_table.follow_user_id))\
                .all()
        finally:
            db.close()
            
        if len(data) == 0:
            return False
        else:
            return {'timeline': [{'user_id': tweet.user_id,
                                  'tweet': tweet.tweet}] for tweet in data}