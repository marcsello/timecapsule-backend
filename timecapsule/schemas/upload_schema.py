#!/usr/bin/env python3
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from marshmallow.validate import Regexp
from marshmallow_utils.fields import SanitizedHTML

from model import Upload


class UploadSchema(ModelSchema):
    have_attachment = fields.Method("get_have_attachment", dump_only=True)
    text_length = fields.Method("get_text_length", dump_only=True)

    email = fields.Email()
    phone = fields.String(validate=Regexp("^\+?[0-9]{6,13}$"))

    text = SanitizedHTML(tags=[], attrs=[])
    address = SanitizedHTML(tags=[], attrs=[])
    name = SanitizedHTML(tags=[], attrs=[])

    def get_have_attachment(self, upload: Upload) -> int:
        return bool(upload.attachment_hash) and bool(upload.attachment_original_filename)

    def get_text_length(self, upload: Upload) -> int:
        return len(upload.text)

    class Meta:
        model = Upload
