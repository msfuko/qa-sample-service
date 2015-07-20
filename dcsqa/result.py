#!/bin/env python
# coding: utf-8

import response
from auth import auth
from flask import request, Blueprint, current_app
from dcsqa.dao.table import DataTable
from dcsqa.model.result import ResultData
from dcsqa.cache import cache

result_blueprint = Blueprint('result', __name__)


@result_blueprint.before_request
@auth.login_required
def before_request():
    current_app.logger.debug("user login - {user}".format(user=auth.username()))


@result_blueprint.route('', methods=['GET'])
@cache.memoize()
def get_all_result():
    raw = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['RESULT_TABLE'],
                    logger=current_app.logger)
    result = raw.find_all()
    return response.get_json(result)


@result_blueprint.route('/<ticket_key>', methods=['GET'])
@cache.memoize()
def get_result_by_ticketkey(ticket_key):
    raw = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['RESULT_TABLE'],
                    logger=current_app.logger)
    result = raw.find_by_ticketkey(ticket_key)
    return response.get_json(result)


@result_blueprint.route('/<ticket_key>/<host>', methods=['GET'])
@cache.memoize()
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
    #    3. validate JSON string
    #    4. save to DB
    #    5. purge cache
    #

    # 1.
    if request.headers['Content-Type'] != 'application/json':
        return response.bad_request("please send application/json")

    # 2.
    # http://flask.pocoo.org/docs/0.10/api/#flask.Request.get_json
    try:
        data = request.get_json()
    except Exception as ex:
        current_app.logger.error(ex)
        return response.bad_request("invalid JSON format")

    # 3.
    try:
        result = ResultData(**data).get_json()
    except Exception as ex:
        current_app.logger.error(ex)
        return response.bad_request(ex.message)

    # 4.
    dao = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['RESULT_TABLE'],
                    logger=current_app.logger)
    dao.save(result)

    # 5.
    cache.delete_memoized(get_all_result)
    cache.delete_memoized(get_result_by_ticketkey, result['TicketKey'])
    cache.delete_memoized(get_result_by_ticketkey_host, result['TicketKey'], result['Host'])

    return response.created()