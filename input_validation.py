import re  # For email validation

def is_valid_username(username):
    # Placeholder function for checking if the username exists in the database
    # Replace this with your actual database check logic
    return not username_exists_in_db(username)

def is_valid_email(email):
    # Simple email validation using regular expression
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_pattern, email))

def is_valid_password(password):
    # Placeholder function for password validation criteria
    # Replace this with your actual password validation logic
    return len(password) >= 8  # Example: Password must be at least 8 characters

def username_exists_in_db(username):
    # Placeholder function for checking if the username exists in the database
    # Replace this with your actual database check logic
    # For now, assume that the username does not exist
    return False

def user_input_validation(username, email, password):
    """
    Validate user input for registration.

    :param username: Username to validate
    :param email: Email to validate
    :param password: Password to validate
    :return: A tuple (is_valid, error_message)
             is_valid is a boolean indicating if the input is valid
             error_message is a string providing an error message if validation fails
    """
    if not is_valid_username(username):
        return False, "Username already exists in the database."

    if not is_valid_email(email):
        return False, "Invalid email address."

    if not is_valid_password(password):
        return False, "Invalid password. Password must be at least 8 characters."

    return True, "Input is valid."