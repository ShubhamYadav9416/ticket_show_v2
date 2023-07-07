import secrets
from flask_security.utils import hash_password
from werkzeug.security import generate_password_hash
from flask_restful import Resource, reqparse


from application.models import db, User

 
user_post_args = reqparse.RequestParser()
user_post_args.add_argument('user_mail', type=str, required=True, help="Username is required !!")
user_post_args.add_argument('password', type=str, required=True, help='password is required')

class RegisterAPI(Resource):
    def post(self):
        args = user_post_args.parse_args()
        user_mail = args.get('user_mail')
        password = args.get('password')

        user = User.query.filter_by(user_mail=user_mail).first()
        if user:
            return {'message': 'Mail is already registered !!'}
        
        hash_password = generate_password_hash(password)

        new_user = User(user_mail=user_mail, password= hash_password, admin = False)
        new_user.fs_uniquifier = secrets.token_hex(16)
        db.session.add(new_user)
        db.session.commit()

        return {'status' : 'success', 'message': 'Successfully Registered !!'}
    

# {
#     "user_mail" : "user2@gamil.com",
#     "password" : "1234"
# }