import mysql.connector

host = 'xxxx'
user = 'xxxxx'
password = 'xxxxxx'
database = 'user_auth_learn'

def get_database_connection():
    
    db_connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    return db_connection