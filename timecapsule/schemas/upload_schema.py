#!/usr/bin/env python3
from marshmallow_sqlalchemy import ModelSchema

from model import Upload


class UploadSchema(ModelSchema):
    class Meta:
        model = Upload
