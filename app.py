from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
#######################################
import database
from model import Forming, User
from login_register import login_page, register_page, mytemp_page, logout_page
from contact_us import forming_page, form_page
# from login_register import login_manager
#######################################
from flask_bootstrap import Bootstrap
from flask_login import login_user, LoginManager, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'WhatTheFuckIsHappening!!!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/form_collector'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)


database.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template("index.html")
    # if request.form['submit_button'] == 'somthing':
    #     return render_template('login.html')

app.register_blueprint(forming_page)
app.register_blueprint(form_page)
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(logout_page)
app.register_blueprint(mytemp_page)




if __name__ == '__main__':
    app.debag = True
    app.run()