from app import db

class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(2), default='0', nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f'<EventRegistration {self.id}>'
