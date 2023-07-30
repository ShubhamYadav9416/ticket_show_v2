from flask import jsonify
import secrets
from flask_security.utils import hash_password
from werkzeug.security import generate_password_hash
from flask_restful import Resource, reqparse


from application.models import db, User

 
user_put_args = reqparse.RequestParser()
user_put_args.add_argument('user_mail', type=str, required=True, help="Username is required !!")
user_put_args.add_argument('password', type=str, required=True, help='password is required')

class ForgetAPI(Resource):
    def post(self):
        args = user_put_args.parse_args()
        user_mail = args.get('user_mail')
        new_password = args.get('password')

        existing_user = User.query.filter_by(user_mail=user_mail).first()
        if existing_user:
            hashed_password = generate_password_hash(new_password)
            existing_user.password = hashed_password
            db.session.commit()
            return jsonify({'status':'success','message':'Password Changed'})
        else:
            return jsonify({'status':'failed','message': 'Mail Not Found!!'})
    

# {
#     "user_mail" : "user2@gamil.com",
#     "password" : "1234"
# }