from models.category_model import Category
from app import db
from services import DbText

def get_category_by_id(category_id):
    return Category.query.get(category_id)

def create_category(name):
    sql = f"""INSERT INTO categories (name) VALUES ('{name}');"""
    DbText.db_execute(sql)
    return True

def update_category(category_id, name=None):
    sql =f"""UPDATE categories SET 
    name = '{name}' WHERE id = '{category_id}';"""
    DbText.db_execute(sql)
    return True

def delete_category(category_id):
    sql = f"""DELETE FROM categories
WHERE id = '{category_id}' ;"""
    DbText.db_execute(sql)
    return True

def get_all_categories():
    sql = """select * from categories"""
    results = DbText.query_all(sql)
    return results
