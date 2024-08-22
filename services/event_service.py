from models.event_model import Event
from app import db
from services import DbText


def get_event_by_id(event_id):
    sql = f"""select * from event where event_id = '{event_id}'"""
    result = DbText.query_one(sql)
    return result

def create_event(name, description, location, date,end_date , category_id,user_id):
    sql = """
    INSERT INTO Events (name, description, location, date, end_date, category_id, author_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    values = (name, description, location, date, end_date , category_id,user_id)

    DbText.execute(sql, values)
    return True

def update_event(event_id, name=None, description=None, location=None, date=None, category_id=None):
    event = get_event_by_id(event_id)
    if event:
        if name:
            event.name = name
        if description:
            event.description = description
        if location:
            event.location = location
        if date:
            event.date = date
        if category_id:
            event.category_id = category_id
        db.session.commit()
    return event

def delete_event(event_id):
    event = get_event_by_id(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
    return event


def get_categories():
    sql = """select * from categories"""
    result = DbText.query_all(sql)
    return result