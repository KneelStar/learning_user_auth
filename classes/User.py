import bcrypt
import secrets
from datetime import datetime, timedelta
import database.db as db
from database.sql_queries import *

'''
User instance variables:
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
    def __init__(self, identifier:str, init_by_email:bool):
        self._user_id = None
        self._username = None
        self._email = None
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
        
        if init_by_email:
            self._email = identifier
            self.get_basic_info_of_user_from_db(by_email=True)
        else:
            self._username = identifier
            self.get_basic_info_of_user_from_db(by_email=False)

    def generate_token(self):
        return secrets.token_hex(32)

    def get_basic_info_of_user_from_db(self, by_email:bool):
        with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
            if(by_email):
                cursor.execute(get_user_id_using_email,(self.get_email(),))
                self.set_user_id(cursor.fetchone()[0])

                cursor.execute(get_username_using_user_id,(self.get_user_id(),))
                self.set_username(cursor.fetchone()[0])
            else:
                cursor.execute(get_user_id_using_username,(self.get_username(),))
                self.set_user_id(cursor.fetchone()[0])

                cursor.execute(get_email_using_username,(self.get_user_id(),))
                self.set_email(cursor.fetchone()[0])

    def validate_password(self, password:str):
        # Placeholder for login logic
        # Check if the provided password matches the hashed password
        is_it_valid_password = bcrypt.checkpw(password.encode('utf-8'), self.get_password_hash().encode('utf-8'))
        return is_it_valid_password, "Username/Email/Password incorrect" if not is_it_valid_password else "Password is valid"
    
    def create_session(self, flag:str):
        if(flag == 'remember-me'):
            pass
        elif flag == 'mobile':
            pass
        elif flag == 'sso':
            pass
        else:
            pass
        pass

    def is_logged_in(self):
        return bool(self.get_current_session())

    def forgot_password(self):
        # Placeholder for generating a password reset token
        # Replace this with your actual password reset logic
        self.set_reset_password_token(self.generate_token())

    def set_user_id(self, user_id:int):
        self._user_id = user_id

    def get_user_id(self):
        return self._user_id

    def set_username(self, user_name:str):
        self._username = user_name

    def get_username(self):
        return self._username

    def set_email(self, email:str):
        self._email = email

    def get_email(self):
        return self._email

    def set_password_hash(self, password_hash:str):
        self._password_hash = password_hash

    def get_password_hash(self):
        if not self._password_hash:
            with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
                cursor.execute(get_password_hash_using_user_id, (self.get_user_id(),))
                self.set_password_hash(cursor.fetchone()[0])

        return self._password_hash

    def set_password_salt(self, password_salt:bytes):
        self._password_salt = password_salt

    def get_password_salt(self):
        return self._password_salt
    
    def set_is_email_verified(self, is_email_verified:bool):
        self._is_email_verified = is_email_verified

    def get_is_email_verified(self):
        return self._is_email_verified
    
    def set_created_at(self, created_at:datetime):
        self._created_at = created_at

    def get_created_at(self):
        return self._created_at
    
    def set_updated_at(self, updated_at:datetime):
        self._updated_at = updated_at

    def get_updated_at(self):
        return self._updated_at

    def set_reset_password_token(self, reset_password_token:str):
        self._reset_password_token = reset_password_token

    def get_reset_password_token(self):
        return self._reset_password_token

    def set_reset_password_token_expiry(self, refresh_password_token_expiry:datetime):
        self._reset_password_token_expiry = refresh_password_token_expiry

    def get_reset_password_token_expiry(self):
        return self._reset_password_token_expiry

    def set_email_verification_token(self, email_verification_token:str):
        self._email_verification_token = email_verification_token
    
    def get_email_verification_token(self):
        return self._email_verification_token

    def set_email_verification_token_expiry(self, email_verification_token_expiry:datetime):
        self._email_verification_token_expiry = email_verification_token_expiry
        
    def get_email_verification_token_expiry(self):
        return self._email_verification_token_expiry

    def get_current_session(self):
        return self._current_session
    
    def get_current_session_expiry(self):
        return self._current_session_expiry
    
    def get_all_current_sessions(self):
        return self._sessions