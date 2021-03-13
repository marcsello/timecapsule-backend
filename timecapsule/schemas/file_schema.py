#!/usr/bin/env python3
from fnmatch import fnmatch

from marshmallow_sqlalchemy import ModelSchema
from marshmallow_utils.fields import SanitizedHTML
from marshmallow.exceptions import ValidationError
from marshmallow import fields

from model import File

ALLOWED_TYPES = [
    # images
    'image/*',

    # types that are simple to check
    'text/plain',
    'application/pdf',
    'application/vnd.oasis.opendocument.text',

    # ms word
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',

    # Sometimes docx files are being identified as simple zip this may cause obvious problems...
    # but I don't care anymore
    'application/zip'
]


def validate_mimetype(mime):
    for glob in ALLOWED_TYPES:
        if fnmatch(mime, glob):
            return

    raise ValidationError(f'Not allowed mime type: {mime}')


class FileSchema(ModelSchema):
    original_filename = SanitizedHTML(tags=[], attrs=[])
    mime = fields.String(validate=validate_mimetype)

    class Meta:
        model = File
