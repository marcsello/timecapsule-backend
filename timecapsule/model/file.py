#!/usr/bin/env python3
from . import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    upload_id = db.Column(db.Integer, db.ForeignKey("upload.id", ondelete="CASCADE"), nullable=False)
    upload = db.relationship("Upload", backref=db.backref("files", lazy='joined'))

    original_filename = db.Column(db.String(255), nullable=True, default=None)  # limits.h NAME_MAX
    md5_hash = db.Column(db.String(32), nullable=True, default=None)
    size = db.Column(db.BigInteger, nullable=True, default=None)

    # TODO: mimetype
