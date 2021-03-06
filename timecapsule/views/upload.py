#!/usr/bin/env python3
import os
import os.path
from flask import request, abort, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_classful import FlaskView

import hashlib

from model import db, Upload
from schemas import UploadSchema
from utils import rechaptcha_required, apikey_required, form_required
from marshmallow.exceptions import ValidationError


class UploadView(FlaskView):
    uploads_schema_simple = UploadSchema(many=True, exclude=['text', 'attachment_original_filename', 'attachment_hash',
                                                             'attachment_url'])
    upload_schema_simple = UploadSchema(many=False, exclude=['text', 'attachment_original_filename', 'attachment_hash',
                                                             'attachment_url'])
    upload_schema_full = UploadSchema(many=False)

    @rechaptcha_required
    @form_required
    def post(self):

        params = request.form.to_dict(flat=True)
        try:
            u = self.upload_schema_full.load(params, session=db.session)
        except ValidationError as e:
            abort(422, str(e))

        # Handle attachement if needed
        if 'attachment' in request.files:
            attachment = request.files['attachment']

            attachment_original_filename = secure_filename(os.path.basename(attachment.filename))
            attachment_hash = hashlib.md5(attachment.read()).hexdigest()
            attachment_size = attachment.tell()
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

            target_filename = os.path.join(target_dir, f"{attachment_hash}_{attachment_size}{target_file_extension}")
            attachment_duplicate = os.path.isfile(target_filename)

            if not attachment_duplicate:
                attachment.save(target_filename)

            u.attachment_hash = attachment_hash
            u.attachment_original_filename = attachment_original_filename
            u.attachment_size = attachment_size

        # Save stuff to database
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
