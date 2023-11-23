from flask import Flask

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
    return "Home"


@app.route('signup/')
def signup():
    pass

@app.route('login/')
def login():
    pass

@app.route('forgot-password/')
def forgot_password():
    pass
