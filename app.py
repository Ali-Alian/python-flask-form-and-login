from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os
from send_email import send_email
#######################################

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#######################################
# from werkzeug.utils import secure_filename
# from werkzeug.middleware.shared_data import SharedDataMiddleware

# import urllib.request

app = Flask(__name__)
##########################
app.config['SECRET_KEY'] = 'WhatTheFuckIsHappening!!!'
##########################
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:A@!Sql@!a633@localhost/form_collector'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Forming(db.Model):
    __tabalename__='data'
    id=db.Column(db.Integer, primary_key=True)
    name_=db.Column(db.String(80), nullable = False)
    company_=db.Column(db.String(120), nullable = False)
    email_=db.Column(db.String(120), unique=True)
    latter_=db.Column(db.String(300))

    def __init__(self, name_, company_, email_, latter_):
        self.name_=name_
        self.company_=company_
        self.email_=email_
        self.latter_=latter_


###############################

class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15),unique=True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class registerForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email!!!'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
   
###############################



@app.route('/')
def index():
    return render_template("index.html")
    # if request.form['submit_button'] == 'somthing':
    #     return render_template('login.html')

@app.route('/form')
def form_page():
    return render_template("form.html")

@app.route('/form', methods=["POST"])
def form():

    if request.method == 'POST':
        name = request.form.get('user_name')
        company = request.form.get('company_name')
        email = request.form.get('email_add')
        latter = request.form.get('text_area')

        if db.session.query(Forming).filter(Forming.email_ == email).count() == 0:

            data=Forming(name,company,email,latter)
            db.session.add(data)
            db.session.commit()
            success_massage = "We will be in tuch soon"
            send_email(name, company, email, latter)
           
            return render_template('form.html',success_massage = success_massage, name=name, company=company, email=email,latter=latter)

    error_massages = f" we alreade have {email} in our database"
    return render_template('form.html', error_massages = error_massages, name = name, company=company, email= email, latter = latter)



@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    #user = User.query.filter_by(username=form.username.data).first()
    if form.validate_on_submit():
        
        
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('mytemp'))
       
    #login_error = "NOTHING FOR ERROR"
    
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()

    if form.validate_on_submit():
        hashed_pass = generate_password_hash(form.password.data, method='sha256')
        if db.session.query(User).filter(User.email == form.email.data).count() == 0:

            new_user = User(username = form.username.data, email = form.email.data,password = hashed_pass)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('mytemp'))
        

   
    return render_template('register.html', form=form)


@app.route('/mytemp')
@login_required
def mytemp():
    
    return render_template('mytemp.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.debag = True
    app.run()