from flask import render_template, request, Blueprint
from send_email import Sending_email

import database
from model import Forming

# send_email = Sending_email()

forming_page = Blueprint('forming_page', __name__, template_folder='templates')
@forming_page.route('/form')
def forming():
    return render_template("form.html")


form_page = Blueprint('form_page', __name__, template_folder='templates')
@form_page.route('/form', methods=["POST"])
def form():

    if request.method == 'POST':
        name = request.form.get('user_name')
        company = request.form.get('company_name')
        email = request.form.get('email_add')
        latter = request.form.get('text_area')

        if database.db.session.query(Forming).filter(Forming.email_ == email).count() == 0:

            data=Forming(name,company,email,latter)
            database.db.session.add(data)
            database.db.session.commit()
            success_massage = "We will be in tuch soon"
            Sending_email(name, company, email, latter).send_email()
            # send_email(name, company, email, latter)
           
            return render_template('form.html',success_massage = success_massage, name=name, company=company, email=email,latter=latter)

    error_massages = f" we alreade have {email} in our database"
    return render_template('form.html', error_massages = error_massages, name = name, company=company, email= email, latter = latter)