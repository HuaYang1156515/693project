from services import DbText

def get_all_events_visit():
    sql = f"""select * from events"""
    result = DbText.query_all(sql)
    return result

def get_all_events(user_id):
    sql =f"""SELECT 
    e.*, 
    IF(e.end_date > NOW(), 0, 1) AS normal,
    IF(f.user_id IS NOT NULL, 1, 2) AS if_f,
    IF(e.author_id = '{user_id}', 1, 2) AS if_my
FROM 
    events e
LEFT JOIN 
    event_registrations er ON e.id = er.event_id
LEFT JOIN 
    favorites f ON e.id = f.event_id AND f.user_id = '{user_id}'
WHERE 
    e.end_date > NOW() and e.status = 0
ORDER BY 
    e.id DESC
LIMIT 12;
"""
    result = DbText.query_all(sql)
    return result

def get_my_events(user_id):
    sql =f"""SELECT 
    e.*, 
    er.status AS registration_status
FROM 
    events e
LEFT JOIN 
    event_registrations er ON e.id = er.event_id AND er.user_id = 1
WHERE 
    e.author_id != '{user_id}' 
    AND e.status = 0
ORDER BY 
    e.id DESC
LIMIT 12;
"""
    result = DbText.query_all(sql)
    return result

def get_my_favorite(user_id):
    sql =f"""SELECT 
    e.*, 
    f.created_at AS favorite_created_at
FROM 
    events e
JOIN 
    favorites f ON e.id = f.event_id
WHERE 
    e.author_id != {user_id}
    AND f.user_id = {user_id} and e.status = 0
ORDER BY 
    e.id DESC
LIMIT 12;"""
    result = DbText.query_all(sql)
    return result

def get_user(user_id):
    sql =f"""select * from users where id = '{user_id}'"""
    result = DbText.query_one(sql)
    return result

def update_user(user_id, name,  password, role, status,description,pic):
    sql =f"""UPDATE users SET 
    name = '{name}',
    password = '{password}',
    role = '{role}', status = '{status}',pic = '{pic}', description = '{description}' WHERE id = '{user_id}';"""
    DbText.db_execute(sql)
    return True