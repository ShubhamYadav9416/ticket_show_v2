import json

from flask import request, jsonify
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from application.models import db,Movie

movie_post_args = reqparse.RequestParser()
movie_post_args.add_argument('movie_name', type=str, required=True, help="movie name is required")
movie_post_args.add_argument('movie_tag', type=str, required=True, help="movie tag is required")
movie_post_args.add_argument('movie_language', type=str, required=True, help="movie language is required")
movie_post_args.add_argument('movie_duration', type=int, required=True, help="movie duration is required")
movie_post_args.add_argument('movie_description', type=str, required=True, help="movie description is required")
movie_post_args.add_argument('movie_image_path', type=str, required=True, help="movie image is required")

movie_put_args = reqparse.RequestParser()
movie_put_args.add_argument('movie_name', type=str)
movie_put_args.add_argument('movie_tag', type=str)
movie_put_args.add_argument('movie_language', type=str)
movie_put_args.add_argument('movie_duration', type=int)
movie_put_args.add_argument('movie_description', type=str)
movie_put_args.add_argument('movie_image_path', type=str)

resource_fields = {
    'movie_id': fields.Integer,
    'movie_name' : fields.String,
    'movie_tag': fields.String,
    'movie_language': fields.String,
    'movie_duration': fields.Integer,
    'movie_description' : fields.String,
    'movie_image_path': fields.String
}

class AllMovieAPI(Resource):
    # @jwt_required()
    def get(resource):
        movies = Movie.query.all()
        movies_list = []
        for movie in movies:
            movies_list.append({'movie_id':movie.movie_id,'id':movie.movie_id , 'movie_name': movie.movie_name, "movie_tag" : movie.movie_tag, "movie_language": movie.movie_language, "movie_duration": movie.movie_duration, "movie_description": movie.movie_description, "movie_image_path" : movie.movie_image_path})
        if movies_list == []:
            return jsonify({"status":"no_data"})
        return movies_list
    
    @marshal_with(resource_fields)
    @jwt_required()
    def post(resource):
        args = movie_post_args.parse_args()
        movie= Movie.query.filter_by(movie_name=args['movie_name']).first()
        if movie:
            abort(409,message= "movie is  already exist")
        input = Movie(movie_name = args["movie_name"], movie_tag = args['movie_tag'], movie_language = args['movie_language'], movie_duration = args['movie_duration'], movie_description =args['movie_description'] , movie_image_path = args['movie_image_path'])
        db.session.add(input)
        db.session.commit()
        return input, 201
    
class MovieAPI(Resource):
    @jwt_required()
    @marshal_with(resource_fields)
    def get(self,movie_id):
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        if not movie:
            abort(404, message="Could not found movie with this id")
        return movie
    
    @jwt_required()
    @marshal_with(resource_fields)
    def put(self,movie_id):
        args = movie_put_args.parse_args()
        movie = Movie.query.filter_by(movie_id = movie_id).first()
        if not movie:
            abort(404, message="movie doesn't exist.")
        # input = Movie(movie_id=movie_id, movie_name = args["movie_name"], movie_tag = args['movie_tag'], movie_language = args['movie_language'], movie_duration = args['movie_duration'], movie_description =args['movie_description'] , movie_image_path = args['movie_image_path'])
        if args['movie_name']:
            movie.movie_name = args['movie_name']
        if args['movie_tag']:
            movie.movie_tag = args['movie_tag']
        if args['movie_language']:
            movie.movie_language = args['movie_language']
        if args['movie_duration']:
            movie.movie_duration = args['movie_duration']
        if args['movie_description']:
            movie.movie_description = args['movie_description']
        if args['movie_image_path']:
            movie.movie_image_path = args['movie_image_path']
        db.session.commit()
        return movie
    
    @jwt_required()
    @marshal_with(resource_fields)
    def delete(self, movie_id):
        movie = Movie.query.filter_by(movie_id = movie_id).first()
        if not movie:
            abort(404,message= "movie id not exist")
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'message' : 'Movie has been deleted!'})

# {
#     "movie_name" : "Dhoom2",
#     "movie_tag" : "Action",
#     "movie_language" : "Hindi",
#     "movie_duration" : "125",
#     "movie_description" : "good movie",
#     "movie_image_path" : "image_path.png"
#  }