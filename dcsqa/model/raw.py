from . import BaseObject


class RawData(BaseObject):

    props = {
        'woTemplateVersion': (int, True),
        'Alert': (list, False),
        'Collector': (basestring, False),
        'DeviceStatus': (basestring, False),
        'FileSystem': (dict, False),
        'Processors': (int, False),
        'ProductionState': (basestring, False),
        'Template': (list, False),
        'IPAddress': (basestring, False),
        'Groups': (list, False),
        'Systems': (list, False),
        'DeviceName': (dict, False)
        }