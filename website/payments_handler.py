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
import requests
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

payments_handler = Blueprint('payments_handler', __name__)
p_h = payments_handler

def getDateTime():
    # Getting Date-Time Info
    current_date = dt.date.today()
    current_time = datetime.now().strftime("%H:%M:%S")

    # Date Format: "YYYY-MM-DD"
    formatted_date = current_date.strftime("%Y-%m-%d")
    date = formatted_date
    time = current_time

    return [date, time]

@p_h.route("/proceed-payments", methods=['POST'])
def proceedPayments():

    UploadData = request.form['uploadata']
    order_id = request.form['order_id']

    auth_headers ={
        "Authorization": "Bearer sk_test_d15379f4ec22d1dd1ae8029efa098ea014866047",
        "Content-Type": "application/json"
    }
    customer_email = dbORM.get_all('User')[f'{current_user.id}']['email']
    auth_data = { "email": customer_email, "amount": f"{int(request.form['price'])}00", "order_id": f"{request.form['order_id']}" } #"{}".format(products[product_id]['price'])
    auth_data = json.dumps(auth_data)
    req = requests.post('https://api.paystack.co/transaction/initialize', headers=auth_headers, data=auth_data)
    response_data = json.loads(req.text)
    paystack_uri = response_data['data']['authorization_url']
    return redirect(paystack_uri)

@p_h.route("/callback")
def showSuccess():
    ref = request.args['trxref']
    auth_headers ={
        "Authorization": "Bearer sk_test_d15379f4ec22d1dd1ae8029efa098ea014866047",
        "Content-Type": "application/json"
    }
    req = requests.get('https://api.paystack.co/transaction/verify/{}'.format(ref), headers=auth_headers)
    tr_data = json.loads(req.text)
    message = tr_data['data']['status']
    amount = tr_data['data']['amount']
    order_id = tr_data['data']['order_id']
    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>{order_id}<<<<<<<<<<<<<<<<<<<<<<<<")
    amount = (amount/100)
    amount = "{:.2f}".format(amount)
    tr_id = tr_data['data']['id']
    return render_template('success.html', tr_id=tr_id, message=message, price=amount, COrder=dbORM.get_all("Record")[f"{order_id}"])