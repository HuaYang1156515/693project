import mysql.connector
from mysql.connector import Error

# Database connection details
dbuser = "HuaYang"   
dbpass = "abcd1234!"   
dbhost = "HuaYang.mysql.pythonanywhere-services.com" 
dbport = "3306"
dbname = "HuaYang$HuaYang777"


"""
dbuser = "root"   
dbpass = "abcd1234"   
dbhost = "localhost" 
dbport = "3306"
dbname = "community_event_planner"
"""

def get_connection():
    
    try:
        connection = mysql.connector.connect(
            host=dbhost,
            user=dbuser,
            password=dbpass,
            database=dbname,
            port=dbport
        )
        if connection.is_connected():
            print("Connected to the database")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
