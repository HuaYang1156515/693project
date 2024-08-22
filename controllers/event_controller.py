from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from services import event_service 
from models.event_model import Event  
from app import db
from config import setting
from models.event_registration_model import EventRegistration

event_bp = Blueprint('event', __name__)

@event_bp.route('/event_management', methods=['GET'])
def event_management():
    events = event_service.get_all_events()
    return render_template("front/event/event_list.html",events=events)

@event_bp.route('/view_event/<int:event_id>', methods=['GET'])
def view_event(event_id):
    event = event_service.get_event_by_id(event_id)
    return render_template("admin/event_detail.html",event = event)

@event_bp.route('/create_event', methods=['GET','POST'])
def create_event():
    categories = event_service.get_categories()
    if request.method == 'POST':
        name = request.form['name']
        description=request.form['description']
        location=request.form['location']
        date=request.form['date']
        end_date=request.form['end_date']
        intro = request.form['intro']
        category_id=request.form['category_id']
        image = request.files['image']
        if image:
            image.save('static/images/event/' + image.filename)
            image_name= '/static/images/event/'+ image.filename
        else:
            image_name = setting.default_image
        event_service.create_event(name, description, location, date,end_date,category_id,intro,image_name,current_user.id)
        flash("Created event successful")
        return redirect(url_for('event.event_management'))
    return render_template("front/event/create_event.html",categories=categories)

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




