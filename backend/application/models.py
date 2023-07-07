from .database import db
from flask_security import UserMixin, RoleMixin



UserRoles = db.Table('UserRoles',
                    db.Column('user_id', db.Integer(), db.ForeignKey('users.user_id')),
                    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255)) 


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_mail = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    
    roles = db.relationship('Role', secondary=UserRoles,
                            backref=db.backref('users', lazy='dynamic'))
    
    # Relationship with Theater
    ratings_theaters = db.relationship('TheaterRating', backref='users', lazy=True)
    
    # Relationship with Movie
    ratings_movies = db.relationship('MovieRating', backref='users', lazy=True)
    
    # token-based authentication
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    # Relationship with Booking
    bookings = db.relationship('Booking', backref='user', lazy=True)
    
    def __init__(self,user_mail, password, admin):
        self.user_mail = user_mail
        self.password = password
        self.admin = admin
    

class Theater(db.Model):
    __tablename__ = 'theaters'
    theater_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theater_name = db.Column(db.String(100), nullable=False)
    theater_place = db.Column(db.String(100), nullable=False)
    theater_location = db.Column(db.String(100), nullable=False)
    theater_capacity = db.Column(db.Integer, nullable=False)
    theater_image_path = db.Column(db.String(100), nullable=False, default="/home/shubham/notes/IITM_Projects/mad2/mad2_final_project/instance/default_theater.jpg")
    
    # Relationship with User
    ratings_by_users = db.relationship('TheaterRating', backref='theater', lazy=True)
    
    # Relationship with Movie
    movies = db.relationship('TheaterMovie',back_populates='theater')

    def __init__(self,theater_name,theater_place,theater_location,theater_capacity,theater_image_path):
        self.theater_name = theater_name
        self.theater_place = theater_place
        self.theater_location = theater_location
        self.theater_capacity= theater_capacity
        self.theater_image_path = theater_image_path
    

class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(100), nullable=False)
    movie_tag = db.Column(db.String(100), nullable=False)
    movie_language = db.Column(db.String(50), nullable=False)
    movie_duration = db.Column(db.Integer, nullable=False)
    movie_description = db.Column(db.Text, nullable=False)
    movie_image_path = db.Column(db.String(100), nullable=False, default="/home/shubham/notes/IITM_Projects/mad2/mad2_final_project/instance/default_theater.jpg")
    
    # Relationship with User
    ratings_by_users = db.relationship('MovieRating', backref='movie', lazy=True)
    
    # Relationship with Theater
    theaters = db.relationship('TheaterMovie',  back_populates='movie')

    def __init__(self,movie_name, movie_tag, movie_language, movie_duration, movie_description, movie_image_path):
        self.movie_name = movie_name
        self.movie_tag = movie_tag
        self.movie_language = movie_language
        self.movie_duration = movie_duration
        self.movie_description = movie_description
        self.movie_image_path = movie_image_path
    


# Association table for User-Theater ratings
class TheaterRating(db.Model):
    __tablename__ = 'user_theater_ratings'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.theater_id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self,users,theater,rating):
        self.users = users
        self.theater = theater
        self.rating = rating


# Association table for User-Movie ratings
class MovieRating(db.Model):
    __tablename__ = 'user_movie_ratings'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self,users,movie,rating):
        self.users = users
        self.movie = movie
        self.rating = rating

# Association table for Theater-Movie relationship
class TheaterMovie(db.Model):
    __tablename__ = 'theater_movies'
    theater_movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.theater_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)
    timing = db.Column(db.DateTime)

    movie= db.relationship('Movie',back_populates = "theaters")
    theater = db.relationship('Theater', back_populates= "movies")

    booking = db.relationship('Booking', backref='theater_movies', lazy=True)

    def __init__(self,theater,movie,ticket_price,timing):
        self.theater = theater
        self.movie = movie
        self.ticket_price = ticket_price
        self.timing = timing


class Booking(db.Model):
    __tablename__ = 'booking'
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    theater_movie_id = db.Column(db.Integer, db.ForeignKey('theater_movies.theater_movie_id'), nullable=False)
    no_of_tickets = db.Column(db.Integer, nullable=False)
    total_paid = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime)
