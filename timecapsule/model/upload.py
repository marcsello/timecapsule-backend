#!/usr/bin/env python3
from sqlalchemy import func

from . import db


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=False)

    # Optional fields
    email = db.Column(db.String(255), nullable=True, default=None)
    phone = db.Column(db.String(15), nullable=True, default=None)

    upload_date = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

    text = db.Column(db.Text, nullable=False)
