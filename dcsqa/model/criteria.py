from . import BaseObject


class CriteriaData(BaseObject):

    props = {
        'Alert': (bool, True),
        'Collector': (bool, True),
        'DeviceStatus': (bool, True),
        'FileSystem': (bool, True),
        'Processors': (bool, True),
        'ProductionState': (bool, True),
        'Template': (list, True),
        'IPAddress': (list, True),
        'Datacenter': (basestring, True),
        'SystemName': (basestring, True),
        'FQDN': (basestring, True)
        }