from jinja2 import Template
from flask import current_app as app
from flask import render_template

import os
import smtplib
from json import dumps

from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import shared_task

from application.data.models import db,Movie,User,Booking,TheaterMovie, Theater

# --------------

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "support@cinepass.com"
SENDER_PASSWORD = ''


# getting PATHS
# --------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, '../templates')

DAILY_REMINDER_HTML_PATH = os.path.join(TEMPLATE_DIR, 'dailyjob.html')
MONTHLY_HTML_PATH = os.path.join(TEMPLATE_DIR, 'MontlyReport.html')

EXPORT_NOTIFICATION_HTML_PATH = os.path.join(TEMPLATE_DIR, 'exportNotification.html')


# -----------------
# handling MAILS.

def mail(user_mail, subject, message, content="text", attachment_files=None):

    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = user_mail
    msg['Subject'] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    if attachment_files:
        for file in attachment_files:
            with open(file, 'rb') as attachment:

                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file)}"')

            encoders.encode_base64(part)
            msg.attach(part)

    server = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)

    server.login(SENDER_ADDRESS, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

    return 'Mail Sent successfully !!'


# ---------------------------------------------------

# DAILY reminders.
# -----------------

@shared_task(ignore_result=False)
def send_daily_mail_to_user(id):
    user = User.query.filter_by(user_id=id).first()
    with open(DAILY_REMINDER_HTML_PATH) as f:
        template = Template(f.read())
        message = template.render(user_mail=user.user_mail)

    today = datetime.now().strftime('%d-%m-%Y')
    subject = f'CINEPASS : Daily Reminder Mail for ({today})'

    mail(user.user_mail, subject=subject, message=message, content='html')


# ---------------------------------------------------------------
# Monthly Entertainment report
# ---------------------------------------------------------------

@shared_task(ignore_result=False)
def send_monthly_to_user(id, email):
    user = User.query.filter_by(user_id=id).first()
    bookings_list = []
    bookings = Booking.query.filter_by(user_id=id).all()
    if bookings:
        for booking in bookings:
            theater_movie = TheaterMovie.query.join(Movie,TheaterMovie.movie_id == Movie.movie_id).join(
            Theater,TheaterMovie.theater_id == Theater.theater_id).filter_by(
            TheaterMovie.theater_movie_id == booking.theater_movie_id).add_columns(
            Movie.movie_name, Theater.theater_name,
            TheaterMovie.timing).all()
            bookings_list.append({"booking_id":booking.booking_id, "theater_name":theater_movie[0].theater_name,
                                  "movie_name":theater_movie[0].movie_name,"time":theater_movie[0].timing,
                                  "no_of_tickets":booking.no_of_tickets, "price": booking.total_paid})
        
    has_booking = False
    if len(bookings_list) > 0:
        has_booking = True
    
    movies = Movie.query.all()

    with open(MONTHLY_HTML_PATH) as f:
        template = Template(f.read())
        message = template.render(user_mail=email, movies=movies, bookings = bookings_list, has_booking = has_booking)

    
    subject = f'We Have Something Special for you!!!!'

    mail(user.user_mail, subject=subject, message=message, content='html')

    return 'Email send this month'