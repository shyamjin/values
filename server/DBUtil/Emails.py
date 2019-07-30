'''
Created on Mar 16, 2016

@author: PDINDA
'''

from datetime import datetime
import re

from bson.objectid import ObjectId

from DBUtil import DBUtil


class Emails(DBUtil):
    '''
        General description:

       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for PermissionGroup.
    '''

    def __init__(self, db):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.Emails

        # indexes
        # self.collection.create_index([('_id', ASCENDING)], unique=True,)

    def AddEmail(self, record):
        '''
        General description:
        Args:
            param1 (record) : This is the parameter which has the details of the\
            Email to be added in the database.
        Returns:
                Returns the record of the newly created Email from the database.
        Example :
             AddEmail(record)
        '''
        result = self.collection.insert_one(record)
        return(result.inserted_id)

    def UpdateEmailStatus(self, object_id, status, reason=None):
        '''
        General description:
        Args:
        param 1 : object_id (object) : This is the unique id of the\
            Email stored in the database.
             param 2 :status(string) :This is the parameter which determines \
            status
            This has two values - True /False .
          param 3 :reason(string) :This is the parameter which determines \
            reason

        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the Email.
        Example :
             UpdateEmailStatus(object_id, status,reason)
        '''
        result = self.collection.update_one(
            {'_id': object_id}, {"$set": {"status": status, 'upddt': datetime.now(), 'reason': reason}})

    def UpdateRetryCount(self, object_id, retrycount):
        '''
        General description:
        Args:
        param 1 : object_id (object) : This is the unique id of the\
            Email stored in the database.
             param 2 :retrycount(integer) :This is the parameter which determines \
            retrycount

        Returns:
        Returns the count of the records updated successfully \
        for the given id of the Email.
        Example :
             UpdateRetryCount( object_id, retrycount)
        '''
        result = self.collection.update_one(
            {'_id': object_id}, {"$set": {"retrycount": retrycount, 'upddt': datetime.now()}})

    def GetAllEmails(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities of all the existing Emails
        Example :
             GetAllEmails(id)
        '''
        return self.collection.find()

    def RemoveEmail(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            Email stored in the database.
        Returns:
                Returns the count of the records deleted successfully\
                for the given id of the Email
        Example :
            RemoveEmail(id)
        '''
        return (self.collection.delete_one({"_id": ObjectId(object_id)}))

    def GetEmailById(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
           Email stored in the database.
        Returns:
                Returns Database entity by the id of the Email
        Example :
             GetEmailById(id)
        '''
        return (self.collection.find_one({"_id": ObjectId(object_id)}))

    def GetEmailByName(self, msgtype):
        '''
        General description:
        Args:
            param1 (msgtype) : This is the unique Name of the \
            Email stored in the database.
        Returns:
                Returns Database entity by the Name of the Email.
        Example :
             GetEmailByName(msgtype)
        '''
        return (self.collection.find_all({"msgtype": msgtype}))

    def GetPendingEmail(self):
        '''
        General description:
        Args:
            no args
        Returns:
                Returns PendingEmail by the id of the Email.
        Example :
              GetPendingEmail(id)
        '''
        return self.collection.find({"status": {"$in": [re.compile("new", re.IGNORECASE), re.compile("pending", re.IGNORECASE)]}})
