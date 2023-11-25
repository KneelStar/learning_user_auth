import bcrypt
import secrets
from datetime import datetime, timedelta

class User:
    def __init__(self, username, email, password):
        self.user_id = None
        self.username = username
        self.email = email
        self.password_salt = self.generate_salt()
        self.password_hash = self.hash_password(password, self.password_salt)
        self.email_verified = False
        self.email_verification_token = self.generate_token()
        self.email_verification_expiry = datetime.utcnow() + timedelta(days=10)
        self.sessions = []
        self.reset_password_token = None
        self.reset_password_token_expiry = None

    def hash_password(self, password, salt):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def generate_salt(self):
        return bcrypt.gensalt()

    def generate_token(self):
        return secrets.token_hex(32)

    def create_user_in_db(self):
        # Placeholder for database interaction to create a new user
        # Replace this with your actual database logic
        # Store user details including hashed password and salt
        
        # connect to db
        # try:
        #   add user to database
        #   return success
        # catach:
        #   return error
        # return generic failure
        pass

    def login(self, password):
        # Placeholder for login logic
        # Check if the provided password matches the hashed password
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def is_logged_in(self):
        # Placeholder for checking if the user is logged in
        # Replace this with your actual session management logic
        return bool(self.sessions)

    def is_email_verified(self):
        return self.email_verified

    def forgot_password(self):
        # Placeholder for generating a password reset token
        # Replace this with your actual password reset logic
        self.reset_password_token = self._generate_token()
        self.reset_password_token_expiry = datetime.utcnow() + timedelta(hours=1)

    def get_user_id(self):
        return self.user_id

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_hashed_password(self):
        return self.password_hash

    def get_user_salt(self):
        return self.password_salt

    def get_all_current_sessions(self):
        return self.sessions

    def get_password_reset_token(self):
        return self.reset_password_token

    def get_password_reset_token_expiry(self):
        return self.reset_password_token_expiry

    def get_current_session(self):
        # Placeholder for retrieving the current session
        # Replace this with your actual session management logic
        return self.sessions[-1] if self.sessions else None

    def get_email_verification_token(self):
        return self.email_verification_token

    def get_email_verification_token_expiry(self):
        return self.email_verification_expiry

# Example usage:
new_user = User("john_doe", "john.doe@example.com", "secure_password123")
new_user.create_user_in_db()

# Simulate a login attempt
login_successful = new_user.login("secure_password123")
print("Login Successful:", login_successful)

# Simulate a forgot password request
new_user.forgot_password()
print("Password Reset Token:", new_user.get_password_reset_token())
print("Password Reset Token Expiry:", new_user.get_password_reset_token_expiry())

# Check if the user is logged in
print("Is Logged In:", new_user.is_logged_in())

# Check if the email is verified
print("Is Email Verified:", new_user.is_email_verified())
