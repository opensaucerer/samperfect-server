# importing required modules
import os
import csv
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


class Hospital(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=False)


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


@app.route('/scrape/')
def scrape():
    try:
        url = 'https://www.hospitalsafetygrade.org/all-hospitals'

        response = requests.get(url).content

        soup = bs(response, "html.parser")
        # opening main page
        try:
            links = soup.select('#BlinkDBContent_849210 ul li a')

        except:
            print("ERROR:  Couldn't find any hospital")

        # start a for loop
        i = 0
        for link in links:

            # opening leap frog page
            try:
                print("Visiting -->  " + link['href'])
                new_response = requests.get(link['href']).content

                soup = bs(new_response, "html.parser")

                redir_one = soup.select(
                    '#survey-results-container a')[0]['href']

            except:
                print("ERROR: Couldn't open hospital Leap Frog Page")

            # Opening survery results page
            try:
                print('  Redirecting to --->  ' + redir_one)
                an_response = requests.get(redir_one).content

                soup = bs(an_response, "html.parser")

            except:
                print("ERROR: Couldn't open survey results")

                # getting the name of the hospital
            try:
                name = soup.find_all(
                    'h1', class_='quote-large blue margin-bottom-20')[0].text
            except:
                name = ""

            # getting the address of the hospital
            try:
                address = soup.select('.facility-address strong')[0].text.replace(
                    '\n', '').replace('                        ', '')
            except:
                address = ""

            try:
                website = soup.select(
                    '.margin-bottom-40')[0].select('tr')[1].select('td a')[0]['href']
            except:
                website = ""

            data = Hospital(name=name, address=address, website=website)
            db.session.add(data)
            db.session.commit()

            # with open('hospital.csv', 'a') as h:
            #     writer = csv.writer(h, delimiter='|')
            #     writer.writerow([name, address, website])

            print(f'SUCCESS --> HOSPITAL INFO GOTTEN ---> {i + 1}')

            i += 1

    except ConnectionError:
        print('Network Error --> Try Again')
    except ConnectionAbortedError:
        print('Network Error --> Try Again')
    except ConnectionRefusedError:
        print('Network Error --> Try Again')
    except ConnectionResetError:
        print('Network Error --> Try Again')

    return "Scraping Complete"


# running the app
if __name__ == '__main__':
    app.run(debug=True)
# running the app end
