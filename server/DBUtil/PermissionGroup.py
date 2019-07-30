from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
import Permissions
import Routes


class PermissionGroup(DBUtil):
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
        self.collection = db.PermissionGroup
        self.permissiondb = Permissions.Permissions(db)
        self.routesb = Routes.Routes(db)
        # indexes
        self.collection.create_index([('groupname', ASCENDING)], unique=True,)

    def get_group_permission_by_id(self, object_id, get_all_details):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            PermissionGroup stored in the database.
            param2 (get_all_details) :This is the parameter which determines \
            whether all PermissionGroup should be visible to user or not.\
            This has two values - true /False .

        Returns:
                Returns Database entity by the id and get_all_details \
                flag of the PermissionGroup.
        Example :
             get_group_permission_by_id(id,True)
        '''
        result = (self.collection.find_one({"_id": ObjectId(object_id)}))
        if get_all_details == True and result is not None:
            return self.add_details(result)
        else:
            return result

    def get_group_permission_by_name(self, name, get_all_details):
        '''
        General description:
        Args:
            param1 (name) : This is the unique name of the\
            PermissionGroup stored in the database.
            param2 (get_all_details) :This is the parameter which determines \
            whether all PermissionGroup should be visible to user or not.\
            This has two values - true /False .

        Returns:
                Returns Database entity by the id and get_all_details \
                flag of the PermissionGroup.
        Example :
             get_group_permission_by_name(name,True)
        '''
        result = dumps(self.collection.find_one({"groupname": name}))
        if get_all_details == True and result is not None:
            return self.add_details(result)
        else:
            return result

    def add_group_permission(self, grouppermdata):
        '''
        General description:
        Args:
            param1 (grouppermdata) : This is the parameter which has the details of the\
            PermissionGroup to be added in the database.Its a JSON object.
        Returns:
                Returns the id of the newly created PermissionGroup from the database.
        Example :
             add_group_permission(grouppermdata)
        '''
        result = self.collection.insert_one(grouppermdata)
        return str(result.inserted_id)

    def get_all_group_permission(self, get_all_details):
        '''
        General description:
        Args:
            param1 (get_all_details) : This is the parameter which determines \
            whether all PermissionGroup should be visible to user or not.\
            This has two values - true /False .
        Returns:
                Returns all existing Database entities by the get_all_details \
                flag of the PermissionGroup.
        Example :
             get_all_group_permission(True)
        '''
        result = self.collection.find()
        if get_all_details == True and result is not None:
            rec_list = []
            for rec in result:
                rec_list.append(self.add_details(rec))
            return rec_list
        else:
            return result


#     def UpdateGroupPermission(self, role_data):
#         permissiongroup_list = []
#         jsonEntry = '{'
#         for key in role_data.keys():
#             if key != "_id":
#                 if isinstance(role_data[key], (list)) and key == "permissions":
#                     permissiongroup_list.append(role_data[key])
#                 else:
#                     jsonEntry += '"' + key + '":"' + role_data[key] + '",'
#         jsonEntry = jsonEntry[:-1] + '}'
#         data=json.loads(jsonEntry)
#         for e in permissiongroup_list:
#             data["permissions"]=e
#         result = self.collection.update_one({"_id": ObjectId( role_data["_id"]["oid"])},\
#                                             {"$set": data}, upsert=False)
#         return result.modified_count

    def update_group_permission(self, role_data):
        '''
        General description:
        Args:
            param1 (role_data) : This is the parameter which has the details of the\
            PermissionGroup to be added in the database.Its a JSON object.
        Returns:
               Returns the count of the records updated successfully \
               for the given id of the PermissionGroup.
        Example :
             update_group_permission(role_data)
        '''
        json_new_entry = {}
        for key in role_data.keys():
            if key != "_id":
                json_new_entry[key] = role_data[key]
        result = self.collection.update_one({"_id": ObjectId(role_data["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_group_permission(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            PermissionGroup stored in the database.
        Returns:
                Returns the count of the records updated successfully \
                for the given id of the PermissionGroup.
        Example :
             delete_group_permission(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def add_details(self, data):
        '''
        General description:
        Args:
            param1 (data) : This is the parameter which has the details of the\
            PermissionGroup to be added in the database.Its a JSON object.
        Returns:
                Adds more details of permissions to the PermissionGroup.
        Example :
             add_details(data)
        '''
        pemissions_arr = []
        for rec in data["permissions"]:
            pemissions_arr.append(self.permissiondb.get_permission_by_id(rec))
        data["permissions_details"] = pemissions_arr
        routes_arr = []
        for rec in data["routes"]:
            routes_arr.append(self.routesb.get_routes_by_id(rec))
        data["routes_details"] = routes_arr
        return data
