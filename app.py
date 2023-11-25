from flask import Flask, render_template, request
from db import getDatabaseConnection
from input_validation import user_input_validation
from security import *

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

    if(user_input_validation):
        pass

    generated_salt = get_random_salt()
    hashed_pass = hash_password(args["Password"], generated_salt)

    db = getDatabaseConnection()
    
    db.close
    return 'User Signed Up'

@app.route('/login/', methods = ["POST"])
def login():
    pass

@app.route('/forgot-password/', methods = ["POST"])
def forgot_password():
    pass
