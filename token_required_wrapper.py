import os
from functools import wraps
import jwt
from flask import jsonify, request


def abort_invalid_token():
    return jsonify({'message': 'a valid token is missing'}), 401


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return abort_invalid_token()

        header_data = request.headers['Authorization']
        header_parts = header_data.split(' ')
        if len(header_parts) != 2 or header_parts[0] != 'Bearer':
            return abort_invalid_token()
        token = header_parts[1]
        try:
            jwt.decode(token, os.environ.get('JWT_SECRET'), algorithms=["HS256"])
        except:
            return abort_invalid_token()

        return f(*args, **kwargs)

    return decorator
