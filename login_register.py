
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, Blueprint, session
import database
from model import Forming, User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class registerForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email!!!'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


# login_manager = LoginManager()
# def init_app(app):

# login_manager.init_app(app)
# login_manager.login_view = 'login'


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# userInfo = False
login_page = Blueprint('login_page', __name__, template_folder='templates')
@login_page.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    #user = User.query.filter_by(username=form.username.data).first()
    if form.validate_on_submit():
        
        
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                # userInfo = True
                return redirect(url_for('mytemp_page.mytemp'))
       
    #login_error = "NOTHING FOR ERROR"
    # userInfo = False
    return render_template('login.html', form=form)


register_page = Blueprint('register_page', __name__, template_folder='templates')
@register_page.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()

    if form.validate_on_submit():
        hashed_pass = generate_password_hash(form.password.data, method='sha256')
        if database.db.session.query(User).filter(User.email == form.email.data).count() == 0:

            new_user = User(username = form.username.data, email = form.email.data,password = hashed_pass)
            database.db.session.add(new_user)
            database.db.session.commit()
            return redirect(url_for('mytemp_page.mytemp'))
        

   
    return render_template('register.html', form=form)



mytemp_page = Blueprint('mytemp_page', __name__, template_folder='templates')
@mytemp_page.route('/mytemp')
@login_required
def mytemp():
    

    return render_template('mytemp.html', name=current_user.username)


logout_page = Blueprint('logout_page', __name__, template_folder='templates')
@logout_page.route('/logout')
@login_required
def logout():
    
    logout_user()
    
    return redirect(url_for('login_page.login'))
