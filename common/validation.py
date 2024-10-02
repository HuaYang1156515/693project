
from functools import wraps
from flask import abort, render_template
from flask_login import current_user

def admin_required(func):
     
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    return wrapper

def user_required(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'user':
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    return wrapper

def role_required(roles):
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)  # Forbidden or redirect to login
            return func(*args, **kwargs)
        return wrapper
    return decorator

