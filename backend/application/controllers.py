from application.models import *

# # Create a new User
# new_user = User(user_mail='test@example.com', password='password123')
# db.session.add(new_user)
# db.session.commit()

# # Create a new Theater
# new_theater = Theater(theater_name='AMC Theatres', theater_rating=4.5, theater_place='New York', theater_location='123 Main Street', theater_capacity=100, theater_image_path='https://example.com/theater_image.jpg')
# db.session.add(new_theater)
# db.session.commit()

# # Create a new Movie
# new_movie = Movie(movie_name='The Matrix', movie_tag='Sci-Fi', movie_language='English', movie_duration=120, movie_description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', movie_image_path='https://example.com/movie_image.jpg')
# db.session.add(new_movie)
# db.session.commit()

# # Associate a User with a Theater and give it a rating
# user = User.query.get(1)
# theater = Theater.query.get(1)
# user.ratings_theaters.append(theater)
# user_theater_rating = user_theater_ratings.insert().values(user_id=user.user_id, theater_id=theater.theater_id, rating=4)
# db.session.execute(user_theater_rating)
# db.session.commit()

# # Associate a User with a Movie and give it a rating
# user = User.query.get(1)
# movie = Movie.query.get(1)
# user.ratings_movies.append(movie)
# user_movie_rating = user_movie_ratings.insert().values(user_id=user.user_id, movie_id=movie.movie_id, rating=4)
# db.session.execute(user_movie_rating)
# db.session.commit()

# # Associate a Theater with a Movie
# theater = Theater.query.get(1)
# movie = Movie.query.get(1)
# theater.movies.append(movie)
# db.session.commit()
# db.create_all()