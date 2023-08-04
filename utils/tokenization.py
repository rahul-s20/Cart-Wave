from flask import Flask, request, jsonify, make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps

# secret = 'rsarkar123456'  //@token_required

secret = 'rsarkar123456'


def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, secret, algorithms=['HS256'])
            print(data)
        # You can use the JWT errors in exception
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        except Exception as er:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)

    return decorated


def encode_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1, minutes=5),
        'iat': datetime.utcnow(),
        'sub': user_id
    }

    options = {
        'expires': f"{datetime.utcnow() + timedelta(days=1, minutes=5)}",
        'httpOnly': True,
        'sameSite': 'none',
        'secure': True,
    }
    return jwt.encode(
        payload,
        secret,
        algorithm='HS256'
    ), options


def decode_token(token):
    return jwt.decode(token, secret, algorithms=['HS256'])
