
from flask_mail import Mail, Message
from flask import Flask

app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'reddi.lokesh@gmail.com',
	MAIL_PASSWORD = ''
	)
mail = Mail(app)

def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


def send_mail(message,email):
	try:
		print('message '+message)
		print('email '+email)
		msg = Message("Send Mail Tutorial!",
		  sender="reddi.lokesh@gmail.com",
		  recipients=[email])
		msg.body = message          
		send_async_email(msg)
		return 'Mail sent!'
	except Exception as e:
		return('exception '+str(e))

