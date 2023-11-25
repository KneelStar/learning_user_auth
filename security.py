import bcrypt

def get_random_salt():
    return bcrypt.gensalt()

def hash_password(password, salt):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')