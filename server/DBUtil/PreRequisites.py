from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class PreRequisites(DBUtil):
    '''
       General description :
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
        self.collection = db.PreRequisites
        # indexes
        self.collection.create_index(
            [('prerequisites_name', ASCENDING)], unique=True)

    def get_pre_requisites(self, name):
        '''
        General description::
        Retrieves from DB the plugin based on name
        Args:
            param1 (name) : This is the unique name of the\
            PreRequisite stored in the database.
        Returns:
                Returns Database entity by the id \
                of the PreRequisite.
        Example :
             get_pre_requisites(name)
        '''
        return self.collection.find_one({"prerequisites_name": name})

    def get_pre_requisites_by_id(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            PreRequisite stored in the database.
        Returns:
                Returns the database entity based on the id of the PreRequisite .
        Example :
             get_pre_requisites_by_id(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def get_all_pre_requisites(self):
        '''
        General description::
        Retrieves from DB all the plugins based on status
        Args:
             No Arguments
        Returns:
                Returns all the existing Database entities  \
                of the PreRequisite.
        Example :
             get_all_pre_requisites()
        '''
        return self.collection.find()

    def add_pre_requisites(self, prerequisites):
        '''
        General description:
        Args:
            param1 (prerequisites) : This is the parameter which has the details of the\
            PreRequisite to be added in the database.Its a JSON object.
        Returns:
                Returns the id of the newly created PreRequisite from the database.
        Example :
             add_pre_requisites(prerequisites)
        '''
        result = self.collection.insert_one(prerequisites)
        return str(result.inserted_id)

    def update_pre_requisites(self, prerequisites):
        '''
        General description:
        Args:
            param1 (prerequisites) : This is the parameter which has the details of the\
            PreRequisite to be added in the database.Its a JSON object.
        Returns:
               Returns the count of the records updated successfully \
               for PreRequisite.
        Example :
             update_pre_requisites(name,status)
        '''
        json_new_entry = {}
        for key in prerequisites.keys():
            if key != "_id":
                json_new_entry[key] = prerequisites[key]
        result = self.collection.update_one({"_id": ObjectId(prerequisites["_id"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_pre_requisites(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            PreRequisite stored in the database.
        Returns:
                Returns the count of the records deleted successfully \
                for the given id of the PreRequisite.
        Example :
             delete_pre_requisites(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def delete_all_pre_requisites(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Deletes the existing database entities of the PreRequisite.
        Example :
             delete_all_pre_requisites(id)
        '''
        self.collection.delete_many({})
