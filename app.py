from flask import Flask, render_template, request
from db import getDatabaseConnection
from input_validation import user_input_validation
from security import *
import User

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
    return render_template('cock.html')


@app.route('/signup/', methods = ["POST"])
def signup():
    args = request.form

    valid_input, message = user_input_validation(args)
    if(not valid_input):
        return message, 409

    valid_nonce, message = nonce_validation(args["Nonce"]
    if(not valid_once):
        return message, 409
    
    user = User(args["Username"], args["Email"], args["Password"]).create_user_in_db()
    return 'User Signed Up
    

@app.route('/login/', methods = ["POST"])
def login():
    pass

@app.route('/forgot-password/', methods = ["POST"])
def forgot_password():
    pass
