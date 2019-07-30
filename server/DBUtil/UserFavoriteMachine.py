'''
Created on Apr 23, 2016

@author: PDINDA
'''


from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
import Machine
import MachineType
import Users


class UserFavoriteMachine(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for UserFavoriteMachine.
    '''

    def __init__(self, db):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.UserFavoriteMachine
        self.machineTypeDb = MachineType.MachineType(db)
        self.machineDB = Machine.Machine(db)
        self.userDB = Users.Users(db)
        # indexes
        self.collection.create_index(
            [('user_id', ASCENDING), ('machine_id', ASCENDING)], unique=True)

    def get_user_favorite_machine_by_user_id(self, userid, all_details):
        '''
        General description:

        Args:
            param1 : userid(object) : This is the unique id of the\
            User which is associated with UserFavoriteMachine stored in the database.

            param2 : all_details(string) :This is the parameter which determines \
            whether all UserFavoriteMachine details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the user id and\
                is_all_details parameter.
        Example :
            get_user_favorite_machine_by_user_id(userid ,True)
        '''
        if self.userDB.get_user_by_id(userid, False) is None:
            raise ValueError(" User was not found")
        result = self.collection.find({"user_id": userid})
        if all_details == True and result is not None:
            return self.all_details(result)
        else:
            return result

    def get_user_favorite_machine_by_machine_id_and_user_id(self, machine_id, user_id):
        '''
        General description:

        Args:
            param 1 : userid(object) : This is the unique id of the\
            User which is associated with UserFavoriteMachine stored in the database.

            param 2 : machine_id (object) : This is the unique id of the\
            Machine which is associated with UserFavoriteMachine stored in the database.

            param 3 : all_details(string) :This is the parameter which determines \
            whether all UserFavoriteMachine details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the userid ,machine_id and\
                is_all_details parameter.
        Example :
            get_user_favorite_machine_by_machine_id_and_user_id(userid ,machine_id ,True)
        '''
        result = self.collection.find_one(
            {"machine_id": machine_id, "user_id": user_id})
        return result

    def get_all_user_favorite_machine(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns the database entities existing for UserFavoriteMachine.
        Example :
            get_all_user_favorite_machine()
        '''
        result = self.collection.find()
        return result

    def add_user_favorite_machine(self, per):
        '''
        General description:

        Args:
            param1 : per(JSON) : This is the parameter which has details \
            for new UserFavoriteMachine .
        Returns:
              Returns the id of the newly created UserFavoriteMachine in the database.
        Example :
             add_user_favorite_machine(per)
        '''
        result = self.collection.insert_one(per)
        return(result.inserted_id)

    def update_user_favorite_machine(self, per_data):
        '''
        General description:

        Args:
            param1 : per_data (JSON) : This is the parameter which has details\
            of UserFavoriteMachine.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_user_favorite_machine(per_data)
        '''
        json_new_entry = {}
        for key in per_data.keys():
            if key != "_id":
                json_new_entry[key] = per_data[key]
        result = self.collection.update_one({"_id": ObjectId(per_data["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_user_favorite_machine(self, object_id):
        '''
        General description:

        Args:
           param1 : object_id(object) : This is the unique id of the\
            UserFavoriteMachine stored in the database.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_user_favorite_machine(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def all_details(self, my_fav_machine):
        '''
        General description:

        Args:
            param1 : my_fav_machine(JSON) : This is the parameter which has details \
            for a UserFavoriteMachine .
        Returns:
              Returns the JSON object with the details of UserFavoriteMachine.
        Example :
             all_details(my_fav_machine)
        '''
        fav_machine = {}
        machinelist = []
        typelist = self.machineTypeDb.get_all_machine_type()
        if typelist is None:
            raise Exception("No machine types were found in MachineType")
        for machinetype in typelist:
            machinelist = []
            my_fav_machine.rewind()
            for favmachine in my_fav_machine:
                is_found = self.machineDB.GetMachine(favmachine["machine_id"])
                if is_found is None:
                    raise Exception("Fav machine with _id :" +
                                    favmachine["machine_id"] + " was not found")
                elif is_found.get("machine_type") is None:
                    raise Exception(
                        "Fav machine with _id :" + favmachine["machine_id"] + "\
                         has no type defined")
                elif is_found.get("machine_name") is None:
                    raise Exception(
                        "Fav machine with _id :" + favmachine["machine_id"] + "\
                         has no name defined")
                elif is_found["machine_type"] == str(machinetype["_id"]):
                    data = {}
                    data["machine_name"] = is_found["machine_name"]
                    data["machine_id"] = str(is_found["_id"])
                    data["_id"] = favmachine["_id"]
                    machinelist.append(data)
            fav_machine[machinetype["type"]] = machinelist
        return fav_machine

    def delete_tools_by_machine_id(self, machine_id):
        '''
        General description:

        Args:
           param1 : machine_id(object) : This is the unique id of the\
            Machine based on which ToolOnMachine will be deleted.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_tools_by_machine_id(id)
        '''
        result = self.collection.delete_many({"machine_id": machine_id})
        return result.deleted_count
