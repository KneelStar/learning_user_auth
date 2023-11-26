from flask import Flask, render_template, request
from field_validation import *
from User import User

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

    valid_input, message = all_user_input_validation(args["Username"], args["Email"], args["Password"])
    if(not valid_input):
        return [message, request.form], 409

    valid_nonce, message = nonce_validation(args["Nonce"])
    if(not valid_nonce):
        return [message, request.form], 409
    
    user = User(args["Username"], args["Email"])
    successful_signup, message = user.create_user_in_db(args["Password"])
    if(not successful_signup):
        return [message, request.form], 409
    
    #send session cookie
    #send verification email
    return 'User Signed Up, !Logged In, and !Verification Email Sent'
    

@app.route('/login/', methods = ["POST"])
def login():
    pass

@app.route('/forgot-password/', methods = ["POST"])
def forgot_password():
    pass
