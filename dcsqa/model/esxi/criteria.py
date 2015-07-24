from dcsqa.model import BaseObject


class CriteriaData(BaseObject):

    props = {
        'woTemplateVersion': (int, True),
        'isVirtual': (bool, True),
        'FQDN': (basestring, True),
        'Version': (basestring, True)
    }

