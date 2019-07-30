from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class Routes(DBUtil):
    '''
        General description:
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for Routes.
    '''

    def __init__(self, db):
        '''
            General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.Routes
        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def get_routes_by_id(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Routes stored in the database.
        Returns:
                Returns the database entity based on the id of the Routes .
        Example :
             get_routes_by_id(id)
        '''
        return (self.collection.find_one({"_id": ObjectId(object_id)}))

    def get_routes_by_role_id(self, role):
        '''
        General description:
        Args:
            param1 (role) : This is the existing unique role id of the\
            Role stored in the database.
        Returns:
                Returns the database entity based on the role id of the Routes .
        Example :
             get_routes_by_role_id(id)
        '''
        return (list(self.collection.find({"_id": {"$in": role}})))

    def get_all_routes(self):
        '''
        General description::
        Retrieves from DB all the plugins based on status
        Args:
             No Arguments
        Returns:
                Returns all the existing Database entities  \
                of the Routes.
        Example :
             get_all_routes()
        '''
        return self.collection.find()

    def add_routes(self, per):
        '''
        General description:
        Args:
            param1 (per) : This is the parameter which has the details of the\
            Routes to be added in the database.Its a JSON object.
        Returns:
                Returns the id of the newly created Routes from the database.
        Example :
             add_routes(per)
        '''
        result = self.collection.insert_one(per)
        return(result.inserted_id)

    def update_role(self, per_data):
        '''
        General description:
        Args:
            param1 (prerequisites) : This is the parameter which has the details of the\
            Routes to be added in the database.Its a JSON object.
        Returns:
               Returns the count of the records updated successfully \
               for Routes.
        Example :
             update_role(per_data)
        '''
        json_new_entry = {}
        for key in per_data.keys():
            if key != "_id":
                json_new_entry[key] = per_data[key]
        result = self.collection.update_one({"_id": ObjectId(per_data["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_routes(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Routes stored in the database.
        Returns:
                Returns the count of the records deleted successfully \
                for the given id of the Routes.
        Example :
             delete_routes(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count
