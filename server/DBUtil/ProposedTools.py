import re
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import ASCENDING
from DBUtil import DBUtil
from settings import mongodb


class ProposedTools(DBUtil):
    '''
    General description :
    This class has definition for functions that provides add /update/ delete \
     search by entities in database for ProposedTools.
    '''

    def __init__(self):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        db = mongodb
        DBUtil.__init__(self, db)
        self.collection = db.ProposedTools

        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def get_all(self,filters_to_apply={}):
        '''
          General description:
          Args:
             no Args
          Returns:
                  Returns Database entities existing in the ProposedTools collection.
          Example :
          get_all()
        '''
        if filters_to_apply:
            return self.collection.find(filters_to_apply)
        return self.collection.find()

    def get_by_id(self, object_id):
        '''
          General description:
          Args:
              param1 (object_id) : This is the ProposedTools Id which is stored in database
          Returns:
                  Returns Database entity of ProposedTools for the given FlexibleAttributes Id
          Example :
              get_by_id(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def get_by_name(self, name):
        '''
         General description:
         Args:
             param1 name(String) : This is the ProposedTools name.
         Returns:
                 Returns Database entity of ProposedTools for the given name.
         Example :
              get_by_name("Test")  
        '''
        return (self.collection.find_one({"name": re.compile('^' + re.escape(name) + '$')}))
    
    
    def add(self, data):
        '''
          General description:
          Args:
              param1 data(String) : This is the parameter which has the details for \
              the data to be added in database.
          Returns:
                  Returns Database entity id of the FlexibleAttributes created
          Example :
               add(data)
        '''
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, data):
        '''
          General description:
          Args:
              param1 ( data) : This is the parameter which has the details for \
              the existing account to be updated in database.Its a JSON object.
          Returns:
                  Returns the count of records successfully updated .
          Example :
               update(data):
        '''
        data["updated_time"] = datetime.now()
        json_new_entry = {}
        for key in data.keys():
            if key != "_id":
                json_new_entry[key] = data[key]

        result = self.collection.update_one({"_id": ObjectId(data["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete(self, object_id):
        '''
         General description:
         Args:
             param1 (object_id) : This is the unique id of \
             the existing Account to be deleted from database.
         Returns:
                 Returns the count of records successfully deleted.
         Example :
              delete(object_id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count