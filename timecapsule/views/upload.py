#!/usr/bin/env python3
from flask import request, abort, jsonify
from flask_classful import FlaskView

import bleach

from model import db, Upload
from schemas import UploadSchema
from utils import form_required

class UploadView(FlaskView):
    upload_schema = UploadSchema(many=False, exclude=['text'])

    @staticmethod
    def __get_and_sanitize_and_check_text(field: str) -> str:
        maxlen = getattr(Upload, field).property.columns[0].type.length

        cleantext = request.form.get(field, '')
        cleantext = cleantext[:maxlen]
        cleantext = bleach.clean(cleantext, tags=[])

        if not cleantext:
            abort(422, "A required field is empty!")

        return cleantext

    @form_required
    def post(self):
        name = self.__get_and_sanitize_and_check_text('name')
        address = self.__get_and_sanitize_and_check_text('address')
        text = self.__get_and_sanitize_and_check_text('text')

        u = Upload(
            name=name,
            address=address,
            text=text
        )

        db.session.add(u)
        db.session.commit()

        return jsonify(self.upload_schema.dump(u)), 201
