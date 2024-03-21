from flask import request
import jwt
from functools import wraps

from config import config_json
from models.user import UserModel
from repository.user import UserRepository


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if (token := request.headers.get("x-access-token")) is None:
            return {"message": "A valid token is missing!"}, 401
        
        current_user = __get_user(token)
        if current_user is None:
            return { "message": "Invalid token!" }, 401
        
        return f(current_user, *args, **kwargs)
    return decorator


def token_optional(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if (token := request.headers.get("x-access-token")) is None:
            return {"message": "A valid token is missing!"}, 401
        
        current_user = __get_user(token)
        
        return f(current_user, *args, **kwargs)
    return decorator

def __get_user(token) -> UserModel:    
    try:
        data = jwt.decode(token, config_json["token_key"], algorithms=['HS256'])
        return UserRepository().find_by_username(data.get("username"))
    except:
        return None