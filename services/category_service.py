from models.category_model import Category
from app import db
from services import DbText

def get_category_by_id(category_id):
    return Category.query.get(category_id)

def create_category(name):
    sql = f"""INSERT INTO categories (name) VALUES ('{name}');"""
    DbText.db_execute(sql)
    return True

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
    sql = """select * from categories"""
    results = DbText.query_all(sql)
    return results
