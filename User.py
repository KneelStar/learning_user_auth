import bcrypt
import secrets
from datetime import datetime, timedelta
import database.db as db
from database.sql_queries import *

'''
User class variables:
user_id
username
email
password_salt
password_hash
_is_email_verified
created_at
updated_at
reset_password_token
reset_password_token_expiry
email_verification_token
email_verification_token_expiry
current_session
current_session_expiry
sessions
'''


class User:
    def __init__(self, username, email):
        self._user_id = None
        self._username = username
        self._email = email
        self._password_salt = None
        self._password_hash = None
        self._is_email_verified = None
        self._created_at = None
        self._updated_at = None
        self._reset_password_token = None
        self._reset_password_token_expiry = None
        self._email_verification_token = None
        self._email_verification_token_expiry = None
        self._current_session = None
        self._current_session_expiry = None
        self._sessions = None

    def hash_password(self, password, salt):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def generate_salt(self):
        return bcrypt.gensalt()

    def generate_token(self):
        return secrets.token_hex(32)

    def create_user_in_db(self, password):
        self._password_salt = self.generate_salt()
        self._password_hash = self.hash_password(password, self.get_password_salt())
        self._email_verification_token = self.generate_token()
        
        try:
            with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
                cursor.execute(add_user_to_db, (self.get_username(), self.get_email(), self.get_password_hash(), self.get_password_salt(),))
                db_connection.commit()
                
                cursor.execute(get_user_id_using_username, (self.get_username(),))
                self._user_id = cursor.fetchone()[0]

                cursor.execute(add_email_verification_token_to_email_veri_table, (self.get_user_id(), self.get_email_verification_token()))
                db_connection.commit()
                
                return True, "User Signed Up Successfully"
        except Exception as e:
            print(e)
            return False, "Error Occured While Signing Up User" 

    def validate_password(self, password):
        # Placeholder for login logic
        # Check if the provided password matches the hashed password
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def create_session(self):
        pass

    def is_logged_in(self):
        return bool(self.get_current_session())

    def forgot_password(self):
        # Placeholder for generating a password reset token
        # Replace this with your actual password reset logic
        self._reset_password_token = self.generate_token()

    def set_user_id(self, user_id):
        self._user_id = user_id

    def get_user_id(self):
        return self._user_id

    def set_user_name(self, user_name):
        self._user_name = user_name

    def get_username(self):
        return self._username

    def set_email(self, email):
        self._email = email

    def get_email(self):
        return self._email

    def set_password_hash(self, password_hash):
        self._password_hash = password_hash

    def get_password_hash(self):
        return self._password_hash

    def set_password_salt(self, password_salt):
        self._password_salt = password_salt

    def get_password_salt(self):
        return self._password_salt
    
    def set_is_email_verified(self, is_email_verified):
        self._is_email_verified = is_email_verified

    def get_is_email_verified(self):
        return self._is_email_verified
    
    def get_created_at(self, created_at):
        self._created_at = created_at

    def get_created_at(self):
        return self._created_at
    
    def set_updated_at(self, updated_at):
        self._updated_at = updated_at

    def get_updated_at(self):
        return self._updated_at

    def set_reset_password_token(self, reset_password_token):
        self._reset_password_token = reset_password_token

    def get_reset_password_token(self):
        return self._reset_password_token

    def set_reset_password_token_expiry(self, refresh_password_token_expiry):
        self._reset_password_token_expiry = refresh_password_token_expiry

    def get_reset_password_token_expiry(self):
        return self._reset_password_token_expiry

    def set_email_verification_token(self, email_verification_token):
        self._email_verification_token = email_verification_token
    
    def get_email_verification_token(self):
        return self._email_verification_token

    def set_email_verification_token_expiry(self, email_verification_token_expiry):
        self._email_verification_token_expiry = email_verification_token_expiry
        
    def get_email_verification_token_expiry(self):
        return self._email_verification_token_expiry

    def get_current_session(self):
        return self._current_session
    
    def get_current_session_expiry(self):
        return self._current_session_expiry
    
    def get_all_current_sessions(self):
        return self._sessions
