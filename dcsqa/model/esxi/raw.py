from dcsqa.model import BaseObject


class RawData(BaseObject):

    props = {
        'woTemplateVersion': (int, True),
        'ARecord': (basestring, False),     # do I need this?
        'NTP': (dict, False),
        'SSH': (dict, False),
        'SyslogHost': (list, False),
        'CoreDump': (dict, False),
        'Account': (list, False)
    }