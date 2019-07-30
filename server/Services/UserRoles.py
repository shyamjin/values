from enum import Enum


class UserRoles(Enum):
    SuperAdmin = 1
    Admin = 2
    Operator = 3
    Guest = 4
    DPMsysCI = 5

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)