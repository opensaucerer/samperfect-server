import os
from flask import Flask, url_for, jsonify, render_template, request
from dotenv import load_dotenv
from flask_mail import Message, Mail
from flask_cors import CORS, cross_origin
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
mail = Mail(app)

# defining the routes
# home route


@app.route('/')
def home():
    response = {"status": "success",
                "message": "API is working", "owner": "Perfection Loveday", "description": "I am a software engineer with 2+ years of experience in both backend and frontend software design using Python, NodeJS, Javascript, CSS, HTML, and other related technologies.",
                "portfolio": "https://samperfect.netlify.app"}
    return jsonify(response), 200


# endpoint for sending email
@app.route('/api/v1/submit', methods=["POST"])
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


# running the app
if __name__ == '__main__':
    app.run()
# running the app end
