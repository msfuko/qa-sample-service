#!/bin/env python
# coding: utf-8

import response
from flask import request
from flask import Blueprint
from dcsqa.dao.table import DataTable
from flask import current_app

result_blueprint = Blueprint('result', __name__)


@result_blueprint.route('', methods=['GET'])
def get_all_result():
    raw = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['RESULT_TABLE'],
                    logger=current_app.logger)
    result = raw.find_all()
    return response.get_json(result)


@result_blueprint.route('/<ticket_key>', methods=['GET'])
def get_result_by_ticketkey(ticket_key):
    raw = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['RESULT_TABLE'],
                    logger=current_app.logger)
    result = raw.find_by_ticketkey(ticket_key)
    return response.get_json(result)


@result_blueprint.route('/<ticket_key>/<host>', methods=['GET'])
def get_result_by_ticketkey_host(ticket_key, host):
    raw = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['RESULT_TABLE'],
                    logger=current_app.logger)
    result = raw.find_by_ticketkey_host(ticket_key, host)
    return response.get_json(result)


@result_blueprint.route('', methods=['POST'])
def set_result_by_ticketkey_host():

    #
    # [Validation]
    #    1. must be content-type is applicaiton/json
    #    2. JSON must be parsed successfully
    #    3. JSON must has TicketKey
    #    4. JSON must has Host
    #

    # 1.
    if request.headers['Content-Type'] != 'application/json':
        return response.bad_request("please send application/json")

    # 2.
    # http://flask.pocoo.org/docs/0.10/api/#flask.Request.get_json
    try:
        data = request.get_json()
    except Exception as ex:
        #criteria_blueprint.loo
        current_app.logger.error(ex)
        return response.bad_request("invalid JSON format")

    # 3.
    if 'TicketKey' not in data:
        return response.bad_request("TiketKey is not found")

    # 4.
    if 'Host' not in data:
        return response.bad_request("Host is not found")

    dao = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['RESULT_TABLE'],
                    logger=current_app.logger)
    result = dao.save(data)

    return response.is_okay()