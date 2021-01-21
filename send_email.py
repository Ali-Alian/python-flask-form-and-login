from email.mime.text import MIMEText
import smtplib



class Sending_email():

    def __init__(self, name, company, email, latter):
        self.name = name 
        self.company = company 
        self.email = email 
        self.latter = latter


    def send_email(self):
        
        # user password for the Admin email
        self.from_email = "Admin.email@gmail.com" # your email gose here
        self.Admin_email_password = "Admin email password" # your password gose here

        # massage for the user and admin
        self.subject = "Email From Kachali.com"
        self.massageToAdmin = f"User {self.name} from {self.company} with {self.email} send you a {self.latter}"
        self.massageToUser = f"Dear: {self.name} we have recived your information"

        # massage bonding for the admin and the user 
        self.msg=MIMEText(self.massageToUser, 'html') 
        self.msg['Subject']=self.subject
        self.msg['To']=self.email
        self.msg['From']=self.from_email

        # server handling and email recivers 
        self.server = smtplib.SMTP("smtp.gmail.com", 587) 
        self.server.starttls()
        self.server.login(self.from_email, self.Admin_email_password) # login to admin email to send email to users
        self.server.sendmail(self.from_email, "Admin.email@gmail.com", self.massageToAdmin) # sending email
        self.server.send_message(self.msg)

        return self.msg, self.server 

# a = Sending_email.send_email()
# a = Sending_email()



# return self.name, self.company, self.email, self.latter, self.from_email, self.Admin_email_password, self.subject, self.massageToAdmin, self.massageToUser, self.msg, self.server 