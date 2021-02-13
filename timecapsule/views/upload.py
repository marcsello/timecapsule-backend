#!/usr/bin/env python3
from flask import request, abort, jsonify
from werkzeug.utils import secure_filename
from flask_classful import FlaskView

import bleach
import hashlib

from model import db, Upload
from schemas import UploadSchema
from utils import form_required, rechaptcha, apikey_required


class UploadView(FlaskView):
    uploads_schema_simple = UploadSchema(many=True, exclude=['text', 'attachment_original_filename', 'attachment_hash',
                                                             'attachment_url'])
    upload_schema_simple = UploadSchema(many=False, exclude=['text', 'attachment_original_filename', 'attachment_hash',
                                                             'attachment_url'])
    upload_schema_full = UploadSchema(many=False)

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
        if not rechaptcha.verify():
            abort(422, "reCAPTCHA validation failed!")

        name = self.__get_and_sanitize_and_check_text('name')
        address = self.__get_and_sanitize_and_check_text('address')
        text = self.__get_and_sanitize_and_check_text('text')

        attachment_original_filename = None
        attachment_hash = None
        if 'attachment' in request.files:
            attachment = request.files['attachment']

            attachment_original_filename = secure_filename(attachment.filename)
            attachment_hash = hashlib.md5(attachment.read()).hexdigest()

        u = Upload(
            name=name,
            address=address,
            text=text,
            attachment_hash=attachment_hash,
            attachment_original_filename=attachment_original_filename
        )

        db.session.add(u)
        db.session.commit()

        return jsonify(self.upload_schema_simple.dump(u)), 201

    @apikey_required
    def index(self):
        uploads = Upload.query.all()
        return jsonify(self.uploads_schema_simple.dump(uploads)), 200

    @apikey_required
    def get(self, id_: int):
        upload = Upload.query.get_or_404(id_)
        return jsonify(self.upload_schema_full.dump(upload)), 200
