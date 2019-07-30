from datetime import datetime, timedelta
from bson.objectid import ObjectId
from DBUtil import DBUtil
from pymongo import DESCENDING
from settings import mongodb




class Auditing(DBUtil):
    '''
    General description :
    This class has definition for functions that provides add /update/ delete \
     search by entities in database for Auditing.
    '''

    def __init__(self):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        db = mongodb
        DBUtil.__init__(self, db)
        self.collection = db.Auditing

        
    def get_all(self, skip=0, limit=0,filter={}):
        '''
          General description:
          Args:
             no Args
          Returns:
                  Returns Database entities existing in the Auditing collection.
          Example :
          get_all()
        '''
        return self.collection.find(filter,{"_id":1,"url":1,"response_time":1,"response_status_code":1,"user":1,"requested_at":1,"request_type":1,"remote_addr":1,"api_type":1,"user":1}).skip(
            skip).limit(limit).sort([['_id', DESCENDING]])

    def add(self, data):
        '''
          General description:
          Args:
              param1 data(String) : This is the parameter which has the details for \
              the data to be added in database.
          Returns:
                  Returns Database entity id of the data created
          Example :
               add()
        '''
        result = self.collection.insert_one(data)
        return str(result.inserted_id)
    
    
    def delete(self, object_id):
        '''
        General description:

        Args:
           param1 : object_id(object) : This is the unique id of the\
            state stored in the database.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_state(id)
        '''
        return self.collection.delete_one({"_id": ObjectId(object_id)}).deleted_count
    
    def remove_all_older_than_date(self,olderthandays):
        '''
          General description:
          Args:
             no Args
          Returns:
                  Returns Database entities existing in the Auditing collection.
          Example :
          get_all()
        '''
        d = datetime.now() - timedelta(days=olderthandays)
        return self.collection.delete_many({"requested_at": {"$lt": d}}).deleted_count
    
    def update(self, data, oid):
        '''
          General description:
          Args:
              param1 data(String) : This is the parameter which has the details for \
              the data to be added in database.
              param2 oid(String) : Object Id.
          Returns:
                  Returns update count
          Example :
               update(data,oid)
        '''
        data["response_time"] = str((datetime.now()-data["requested_at"]).total_seconds() * 1000) + " ms"
        result = self.collection.update_one(
            {"_id": ObjectId(oid)}, {"$set": data}, upsert=True)
        return str(result.modified_count)
    
    def get_audit_by_id(self, object_id):
        audit = self.collection.find_one({"_id": ObjectId(str(object_id))})
        return audit                                               