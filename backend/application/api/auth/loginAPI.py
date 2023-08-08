# import essential libraries
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password, hash_password
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity 

# import model tables
from application.data.models import db,User


parser = reqparse.RequestParser()
parser.add_argument('user_mail', type=str, required=True, help='user_mail is required !!')
parser.add_argument('password', type=str, required=True, help='Password is required !!')

# API for login 
class LoginAPI(Resource):
    def post(self):
        args = parser.parse_args()
        user_mail = args.get('user_mail')
        password = args.get('password')
        
        user = User.query.filter_by(user_mail=user_mail).first() 

        # if user not exist it throw status fail
        if user is None:
            return jsonify({'status':'failed','message': 'User doesn\'t exist !!'})

        # Check for user passsword
        if  verify_password(password, user.password):
            return jsonify({'status':'failed','message': 'wrong password'})

        # initialize tokens
        refresh_token = create_refresh_token(identity=user.user_id)
        access_token = create_access_token(identity=user.user_id)
        
        # make user login
        login_user(user)

        print("admin = ",user.admin)
        return jsonify({'status': 'success','message': 'Successfully logged in !!', 'access_token': access_token, 'refresh_token': refresh_token , "user_mail": user_mail, "admin" : user.admin})


# refresh token in case of token expiry
class RefreshTokenAPI(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {'access_token': access_token}, 200
