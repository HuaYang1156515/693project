from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from services import event_service 
from models.event_model import Event  
from app import db
from models.event_registration_model import EventRegistration

event_bp = Blueprint('event', __name__)

@event_bp.route('/event_management', methods=['GET'])
def event_management():
    events = event_service.get_all_events()
    return jsonify([event.serialize() for event in events]), 200

@event_bp.route('/view_event/<int:event_id>', methods=['GET'])
def view_event(event_id):
    event = event_service.get_event_by_id(event_id)
    return render_template("admin/event_detail.html",event = event)

@event_bp.route('/event', methods=['POST'])
def add_event():
    data = request.json
    new_event = event_service.create_event(
        name=data['name'],
        description=data['description'],
        location=data['location'],
        date=data['date'],
        created_by=data['created_by'],
        category_id=data['category_id']
    )
    return jsonify(new_event.serialize()), 201

@event_bp.route('/event/<int:event_id>', methods=['PUT'])
def update_event_info(event_id):
    data = request.json
    updated_event = event_service.update_event(
        event_id,
        name=data.get('name'),
        description=data.get('description'),
        location=data.get('location'),
        date=data.get('date'),
        category_id=data.get('category_id')
    )
    if updated_event:
        return jsonify(updated_event.serialize()), 200
    return jsonify({"error": "Event not found"}), 404

@event_bp.route('/event/<int:event_id>', methods=['DELETE'])
def delete_event_info(event_id):
    deleted_event = event_service.delete_event(event_id)
    if deleted_event:
        return jsonify({"message": "Event deleted successfully"}), 200
    return jsonify({"error": "Event not found"}), 404

@event_bp.route('/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)




@event_bp.route('/event/<int:event_id>/register', methods=['POST'])
@login_required 
def register_event(event_id):
    event = Event.query.get_or_404(event_id) 
    if event:
        registration = EventRegistration(user_id=current_user.id, event_id=event.id)
        db.session.add(registration)
        db.session.commit()
        flash('Successfully registered for the event!')
        return redirect(url_for('event_bp.event_detail', event_id=event.id))
    flash('Event not found!')
    return redirect(url_for('home'))
