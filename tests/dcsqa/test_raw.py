import unittest
import base64
import boto3
import json
import mock
from entry import app
from moto.dynamodb2 import mock_dynamodb2
from moto.sqs import mock_sqs
from dcsqa.dao.queue import Queue


class RawRequestTest(unittest.TestCase):

    def setUp(self):
        self.region_name = 'us-east-1'
        self.table_name = 'test-RawData'
        app.config.from_object('config.TestConfig')
        self.app = app.test_client()

    def _create_table(self):
        dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        dynamodb.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'TicketKey',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Host',
                    'AttributeType': 'S'
                },
                ],
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'TicketKey',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'Host',
                    'KeyType': 'RANGE'
                },
                ],

            ProvisionedThroughput={
                'ReadCapacityUnits': 3,
                'WriteCapacityUnits': 3
            }
        )

    def _get_auth_header(self, json=False):
        header = {'Authorization': 'Basic ' + base64.b64encode("{0}:{1}".format('dcsrd', 'happy'))}
        if json:
            header['Content-Type'] = 'application/json'
        return header

    @mock_dynamodb2
    @mock.patch('dcsqa.criteria.Queue')
    def test_post_raw(self, mock_queue):
        self._create_table()

        # test no content
        self.assertEqual(204, self.app.get('/zenoss/v1/raw', headers=self._get_auth_header()).status_code)

        # test post 400 wrong header
        response = self.app.post('/zenoss/v1/raw/testKey/test', headers=self._get_auth_header(),
                                 data=dict(Alert=['4']), follow_redirects=True)
        self.assertEqual(400, response.status_code)
        self.assertIn("please send application/json", response.data)

        # test validation
        response = self.app.post('/zenoss/v1/raw/testKey/test', headers=self._get_auth_header(json=True),
                                 data=json.dumps(dict(Alert=['4'])), follow_redirects=True)
        self.assertEqual(400, response.status_code)

        # test success
        response = self.app.post('/zenoss/v1/raw/testKey/test', headers=self._get_auth_header(json=True),
                                 data=json.dumps(dict(Alert=['4'], woTemplateVersion=110)), follow_redirects=True)
        self.assertEqual(201, response.status_code)

