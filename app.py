from flask import Flask, render_template, request
from classes.User import User
from classes.New_User import New_User
from utils.field_validation import *

app = Flask(__name__)

'''
       +----------------+
       | User Visits '/'|
       +--------+-------+
                |
                v
          +-----+------+
          | Has Valid  |
          |   Cookie?  |
          +-----+------+
                |
        +-------+--------+
    No  |           Yes  |
        v                v
  +-----+-----+    +-----+------+
  | Not Logged |   |   Show     |
  |   In       |   |   Pic      |
  +------------+   +------------+
'''
@app.route('/')
def home():
    return render_template('website/cock.html')

@app.route('/signup/', methods = ["POST"])
def signup():
    args = request.form

    valid_input, message = signup_input_validation(args["Username"], args["Email"], args["Password"])
    if(not valid_input):
        return [message, args], 409

    valid_nonce, message = nonce_validation(args["Nonce"])
    if(not valid_nonce):
        return [message, args], 409
    
    new_user_saved_to_db, message = New_User(args["Username"], args["Email"], args["Password"])

    if(not new_user_saved_to_db):
        return [message, request.form], 409
    
    user = User(args["Email"], init_by_email=True)
    
    #send verification email (@app.route('/send-email-veri/'))
    #response, code = url_for(send_email_verification)
    #create a modal notifying the status of verification email to the user (https://www.w3schools.com/w3css/tryit.asp?filename=tryw3css_modal) 

    user.create_session(flag="regular")
    #send session cookie
    #send verification email
    return 'User Signed Up, !Logged In, and !Verification Email Sent'
    

@app.route('/login/', methods = ["POST"])
def login():
    args = request.form
    
    #user input validation. user can use username or email, and password to login
    valid_input, message = [None, None]
    if(args.get('Username')):
        valid_input, message = is_valid_username(args["Username"])
    else:
        valid_input, message = is_valid_email(args["Email"])

    if(not valid_input):
        return [message, request.form], 409
    
    #nonce validation
    valid_nonce, message = nonce_validation(args["Nonce"])
    if(not valid_nonce):
        return [message, request.form], 409
    
    #create user
    user = None
    if(args.get('Username')):
        user = User(args["Username"], init_by_email=False)
    else:
        user = User(args["Email"], init_by_email=True)
    
    #check password
    valid_password, message = user.validate_password(args["Password"])
    if(not valid_password):
        return [message, request.form], 409
    
    #create session
    was_session_created, message = user.create_session(flag="regular")
    if not was_session_created:
        return [message, request.form], 409
    
    #send session cookie ((hostonly vs httponly), samesite, sessiontoken, username, secure?)
    return "User logged in"

@app.route('/forgot-password/', methods = ["POST"])
def forgot_password():
    pass
