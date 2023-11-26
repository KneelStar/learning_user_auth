import re
import database.db as db
from database.sql_queries import *

def is_valid_username(username):
    with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
        cursor.execute(count_if_username_exist_in_db, (username,))
        result = cursor.fetchone()

    return result[0] == 0, "Valid Username" if result[0] == 0 else "Username already exists in the database"

def is_valid_email(email):
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if(not re.match(email_pattern, email)):
        return False, "Invalid Email"

    with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
        cursor.execute(count_if_email_exist_in_db, (email,))
        result = cursor.fetchone()

    if(result[0] > 0):
        return False, "Email already in database"
    
    if(result[0] == 0):
        return True, "Valid Email"
    
    return False, "Error occured while validating email"

def is_valid_password(password):
    if len(password) < 8:
        return False, "Password less than 8 characters"

    if not any(char.isdigit() for char in password):
        return False, "Password needs at least 1 digit"

    if not any(char in r'!@#$%^&*(),.?":{}|<>' for char in password):
        return False, "Password needs at least 1 special character"

    if not any(char.isupper() for char in password):
        return False, "Password needs at least 1 capital letter"

    return True, "Valid Password"

def nonce_validation(nonce_val):
    with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
        cursor.execute(count_if_non_expired_nonce_exist_in_db, (nonce_val,))
        result = cursor.fetchone()

        if result[0] > 0:
            cursor.execute(delete_nonce, (nonce_val,))
            db_connection.commit()
            return True, "Nonce was valid, now deleted from db"

    return False, "Nonce not found in db" if result[0] == 0 else "An Error Occurred While Validating Nonce"

def all_user_input_validation(username, email, password):
    valid_username_bool, message = is_valid_username(username)
    if not valid_username_bool:
        return valid_username_bool, message

    valid_email_bool, message = is_valid_email(email)
    if not valid_email_bool:
        return valid_email_bool, message

    valid_password_bool, message = is_valid_password(password)
    if not valid_password_bool:
        return valid_password_bool, message

    return True, "Input is valid."