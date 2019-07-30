'''
Created on Apr 23, 2016

@author: PDINDA
'''

from bson.objectid import ObjectId
from pymongo import ASCENDING
import re
from DBUtil import DBUtil


class MachineType(DBUtil):
    '''
        General description:

       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for MachineType.
    '''

    def __init__(self, db):
        '''
           General description :
           This function initializes the database variables and \
           index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.MachineType
        # indexes
        self.collection.create_index([('type', ASCENDING)], unique=True,)

    def get_machine_type_by_id(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the MachineType store in the database.
        Returns:
                Returns Database entity by the id of the MachineType.
        Example :
             get_machine_type_by_id(id)
        '''
        return (self.collection.find_one({"_id": ObjectId(object_id)}))

    def get_machine_type_by_name(self, name):
        '''
        General description:
        Args:
            param1 (name) : This is the MachineType name .
        Returns:
                Returns Database entity by MachineType name of the existing MachineType.
        Example :
             get_machine_type_by_name(name)
        '''
        return (self.collection.find_one({"type":  re.compile('^' + re.escape(name) + '$', re.IGNORECASE)}))

    def get_all_machine_type(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities existing in the MachineType collection.
        Example :
             get_all_machine_type()
        '''
        return self.collection.find()

    def add_machine_type(self, per):
        '''
        General description:
        Args:
            param1 (per) : This is the parameter which has the details for \
            the new machine Type to be added in database.
        Returns:
                Returns Database entity id of the new MachineType created
        Example :
             add_machine_type(per)
        '''
        result = self.collection.insert_one(per)
        return(result.inserted_id)

    def update_machine_type(self, perData):
        '''
        General description:
        Args:
            param1 (perData) : This is the parameter which has the details for \
            the existing machine type to be updated in database.Its a JSON object.
        Returns:
                Returns the count of records successfully updated .
        Example :
             update_machine_type(perData)
        '''
        json_new_entry = {}
        for key in perData.keys():
            if key != "_id":
                json_new_entry[key] = perData[key]
        result = self.collection.update_one({"_id": ObjectId(perData["_id"]["oid"])}, {
                                            "$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_machine_type(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of \
            the existing machine type to be deleted from database.
        Returns:
                Returns the count of records successfully deleted.
        Example :
             delete_machine_type(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count
