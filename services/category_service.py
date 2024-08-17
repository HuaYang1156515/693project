from models.category_model import Category
from app import db

def get_category_by_id(category_id):
    return Category.query.get(category_id)

def create_category(name, status='0'):
    new_category = Category(name=name, status=status)
    db.session.add(new_category)
    db.session.commit()
    return new_category

def update_category(category_id, name=None, status=None):
    category = get_category_by_id(category_id)
    if category:
        if name:
            category.name = name
        if status is not None:
            category.status = status
        db.session.commit()
    return category

def delete_category(category_id):
    category = get_category_by_id(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
    return category

def get_all_categories():
    return Category.query.all()
