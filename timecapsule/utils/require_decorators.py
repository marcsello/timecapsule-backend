#!/usr/bin/env python3
from flask import request, abort, current_app

from functools import wraps


def json_required(f):
    @wraps(f)
    def call(*args, **kwargs):

        if request.is_json:
            return f(*args, **kwargs)
        else:
            abort(400, "JSON required")

    return call


def form_required(f):
    @wraps(f)
    def call(*args, **kwargs):

        if request.form:
            return f(*args, **kwargs)
        else:
            abort(400, "FormData required")

    return call


def apikey_required(f):

    @wraps(f)
    def call(*args, **kwargs):

        if not current_app.config['LOCAL_API_KEY']:
            abort(401, "Unauthorized")

        apikey_recieved = request.headers.get('Authorization', None)

        if apikey_recieved == current_app.config['LOCAL_API_KEY']:
            return f(*args, **kwargs)
        else:
            abort(401, "Unauthorized")

    return call

