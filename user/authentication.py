from flask import request, jsonify, session, redirect
from datetime import datetime, timedelta
from .database import user_info
from functools import wraps
import jwt


encryption_secret = '\xb2\x91a\x9d\xac\x18/\xfe\xeeH\x00\xbf7\x9cP\xbe'
algorithm = 'HS256'

#Creating jwt for the user after login
def provide_jwt(user):
    data = {
        '_id': user['_id'],
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }

    token = jwt.encode(data,encryption_secret,algorithm=algorithm)

    return jsonify({'token':token}), 201

#Decorator for verifying if the client has a valid token
def login_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"error":"Token is missing!"}), 401

        try:
            token_payload = jwt.decode(token, encryption_secret, algorithms=[algorithm])
            current_user = user_info.find_one({"_id":token_payload['_id']})
        except:
            return jsonify({"error":"Token is not valid!"}), 401

        return function(current_user, *args, **kwargs)

    return wrap


#### session method ####

def create_session(user):
    session['current_user'] = user['_id']
    return jsonify({"result":"login success"}), 200

def login_required_session(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if 'current_user' in session:
            if session['current_user'] is not None:
                _id  = session['current_user']
                current_user = user_info.find_one({"_id":_id})
                return function(current_user, *args, **kwargs)

        return redirect('/login')

    return wrap

def check_if_session_exists(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if 'current_user' in session:
            if session['current_user'] is not None:
                return redirect('/mypage')

        return function(*args, **kwargs)

    return wrap




def remove_session():
    session.clear()
    return redirect('/')







