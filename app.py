from flask import Flask, render_template, request, make_response
from classes.User import User
from classes.New_User import New_User
from utils.field_validation import *
from utils.response_creator import *
from utils.constants import *

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
@app.route('/', methods=["GET"])
def home():
    response = make_response()

    is_user_authenticated, message = check_if_authenticated(request)
    if not is_user_authenticated:
        return create_error_response(response, 403, message, None)

    return render_template('website/cock.html')

@app.route('/signup/', methods=["POST"])
def signup():
    args = request.form
    response = make_response()

    valid_input, message = signup_input_validation(args["Username"], args["Email"], args["Password"])
    if not valid_input:
        return create_error_response(response, 409, message, args)

    valid_nonce, message = nonce_validation(args["Nonce"])
    if not valid_nonce:
        return create_error_response(response, 409, message, args)

    new_user_saved_to_db = New_User(args["Username"], args["Email"], args["Password"])
    if not new_user_saved_to_db:
        return create_error_response(response, 409, message, args)

    user = User(args["Email"], init_by_email=True)

    was_session_created, session_validity_amount, message = user.create_session(args["Session_flag"])
    if not was_session_created:
        return create_error_response(response, 409, message, args)

    # Send verification email
    user.send_email_verification()

    # Send session cookie
    message = "User signed up, logged in, and !verification email sent"
    return create_login_success_response(user, response, message, session_validity_amount, "Lax")

@app.route('/login/', methods = ["POST"])
def login():
    args = request.form
    response = make_response()
    
    #user input validation. user can use username or email, and password to login
    valid_input, message = [None, None]
    if(args.get('Username')):
        valid_input, message = is_valid_username(args["Username"])
    else:
        valid_input, message = is_valid_email(args["Email"])

    if(not valid_input):
        return create_error_response(response, 409, message, args)
    
    #nonce validation
    valid_nonce, message = nonce_validation(args["Nonce"])
    if(not valid_nonce):
        return create_error_response(response, 409, message, args)
    
    #create user
    user = None
    if(args.get('Username')):
        user = User(args["Username"], init_by_email=False)
    else:
        user = User(args["Email"], init_by_email=True)
    
    #check password
    valid_password, message = user.validate_password(args["Password"])
    if(not valid_password):
        return create_error_response(response, 409, message, args)
    
    #create session
    was_session_created, session_validity_amount, message = user.create_session(args["Session_flag"])
    if not was_session_created:
        return create_error_response(response, 409, message, args)
    
    #send session cookie ((hostonly vs httponly), samesite, sessiontoken, username, secure?)
    message = "User logged in"
    return create_login_success_response(user, response, message, session_validity_amount, "Lax")

@app.route('/forgot-password/', methods = ["POST"])
def forgot_password():
    pass
