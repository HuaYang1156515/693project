from services import DbText

def get_all_events():
    sql ="""select * from events"""
    result = DbText.query_all(sql)
    return result
