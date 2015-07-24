from dcsqa.model import BaseObject


class ResultData(BaseObject):

       props = {
        'woTemplateVersion': (int, True),
        'vmSCSIControllerMode': (list, False),
        'vmDiskProvisionMode': (list, False),
        'vmNICType': (list, False),
        'vmCPULayout': (dict, False),
        'vmHostGroup': (dict, False),
        'vmDatastores': (list, False),
        'vmToolStatus': (int, False),
        'vmCPUResAlloc': (dict, False),
        'vmMemResAlloc': (dict, False),
        'vmHardwareVersion': (int, False)
    }