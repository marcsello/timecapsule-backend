#!/usr/bin/env python3
from flask import request, abort, jsonify
from flask_classful import FlaskView


from model import db, Upload
from schemas import UploadSchema

class AdminView(FlaskView):
    upload_schema_list = UploadSchema(many=False, exclude=['text'])

