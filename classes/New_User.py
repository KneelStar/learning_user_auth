import bcrypt
import database.db as db
from database.sql_queries import *

class New_User:
    def __init__(self, username:str, email:str, password:str):
        self._username = username
        self._email = email
        self._password_salt = self.generate_salt()
        self._password_hash = self.hash_password(password, self._password_salt) 

    def generate_salt(self):
        return bcrypt.gensalt()
    
    def hash_password(self, password:str, salt:bytes):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    
    def save_user_to_db(self):
        try:
            with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
                cursor.execute(add_user_to_db, (self._username, self._email, self._password_hash, self._password_salt,))
                db_connection.commit()
                return True, "User Signed Up Successfully"
        except Exception as e:
            print(e)
            return False, "Error Occured While Signing Up User" 