import json

from flask import request, jsonify
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from application.models import db,Theater,User, TheaterRating

rating_post_args = reqparse.RequestParser()
rating_post_args.add_argument('rating', type=int, required = True, help='rating is required')

class TheaterRatingAPI(Resource):
    def get(self,user_id,theater_id):
        theaterrating = TheaterRating.query.filter_by(user_id=user_id).filter_by(theater_id=theater_id).first()
        if not theaterrating:
            abort(404,message='User does\'nt rate this theater')
        return jsonify({'rating':theaterrating.rating})
    
    def post(self,user_id,theater_id):
        args = rating_post_args.parse_args()
        theater = Theater.query.filter_by(theater_id=theater_id).first()
        user = User.query.filter_by(user_id=user_id).first()
        if not theater:
            abort(404, message = 'theater not found')
        if not user:
            abort(404, message = 'user not found')
        input = TheaterRating(users = user, theater=theater, rating = args['rating'])
        db.session.add(input)
        db.session.commit()
        return  {'status' : 'success', 'message': 'Rated!!'}