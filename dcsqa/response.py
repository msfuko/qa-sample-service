import simplejson as json
from flask import make_response
from flask.ext.api import status
from flask import jsonify


def get_json(obj):
    response_status = status.HTTP_204_NO_CONTENT if obj is None else status.HTTP_200_OK
    response = jsonify({
        "status": response_status,
        "errorMessage": "",
        "result": obj
    })
    response.status_code = response_status
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


