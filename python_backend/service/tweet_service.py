class TweetService:
    def __init__(self, tweet_dao: object):
        self.dao = tweet_dao
        
    def tweet(self,
              user_id: int,
              tweet_content: str):
        
        if len(tweet_content) > 300:
            return False
        
        return self.dao.insert_tweet(user_id=user_id,
                                     tweet_content=tweet_content)
        
    def timeline(self,
                 user_id: int):
        return self.dao.get_timeline(user_id)
