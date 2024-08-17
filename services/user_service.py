from models.user_model import User
from app import db

def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()

def create_user(name, login, password, role='user', status='active'):
    new_user = User(name=name, login=login, password=password, role=role, status=status)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_login(login):
    return User.query.filter_by(login=login).first()

def update_user(user_id, name=None, login=None, password=None, role=None, status=None):
    user = get_user_by_id(user_id)
    if user:
        if name:
            user.name = name
        if login:
            user.login = login
        if password:
            user.password = password
        if role:
            user.role = role
        if status:
            user.status = status
        db.session.commit()
    return user

def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user
