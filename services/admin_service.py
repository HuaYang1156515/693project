from models.user_model import User
from app import db
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
    sql = """
    SELECT
        workshop_id AS id,
        title,
        CONCAT(:url_base, '/event/view_event/', workshop_id) AS url,
        'event' AS class,
        UNIX_TIMESTAMP(DATE_SUB(start_date, INTERVAL 12 HOUR)) * 1000 AS start,
        UNIX_TIMESTAMP(DATE_SUB(end_date, INTERVAL 12 HOUR)) * 1000 AS end
    FROM
        workshops
    """
    
    result = db.session.execute(sql, {
        'url_base': setting.url
    })
    
    # Convert result to a list of dictionaries
    data = [dict(row) for row in result]
    
    return data