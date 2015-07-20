#!/bin/env python
# coding: utf-8

import response
from auth import auth
from flask import request, Blueprint, current_app
from dcsqa.dao.table import DataTable
from dcsqa.model.raw import RawData
from dcsqa.cache import cache

raw_blueprint = Blueprint('raw', __name__)


@raw_blueprint.before_request
@auth.login_required
def before_request():
    current_app.logger.debug("user login - {user}".format(user=auth.username()))


@raw_blueprint.route('', methods=['GET'])
@cache.memoize()
def get_all_raw():
    raw = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['RAW_TABLE'],
                    logger=current_app.logger)
    result = raw.find_all()
    return response.get_json(result)


@raw_blueprint.route('/<ticket_key>', methods=['GET'])
@cache.memoize()
def get_raw_by_ticketkey(ticket_key):
    raw = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['RAW_TABLE'],
                    logger=current_app.logger)
    result = raw.find_by_ticketkey(ticket_key)
    return response.get_json(result)


@raw_blueprint.route('/<ticket_key>/<host>', methods=['GET'])
@cache.memoize()
def get_raw_by_ticketkey_host(ticket_key, host):
    raw = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['RAW_TABLE'],
                    logger=current_app.logger)
    result = raw.find_by_ticketkey_host(ticket_key, host)
    return response.get_json(result)


@raw_blueprint.route('', methods=['POST'])
def set_raw_by_ticketkey_host():

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
        raw = RawData(**data).get_json()
    except Exception as ex:
        current_app.logger.error(ex)
        return response.bad_request(ex.message)

    # 4.
    dao = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                    table_name=current_app.config['RAW_TABLE'],
                    logger=current_app.logger)
    dao.save(raw)

    # 5.
    cache.delete_memoized(get_all_raw)
    cache.delete_memoized(get_raw_by_ticketkey, raw['TicketKey'])
    cache.delete_memoized(get_raw_by_ticketkey_host, raw['TicketKey'], raw['Host'])

    return response.created()