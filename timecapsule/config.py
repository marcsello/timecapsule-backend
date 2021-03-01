#!/usr/bin/env python3
import os

"""
Configuration
"""


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite://")
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(12))
    CORS_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*")

    SENTRY_DSN = os.environ.get("SENTRY_DSN")
    RELEASE_ID = os.environ.get("RELEASE_ID", "test")
    RELEASEMODE = os.environ.get("RELEASEMODE", "dev")

    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 512 * 1024 * 1024))

    RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")
    RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "/tmp/timecapsule/")

    LOCAL_API_KEY = os.environ.get('LOCAL_API_KEY')
