from flask import Flask, jsonify, Response
from classes.User import User
from datetime import *

def create_response(response:Response, status_code: int, message: str, args:dict):
    response.data = jsonify({'message': message, "args": args}).get_data()
    response.status_code = status_code
    return response

def create_login_success_response(user:User, response:Response, message:str, max_age: timedelta | int , samesite_val:str):
    response.data = jsonify({'message': message}).get_data()
    response.set_cookie(key="login_session", value=user.get_current_session(), max_age=max_age, samesite=samesite_val)
    response.status_code = 200
    return response