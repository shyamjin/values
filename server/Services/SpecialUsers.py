from enum import Enum


class SpecialUsers(Enum):
    superadmin = 1
    admin = 2
    guest = 3
    operator = 4
    DPMsysCI = 5

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)