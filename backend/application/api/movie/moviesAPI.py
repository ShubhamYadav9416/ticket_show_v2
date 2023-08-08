# impor essential libraries
import json
import os
from time import perf_counter_ns
from flask import request, jsonify, send_file
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

# import internal functions
from application.data.models import db,Movie
from application.config import ALLOWED_IMAGE_EXTENSIONS
from application.utils.save_movie_img import save_movie_image
from application.utils.image_encoder import image_to_base64
from application.data.data_access import get_all_movies

# check is file has right format
def extension_okay(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
 


movie_put_args = reqparse.RequestParser()
movie_put_args.add_argument('movie_name', type=str)
movie_put_args.add_argument('movie_tag', type=str)
movie_put_args.add_argument('movie_language', type=str)
movie_put_args.add_argument('movie_duration', type=str)
movie_put_args.add_argument('movie_description', type=str)

resource_fields = {
    'movie_id': fields.Integer,
    'movie_name' : fields.String,
    'movie_tag': fields.String,
    'movie_language': fields.String,
    'movie_duration' : fields.String,
    'movie_description' : fields.String,
}


class AllMovieAPI(Resource):
    # ------------------------------------------------------
    # ----------------Cached endpoint ---------------------
    # ----------------------------------------------------
    @jwt_required()
    def get(resource):
        start = perf_counter_ns()
        movies_list = get_all_movies()
        stop = perf_counter_ns()
        print('Time Taken', stop-start)
        return movies_list

    # post api to add new api
    @jwt_required()
    def post(resource):
        
        data = json.loads(request.form['data'])

        movie_name = data.get('movie_name', '').strip()
        movie_tag = data.get('movie_tag', '').strip()
        movie_language = data.get('movie_language', '').strip()
        movie_duration = data.get('movie_duration', '').strip()
        movie_description = data.get('movie_description', '').strip()

        movie_poster = request.files.get('movie_poster',None)

        

        if movie_poster and not extension_okay(movie_poster.filename):
            return jsonify({'status':'fail','message': 'invalid file type'})

        movie= Movie.query.filter_by(movie_name=movie_name).first()

        if movie:
            abort(409,message= "movie is  already exist")
        print(movie_poster)
        movie_image_path = "./none.png"
        
        if movie_poster:
            movie_image_path = save_movie_image(movie_poster)
        input = Movie(movie_name = movie_name, movie_tag = movie_tag, movie_language = movie_language, movie_duration = movie_duration, movie_description = movie_description , movie_image_path = movie_image_path)
        db.session.add(input)
        db.session.commit()
        return "hello", 200


class MovieAPI(Resource):
    # get for specific movie 
    @jwt_required()
    @marshal_with(resource_fields)
    def get(self,movie_id):
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        if not movie:
            abort(404, message="Could not found movie with this id")
        return movie
    

    # edit movie
    @jwt_required()
    @marshal_with(resource_fields)
    def put(self,movie_id):

        args = movie_put_args.parse_args()

        movie = Movie.query.filter_by(movie_id = movie_id).first()
        if not movie:
            abort(404, message="movie doesn't exist.")
        if args["movie_name"]:
            movie.movie_name =args["movie_name"]
        if args['movie_tag']:
            movie.movie_tag = args['movie_tag']
        if args['movie_language']:
            movie.movie_language = args['movie_language']
        if args['movie_duration']:
            movie.movie_duration = args['movie_duration']
        if args['movie_description']:
            movie.movie_description = args['movie_description']
        db.session.commit()
        return movie
    

    # API for delete a movie 
    @jwt_required()
    @marshal_with(resource_fields)
    def delete(self, movie_id):
        movie = Movie.query.filter_by(movie_id = movie_id).first()
        if not movie:
            abort(404,message= "movie id not exist")
        path = movie.movie_image_path
        db.session.delete(movie)
        db.session.commit()
        os.remove(path)
        return jsonify({'message' : 'Movie has been deleted!'})









# {
#     "movie_name" : "Dhoom2",
#     "movie_tag" : "Action",
#     "movie_language" : "Hindi",
#     "movie_duration" : "125",
#     "movie_description" : "good movie",
#     "movie_image_path" : "image_path.png"
#  }