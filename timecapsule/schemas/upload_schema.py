#!/usr/bin/env python3
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from model import Upload


class UploadSchema(ModelSchema):
    have_attachment = fields.Method("get_have_attachment", dump_only=True)
    text_length = fields.Method("get_text_length", dump_only=True)
    attachment_url = fields.Method("get_attachment_url", dump_only=True)

    def get_have_attachment(self, upload: Upload) -> int:
        return bool(upload.attachment_hash) and bool(upload.attachment_original_filename)

    def get_text_length(self, upload: Upload) -> int:
        return len(upload.text)

    def get_attachment_url(self, upload: Upload):
        return "TODO"

    class Meta:
        model = Upload
