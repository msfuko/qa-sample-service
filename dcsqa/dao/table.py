#
# refer to https://boto3.readthedocs.org/en/latest/guide/dynamodb.html
#

import boto3
import logging
from boto3.dynamodb.conditions import Key, Attr, And


class DataTable(object):

    def __init__(self, region_name, table_name, logger=logging.getLogger(__name__)):
        dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = dynamodb.Table(table_name)
        self.logger = logger

    def find_all(self):
        #full scan
        response = self.table.scan()
        if response['Count'] > 0:
            return response['Items']
        else:
            self.logger.warn("there are no record in %s" % self.table.name)
            return None        

    def find_by_ticketkey(self, ticket_key):
        response = self.table.query(
            KeyConditionExpression=Key('TicketKey').eq(ticket_key)
        )
        if response['Count'] > 0:
            self.logger.debug(response['Items'])
            return response['Items']
        else:
            self.logger.warn("there are no record TicketKey=%s in %s" % (ticket_key, self.table.name))
            return None

    def find_by_ticketkey_host(self, ticket_key, host):
        response = self.table.query(
            KeyConditionExpression=Key('TicketKey').eq(ticket_key) & Key('Host').eq(host)
        )
        
        if response['Count'] > 0:
            items = response['Items']
            self.logger.debug(items[0])
            #not return array
            return items[0]
        else:
            self.logger.warn("there are no record TicketKey=%s, Host=%s in %s" % (ticket_key, host, self.table.name))
            return None

    def find_by_ticketkey_status(self, ticket_key, status):
        response = self.table.query(
            IndexName="Summary-index",
            KeyConditionExpression=Key('TicketKey').eq(ticket_key) & Key('Summary').eq(int(status))
        )
        if response['Count'] > 0:
            self.logger.debug(response['Items'])
            return response['Items']
        else:
            self.logger.warn("there are no record TicketKey=%s greater than %s in %s"
                             % (ticket_key, status, self.table.name))
            return None

    def find_by_ticketkey_gt_status(self, ticket_key, status):
        response = self.table.query(
            IndexName="Summary-index",
            KeyConditionExpression=Key('TicketKey').eq(ticket_key) & Key('Summary').gt(int(status))
        )
        if response['Count'] > 0:
            self.logger.debug(response['Items'])
            return response['Items']
        else:
            self.logger.warn("there are no record TicketKey=%s greater than %s in %s"
                             % (ticket_key, status, self.table.name))
            return None

    def save(self, item, **kwargs):
        """
        Save item into Table
        :param item: (dict) of saved item
        :return:
        """
        item.update(kwargs)
        response = self.table.put_item(Item=item)
        self.logger.info(response)
        return response
    
    def update(self, ticket_key, text_json):
        pass
    
    def delete(self, ticket_key):
        pass