from flask import Flask, request
from app import app

@app.route('/send-email-verification/')
def send_email_verification():
    # args = request.form
    pass