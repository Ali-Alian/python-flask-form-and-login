from database import db

from flask_login import UserMixin


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