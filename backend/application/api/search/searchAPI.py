import json
from datetime import datetime

from flask import request, jsonify
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.data.models import db,Theater, Movie, TheaterMovie,Dyanmic

class Filters(Resource):
    @jwt_required()
    def get(resource):
        movies  = Movie.query.all()
        theaters = Theater.query.all()
        movie_list = []
        theater_list = []
        place_list = []
        if movies:
            for movie in movies:
                movie_list.append({'id':movie.movie_id , "movie_id": movie.movie_id, "movie_name" : movie.movie_name})
        if theaters:
            for theater in theaters:
                theater_list.append({'id':theater.theater_id , "theater_id": theater.theater_id, "theater_name" : theater.theater_name})
                place_list.append({'id':theater.theater_id, "theater_id": theater.theater_id, "theater_place" : theater.theater_place})
        return jsonify({'movie':movie_list, 'theater':theater_list, 'place': place_list}) 


class FilterByMovie(Resource):
    @jwt_required()
    def get(self,id):
        theaters = Theater.query.all()
        theaters_list = []
        for theater in theaters:
            theatermovies = TheaterMovie.query.join(Movie,Theater).filter(
            TheaterMovie.movie_id == id).filter(
            TheaterMovie.theater_id == theater.theater_id).add_columns(
            TheaterMovie.theater_movie_id,Movie.movie_name, Movie.movie_tag,
            TheaterMovie.timing)
            movies_list = []
            for theatermovie in theatermovies:
                dynamic = Dyanmic.query.filter_by(theater_movie_id = theatermovie.theater_movie_id).first()
                if datetime.strptime(theatermovie.timing, '%Y-%m-%dT%H:%M') > datetime.now(): #2023-07-31T23:37
                    if dynamic.seats_left > 0:
                        movies_list.append({'theater_movie_id': theatermovie.theater_movie_id ,'theater_id' : theater.theater_id,
                                           'movie_name': theatermovie.movie_name,'movie_tag':theatermovie.movie_tag, "timing" : theatermovie.timing, "housefull": False})
                    else:
                        movies_list.append({'theater_movie_id': theatermovie.theater_movie_id ,'theater_id' : theater.theater_id,
                                           'movie_name': theatermovie.movie_name,'movie_tag':theatermovie.movie_tag, "timing" : theatermovie.timing, "housefull": True})
            theaters_list.append({'id':theater.theater_id,'theater_id':theater.theater_id,'theater_name':theater.theater_name, 'theater_place':theater.theater_place,
                            'theater_location':theater.theater_location,"movies":movies_list})
        
        return theaters_list
    


class FilterByTheater(Resource):
    @jwt_required()
    def get(self,id):
        theater = Theater.query.filter_by(theater_id = id).first()
        theaters_list = []
        theatermovies = TheaterMovie.query.join(Movie,Theater).filter(
            TheaterMovie.movie_id == Movie.movie_id).filter(
            TheaterMovie.theater_id == id).add_columns(
            TheaterMovie.theater_movie_id,Movie.movie_name, Movie.movie_tag,
            TheaterMovie.timing)
        movies_list = []
        for theatermovie in theatermovies:
            dynamic = Dyanmic.query.filter_by(theater_movie_id = theatermovie.theater_movie_id).first()
            if datetime.strptime(theatermovie.timing, '%Y-%m-%dT%H:%M') > datetime.now(): #2023-07-31T23:37
                if dynamic.seats_left > 0:
                        movies_list.append({'theater_movie_id': theatermovie.theater_movie_id ,'theater_id' : theater.theater_id,
                                           'movie_name': theatermovie.movie_name,'movie_tag':theatermovie.movie_tag, "timing" : theatermovie.timing, "housefull": False})
                else:
                        movies_list.append({'theater_movie_id': theatermovie.theater_movie_id ,'theater_id' : theater.theater_id,
                                           'movie_name': theatermovie.movie_name,'movie_tag':theatermovie.movie_tag, "timing" : theatermovie.timing, "housefull": True})
        theaters_list.append({'id':theater.theater_id,'theater_id':theater.theater_id,'theater_name':theater.theater_name, 'theater_place':theater.theater_place,
                            'theater_location':theater.theater_location,"movies":movies_list})
        
        return theaters_list