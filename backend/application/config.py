

SECRET_KEY = 'SECRET_KEY'
SQLALCHEMY_DATABASE_URI = 'sqlite:///../db_directory/flaskblog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
SECURITY_PASSWORD_SALT = 'SALT'
SECURITY_PASSWORD_HASH = 'bcrypt'
WTF_CSRF_ENABLED = False
JWT_SECRET_KEY = 'JWT_SECRET_KEY'

MOVIE_UPLOAD_FOLDER = 'static/img/movies/'
THEATER_UPLOAD_FOLDER = 'static/img/theaters/'


ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'png', 'jpeg','avif']


# CACHE_TYPE = "RedisCache"
# CACHE_REDIS_URL = "redis://localhost:6379/0"
# CACHE_DEFAULT_TIMEOUT = 300
# DEBUG = False


CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"