import json
import os
from datetime import datetime
from flask import request, jsonify, send_file
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt_identity

from application.data.models import db,TheaterMovie, Booking,User,Dyanmic,Movie,Theater
from application.utils.image_encoder import image_to_base64


booking_post_args = reqparse.RequestParser()
booking_post_args.add_argument('theater_movie_id', type=int)
booking_post_args.add_argument('no_of_tickets', type=int)
booking_post_args.add_argument('total_paid', type=int)

# resource_fields = {
#     'theater_movie_id': fields.Integer,
#     'no_of_ticekts' : fields.Integer
# }


class bookTicket(Resource):
    @jwt_required()
    def post(self,theater_movie_id):
        data = json.loads(request.form['data'])
        no_of_tickets = data.get('no_of_tickets', '')
        total_paid = data.get('total_paid', '')
        user_id = get_jwt_identity()
        dynamic = Dyanmic.query.filter_by(theater_movie_id = theater_movie_id).first()
        if dynamic:
            dynamic.seats_left = dynamic.seats_left - no_of_tickets
            db.session.commit()
        input = Booking(user_id = user_id, theater_movie_id = theater_movie_id, no_of_tickets = no_of_tickets, total_paid = total_paid,booking_time= datetime.now())  #, theater_image_path = args['theater_image_path'])
        db.session.add(input)
        db.session.commit()
        return jsonify({'status':"booked"})
    

class userBookedTicket(Resource):
    @jwt_required()
    def get(resource):
        user_id = get_jwt_identity()
        user = User.query.filter_by(user_id = user_id).first()
        bookings = Booking.query.filter_by(user_id = user_id).all()
        tickets = []
        for booking in bookings:
            theatermovies = TheaterMovie.query.join(Movie,TheaterMovie.movie_id == Movie.movie_id).join(
            Theater,TheaterMovie.theater_id == Theater.theater_id).filter_by(
            TheaterMovie.theater_movie_id == booking.theater_movie_id).add_columns(
            TheaterMovie.theater_movie_id,TheaterMovie.timing,Movie.movie_name, Movie.movie_tag,Movie.movie_duration, Movie.movie_language,
            Theater.theater_place,Theater.theater_location,Theater.theater_name, Movie.movie_image_path,
            TheaterMovie.timing).all()
            for theatermovie in theatermovies:
                tickets.append({'id': booking.booking_id ,'movie_name':theatermovie.movie_name, 'theater_location':theatermovie.theater_location, 'theater_place':theatermovie.theater_place,'theater_name': theatermovie.theater_name,
                            'movie_tag':theatermovie.movie_tag, 'movie_duration':theatermovie.movie_duration, 'movie_language':theatermovie.movie_language,'show_time':theatermovie.timing,
                            'no_of_tickets':booking.no_of_tickets, 'price':booking.total_paid, 'booking_time':str(booking.booking_time),'booking_id':booking.booking_id,"poster_url": image_to_base64(theatermovie.movie_image_path)})
        return jsonify({'user_id':user.user_id,'user_mail':user.user_mail, 'tickets': tickets})