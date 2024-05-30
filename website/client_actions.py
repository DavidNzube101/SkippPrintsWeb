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

client_actions = Blueprint('client_actions', __name__)
c_a = client_actions

def encode_image(file_storage):
    # Read the uploaded image data
    image_data = file_storage.read()

    # Encode the image data
    encoded_string = base64.b64encode(image_data).decode("utf-8")

    return encoded_string

def getDateTime():
    # Getting Date-Time Info
    current_date = dt.date.today()
    current_time = datetime.now().strftime("%H:%M:%S")

    # Date Format: "YYYY-MM-DD"
    formatted_date = current_date.strftime("%Y-%m-%d")
    date = formatted_date
    time = current_time

    return [date, time]

def get_mime_type(data):
    decoded_data = base64.b64decode(data)
    image_type = imghdr.what(None, h=decoded_data)
    return f'image/{image_type}' if image_type else f'text/{image_type}'

@c_a.route("/create-order", methods=['POST'])
def create_order():
    
    # request.form = json.loads(request.data)

    nums = []
    for x in range(10):
        nums.append(x)

    datestamp = getDateTime()[0]

    try:
        payment_type = "both" if dbORM.get_all("User")[f'{current_user.id}']['is_pro_user'] == "True" else "online"
    except:
        payment_type = "online"

    _ = {
      "narration": request.form['narration'],
      "price": request.form['price'],
      "image": payment_type,
      "image_path": "",
      "password": f'{random.choice(nums)}{random.choice(nums)}{random.choice(nums)}{random.choice(nums)}',
      "user_id": str(current_user.id),
      "delivery_period_date": request.form['delivery_date_period'],
      "delivery_period_time": request.form['delivery_time_period'],
      "number_of_copies": request.form['noc'],
      "print_format": request.form['print_format'],
      'timestamp': f'{getDateTime()[1]}',
      'datestamp': f'{getDateTime()[0]}',
      "delivery_address_period": request.form['delivery_address_period'],
      "phone_number": request.form['phone_num'],
      "address_close": request.form['address_close'] if request.form['address_close'] != "Select a location close to you" else "Nil"
    }

    dbORM.add_entry("Record", encrypt.encrypter(str(_)))

    _stringedUD = str([True, dbORM.find_one("Record", "narration", str(request.form['narration'])), int(request.form['noc']), range])

    return render_template("to-payments.html", UploadData=_stringedUD, price=(request.form['price']).replace("N", "").replace(".00", ""), COrder=dbORM.get_all("Record")[f"{dbORM.find_one('Record', 'datestamp', datestamp)}"], CUser=dbORM.get_all("User")[f'{current_user.id}'], ToInt=int)

    # return ScreenGoRoute.go_to("5", OrderData='None', MerchantData=[['None', 'Enter your Merchant ID to see orders']], UploadData=[True, dbORM.find_one("Record", "narration", str(request.form['narration'])), int(request.form['noc']), range])

@c_a.route('/upload-documents', methods=['POST'])
def upload_documents():
    Record = dbORM.get_all("Record")
    order_id = dbORM.find_one("Record", "id", str(request.form["order_id"]))
    order_id_str = str(order_id)
    the_order = Record[f'{order_id}']
    copies = int(the_order['number_of_copies'])

    for n in range(copies):
        image = request.files[f'documents_to_print_{n}']
        filename = secure_filename(image.filename)

        # image_path = eval(eval("Record[order_id_str]['image_path']"))
        # print(f">>>>>>>>>>>{eval(image_path)}<<<<<<>>>>>>>>>>>{type(eval(image_path))}<<<<<<<<<<<<<<<<<<<<<")
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')

        # image_list = eval(eval("Record[order_id_str]['image']"))
        # image_list.append(encode_image(image))

        _image_path = {f'image_path{n}': str(image_path)}

        dbORM.update_entry("Record", f'{dbORM.find_one("Record", "id", order_id_str)}', encrypt.encrypter(str(_image_path).replace('"', "'")), dnd=False)

        dbORM.update_entry("Record", f'{dbORM.find_one("Record", "id", order_id_str)}', str({f'image{n}': f'{encode_image(image)}'}), dnd=True)

    
    return ScreenGoRoute.go_to("1", _redirect=True, OrderData='None', UploadData='None', MerchantData=[['None', 'Enter your Merchant ID to see orders']])

@c_a.route("/re-order", methods=['POST'])
def reOrder():
    try:
        dbORM.delete_entry("Record", f'{request.form["order_id"]}')
    except Exception as e:
        pass

    return ScreenGoRoute.go_to("3", OrderData='None', UploadData='None', MerchantData=[['None', 'Enter your Merchant ID to see orders']])

@c_a.route("/delete-order/<string:order_id>")
def deleteOrder(order_id):
    dbORM.delete_entry("Record", f'{order_id}')
    return ScreenGoRoute.go_to("1", _redirect=True, OrderData='None', UploadData='None', MerchantData=[['None', 'Enter your Merchant ID to see orders']])






