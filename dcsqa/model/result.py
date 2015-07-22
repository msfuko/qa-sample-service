from . import BaseObject


class ResultData(BaseObject):

    props = {
        'woTemplateVersion': (int, True),
        'Alert': (int, False),
        'Collector': (int, False),
        'DeviceStatus': (int, False),
        'FileSystem': (int, False),
        'Processors': (int, False),
        'ProductionState': (int, False),
        'Template': (dict, False),
        'IPAddress': (int, False),
        'Groups': (int, False),
        'Systems': (int, False),
        'DeviceName': (int, False)
        }