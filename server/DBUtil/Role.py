import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
import PermissionGroup


class Role(DBUtil):
    '''
        General description:
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for Role.
    '''

    def __init__(self, db):
        '''
            General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.Role
        self.group_permission_db = PermissionGroup.PermissionGroup(db)

        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True,)

    def get_role_by_id(self, object_id, get_all_details):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Roles stored in the database.
            param2 (get_all_details) :This is the parameter which determines \
            whether all details of Role should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the id and\
                get_all_details flag of the Roles .
        Example :
             get_role_by_id(id,True)
        '''
        result = (self.collection.find_one({"_id": ObjectId(object_id)}))
        if get_all_details == True and result is not None:
            return self.add_details(result)
        else:
            return result

    def get_role_by_name(self, role_name, get_all_details):
        '''
        General description:
        Args:
            param1 (role_name) : This is the unique name of the\
            Role stored in the database.
            param2 (get_all_details) :This is the parameter which determines \
            whether all Role should be visible to user or not.\
            This has two values - true /False .
        Returns:
                Returns Database entity by the id and get_all_details \
                flag of the Role.
        Example :
             get_role_by_name(role_name,True)
        '''
        result = (self.collection.find_one(
            {"name": re.compile(role_name, re.IGNORECASE)}))
        if get_all_details == True and result is not None:
            return self.add_details(result)
        else:
            return result

    def get_role_name_by_id(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Role stored in the database.
        Returns:
                Returns Database entity by the id and get_all_details \
                flag of the Role.
        Example :
             get_role_name_by_id(id)
        '''
        return (self.collection.find_one({"_id": ObjectId(object_id)},
                                         {'_id': 0, 'name': 1}))

    def get_all_roles(self):
        '''
        General description:
        Args:
           No Arguments.
        Returns:
                Returns all existing Database entities \
                of the Role.
        Example :
             get_all_roles()
        '''
        return self.collection.find()

    def add_role(self, role):
        '''
        General description:
        Args:
            param1 (role) : This is the parameter which has the details of the\
            Role to be added in the database.Its a JSON object.
        Returns:
                Returns the id of the newly created Role from the database.
        Example :
             add_role(role)
        '''
        role["status"] = "active"
        result = self.collection.insert_one(role)
        return(result.inserted_id)

#     def UpdateRole(self, role_data):
#         permissiongroup_list = None
#         routegroup_list = None
#         jsonEntry = '{'
#         for key in role_data.keys():
#             if key != "_id":
#                 if isinstance(role_data[key], (list)) and key == "permissiongroup":
#                     permissiongroup_list=role_data[key]
#                 else:
#                     jsonEntry += '"' + key + '":"' + role_data[key] + '",'
#         jsonEntry = jsonEntry[:-1] + '}'
#         data=json.loads(jsonEntry)
#         if permissiongroup_list is not None:
#             data["permissiongroup"]=permissiongroup_list
#         result = self.collection.update_one({"_id": ObjectId( role_data["_id"]["oid"])},
#                                             {"$set": data}, upsert=False)
#         return result.modified_count

    def update_role(self, role_data):
        '''
        General description:
        Args:
            param1 (role_data) : This is the parameter which has the details of the\
            Role to be added in the database.Its a JSON object.
        Returns:
               Returns the count of the records updated successfully \
               for the given id of the Role.
        Example :
             update_role(role_data)
        '''
        json_new_entry = {}
        for key in role_data.keys():
            if key != "_id":
                json_new_entry[key] = role_data[key]
        result = self.collection.update_one({"_id": ObjectId(role_data["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_role(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Role stored in the database.
        Returns:
                Returns the count of the records updated successfully \
                for the given id of the Role.
        Example :
             delete_role(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def add_group_permission_to_role(self, object_id, per_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Role stored in the database.
            param2 (per_id) :This is the parameter which determines \
            which Role is associated with this role.\
        Returns:
               Returns the count of the records updated successfully \
               for the given Role id of the existing Role ID.
        Example :
             add_group_permission_to_role(id,per_id)
        '''
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$push": {"permissiongroup": per_id}})
        return result.modified_count

    def remove_group_permission_to_role(self, object_id, per_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Role stored in the database.
            param2 (per_id) :This is the parameter which determines \
            which Role is associated with this role.
        Returns:
               Returns the count of the records removed successfully \
               for the given Role id of the existing Role ID.
        Example :
             remove_group_permission_to_role(id,per_id)
        '''
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$pull": {"permissiongroup": per_id}})
        return result.modified_count

    def add_details(self, data):
        '''
        General description:
        Args:
            param1 (data) : This is the parameter which has the details of the\
            Role to be added in the database.Its a JSON object.
        Returns:
                Adds more details of permissions to the Role.
        Example :
             add_details(data)
        '''
        permission_group_group = []
        if data.get("permissiongroup") is not None:
            for rec in data["permissiongroup"]:
                permission_group_group.append(
                    self.group_permission_db.get_group_permission_by_id(rec, True))
            data["permissiongroup_details"] = permission_group_group
        return data
