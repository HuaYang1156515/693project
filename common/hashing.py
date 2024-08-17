"""from flask_hashing import Hashing
from config import setting

hashing = Hashing()

def init_app(app=None):
    if app:
        hashing.init_app(app)

def hash_password(password):
     
    return hashing.hash_value(password, setting.salt)

def check_password(password, hashed_password):
     
    return hashing.check_value(password, hashed_password, setting.salt)
"""