from models.user_model import User
from app import db
from services import DbText
from config import setting

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


def query_workshop_cal():
    sql = f"""
    SELECT
        id AS id,
        name,
        CONCAT( '{setting.url}/event/view_event/', id) AS url,
        UNIX_TIMESTAMP(DATE_SUB(date, INTERVAL 12 HOUR)) * 1000 AS start,
        UNIX_TIMESTAMP(DATE_SUB(end_date, INTERVAL 12 HOUR)) * 1000 AS end
    FROM
        events
    """
    return DbText.query_all(sql)
    


def get_all_events():
    sql = """select events.*,
    users.name AS author_name
FROM 
    events 
JOIN 
    users 
ON 
    events.author_id = users.id where events.status = 0;"""
    result = DbText.query_all(sql)
    return result

def cancel_event(event_id, status):
    sql = f"""update events set status = '{status}' where id = '{event_id}'"""
    DbText.db_execute(sql)
    return True

def filter_events(query):
    result= DbText.query_all(query)
    return result

def get_all_categories():
    sql = """select * from categories"""
    results = DbText.query_all(sql)
    return results

def get_event(id):
    sql = f"""select * from events where id ='{id}'"""
    results = DbText.query_one(sql)
    return results

def edit_event(id,name, description, location, date,end_date,category_id,intro,image_name):
    sql = f"""UPDATE events
SET 
    name = '{name}',
    description = '{description}',
    location = '{location}',
    date = '{date}',
    end_date = '{end_date}',
    category_id = {category_id},
    intro = '{intro}',
    img = '{image_name}'
WHERE 
    id = {id};"""
    DbText.db_execute(sql)
    return True