import json

from flask import request, jsonify, send_file
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.data.models import db,Theater

from celery import shared_task

from application.jobs import task

class Export_CSV_API(Resource):
    @jwt_required()
    def get(self,id):
        async_result = task.export_csv.delay(id)
        
        # Wait for the task to complete and retrieve the result
        result = async_result.get()
        print(result)
        # csv_path = result['csv_path']
        
        # Send the file as an attachment in the response
        # return send_file(csv_path, as_attachment=True)
        return ""