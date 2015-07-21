import unittest
from dcsqa.app import app
import dcsqa.response as response
from decimal import Decimal
from flask import Flask
from flask.ext.testing import TestCase


class ResponseTest(TestCase):

    def create_app(self):
        #
        # for making response
        # refer to - http://pythonhosted.org/Flask-Testing/
        #
        app = Flask(__name__)
        app.config.from_object('config.TestConfig')
        return app

    def test_get_json(self):
        test_response = [{u'Hostname': u'dcs-qauat01.sjdc', u'Memory': Decimal('0'),
                          u'OSType': u'linux', u'CPU': Decimal('0'),
                          u'DataPartition': [{u'name': u'/', u'size': Decimal('20000')},
                                             {u'type': u'SAS', u'local': True,
                                              u'name': u'/trend', u'size': Decimal('80000')}],
                          u'AccountGroup': set([u'dcsqa', u'dcsrd'])
                         }]

        self.assertEqual(200, response.get_json(test_response).status_code)
        self.assertEqual(200, response.get_json("").status_code)
        self.assertEqual(204, response.get_json(None).status_code)

    def test_bad_request(self):
        test_response = response.bad_request("it's really bad")
        self.assertEqual(400, test_response.status_code)
        self.assertIn("it's really bad", response.bad_request("it's really bad").data)

    def test_created(self):
        self.assertEqual(201, response.created().status_code)
