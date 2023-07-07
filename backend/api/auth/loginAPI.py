from flask import jsonify
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password, hash_password
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity 

from application.models import db,User
# from application.security import user_datastore
# -------------------------------

parser = reqparse.RequestParser()
parser.add_argument('user_mail', type=str, required=True, help='user_mail is required !!')
parser.add_argument('password', type=str, required=True, help='Password is required !!')


class LoginAPI(Resource):
    def post(self):
        args = parser.parse_args()
        user_mail = args.get('user_mail')
        password = args.get('password')
        
        user = User.query.filter_by(user_mail=user_mail).first() 

        if user is None:
            return jsonify({'status':'failed','message': 'User doesn\'t exist !!'})

        if  verify_password(password, user.password):
            return jsonify({'status':'failed','message': 'wrong password'})

        refresh_token = create_refresh_token(identity=user.user_id)
        access_token = create_access_token(identity=user.user_id)
        
        login_user(user)
        print(user.admin)
        return jsonify({'status': 'success','message': 'Successfully logged in !!', 'access_token': access_token, 'refresh_token': refresh_token , "user_mail": user_mail, "admin" : user.admin})



class RefreshTokenAPI(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {'access_token': access_token}, 200
