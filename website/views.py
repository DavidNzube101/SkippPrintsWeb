from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from flask_login import login_required, current_user


import base64
import imghdr
import datetime as dt

from .db import db
from .db import dbORM
from . import encrypt
from . import ScreenGoRoute

if dbORM == None:
    User, Record = None, None
else:
    User, Record = dbORM.get_all("User"), dbORM.get_all("Record")


today = dt.datetime.now().date()


views = Blueprint('views', __name__)

def get_mime_type(data):
    decoded_data = base64.b64decode(data)
    image_type = imghdr.what(None, h=decoded_data)
    return f'image/{image_type}' if image_type else ''

@views.route("/")
def welcome():
    
    return render_template("landing.html")

@views.route("/dashboard")
@login_required
def dashboard():
    
    return ScreenGoRoute.go_to("1", OrderData='None', UploadData='None', MerchantData=[['None', 'Enter your Merchant ID to see orders']])

@views.route("/dashboard/<string:screen_number>")
@login_required
def dashboardPages(screen_number):
    
    return ScreenGoRoute.go_to(screen_number, OrderData='None', UploadData='None', MerchantData=[['None', 'Enter your Merchant ID to see orders']])

@views.route("/view-order/<string:user_name>/order/<string:order_id>")
@login_required
def viewOrder(user_name, order_id):
    
    try:
        theUser = dbORM.find_one("User", "name", user_name)
        CUser = User[f'{theUser}']

        theOrder = dbORM.find_one("Record", "id", order_id)
        COrder = Record[f'{theOrder}']

        return ScreenGoRoute.go_to("94", _redirect=False, UploadData='None', MerchantData=[['None', 'Enter your Merchant ID to see orders']], OrderData=[CUser, COrder, int(COrder['number_of_copies'])])
    except Exception as e:
        return ScreenGoRoute.go_to("1", _redirect=False, UploadData='None', MerchantData=[['None', 'Enter your Merchant ID to see orders']], OrderData='None')
        