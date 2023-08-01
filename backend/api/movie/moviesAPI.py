import json
import os
from flask import request, jsonify, send_file
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from application.models import db,Movie
from application.config import ALLOWED_IMAGE_EXTENSIONS
from application.utils.save_movie_img import save_movie_image
from application.utils.image_encoder import image_to_base64


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
    @jwt_required()
    def get(resource):
        movies = Movie.query.all()
        movies_list = []
        for movie in movies:
            base64Poster = image_to_base64(movie.movie_image_path)
            movies_list.append({'movie_id':movie.movie_id,'id':movie.movie_id ,'movie_name': movie.movie_name,'movie_tag':movie.movie_tag,'movie_language':movie.movie_language,'movie_duration':movie.movie_duration,'movie_description':movie.movie_description,'poster_url':base64Poster})

        if movies_list == []:
            return jsonify({"status":"no_data"})
        return movies_list


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
    @jwt_required()
    def get(self,movie_id):
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        if not movie:
            abort(404, message="Could not found movie with this id")
        return movie
    
    @jwt_required()
    @marshal_with(resource_fields)
    def put(self,movie_id):

        args = movie_put_args.parse_args()

        movie = Movie.query.filter_by(movie_id = args['movie_id']).first()
        if not movie:
            abort(404, message="movie doesn't exist.")
        # input = Movie(movie_id=movie_id, movie_name = args["movie_name"], movie_tag = args['movie_tag'], movie_language = args['movie_language'], movie_duration = args['movie_duration'], movie_description =args['movie_description'] , movie_image_path = args['movie_image_path'])
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
    
    @jwt_required()
    @marshal_with(resource_fields)
    def delete(self, movie_id):
        movie = Movie.query.filter_by(movie_id = movie_id).first()
        if not movie:
            abort(404,message= "movie id not exist")
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'message' : 'Movie has been deleted!'})






# class MoviePoster(Resource):
#     @jwt_required()
#     def get(self,movie_id):
#         movie = Movie.query.filter_by(movie_id=movie_id).first()
#         if movie:
#             try:
#                 base64Poster = image_to_base64(movie.movie_image_path)
#                 return send_file(base64Poster, mimetype='image/jpeg')
#             except FileNotFoundError:
#                 return "Image not found", 404
#         return "Image not found", 404
    



# {
#     "movie_name" : "Dhoom2",
#     "movie_tag" : "Action",
#     "movie_language" : "Hindi",
#     "movie_duration" : "125",
#     "movie_description" : "good movie",
#     "movie_image_path" : "image_path.png"
#  }