#!/bin/env python
# coding: utf-8

import response
from auth import auth
from flask import request, Blueprint, current_app
from dcsqa.dao.table import DataTable
from dcsqa.dao.queue import Queue
from dcsqa.model.criteria import CriteriaData
from dcsqa.cache import cache

criteria_blueprint = Blueprint('criteria', __name__)


@criteria_blueprint.before_request
@auth.login_required
def before_request():
    current_app.logger.debug("user login - {user}".format(user=auth.username()))


@criteria_blueprint.route('', methods=['GET'])
@cache.memoize()
def get_all_criteria():
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                         table_name=current_app.config['CRITERIA_TABLE'],
                         logger=current_app.logger)
    result = criteria.find_all()
    return response.get_json(result)


@criteria_blueprint.route('/<ticket_key>', methods=['GET'])
@cache.memoize()
def get_criteria_by_ticketkey(ticket_key):
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                         table_name=current_app.config['CRITERIA_TABLE'],
                         logger=current_app.logger)
    result = criteria.find_by_ticketkey(ticket_key)
    return response.get_json(result)


@criteria_blueprint.route('/<ticket_key>/<host>', methods=['GET'])
@cache.memoize()
def get_criteria_by_ticketkey_host(ticket_key, host):
    criteria = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                         table_name=current_app.config['CRITERIA_TABLE'],
                         logger=current_app.logger)
    result = criteria.find_by_ticketkey_host(ticket_key, host)
    return response.get_json(result)


@criteria_blueprint.route('', methods=['POST'])
def set_criteria_by_ticketkey_host():
    
    #
    # [Validation]
    #    1. must be content-type is applicaiton/json
    #    2. JSON must be parsed successfully
    #    3. validate JSON string
    #    4. save to DB
    #    5. purge cache
    #    6. enqueue
    #
    
    # 1.
    if request.headers['Content-Type'] != 'application/json':
        current_app.logger.warn("received Content-Type %s" % request.headers['Content-Type'])
        return response.bad_request("please send application/json")

    # 2.
    # http://flask.pocoo.org/docs/0.10/api/#flask.Request.get_json
    try:
        data = request.get_json()
    except Exception as ex:
        current_app.logger.warn("couldn't parse JSON %s" % ex)
        return response.bad_request("invalid JSON format")

    # 3.
    try:
        criteria = CriteriaData(**data).get_json()
    except Exception as ex:
        current_app.logger.error(ex)
        return response.bad_request(ex.message)

    # 4.
    table = DataTable(region_name=current_app.config['DYNAMODB_REGION'],
                      table_name=current_app.config['CRITERIA_TABLE'],
                      logger=current_app.logger)
    result = table.save(criteria)

    # 5.
    cache.delete_memoized(get_all_criteria)
    cache.delete_memoized(get_criteria_by_ticketkey, criteria['TicketKey'])
    cache.delete_memoized(get_criteria_by_ticketkey_host, criteria['TicketKey'], criteria['Host'])

    # 6.
    queue = Queue(region_name=current_app.config['SQS_REGION'],
                  queue_name=current_app.config['SQS_NAME'],
                  logger=current_app.logger)
    queue.push({key: data[key] for key in ['TicketKey', 'Host']})

    return response.created()

