#!/usr/bin/env python3
from flask import jsonify


def get_standard_error_handler(code: int):
    def error_handler(err):
        return jsonify({"msg": err.description, "status": str(code)}), code

    return error_handler


def register_all_error_handlers(app):
    """
    function to register all handlers
    """

    error_codes_to_override = [404, 403, 401, 405, 400, 409, 413, 422]

    for code in error_codes_to_override:
        app.register_error_handler(code, get_standard_error_handler(code))
