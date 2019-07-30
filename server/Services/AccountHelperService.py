from DBUtil import Accounts
from settings import mongodb
from Services import Utils
AccountsDb= Accounts.Accounts()

def validate_account_id(account_id):
    result=None
    if Utils.is_valid_obj_id(account_id):
        result=AccountsDb.get_account(account_id)
    else:
        result=AccountsDb.get_account_by_name(account_id)       
    if result is None:
        raise Exception("Account Id provided is invalid")
    return str(result.get("_id"))