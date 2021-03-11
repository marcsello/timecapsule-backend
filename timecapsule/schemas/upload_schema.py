#!/usr/bin/env python3
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from marshmallow.validate import Regexp, Length
from marshmallow_utils.fields import SanitizedHTML

from model import Upload


class UploadSchema(ModelSchema):
    attachment_count = fields.Method("get_attachement_count", dump_only=True)
    text_length = fields.Method("get_text_length", dump_only=True)

    email = fields.Email()
    phone = fields.String(validate=Regexp(r"^\+?[0-9]{6,13}$"))

    text = SanitizedHTML(validate=Length(max=(2 * 1024 * 1024)), tags=[], attrs=[])  # ~2MB (or a lot more bc UTF-8)
    address = SanitizedHTML(tags=[], attrs=[])
    name = SanitizedHTML(tags=[], attrs=[])

    files = fields.Nested('FileSchema', many=True)

    def get_attachement_count(self, upload: Upload) -> int:
        return len(upload.files)  # backref

    def get_text_length(self, upload: Upload) -> int:
        return len(upload.text)

    class Meta:
        model = Upload
