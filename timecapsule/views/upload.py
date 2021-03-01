#!/usr/bin/env python3
import os
import os.path
from flask import request, abort, jsonify, current_app
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

    # @form_required # Using this decorator would mean that the form data is being parsed before the request is handled
    # This is not a problem unto itself, but long file uploads could cause reChaptcha to time out
    # So we want to validate reChaptcha as fast as possible, and parse the formData later
    def post(self):

        # Chaptcha response is moved to header so it can be parsed quickly before the formdata is being parsed
        rechaptcha_response = request.headers.get('X-G-Recaptcha-Response')

        if not rechaptcha_response:
            abort(422, "Missing reCAPTCHA response! (should be provided as a header)")

        if not rechaptcha.verify(response=rechaptcha_response):
            abort(422, "reCAPTCHA validation failed!")

        # Start parsing the form data from here -----

        if not request.form:
            abort(400, "Form Data required")

        name = self.__get_and_sanitize_and_check_text('name')
        address = self.__get_and_sanitize_and_check_text('address')
        text = self.__get_and_sanitize_and_check_text('text')

        attachment_original_filename = None
        attachment_hash = None
        if 'attachment' in request.files:
            attachment = request.files['attachment']

            attachment_original_filename = secure_filename(os.path.basename(attachment.filename))
            attachment_hash = hashlib.md5(attachment.read()).hexdigest()
            # MD5 calculating read the file to the end, so we have to seek back to it's beginning to actually save it
            attachment.seek(0, 0)

            # ensure a containing directory
            target_dir = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(target_dir, 0o755, exist_ok=True)

            # Save file
            target_file_extension = os.path.splitext(attachment_original_filename)[-1]
            # We don't want filenames ending with a dot
            if target_file_extension == '.':
                target_file_extension = ''

            target_filename = os.path.join(target_dir, attachment_hash + target_file_extension)
            attachment.save(target_filename)

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
