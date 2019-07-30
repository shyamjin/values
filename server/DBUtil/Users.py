import datetime
import random
import re
import string

from bson.objectid import ObjectId
from pymongo import ASCENDING

import Accounts
from DBUtil import DBUtil
import Permissions
import Role
from Services import PasswordHelper
from settings import key


class Users(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for Users.
    '''

    def __init__(self, db):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.Users
        self.roledb = Role.Role(db)
        self.permissiondb = Permissions.Permissions(db)
        self.account_db = Accounts.Accounts()
        self.pass_helper = PasswordHelper.PasswordHelper(key)

        # indexes
        self.collection.create_index([('user', ASCENDING)], unique=True,)

    def decrypt(self, user_details):
        '''
        General description:
        Args:
            param1 : user_details(JSON) : This is the parameter which has details like \
            password /access token .
        Returns:
                Returns Database entity by the userdetails \
                of the User.
        '''
        if user_details:
            if user_details.get("password"):
                user_details["password"] = self.pass_helper.decrypt(
                    user_details["password"])
            if user_details.get("temp_password"):
                user_details["temp_password"] = self.pass_helper.decrypt(
                    user_details["temp_password"])
            if user_details.get("access_token"):
                user_details["access_token"] = self.pass_helper.decrypt(
                    user_details["access_token"])
        return user_details

    def encrypt(self, user_details):
        '''
        General description:
        Args:
            param1 user_details(JSON) : This is the JSON object which has details like \
            password /access token / access_exp_date .
        Returns:
                Returns Database entity by the userdetails \
                of the User.

        '''
        if user_details:
            if user_details.get("password"):
                user_details["password"] = self.pass_helper.encrypt(
                    user_details["password"])
            if user_details.get("temp_password"):
                user_details["temp_password"] = self.pass_helper.encrypt(
                    user_details["temp_password"])
            if user_details.get("access_token"):
                user_details["access_token"] = self.pass_helper.encrypt(
                    user_details["access_token"])
                if user_details.get("access_exp_date"):
                    user_details["access_exp_date"] = datetime.datetime.strptime(
                        str(user_details.get("access_exp_date")).split(".")[0], "%Y-%m-%dT%H:%M:%S")
                else:
                    user_details["access_exp_date"] = datetime.datetime.now(
                    ) + datetime.timedelta(days=365)
        return user_details

    def get_user_by_name(self, text):
        '''
        General description:

        Args:
            param 1: text(string) :This is the parameter which \
            has the unique name of the existing user in the database.

             Returns:
                Returns the existing database entity id based on the user name \
                from the user database.
        Example :
            get_user_by_name(text)
        '''
        user = self.collection.find_one(
            {"user": re.compile('^' + re.escape(text) + '$', re.IGNORECASE)})
        return str(user["_id"])

    def add_user(self, user):
        '''
        General description:

        Args:
            param1 (user) : This is the parameter which has the details of the\
            User to be added in the database.Its a JSON object.
        Returns:
                Returns the id of the newly created User from the database.
        Example :
             add_user(user)
        '''
        user = self.encrypt(user)
        result = self.collection.insert_one(user)
        if user.get("teams") is not None:
            self.collection.update_one({"_id": result.inserted_id},
                                       {"$unset": {"teams": user.get("teams")}})
        return(result.inserted_id)

    def get_user(self, user, get_all_details):
        '''
        General description:

        Args:
            param1 (user) : This is the parameter which has the details of the\
            User to be added in the database.Its a JSON object.
            param2 (get_all_details) :This is the parameter which determines \
            whether all User should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns Database entity by the user and get_all_details \
                flag of the User.
        Example :
             get_user(id,True)
        '''
        result = self.collection.find_one(
            {"user": re.compile('^' + re.escape(user) + '$', re.IGNORECASE)})
        result = self.decrypt(result)
        if get_all_details == True and result is not None:
            return self.add_details(result)
        else:
            return result

    def get_users_by_role_id(self, roleid):
        '''
        General description:

        Args:
            param1: roleid (object) : This is the unique id of the existing\
            role stored in the database.
        Returns:
                Returns the database entity based on the role id of the User .
        Example :
             get_users_by_role_id(id)
        '''
        list_of_users = []
        result = self.collection.find({"roleid": roleid})
        if result:
            for rec in result:
                rec = self.decrypt(rec)
            list_of_users.append(rec)
        return list_of_users

    def get_user_by_id(self, object_id, get_all_details=False):
        '''
        General description:

        Args:
            param1 : object_id (object) : This is unique id of the existing\
            User in database.
            param2 : get_all_details(string) :This is the parameter which determines \
            whether all User should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns Database entity by the user and get_all_details \
                flag of the User.
        Example :
             get_user_by_id(id,True)
        '''
        result = self.collection.find_one({"_id": ObjectId(object_id)})
        result = self.decrypt(result)
        if get_all_details == True and result is not None:
            return self.add_details(result)
        else:
            return result

    def get_user_by_access_token(self, access_token, get_all_details):
        '''
        General description:

        Args:
            param1 : access_token(string) : This is unique access_token with an \
            expiry date time existing for a User in database.
            param2 : get_all_details(string) :This is the parameter which determines \
            whether all User details should be fetched.\
            This has two values - True /False .
        Returns:
                Returns Database entity by the access_token and get_all_details \
                flag of the User.
        Example :
             get_user_by_access_token(access_token,True)
        '''
        user_details = None
        result = self.collection.find({"status":  re.compile("active", re.IGNORECASE),
                                       "access_token": {"$exists": True},
                                       "access_exp_date": {"$gte": datetime.datetime.now()}})
        for rec in result:
            if rec.get("access_token"):
                if access_token == self.decrypt(rec)["access_token"]:
                    user_details = rec
                    break
        if get_all_details == True and user_details is not None:
            return self.add_details(user_details)
        else:
            return user_details

    def add_user_access_token(self, object_id, date_given):
        '''
        General description:

        Args:
            param1 : object_id () : This is unique id \
            existing for a User in database.
            param2 : date_given (JSON) :This is the parameter which has access token \
            and other details to be added in user database.
        Returns:
              Returns the id of the newly created user from the database.
        Example :
             add_user_access_token(id,date_given)
        '''
        user = self.get_user_by_id(object_id, False)
        if not user:
            raise Exception("No such user found")
        object_id = str(user["_id"])
        user = {}
        key = self.id_generator()
        user["access_token"] = key
        if date_given:
            user["access_exp_date"] = date_given
        user["_id"] = {"oid": object_id}
        self.update_user(user)
        return key

    def id_generator(self, size=25, chars=string.ascii_uppercase + string.digits):
        '''
        General description:

        Args:
            param1 (size) : This is to specify the length of database unique ids \
            to be generated at random.
            param2 (chars) :This is the parameter which defines the combination \
            of characters which makes unique id for database.
          *** This has default values defined for both parameters ***
        Returns:
              Returns the id of the newly created user from the database.
        '''
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

    def get_all_users(self):
        '''
        General description:

        Args:
           No arguments.
        Returns:
                Returns Database entity existing in the database for \
                Users.
        '''
        return self.collection.find()

    def update_user(self, user_data):
        '''
        General description:

        Args:
            param1 :user_data (JSON) :This is the parameter which has access token \
            and other details to be updated for a user.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_user(id,user_data)
        '''
        user_data = self.encrypt(user_data)
        json_new_entry = {}
        for key in user_data.keys():
            if key != "_id":
                json_new_entry[key] = user_data[key]

        obj_id = user_data["_id"] if type(user_data["_id"]) is ObjectId else ObjectId(user_data["_id"]["oid"])
        result = self.collection.update_one({"_id": obj_id},
                                            {"$set": json_new_entry}, upsert=False)
        if user_data.get("included_in") is not None:
            self.collection.update_one({"_id": obj_id},
                                       {"$unset": {"included_in": user_data.get("included_in")}})
        return result.modified_count

    def delete_user(self, object_id):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            existing User stored in the database.
        Returns:
                Returns the count of the records deleted successfully \
                for the given id of the User.
        Example :
             delete_user(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def update_user_status(self, object_id, status,status_message = ""):
        '''
        General description:

        Args:
            param1 : object_id (object) : This is the unique id of the\
            existing User stored in the database.
            param2 :status(string) :This is the parameter which has status of user\
            as "active" / "suspend " .
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_user_status(id,status)
        '''
        result = self.collection.update_one(
            {'_id': ObjectId(object_id)}, {"$set": {"status": status,"status_message":status_message}})
        return result.modified_count

    def update_user_account_name(self, name):
        '''
        General description:

        Args:
            param1 : name(string) :This is the unique account name of the\
            existing User stored in the database.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_user_account_name(name)
        '''
        result = self.collection.update_many(
            {}, {"$set": {"accountid": str(self.account_db.get_account_by_name(name)["_id"])}})
        return result.modified_count

    def add_details(self, user):
        '''
        General description:

        Args:
            param1 : user(JSON) : This is the parameter which has the details of the\
            User to be added in the database.Its a JSON object.
        Returns:
                Adds more details of User.
        Example :
             add_details(user)
        '''
        role = self.roledb.get_role_by_id(user["roleid"], True)
        if role is None:
            raise Exception("No role with _id :" +
                            user["roleid"] + " was found")
        user["role_details"] = role
        return user

    def delete_user_access_token(self, object_id):
        '''
        General description:

        Args:
            param1 : object_id (object) : This is unique id \
            existing for a User in database.
        Returns:
                Returns the count of the records deleted successfully \
                for the given id of the User.
        Example :
             delete_user_access_token(id)
        '''
        user = self.get_user_by_id(object_id, False)
        modified_count = 0
        if not user:
            raise Exception("No such user found")
        if user.get("access_token") and user.get("access_exp_date"):
            result = self.collection.update_one({"_id": user.get("_id")},
                                                {"$unset": {"access_token": 1, "access_exp_date": 1}}, upsert=False)
            modified_count = result.modified_count
        return modified_count
    
    def is_duplicate(self, text):
        '''
        General description:

        Args:
            param 1: text(string) :This is the parameter which \
            has the unique name of the existing user in the database.

             Returns:
                Returns the status of user presence based on the user name \
                from the user database.
        Example :
            is_duplicate(text)
        '''
        user = self.collection.find_one(
            {"user": re.compile('^' + re.escape(text) + '$', re.IGNORECASE)})
        if user is None:
            return False
        else:
            return True