#!/usr/bin/env python3
import os
import os.path
from magic import Magic
from flask import request, abort, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_classful import FlaskView

import hashlib

from model import db, Upload
from schemas import UploadSchema, FileSchema
from utils import rechaptcha_required, apikey_required, form_required
from marshmallow.exceptions import ValidationError


class UploadView(FlaskView):
    uploads_schema_simple = UploadSchema(many=True, exclude=['text', 'files'])
    upload_schema_simple = UploadSchema(many=False, exclude=['text', 'files'])
    upload_schema_full = UploadSchema(many=False)
    file_schema_full = FileSchema(many=False)

    @rechaptcha_required
    @form_required
    def post(self):

        params = request.form.to_dict(flat=True)
        try:
            u = self.upload_schema_full.load(params, session=db.session)
        except ValidationError as e:
            return abort(422, str(e))  # This is not a return actually, I just want PyCharm to shut up

        db.session.add(u)

        # Start handling of files
        if request.files:
            # ensure a containing directory
            os.makedirs(current_app.config["UPLOAD_FOLDER"], 0o755, exist_ok=True)

        if len(request.files) > current_app.config['MAX_FILES_IN_UPLOAD']:
            return abort(422, "Too many files")

        # Handle attachments if needed
        files_to_save = []
        m = Magic(mime=True)
        for field_name, attachment in request.files.items():

            original_filename = secure_filename(os.path.basename(attachment.filename))
            md5_hash = hashlib.md5(attachment.read()).hexdigest()
            size = attachment.tell()

            if size > current_app.config['MAX_SINGLE_FILE_LENGTH']:
                return abort(413, f"{field_name} is too big")

            # MD5 calculating read the file to the end, so we have to seek back to it's beginning to actually save it
            attachment.seek(0, 0)

            # Apparently .doc requires to be fully read in order to being identified properly
            mime = m.from_buffer(attachment.read())
            attachment.seek(0, 0)

            # prepare file to be saved
            target_file_extension = os.path.splitext(original_filename)[-1]
            # We don't want filenames ending with a dot
            if target_file_extension == '.':
                target_file_extension = ''

            target_filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                f"{md5_hash}_{size}{target_file_extension}"
            )

            # Files will be saved later, after all validated successfully
            files_to_save.append((attachment, target_filepath))

            # Store meta data

            file_params = {
                'original_filename': original_filename,
                'md5_hash': md5_hash,
                'size': size,
                'mime': mime
            }

            try:
                f = self.file_schema_full.load(file_params, session=db.session)
            except ValidationError as e:
                return abort(422, str(e))  # This is not a return actually, I just want PyCharm to shut up

            f.upload = u
            db.session.add(f)

        # All single validation succeeded so far
        # But database constraints are not yet enforced
        # We just save the files here, so that if saving fails, the data won't be committed to the db

        for attachment, target_filepath in files_to_save:
            if not os.path.isfile(target_filepath):
                attachment.save(target_filepath)

        # Commit all that stuff to database
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
