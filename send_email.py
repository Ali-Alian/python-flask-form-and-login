from email.mime.text import MIMEText
import smtplib

def send_email(name, company, email, latter):
    name = name
    company = company
    email = email
    latter = latter

    from_email = "example@gmail.com"
    Admin_email_password = "Your_email_password"

    subject = "Email From Kachali.com"
    massageToAdmin = f"User {name} from {company} with {email} send you a {latter}"
    massageToUser = f"Dear: {name} we have recived your information"

    msg=MIMEText(massageToUser, 'html')
    msg['Subject']=subject
    msg['To']=email
    msg['From']=from_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, Admin_email_password)
    server.sendmail(from_email, "example@gmail.com", massageToAdmin)
    server.send_message(msg)
