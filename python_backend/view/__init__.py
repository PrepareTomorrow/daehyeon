import os
import jwt
from functools import wraps

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


def login_required(func):
    @wraps(func)
    def decorated(request: Request, *args, **kwargs):
        access_token = request.headers.get('Authorization')

        if access_token is None:
            return JSONResponse({'message': 'Unauthorized'},
                                status_code=401)
        else:
            try:
                payload = jwt.decode(access_token, os.environ['JWT_SECRET_KEY'], 'HS256')
            except jwt.InvalidTokenError:
                return JSONResponse({'message': 'Unauthorized'},
                                    status_code=401)
            request.__setattr__('user_id', payload['user_id'])
        return func(request, *args, **kwargs)
    return decorated


def create_endpoints(app, services, schemas):
    user_service = services.user_service
    tweet_service = services.tweet_service
    
    user_schemas = schemas.user_schemas
    tweet_schemas = schemas.tweet_schemas
    
    @app.get('/ping', tags=['Health Check'])
    def ping():
        content = {'message': 'pong'}
        return JSONResponse(content=content, status_code=200)
    
    @app.put('/sign-up', tags=['User'])
    def sign_up(new_user: user_schemas.UserBase):

        new_user = user_service.create_new_user(new_user)

        if not new_user:
            return JSONResponse(content=f'Duplicate Entry {new_user}', status_code=400)
        else:
            return JSONResponse(content=new_user, status_code=200)


    @app.post('/login', tags=['User'])
    def login(request: Request,
              user: user_schemas.UserLogin):
        access_token = user_service.login(user)

        if not access_token:
            return JSONResponse(content={'detail': 'Wrong Email or Password'},
                                status_code=400)
        else:
            return JSONResponse(content={'message': 'Login Success!',
                                        'access_token': access_token},
                                status_code=200)


    @app.put('/tweet', tags=['Tweet'])
    @login_required
    def tweet(request: Request,
              new_tweet: tweet_schemas.TweetBase):
        tweet_content = new_tweet.tweet
        user_id = request.headers.get('user_id')

        if len(tweet_content) > 300:
            return HTTPException(400, detail='Cannot Over 300')

        content = tweet_service.tweet(user_id, tweet_content)

        if content is None:
            return HTTPException(400, detail='Unknown Error')

        return JSONResponse(content=content, status_code=200)


    @app.put('/follow', tags=['User'])
    @login_required
    def follow(request: Request,
               user_follow: user_schemas.Follow):
        user_id = request.user_id
        follow_info = [user_id, user_follow.user_id_to_follow]

        for info in follow_info:
            if not user_service.get_user_by_id(info):
                return JSONResponse(content={'detail': 'No User'},
                                    status_code=400)

        if not user_service.follow(follow_info[0], follow_info[1]):
            return JSONResponse(content={'detail': 'Already Following'}, status_code=400)
        else:
            return JSONResponse(content={'user_id': follow_info[0],
                                         'user_id_to_follow': follow_info[1]}, status_code=200)


    @app.delete('/unfollow', tags=['User'])
    @login_required
    def unfollow(request: Request,
                 user_unfollow: user_schemas.UnFollow):
        user_id = request.user_id
        unfollow_info = [user_id, user_unfollow.user_id_to_unfollow]
        
        for info in unfollow_info:
            if not user_service.get_user_by_id(info):
                return JSONResponse(content={'detail': 'No User'},
                                    status_code=400)

        if not user_service.unfollow(unfollow_info[0], unfollow_info[1]):
            return JSONResponse(content={'detail': 'Invalid User'},
                                status_code=400)
        else:
            return JSONResponse(content={'user_id': unfollow_info[0],
                                         'user_id_to_unfollow': unfollow_info[1]},
                                status_code=200)


    @app.get('/timeline', tags=['Tweet'])
    @login_required
    def timeline(request: Request):
        user_id = request.user_id
        tweets = tweet_service.timeline(user_id)
        return JSONResponse(content=tweets, status_code=200) if tweets is not None \
            else JSONResponse(content={'detail': 'No Contents'}, status_code=400)