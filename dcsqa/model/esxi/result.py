from dcsqa.model import BaseObject


class ResultData(BaseObject):

    props = {
        'woTemplateVersion': (int, True),
        'ARecord': (int, False),        # do I need this?
        'NTP': (dict, False),
        'SSH': (dict, False),
        'SyslogHost': (int, False),
        'CoreDump': (dict, False),
        'Account': (dict, False)
    }