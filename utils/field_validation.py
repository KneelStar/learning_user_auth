import re
import database.db as db
from database.sql_queries import *

def is_valid_username(username):
    if '@' in username:
        return False, "Username cannot have @ in it"
    
    if len(username) > 50:
        return False, "Username cannot be more than 50 characters long"
    
    return True, "Username is valid"

def is_valid_email(email):
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if(not re.match(email_pattern, email)):
        return False, "Invalid email"
    
    if len(email) > 100:
        return False, "Email cannot be more than 100 characters long"
    
    return True, "Valid email"

def is_valid_password(password):
    if len(password) < 8:
        return False, "Password less than 8 characters"

    if not any(char.isdigit() for char in password):
        return False, "Password needs at least 1 digit"

    if not any(char in r'!@#$%^&*(),.?":{}|<>' for char in password):
        return False, "Password needs at least 1 special character " + r'(!@#$%^&*(),.?":{}|<>)'

    if not any(char.isupper() for char in password):
        return False, "Password needs at least 1 capital letter"

    return True, "Valid Password"

def check_if_username_or_email_in_db(identifier, email_check):
    does_it_exist_in_db = None
    message = None

    query = count_if_email_exist_in_db if email_check else count_if_username_exist_in_db

    with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
        cursor.execute(query, (identifier,))
        result = cursor.fetchone()

        does_it_exist_in_db = result[0] != 0 
        message = "Email exists in db" if email_check and does_it_exist_in_db else "Username exists in db" if not email_check and does_it_exist_in_db else "Email/Username does not exist in db"

    return does_it_exist_in_db, message

def nonce_validation(nonce_val):
    with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
        cursor.execute(count_if_non_expired_nonce_exist_in_db, (nonce_val,))
        result = cursor.fetchone()

        if result[0] > 0:
            cursor.execute(delete_nonce, (nonce_val,))
            db_connection.commit()
            return True, "Nonce was valid, now deleted from db"

    return False, "Nonce not found in db" if result[0] == 0 else "An Error Occurred While Validating Nonce"

def signup_input_validation(username, email, password):
    valid_username_bool, message = is_valid_username(username)
    if not valid_username_bool:
        return False, message
    
    if check_if_username_or_email_in_db(username, email_check=False)[0]:
        return False, "Username already in databse"

    valid_email_bool, message = is_valid_email(email)
    if not valid_email_bool:
        return False, message
    
    if check_if_username_or_email_in_db(email, email_check=True)[0]:
        return False, "Email already in database"
    
    valid_password_bool, message = is_valid_password(password)
    if not valid_password_bool:
        return False, message

    return True, "Input is valid."