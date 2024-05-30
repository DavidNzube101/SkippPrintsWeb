from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from .db import dbORM
from . import DateToolKit as dtk

import base64
import imghdr
import random
import datetime as dt
from datetime import datetime

def getOppositeTheme(theme):
	if theme == 'light':
		return 'dark'
	else:
		return 'light'

def getDateTime():
	# Getting Date-Time Info
	current_date = dt.date.today()
	current_time = datetime.now().strftime("%H:%M:%S")

	# Date Format: "YYYY-MM-DD"
	formatted_date = current_date.strftime("%Y-%m-%d")
	date = formatted_date
	time = current_time

	return [date, time]

def HTMLBreak(n):
	breaks = ""

	for x in range(int(n)):
		breaks = breaks + "\n<br>"	

	return breaks

def get_mime_type(data):
    decoded_data = base64.b64decode(data)
    image_type = imghdr.what(None, h=decoded_data)
    return f'image/{image_type}' if image_type else 'application/pdf'

def calcTimeDifference(dpt, ct):
	return [int(x) for x in ("[" + str(datetime.strptime(dpt, "%H:%M") - datetime.strptime(ct, "%H:%M:%S")).replace(":", ", ").replace("-1 day, ", "") + "]").strip("[]").split(", ")]

User, Record = dbORM.get_all("User"), dbORM.get_all("Record")

def go_to(screen_id, _redirect=False, **kwargs):
	if _redirect == False:
		u = User[f'{current_user.id}']
	
		return render_template("dashboard.html",
			CUser = u,
			UserOrders = dbORM.find_all('Record', 'user_id', u['id']),

			ScreenID = screen_id,

			UploadData = kwargs['UploadData'],
			OrderData = kwargs['OrderData'],
			MerchantData = kwargs['MerchantData'],

			AppTheme = u['user_theme'],
			AppThemeOpposite = getOppositeTheme(u['user_theme']),

			DTK = dtk,
			ToString = str,
			getMIME = get_mime_type,
			TimeDifference = calcTimeDifference,
			CurrentTime = getDateTime()[1],
			HTMLBreak_ = HTMLBreak
		)
	else:
		return redirect(url_for("views.dashboard"))
	