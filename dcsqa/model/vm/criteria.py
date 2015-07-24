from dcsqa.model import BaseObject


class CriteriaData(BaseObject):

    props = {
        'woTemplateVersion': (int, True),
        'isVirtual': (bool, True),
        'Hypervisor': (basestring, True),         # temporary adding - for hypervisor name or cluster name
        'Datastore': (list, True)
    }

