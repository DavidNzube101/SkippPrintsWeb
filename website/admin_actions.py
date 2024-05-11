# Flask essentials
from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

# Python Essentials
import random
import os
import datetime as dt
from datetime import datetime
from datetime import timedelta
import json
import base64
import imghdr

# App Essentials
from .db import dbORM
from . import DateToolKit as dtk
from . import encrypt
from . import ScreenGoRoute

if dbORM == None:
    User, Record = None, None

today = dt.datetime.now().date()

current_date = dt.date.today()
formatted_date = current_date.strftime("%Y-%m-%d")
cleanDate = dtk.clean_date(formatted_date)

admin_actions = Blueprint('admin_actions', __name__)
a_a = admin_actions

def encode_image(file_storage):
    # Read the uploaded image data
    image_data = file_storage.read()

    # Encode the image data
    encoded_string = base64.b64encode(image_data).decode("utf-8")

    return encoded_string

def getDateTime():
    # Getting Date-Time Info
    current_date = dt.date.today()
    current_time = datetime.now().strftime("%H:%M")

    # Date Format: "YYYY-MM-DD"
    formatted_date = current_date.strftime("%Y-%m-%d")
    date = formatted_date
    time = current_time

    return [date, time]

def get_mime_type(data):
    decoded_data = base64.b64decode(data)
    image_type = imghdr.what(None, h=decoded_data)
    return f'image/{image_type}' if image_type else f'text/{image_type}'

merchant_ids = [950395, 902922, 990234, 443256, 998283, 586992, 423881, 345991, 199372, 109120, 495204, 121109, 331245, 425331, 553991, 434111]

@a_a.route('/verify-merchant', methods=['GET', 'POST'])
def verifyMerchant():
    if request.method == 'POST':
        if request.form['merchant_id'] != "" and int(request.form['merchant_id']) in merchant_ids:
            allOrders = dbORM.get_all("Record")
            allOrdersList = []
            for k, v in allOrders.items():
                allOrdersList.append(allOrders[f'{k}'])

            allOrdersList.remove({"id": "0", "narration": "NULL", "price": "NULL", "image": "NULL", "image_path": "NULL", "user_id": "NULL", "timestamp": "NULL", "datestamp": "NULL", "delivery_period_date": "NULL", "delivery_period_time": "NULL", "number_of_copies": "NULL", "print_format": "NULL"})

            return ScreenGoRoute.go_to("23", UploadData='None', OrderData='None', MerchantData=[[True, ''], allOrdersList])

        else:
            return ScreenGoRoute.go_to("23", UploadData='None', OrderData='None', MerchantData=[['None', 'Merchant ID incorrect']])

    return ScreenGoRoute.go_to("23", UploadData='None', OrderData='None', MerchantData=[['None', 'Enter your Merchant ID to see orders']])

@a_a.route('/merchant-view-order/<string:order_id>')
def merchantViewOrder(order_id):
    try:
        allOrders = dbORM.get_all("Record")
        theOrder = dbORM.find_one("Record", "id", order_id)

        return render_template("m-order-view.html", OrderData=allOrders[f'{theOrder}'], status_text="")
    except Exception as e:
        
        return ScreenGoRoute.go_to("1", _redirect=True, OrderData='None', MerchantData=['None', 'Enter your Merchant ID to see orders'], UploadData='None')

@a_a.route('/verify-order-password', methods=['POST'])
def verifyOrderPassword():

    order_id = request.form['order_id']
    theOrder = dbORM.get_all("Record")[f'{dbORM.find_one("Record", "id", order_id)}']
    if request.form['order_password'] == theOrder['password']:
        dbORM.delete_entry("Record", order_id)
        return render_template("m-order-view.html", OrderData=theOrder, status_text="Client's code match. Order dispatched successfully")


    return render_template("m-order-view.html", OrderData=theOrder, status_text="Client's code doesn't match")