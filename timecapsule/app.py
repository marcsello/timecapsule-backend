#!/usr/bin/env python3
from flask import Flask
from config import Config

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from flask_cors import CORS

from model import db
from utils import register_all_error_handlers

from views import UploadView

app = Flask(__name__)
app.config.from_object(Config)

if Config.SENTRY_DSN:
    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        integrations=[FlaskIntegration(), SqlalchemyIntegration()],
        send_default_pii=True,
        release=Config.RELEASE_ID,
        environment=Config.RELEASEMODE
    )

db.init_app(app)
register_all_error_handlers(app)
CORS(app)


@app.before_first_request
def init_db():
    db.create_all()


for view in [UploadView]:
    view.register(app, trailing_slash=False)

if __name__ == '__main__':
    app.run()
