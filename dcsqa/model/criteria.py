from . import BaseObject


class CriteriaData(BaseObject):

    props = {
        'TicketKey': (basestring, True),
        'Host': (basestring, True),
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