from models.user_model import User
from app import db

def get_admin_by_id(admin_id):
    return User.query.filter_by(id=admin_id, role='admin').first()

def create_admin(name, login, password, status='active'):
    new_admin = User(name=name, login=login, password=password, role='admin', status=status)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin

def update_admin(admin_id, name=None, login=None, password=None, status=None):
    admin = get_admin_by_id(admin_id)
    if admin:
        if name:
            admin.name = name
        if login:
            admin.login = login
        if password:
            admin.password = password
        if status:
            admin.status = status
        db.session.commit()
    return admin

def delete_admin(admin_id):
    admin = get_admin_by_id(admin_id)
    if admin:
        db.session.delete(admin)
        db.session.commit()
    return admin
