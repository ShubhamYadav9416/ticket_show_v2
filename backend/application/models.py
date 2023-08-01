from .database import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import event


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
    
    
    
    # token-based authentication
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    
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
    
    # Relationship with User
    # ratings_by_users = db.relationship('TheaterRating', backref='theater', lazy=True)
    
    # Relationship with Movie
    movies = db.relationship('TheaterMovie',back_populates='theater')

    def __init__(self,theater_name,theater_place,theater_location,theater_capacity):
        self.theater_name = theater_name
        self.theater_place = theater_place
        self.theater_location = theater_location
        self.theater_capacity= theater_capacity
    

class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(100), nullable=False)
    movie_tag = db.Column(db.String(100), nullable=False)
    movie_language = db.Column(db.String(50), nullable=False)
    movie_duration = db.Column(db.String(10), nullable=False)
    movie_description = db.Column(db.String(200), nullable=False)
    movie_image_path = db.Column(db.String(100), nullable=False, default="/home/shubham/notes/IITM_Projects/mad2/mad2_final_project/instance/default_theater.jpg")
        
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
class UserTheaterRating(db.Model):
    __tablename__ = 'user_theater_ratings'
    user_id = db.Column(db.Integer, primary_key = True)
    theater_id = db.Column(db.Integer, primary_key =True)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self,user_id,theater_id,rating):
        self.user_id = user_id
        self.theater_id = theater_id
        self.rating = rating



# Association table for Theater-Movie relationship
class TheaterMovie(db.Model):
    __tablename__ = 'theater_movies'
    theater_movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.theater_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)
    timing = db.Column(db.String,nullable=False)

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
    user_id = db.Column(db.Integer, nullable=False)
    theater_movie_id = db.Column(db.Integer, db.ForeignKey('theater_movies.theater_movie_id'), nullable=False)
    no_of_tickets = db.Column(db.Integer, nullable=False)
    total_paid = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime)

    # user_id = user_id, theater_movie_id = args['theater_movie_id'], no_of_tickets = args['no_of_tickets'], total_paid = args['total_paid'],booking_time= datetime.now())  #, theater_image_path = args['theater_image_path']
    def __init__(self,user_id,theater_movie_id,no_of_tickets,total_paid,booking_time):
        self.user_id = user_id
        self.theater_movie_id = theater_movie_id
        self.no_of_tickets = no_of_tickets
        self.total_paid = total_paid
        self.booking_time = booking_time


class Dyanmic(db.Model):
    __tablename__ = "dynamic"
    theater_movie_id = db.Column(db.Integer, db.ForeignKey('theater_movies.theater_movie_id'), primary_key=True)
    seats_left = db.Column(db.Integer)
    current_price = db.Column(db.Integer)


    @event.listens_for(TheaterMovie, 'after_insert')
    def add_dynamic_row(mapper, connection, target):
        theater = Theater.query.filter_by(theater_id=target.theater_id).first()
        dynamic_row = Dyanmic(theater_movie_id=target.theater_movie_id,
                          seats_left=theater.theater_capacity,
                          current_price=target.ticket_price)
        connection.execute(Dyanmic.__table__.insert(), dynamic_row.__dict__)


    @event.listens_for(TheaterMovie, 'after_delete')
    def delete_dynamic_row(mapper, connection, target):
        dynamic_row = Dyanmic.query.filter_by(theater_movie_id=target.theater_movie_id).first()
        if dynamic_row:
            connection.execute(Dyanmic.__table__.delete(), dynamic_row.__dict__)
