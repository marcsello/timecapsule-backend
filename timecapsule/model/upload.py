#!/usr/bin/env python3
from sqlalchemy import func

from . import db


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    upload_date = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

    text = db.Column(db.Text(2 * 1024 * 1024), nullable=False)  # 2MB maximum

    attachment_original_filename = db.Column(db.String(32), nullable=True, default=None)
    attachment_hash = db.Column(db.String(32), nullable=True, default=None)
    attachment_size = db.Column(db.BigInteger, nullable=True, default=None)
