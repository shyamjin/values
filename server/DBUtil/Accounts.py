import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
from settings import mongodb


class Accounts(DBUtil):
    '''
    General description :
    This class has definition for functions that provides add /update/ delete \
     search by entities in database for Accounts.
    '''

    def __init__(self):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        db = mongodb
        DBUtil.__init__(self, db)
        self.collection = db.Accounts

        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def get_accounts(self):
        '''
          General description:
          Args:
             no Args
          Returns:
                  Returns Database entities existing in the Accounts collection.
          Example :
          get_accounts()
        '''
        return self.collection.find()

    def get_account(self, object_id):
        '''
          General description:
          Args:
              param1 (object_id) : This is the Account Id which is stored in database
          Returns:
                  Returns Database entity of Account for the given Account Id
          Example :
              get_account(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def get_account_by_name(self, name):
        '''
         General description:
         Args:
             param1 name(String) : This is the Account_name which is part of a account.
         Returns:
                 Returns Database entity of account for the given account_name.
         Example :
              get_account_by_name("Test")
        '''

        return (self.collection.find_one({"name": re.compile('^' + re.escape(name) + '$', re.IGNORECASE)}))

    def add_account(self, NEW_ACCOUNT):
        '''
          General description:
          Args:
              param1 NEW_ACCOUNT(String) : This is the parameter which has the details for \
              the NEW_ACCOUNT to be added in database.
          Returns:
                  Returns Database entity id of the newAccount created
          Example :
               add_account(NEW_ACCOUNT)
        '''
        NEW_ACCOUNT["status"] = "1"
        result = self.collection.insert_one(NEW_ACCOUNT)
        return str(result.inserted_id)

    def update_account_by_name(self, old_account_name, new_account_name):
        '''
         General description:
         Args:
             param1 (old_account_name) : This is the account details of the existing account
             which we have to update.Its a new_account_name.
            param2 (new_account_name) : This is the account details of the new account
            which will  update.Its a old_account_name.
         Returns:
                 Returns the count of records that has been updated \
                 successfully for a given account .
         Example :
              update_account_by_name(old_account_name, new_account_name)
       '''
        result = self.collection.update_one({"name": re.compile(old_account_name, re.IGNORECASE)},
                                            {"$set": {"name": new_account_name}})
        return result.modified_count

    def update_account(self, account):
        '''
          General description:
          Args:
              param1 ( account) : This is the parameter which has the details for \
              the existing account to be updated in database.Its a JSON object.
          Returns:
                  Returns the count of records successfully updated .
          Example :
               update_account( account):
        '''

        result = self.collection.update_one({"_id": ObjectId(account["_id"]["oid"])},
                                            {"$set": {"name": account["name"]}})
        return result.modified_count

    def delete_account(self, object_id):
        '''
         General description:
         Args:
             param1 (object_id) : This is the unique id of \
             the existing Account to be deleted from database.
         Returns:
                 Returns the count of records successfully deleted.
         Example :
              delete_account(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count
