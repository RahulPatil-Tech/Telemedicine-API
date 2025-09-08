from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import jsonify
from .models import User

def roles_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if user.role not in roles:
                return jsonify({"msg": "Forbidden: You do not have the required role"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper