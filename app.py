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
    cookie = request.cookies

    is_user_authenticated, message = check_if_authenticated(cookie)
    if not is_user_authenticated:
        message = "Please login to view cock"
        return create_error_response(response, 403, message, None)

    return render_template('website/cock.html')

@app.route('/signup/', methods=["POST"])
def signup():
    args = request.form
    response = make_response()

    #check if user already logged in
    is_user_authenticated, message = check_if_authenticated(request.cookies)
    if is_user_authenticated:
        message = "You are already logged in silly"
        return create_error_response(response, 403, message, None)

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

    #check if user already logged in
    is_user_authenticated, message = check_if_authenticated(request.cookies)
    if is_user_authenticated:
        message = "You are already logged in silly"
        return create_error_response(response, 403, message, None)
    
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

@app.route('/logout/', methods = ["POST"])
def logout():
    args = request.form
    response = make_response()

    #check if user already logged in
    is_user_authenticated, message = check_if_authenticated(request.cookies)
    if not is_user_authenticated:
        message = "You are not even logged in"
        return create_error_response(response, 403, message, None)

    cookie = request.cookies
    session_token = cookie.get("login_session")

    #nonce validation
    valid_nonce, message = nonce_validation(args["Nonce"])
    if(not valid_nonce):
        return create_error_response(response, 409, message, args)
    
    #check if user is authenticated
    is_user_authenticated, message = check_if_authenticated(cookie)
    if not is_user_authenticated:
        return create_error_response(response, 403, message, None)
    
    #create the user
    userID = None
    with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
        cursor.execute(get_user_id_using_session_token,(session_token,))
        userID = cursor.fetchone()[0]
        cursor.execute(get_username_using_user_id, (userID,))
        userName = cursor.fetchone()[0]
    user = User(userName, init_by_email=False)
    
    #delete session from db
    was_session_deleted, message = user.logout(request)
    if not was_session_deleted:
        return create_error_response(response, 403, message, args)
    
    #delete cookie from user browser
    message = "User logged out"
    response.data = jsonify({'message': message}).get_data()
    response.set_cookie(key="login_session", value=session_token, max_age=-1, samesite="Lax")
    response.status_code = 200

    return response

@app.route('/forgot-password/', methods = ["POST"])
def forgot_password():
    pass
