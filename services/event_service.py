from models.event_model import Event
from app import db
from services import DbText
from config import setting

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



def get_all_events():
    sql = """SELECT 
    events.*,
    users.name AS author_name
FROM 
    events 
JOIN 
    users 
ON 
    events.author_id = users.id where events.status = 0;"""
    result = DbText.query_all(sql)
    return result

def get_event_by_id(event_id):
    sql = f"""SELECT 
    e.*, 
    er.status AS registration_status
FROM 
    events e
LEFT JOIN 
    event_registrations er ON e.id = er.event_id 
WHERE 
    e.id = '{event_id}' 
    AND e.status = 0;"""
    result = DbText.query_one(sql)
    return result

def create_event(name, description, location, date,end_date,category_id,intro,image_name,user_id):
    sql = """
    INSERT INTO events (name, description, location, date, end_date, category_id, author_id,intro,img)
    VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s);"""
    values = (name, description, location, date, end_date , category_id,user_id,intro,image_name)

    DbText.execute(sql, values)
    return True

def update_event(name, description, location, date, end_date, category_id, intro, image_name, id):
    
    update_query = f"""
    UPDATE events
    SET 
        name = '{name}',
        description = '{description}',
        location = '{location}',
        date = '{date}',
        end_date = '{end_date}',
        category_id = '{category_id}',
        intro = '{ intro}', img = '{image_name}' where id = '{id}';
    """
    DbText.db_execute(update_query)
    return True
    

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


def delete_register(event_id,user_id):
    sql = f"""DELETE FROM event_registrations
WHERE event_id = '{event_id}' AND user_id = '{user_id}';"""
    DbText.db_execute(sql)
    return True

def delete_favorite(event_id,user_id):
    sql = f"""DELETE FROM favorites
WHERE event_id = '{event_id}' AND user_id = '{user_id}';"""
    DbText.db_execute(sql)
    return True

def add_favorite(event_id,user_id):
    sql = f""" INSERT INTO favorites (user_id,event_id)
    VALUES ('{user_id}','{event_id}');"""
    DbText.db_execute(sql)
    return True

def add_register(event_id,user_id):
    sql = f""" INSERT INTO event_registrations (user_id,event_id)
    VALUES ('{user_id}','{event_id}');"""
    DbText.db_execute(sql)
    return True


def query_workshop_cal():
    sql = f"""
    SELECT
        id AS id,
        name,
        CONCAT( '{setting.url}/event/event_detail/', id) AS url,
        UNIX_TIMESTAMP(DATE_SUB(date, INTERVAL 12 HOUR)) * 1000 AS start,
        UNIX_TIMESTAMP(DATE_SUB(end_date, INTERVAL 12 HOUR)) * 1000 AS end
    FROM
        events
    """
    return DbText.query_all(sql)


def  update_event_status(id,status):
    sql =f"""update events set status = '{status}' where id ='{id}'"""
    DbText.db_execute(sql)
    return True
 