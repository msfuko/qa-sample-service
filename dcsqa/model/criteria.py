from . import BaseObject


class CriteriaData(BaseObject):

    props = {
        'woTemplateVersion': (int, True),
        'OsType': (basestring, True),       # for checking it's esxi or not
        'Datacenter': (basestring, True),   # for checking collector
        'SystemName': (basestring, True),   # for checking which zenoss site
        'Alert': (bool, True),
        'Collector': (bool, True),
        'DeviceStatus': (bool, True),
        'FileSystem': (bool, True),
        'Processors': (bool, True),
        'ProductionState': (bool, True),
        'Template': (list, True),
        'IPAddress': (list, True),
        'FQDN': (basestring, True)
        }