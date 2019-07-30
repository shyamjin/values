from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class Permissions(DBUtil):
    '''
        General description :
        This class has definition for functions that provides add /update/ delete \
        or search by entities in database for Permissions.
    '''

    def __init__(self, db):
        '''
            General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.Permissions
        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True,)

    def get_permission_by_id(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Permissions stored in the database.
        Returns:
                Returns Database entity by the id \
                of the Permissions.
        Example :
             get_group_permission_by_id(id)
        '''
        return (self.collection.find_one({"_id": ObjectId(object_id)}))

    def get_permission_by_role_id(self, role):
        '''
        General description:
        Args:
            param1 (role) : This is the unique id of the\
            Role stored in the database.
        Returns:
               Returns Database entity by the id \
               of the Permissions.
        Example :
             get_permission_by_role_id(role)
        '''
        return (list(self.collection.find({"_id": {"$in": role}})))

    def get_all_permission(self):
        '''
        General description:
        Args:
            No Arguments
        Returns:
                Returns all existing Database entities of the Permissions.
        Example :
             get_all_permission()
        '''
        return self.collection.find()

    def add_permission(self, per):
        '''
        General description:
        Args:
            param1 (per) : This is the parameter which has the details of the\
            Permissions to be added in the database.Its a JSON object.
        Returns:
                Returns the id of the newly created Permissions from the database.
        Example :
             add_permission(per)
        '''
        result = self.collection.insert_one(per)
        return(result.inserted_id)

    def update_group_permission(self, per_data):
        '''
        General description:
        Args:
            param1 (perData) : This is the parameter which has the details of the\
            Permissions to be added in the database.Its a JSON object.
        Returns:
               Returns the count of the records updated successfully \
               for the given id of the Permissions.
        Example :
             update_group_permission(perData)
        '''
        json_new_entry = {}
        for key in per_data.keys():
            if key != "_id":
                json_new_entry[key] = per_data[key]
        result = self.collection.update_one({"_id": ObjectId(per_data["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_permission(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Permissions stored in the database.
        Returns:
                Returns the count of the records deleted successfully \
                for the given id of the Permissions.
        Example :
             delete_group_permission(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count
