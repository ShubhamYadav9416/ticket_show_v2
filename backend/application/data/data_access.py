from flask import jsonify
from application.data.models import Movie, User, Theater
from application.utils.image_encoder import image_to_base64

from application.cache import cache

@cache.cached(timeout=50 , key_prefix='get_all_theaters')
def get_all_theaters():
    theaters = Theater.query.all()
    theaters_list = []
    for theater in theaters:
        theaters_list.append({'theater_id': theater.theater_id ,'theater_id': theater.theater_id ,'theater_name': theater.theater_name, "theater_place" : theater.theater_place, "theater_location": theater.theater_location, "theater_capacity": theater.theater_capacity})
    return theaters_list

@cache.cached(timeout=50, key_prefix='get_all_movies')
def get_all_movies():
    movies = Movie.query.all()
    movies_list = []
    for movie in movies:
        base64Poster = image_to_base64(movie.movie_image_path)
        movies_list.append({'movie_id':movie.movie_id,'id':movie.movie_id ,'movie_name': movie.movie_name,'movie_tag':movie.movie_tag,'movie_language':movie.movie_language,'movie_duration':movie.movie_duration,'movie_description':movie.movie_description,'poster_url':base64Poster})
        if movies_list == []:
            return jsonify({"status":"no_data"})
    return movies_list

