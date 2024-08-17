from models.event_model import Event
from app import db

def get_event_by_id(event_id):
    return Event.query.get(event_id)

def create_event(name, description, location, date, created_by, category_id):
    new_event = Event(
        name=name,
        description=description,
        location=location,
        date=date,
        created_by=created_by,
        category_id=category_id
    )
    db.session.add(new_event)
    db.session.commit()
    return new_event

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

def get_all_events():
    return Event.query.all()
