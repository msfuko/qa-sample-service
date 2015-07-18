import unittest
from dcsqa.model import BaseObject
from dcsqa.app import app


class ModelTest(unittest.TestCase):

    def setUp(self):
        #
        # to resolve 'working outside of application context' error when make_reponse
        # refer to http://flask.pocoo.org/docs/0.10/appcontext/
        #
        app.config.from_object('config.TestConfig')
        self.app_context = app.app_context()
        self.app_context.push()
        self.base_test_data = {
            'TicketKey': 'test-1',
            'Host': 'test-host'
        }

    def tearDown(self):
        self.app_context.pop()

    def test_key(self):
        class TestData(BaseObject):
            props = {
                'TicketKey': (basestring, True),
                'Host': (basestring, True),
            }

        # test no required 'Host'
        test_data = {
            'TicketKey': 'test-1'
        }
        with self.assertRaises(ValueError) as ex:
            fail = TestData(**test_data).get_json()
        self.assertEqual("Properties Host is required in type <type 'basestring'>", ex.exception.message)

        # test success
        obj = TestData(**self.base_test_data)
        self.assertIsInstance(obj, TestData)
        self.assertEquals(obj.get_json(), self.base_test_data)

    def test_bool(self):
        class TestBooleanData(BaseObject):
            props = {
                'TicketKey': (basestring, True),
                'Host': (basestring, True),
                'Unrequired_boolean': (bool, False),
                'Required_boolean': (bool, True)
            }

        # test no required boolean
        with self.assertRaises(ValueError) as ex:
            fail = TestBooleanData(**self.base_test_data).get_json()
        self.assertEqual("Properties Required_boolean is required in type <type 'bool'>", ex.exception.message)

        # test success
        self.base_test_data['Required_boolean'] = True
        obj = TestBooleanData(**self.base_test_data)
        self.assertIsInstance(obj, TestBooleanData)
        self.assertEquals(obj.get_json(), self.base_test_data)

        # test unrequired field
        self.base_test_data['Unrequired_boolean'] = True
        obj = TestBooleanData(**self.base_test_data)
        self.assertIsInstance(obj, TestBooleanData)
        self.assertEquals(obj.get_json(), self.base_test_data)

    def test_list(self):
        class TestListData(BaseObject):
            props = {
                'TicketKey': (basestring, True),
                'Host': (basestring, True),
                'Unrequired_list': (list, False),
                'Required_list': (list, True)
            }

        # test no required list
        with self.assertRaises(ValueError) as ex:
            fail = TestListData(**self.base_test_data).get_json()
        self.assertEqual("Properties Required_list is required in type <type 'list'>", ex.exception.message)

        # test success
        self.base_test_data['Required_list'] = [{'1': 1, '2': 2}, {'2': 2, '3': 3}]
        obj = TestListData(**self.base_test_data)
        self.assertIsInstance(obj, TestListData)
        self.assertEquals(obj.get_json(), self.base_test_data)

        # test unrequired field
        self.base_test_data['Unrequired_list'] = [{'1': 1, '2': 2}, {'2': 2, '3': 3}]
        obj = TestListData(**self.base_test_data)
        self.assertIsInstance(obj, TestListData)
        self.assertEquals(obj.get_json(), self.base_test_data)
