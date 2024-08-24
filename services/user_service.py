from models.user_model import User
from app import db
from services import DbText

def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()

def create_user(name, login, password, role, status, description, image_name):
    new_user = User(name=name, login=login, password=password, role=role, status=status,description=description,pic=image_name)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_login(login):
    return User.query.filter_by(login=login).first()

def update_user(user_id, name,  password, role, status,description,pic):
    sql =f"""UPDATE users SET 
    name = '{name}',
    password = '{password}',
    role = '{role}', status = '{status}',pic = '{pic}', description = '{description}' WHERE id = '{user_id}';"""
    DbText.db_execute(sql)
    return True

def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user

def get_all_users():
    sql ="""select * from users"""
    result = DbText.query_all(sql)
    return result