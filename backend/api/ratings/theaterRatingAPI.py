import json

from flask import request, jsonify
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.models import db,Theater,User, TheaterRating

rating_post_args = reqparse.RequestParser()
rating_post_args.add_argument('rating', type=int, required = True, help='rating is required')

class TheaterUserRatingAPI(Resource):
    @jwt_required()
    def get(self,theater_id):
        user_id = get_jwt_identity()
        theaterrating = TheaterRating.query.filter(user_id=user_id).filter(theater_id=theater_id).first()
        if not theaterrating:
            return jsonify({'status':'not_rated'})
        return jsonify({'rating':theaterrating.rating})
    
    @jwt_required()
    def post(self,theater_id):
        args = rating_post_args.parse_args()
        user_id = get_jwt_identity()
        input = TheaterRating(user_id = user_id, theater_id =theater_id, rating = args['rating'])
        db.session.add(input)
        db.session.commit()
        return  {'status' : 'success', 'message': 'Rated!!'}
    
class TheaterRating(Resource):
    @jwt_required()
    def get(self,theater_id):
        theaterratings = TheaterRating.query.filter_by(theater_id=theater_id).all()
        votes = 0
        total_rating = 0
        for theaterrating in theaterratings:
            votes = votes + 1
            total_rating = total_rating + theaterrating.rating
        return jsonify({'votes': votes, 'total_rating': total_rating})
        
    