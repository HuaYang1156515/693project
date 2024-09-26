from models.user_model import User
from app import db
from services import DbText

def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()

def create_user(name, login, password, role, status, description, image_name):
    new_user = User(name=name, login=login, password=password, role=role, status=status,description=description,pic=image_name)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_login(login):
    return User.query.filter_by(login=login).first()

def update_user(user_id, name,  password, role, status,description,pic):
    sql =f"""UPDATE users SET 
    name = '{name}',
    password = '{password}',
    role = '{role}', status = '{status}',pic = '{pic}', description = '{description}' WHERE id = '{user_id}';"""
    DbText.db_execute(sql)
    return True

def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user

def get_all_users():
    sql ="""select * from users"""
    result = DbText.query_all(sql)
    return result




def paginate_results(total_sql, sql, page, per_page):
    # 查询总记录数
    total_items = query_total_items(total_sql)
    
    # 查询分页数据
    items = query_items(page, per_page, sql)
    
    # 创建分页信息
    pagination = paginate(page, per_page, total_items)
    
    return items, pagination

# 分页函数
def paginate(page, per_page, total_items):
    num_pages = (total_items + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < num_pages
    return {
        'page': page,
        'per_page': per_page,
        'total_items': total_items,
        'num_pages': num_pages,
        'has_prev': has_prev,
        'has_next': has_next,
    }

# 查询函数
def query_total_items(sql):
    # 查询总记录数
    result = DbText.query_one(sql)
    total_items = result['total_count'] if result else 0
    return total_items

def query_items(page, per_page, item_sql):
    # 计算起始位置
    offset = (page - 1) * per_page
    
    # 附加分页语句
    item_sql = item_sql + f" LIMIT {offset}, {per_page}"
    
    # 执行分页查询
    items = DbText.query_all(item_sql)
    
    return items
