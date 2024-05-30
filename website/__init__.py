from flask import Flask, render_template, request, flash, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, logout_user, current_user, login_user, UserMixin

import json
import os
import random

from .db import db
from .db import dbORM
from .encrypt import encrypter

if dbORM == None:
    User, Record = None, None


def initialize_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'skskksksksskkssksksksksk'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__).replace('\\', '/'), 'static/_UM_')
    print(f"UF: ({UPLOAD_FOLDER})")

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .views import views
    from .admin_actions import admin_actions
    from .client_actions import client_actions
    from .payments_handler import payments_handler

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(client_actions, url_prefix='/')
    app.register_blueprint(payments_handler, url_prefix='/')
    app.register_blueprint(admin_actions, url_prefix='/')

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(f"Internal Server Error: {e}")
        return render_template('broken-page.html', error=e), 500

    from flask_login import UserMixin, LoginManager

    FL_Login = LoginManager(app)
    FL_Login.login_view = 'login'

    class UserClass:
        def __init__(self, id):
            self.id = id

        @staticmethod
        def is_authenticated():
            return True

        @staticmethod
        def is_active():
            return True

        @staticmethod
        def is_anonymous():
            return False

        def get_id(self):
            return self.id


        @FL_Login.user_loader
        def load_user(id):
            try:
                u = dbORM.find_one("User", "id", id)
                if not u:
                    return None
                return UserClass(id=dbORM.get_all("User")[f'{u}']['id'])
            except:
                anonymous = {
                    "0": {
                        "id": "0", 
                        "email": "NULL"
                    }
                }
                return UserClass(id=anonymous['0']['id'])


    @app.route("/login", methods=['GET', 'POST']) 
    def login():
        User = dbORM.get_all("User")

        if request.method == 'POST':
            email = request.form.get('user_email')
            password = request.form.get('user_password')

            user = dbORM.find_one("User", "email", email)
            if user and check_password_hash(User[f'{user}']['password'], password):
                # flash("Logged in successfully.", category='Success')

                t_user = UserClass(id=f'{user}')

                login_user(t_user, remember=True)
                

                return redirect(url_for('views.dashboard'))
            else:
                return render_template("login.html", status=("Incorrect password or email. Please try again.", "Error occurred"))

        return render_template('login.html', status=())

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out successfully.", category='Success')
        return redirect(url_for('login'))
    

    return app