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
import os
import pymongo
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
# setting mail configs
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASSWORD")

mail = Mail(app)
CORS(app)


# defining the routes
# home route
@app.route('/')
def home():
    response = {"status": true,
                "message": "up and active (:", "author": "opensaucerer", "description": "software engineer with 5+ years of experience busy doing juju?",
                "portfolio": "https://opensaucerer.com"}
    return jsonify(response), 200


def populate(name, email, message):

    body = f"""
             <h3> Hello Perfection, You've got a message from {name}</h3>

             <p>Below is the message</p><br />

              <p>{message}</p>
              <p> </p>
              <p> </p>
              <p>You can reach out back to {name} through their email--: {email}</p>
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
                      sender=name, recipients=[os.environ.get('EMAIL_RECIPIENT')])
        msg.body = populate(name=name, email=email, message=message)
        msg.html = populate(name=name, email=email, message=message)

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
