import json
import decimal
from flask import make_response
from flask.ext.api import status
from flask import jsonify


def get_json(obj):

    def _convert_decimal_to_int(obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)

    if obj is not None:
        response = make_response(json.dumps(obj, default=_convert_decimal_to_int))
    else:
        # Response does not contain any data
        response = make_response()
        response.status_code = status.HTTP_204_NO_CONTENT

    response.mimetype = 'application/json'

    return response


def bad_request(message):
    response = jsonify({
        "status": status.HTTP_400_BAD_REQUEST,
        "errorMessage": message
    })
    response.status_code = status.HTTP_400_BAD_REQUEST
    return response


def created():
    response = jsonify({
        "status": status.HTTP_201_CREATED,
        "errorMessage": ""
    })
    response.status_code = status.HTTP_201_CREATED
    return response


