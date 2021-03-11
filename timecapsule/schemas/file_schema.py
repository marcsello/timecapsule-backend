#!/usr/bin/env python3
from marshmallow_sqlalchemy import ModelSchema
from marshmallow_utils.fields import SanitizedHTML

from model import File


class UploadSchema(ModelSchema):
    original_filename = SanitizedHTML(tags=[], attrs=[])

    class Meta:
        model = File
