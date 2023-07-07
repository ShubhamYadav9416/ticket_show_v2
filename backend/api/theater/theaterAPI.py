import json

from flask import request,jsonify
from flask_restful import Resource,reqparse,abort,fields,marshal_with

from application.models import db,Theater

theater_post_args = reqparse.RequestParser()
theater_post_args.add_argument('theater_name', type=str, required=True, help="theater name is required")
theater_post_args.add_argument('theater_place', type=str, required=True, help="theater place is required")
theater_post_args.add_argument('theater_location', type=str, required=True, help="theater location is required")
theater_post_args.add_argument('theater_capacity', type=str, required=True, help="theater capacity is required")
theater_post_args.add_argument('theater_image_path', type=str, required=True, help="theater image path is required")

theater_put_args = reqparse.RequestParser()
theater_put_args.add_argument('theater_name', type=str)
theater_put_args.add_argument('theater_place', type=str)
theater_put_args.add_argument('theater_location', type=str)
theater_put_args.add_argument('theater_capacity', type=str)
theater_put_args.add_argument('theater_image_path', type=str)

resource_fields = {
    'theater_id': fields.Integer,
    'theater_name' : fields.String,
    'theater_place': fields.String,
    'theater_location': fields.String,
    'theater_capacity': fields.Integer,
    'theater_image_path' : fields.String
}

class AllTheaterAPI(Resource):
    def get(resource):
        theaters = Theater.query.all()
        theaters_list = {}
        for theater in theaters:
            theaters_list.append({'theater_id': theater.theater_id ,'theater_id': theater.theater_id ,'theater_name': theater.theater_name, "theater_place" : theater.theater_place, "theater_location": theater.theater_location, "theater_capacity": theater.theater_capacity, "theater_image_path": theater.theater_image_path})
        return theaters_list
    
    @marshal_with(resource_fields)
    def post(resource):
        args = theater_post_args.parse_args()
        theater= Theater.query.filter_by(theater_name=args["theater_name"]).first()
        if theater:
            abort(409,message= "theater is already exist")
        input = Theater(theater_name = args["theater_name"], theater_place = args['theater_place'], theater_location = args['theater_location'], theater_capacity = args['theater_capacity'], theater_image_path = args['theater_image_path'])
        db.session.add(input)
        db.session.commit()
        return input, 201
    
class TheaterAPI(Resource):
    @marshal_with(resource_fields)
    def get(self,theater_id):
        theater = Theater.query.filter_by(theater_id=theater_id).first()
        if not theater:
            abort(404, message="Could not found theater with this id")
        return theater
    
    @marshal_with(resource_fields)
    def put(self,theater_id):
        args = theater_put_args.parse_args()
        theater = Theater.query.filter_by(theater_id = theater_id).first()
        if not theater:
            abort(404, message="theater doesn't exist.")
        # input = theater(theater_id=theater_id, theater_name = args["theater_name"], theater_place = args['theater_place'], theater_location = args['theater_location'], theater_capacity = args['theater_capacity'], theater_image_path = args['theater_image_path'])
        if args['theater_name']:
            theater.theater_name = args['theater_name']
        if args['theater_place']:
            theater.theater_place = args['theater_place']
        if args['theater_location']:
            theater.theater_location = args['theater_location']
        if args['theater_capacity']:
            theater.theater_capacity = args['theater_capacity']
        if args['theater_image_path']:
            theater.theater_image_path = args['theater_image_path']
        db.session.commit()
        return theater
    
    @marshal_with(resource_fields)
    def delete(self, theater_id):
        theater = Theater.query.filter_by(theater_id = theater_id).first()
        if not theater:
            abort(404,message= "theater id not exist")
        db.session.delete(theater)
        db.session.commit()
        return jsonify({'message' : 'Movie has been deleted!'})

# {
#     "theater_name" : "INox",
#     "theater_place": "New delhi",
#     "theater_location" : "connaugt palace",
#     "theater_capacity": 50,
#     "theater_image_path" : "image_path.png"
# }
