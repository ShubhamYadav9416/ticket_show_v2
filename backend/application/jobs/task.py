import datetime
import os
import csv
from jinja2 import Template

from celery import shared_task
from celery.schedules import crontab
from flask import current_app, render_template,jsonify


from application.data.models import db, User, Booking, Movie, Theater, TheaterMovie,UserTheaterRating
from application.jobs.messages import mail,send_monthly_to_user,send_daily_mail_to_user


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, '../templates')


EXPORT_NOTIFICATION_HTML_PATH = os.path.join(TEMPLATE_DIR, 'ExportCSV.html')


# 1. DAILY reminder TASKS [Daily Reminder Jobs]
# -----------------------


@shared_task(ignore_result=False)
def send_mail_daily():
    users = User.query.all()

    for user in users:
        last_booking = Booking.query.filter_by(user_id=user.user_id).first()

        if not last_booking  or  last_booking.booking_time - datetime.timedelta(days=1):
            send_daily_mail_to_user.delay(user.user_id)

    return 'Daily mail send to every user!!'




# 2. MONTHLY mail - tasks [Scheduled Job - Monthly Engagement Report]
# -------------------------


@shared_task(ignore_result=False)
def send_mail_monthly():
    users = User.query.all()
    for user in users:
        send_monthly_to_user.delay(user.user_id, user.user_mail)
    return 'Emails sent to every users'



@shared_task(ignore_result=False)
def export_csv(id):

    fields = ["id", "theater_name", "movie_name","theater_rating", "no_of_bookings", "revenue"]
    rows = []
    theater_ratings = UserTheaterRating.query.filter_by(theater_id = id).all()

    
    if theater_ratings is None:
        rating = None
    else:
        count = 0
        total_rate = 0
        for theater_rating in theater_ratings:
            count = count + 1
            total_rate = total_rate + theater_rating.rating

    rating = total_rate / count

    theater_movies = TheaterMovie.query.join(Movie,Theater).filter(
            TheaterMovie.movie_id == Movie.movie_id).filter(
            TheaterMovie.theater_id == id).add_columns(
            TheaterMovie.theater_movie_id,
            Movie.movie_name,Theater.theater_name)
    if theater_movies:
        for theater_movie in theater_movies:
            bookings = Booking.query.filter_by(theater_movie_id = theater_movie.theater_movie_id).all()
            no_of_bookings = 0
            revenue = 0
            if bookings:
                for booking in bookings:
                    no_of_bookings = no_of_bookings + booking.no_of_tickets
                    revenue = revenue + booking.total_paid
            rows.append([theater_movie.theater_movie_id, theater_movie.theater_name, theater_movie.movie_name, rating ,no_of_bookings, revenue])
    
    file_name = f'theater_id_{id}.csv'

    csv_path = os.path.join('templates/CSV', file_name)

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    print('FILE SAVED!')

    with open(csv_path, '+a', newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

    result = {'csv_path': csv_path}

    user_mail = "admin@gmail.com"
    subject = "CSV Reports you requested for"

    with open(EXPORT_NOTIFICATION_HTML_PATH) as f:
        template = Template(f.read())
        message = template.render(user_mail=user_mail,attachment_url=csv_path)
    mail(user_mail, subject, message, content="html", attachment_files=[csv_path])

    return result
            