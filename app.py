from flask import Flask, render_template, request, make_response
from classes.User import User
from classes.New_User import New_User
from utils.field_validation import *
from utils.response_creator import *
from utils.constants import *
from utils.emailer import *

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
        return create_response(response, 403, message, None)

    return render_template('website/cock.html')

@app.route('/signup/', methods=["POST"])
def signup():
    args = request.form
    response = make_response()

    #check if user already logged in
    is_user_authenticated, message = check_if_authenticated(request.cookies)
    if is_user_authenticated:
        message = "You are already logged in silly"
        return create_response(response, 403, message, None)

    valid_input, message = signup_input_validation(args["Username"], args["Email"], args["Password"])
    if not valid_input:
        return create_response(response, 409, message, args)

    valid_nonce, message = nonce_validation(args["Nonce"])
    if not valid_nonce:
        return create_response(response, 409, message, args)

    new_user_saved_to_db = New_User(args["Username"], args["Email"], args["Password"])
    if not new_user_saved_to_db:
        return create_response(response, 409, message, args)

    user = User(args["Email"], init_by_email=True)

    was_session_created, session_validity_amount, message = user.create_session(args["Session_flag"])
    if not was_session_created:
        return create_response(response, 409, message, args)

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
        return create_response(response, 403, message, None)
    
    #user input validation. user can use username or email, and password to login
    valid_input, message = [None, None]
    if(args.get('Username')):
        valid_input, message = is_valid_username(args["Username"])
    else:
        valid_input, message = is_valid_email(args["Email"])

    if(not valid_input):
        return create_response(response, 409, message, args)
    
    #nonce validation
    valid_nonce, message = nonce_validation(args["Nonce"])
    if(not valid_nonce):
        return create_response(response, 409, message, args)
    
    #create user
    user = None
    if(args.get('Username')):
        user = User(args["Username"], init_by_email=False)
    else:
        user = User(args["Email"], init_by_email=True)
    
    #check password
    valid_password, message = user.validate_password(args["Password"])
    if(not valid_password):
        return create_response(response, 409, message, args)
    
    #create session
    was_session_created, session_validity_amount, message = user.create_session(args["Session_flag"])
    if not was_session_created:
        return create_response(response, 409, message, args)
    
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
        return create_response(response, 403, message, None)

    cookie = request.cookies
    session_token = cookie.get("login_session")

    #nonce validation
    valid_nonce, message = nonce_validation(args["Nonce"])
    if(not valid_nonce):
        return create_response(response, 409, message, args)
    
    #check if user is authenticated
    is_user_authenticated, message = check_if_authenticated(cookie)
    if not is_user_authenticated:
        return create_response(response, 403, message, None)
    
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
        return create_response(response, 403, message, args)
    
    #delete cookie from user browser
    message = "User logged out"
    response.data = jsonify({'message': message}).get_data()
    response.set_cookie(key="login_session", value=session_token, max_age=-1, samesite="Lax")
    response.status_code = 200

    return response

@app.route('/forgot-password/', methods = ["POST"])
def forgot_password():
    args = request.form
    response = make_response()

    #nonce validation
    valid_nonce, message = nonce_validation(args["Nonce"])
    if(not valid_nonce):
        return create_response(response, 409, message, args)

    #1. username or email valid? 
    #2. If so, but doesn't exist in db, return 200 even if username/email is not in db. 
        #It's lying but good for security to not tell if the username/email someone entered exists or 
        #not. Avoids brute force attacks.
    #3. get userid from username/email
    valid_input, message = [None, None]
    input_in_db, message2 = [None, None]
    
    if(args.get('Username')):
        valid_input, message = is_valid_username(args["Username"])
        input_in_db, message2 = check_if_username_or_email_in_db(args["Username"], email_check=False)
    else:
        valid_input, message = is_valid_email(args["Email"])
        input_in_db, message2 = check_if_username_or_email_in_db(args["Email"], email_check=True)

    if not valid_input:
        return create_response(response, 409, message, args)

    if not input_in_db:
        return create_response(response, 200, "Email with a reset password link has been emailed to you", args)
    
    #generate reset token
    password_reset_token = User.generate_forgot_pass_or_session_token(User)
    
    #save the token to db
    userID = None
    with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
        if args.get("Username"):
            cursor.execute(get_user_id_using_username,(args["Username"],))
            userID = cursor.fetchone()[0]
        else:
            cursor.execute(get_user_id_using_email,(args["Email"],))
            userID = cursor.fetchone()[0]
            # print(userID, password_reset_token)

        cursor.execute(add_reset_pass_token_with_userID, (userID, password_reset_token))
        db_connection.commit()

    #send forgot pass token to user email
    user_email_address = None
    if(args.get('Email')):
        user_email_address = args["Email"]
    else:
        with db.get_database_connection() as db_connection, db_connection.cursor() as cursor:
            cursor.execute(get_email_using_username, (args["Username"],))
            user_email_address = cursor.fetchone()[0]

    send_email("Password Reset Link", password_reset_token, "DEFAULT_EMAIL", user_email_address)
    return create_response(response, 200, "Email with a reset password link has been emailed to you", args)
