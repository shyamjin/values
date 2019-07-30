'''
Created on Jun 3, 2016

@author: PDINDA
'''

from datetime import datetime
import json
import re

from bson.objectid import ObjectId

from DBUtil import DBUtil
from Services import PasswordHelper
from settings import key


class SyncRequest(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for SyncRequest.
    '''

    def __init__(self, db):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.SyncRequest
        self.passHelper = PasswordHelper.PasswordHelper(key)

        # indexes
        # self.collection.create_index([('_id', ASCENDING)], unique=True,)

    def decrypt(self, sync_details):
        '''
        General description:
        Args:
            param1 : sync_details(JSON) : This is the parameter which has details like \
            username /dpm_username / target_dpm_detail etc .
        Returns:
                Returns Database entity by the sync_details \
                of the Sync Request.
        '''
        if sync_details.get("username") is not None:
            sync_details["username"] = self.passHelper.decrypt(
                sync_details["username"])
        if sync_details.get("password") is not None:
            sync_details["password"] = self.passHelper.decrypt(
                sync_details["password"])

        if sync_details.get("target_dpm_detail") and len(sync_details.get("target_dpm_detail")) > 0:
            target_dpm_detail = sync_details["target_dpm_detail"]
            # PULL URL AND PUSH Uses dpm_username,dpm_password
            if target_dpm_detail.get("dpm_username"):
                target_dpm_detail["dpm_username"] = self.passHelper.decrypt(
                    target_dpm_detail["dpm_username"])
            if target_dpm_detail.get("dpm_password"):
                target_dpm_detail["dpm_password"] = self.passHelper.decrypt(
                    target_dpm_detail["dpm_password"])
            # PULL FILE USES      username,password
            if target_dpm_detail.get("username"):
                target_dpm_detail["username"] = self.passHelper.decrypt(
                    target_dpm_detail["username"])
            if target_dpm_detail.get("password"):
                target_dpm_detail["password"] = self.passHelper.decrypt(
                    target_dpm_detail["password"])
            sync_details["target_dpm_detail"] = target_dpm_detail

        steps_to_auth = []
        if sync_details.get("steps_to_auth") and len(sync_details.get("steps_to_auth")) > 0:
            for data in sync_details["steps_to_auth"]:
                if data.get("username"):
                    data["username"] = self.passHelper.decrypt(
                        data["username"])
                if data.get("password"):
                    data["password"] = self.passHelper.decrypt(
                        data["password"])
                steps_to_auth.append(data)
            sync_details["steps_to_auth"] = steps_to_auth
        return sync_details

    def encrypt(self, sync_details):
        '''
        General description:
        Args:
            param1 : sync_details(JSON) : This is the parameter which has details like \
            username /dpm_username / target_dpm_detail .
        Returns:
                Returns Database entity by the sync_details \
                of the Sync Request.
        '''
        if sync_details.get("username") is not None:
            sync_details["username"] = self.passHelper.encrypt(
                sync_details["username"])
        if sync_details.get("password") is not None:
            sync_details["password"] = self.passHelper.encrypt(
                sync_details["password"])

        if sync_details.get("target_dpm_detail") and len(sync_details.get("target_dpm_detail")) > 0:
            target_dpm_detail = sync_details["target_dpm_detail"]
            # PULL URL AND PUSH Uses dpm_username,dpm_password
            if target_dpm_detail.get("dpm_username"):
                target_dpm_detail["dpm_username"] = self.passHelper.encrypt(
                    target_dpm_detail["dpm_username"])
            if target_dpm_detail.get("dpm_password"):
                target_dpm_detail["dpm_password"] = self.passHelper.encrypt(
                    target_dpm_detail["dpm_password"])
            # PULL FILE USES      username,password
            if target_dpm_detail.get("username"):
                target_dpm_detail["username"] = self.passHelper.encrypt(
                    target_dpm_detail["username"])
            if target_dpm_detail.get("password"):
                target_dpm_detail["password"] = self.passHelper.encrypt(
                    target_dpm_detail["password"])
            sync_details["target_dpm_detail"] = target_dpm_detail

        if sync_details.get("steps_to_auth") and len(sync_details.get("steps_to_auth")) > 0:
            steps_to_auth = []
            for data in sync_details["steps_to_auth"]:
                if data.get("username"):
                    data["username"] = self.passHelper.encrypt(
                        data["username"])
                if data.get("password"):
                    data["password"] = self.passHelper.encrypt(
                        data["password"])
                steps_to_auth.append(data)
            sync_details["steps_to_auth"] = steps_to_auth
        return sync_details

    def add_sync_request(self, sync_details):
        '''
        General description:

        Args:
            param1 : sync_details(JSON) : This is the parameter which has details like \
            username /dpm_username / target_dpm_detail etc .
        Returns:
              Returns the id of the newly created sync request from the database.
        Example :
             add_sync_request(sync_details)
        '''
        sync_details["status"] = "active"
        sync_details = self.encrypt(sync_details)
        result = self.collection.insert_one(sync_details)
        return str(result.inserted_id)

    def update_sync_request(self, sync_data):
        '''
        General description:

        Args:
            param1 : sync_data(JSON) : This is the parameter which has details like \
            username /dpm_username / target_dpm_detail etc .
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_sync_request(sync_data)
        '''
        sync_data = self.encrypt(sync_data)
        # Check if sync of pull type is getting updated.If so allow only one
        # active pull
        if sync_data.get("_id"):
            if sync_data["_id"].get("oid"):
                request = self.get_sync_request_by_id(
                    sync_data["_id"].get("oid"))
                if request is None:
                    raise ValueError(
                        "No such SyncRequest was found with id :" + sync_data["_id"].get("oid"))
                if str(request["sync_type"]).lower() == "pull":
                    if sync_data.get("status"):
                        if sync_data.get("status").lower() == "active":
                            if len(self.get_pending_sync_pull()) > 0:
                                raise ValueError(
                                    "Existing active pull requests were found.Only 1 Pull request can be active at once")
        json_new_entry = {}
        for key in sync_data.keys():
            if key != "_id":
                json_new_entry[key] = sync_data[key]
        result = self.collection.update_one({"_id": ObjectId(sync_data["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def update_deployment_request_status(self, object_id, status, message):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            SyncRequest stored in the database
            param2 : status (string) : It can be "New"/"compared" /"processed "/"success" /"failed".
            param3 : message(string) : This is the parameter which has the details of the\
            status of the SyncRequest .It either has update successful \
            or no changes found to be updated.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_deployment_request_status(id , status , message)
        '''
        json_entry = {}
        json_entry["last_sync_status"] = status
        json_entry["last_sync_message"] = message
        json_entry["last_sync_time"] = datetime.now()
        result = self.collection.update_one({"_id": ObjectId(object_id)},
                                            {"$set": json_entry}, upsert=False)

    def remove_sync_request(self, object_id):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            SyncRequest stored in the database.
        Returns:
                Returns the count of the records deleted successfully \
                for the given id .
        Example :
             remove_sync_request(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def get_all_sync_request(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns the database entities existing for SyncRequest.
        Example :
            get_all_sync_request()
        '''
        return self.collection.find()

    def get_sync_request_by_id(self, object_id):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            SyncRequest stored in the database.
        Returns:
                Returns the database entity based on the sync request id.
        Example :
            get_sync_request_by_id(id)
        '''
        result = self.collection.find_one({"_id": ObjectId(object_id)})
        if not result:
            return result
        else:
            return self.decrypt(result)

    def get_sync_request_type(self, sync_type):
        '''
        General description:

        Args:
            param1: sync_type(string) : This is the type of sync request causing service.
            Its vales can be (Push / Pull / Manual )
        Returns:
                Returns the database entity based on the sync type.
        Example :
             get_sync_request_type(sync_type)
        '''
        return (self.collection.find({"type": sync_type}))

    def get_pending_sync_pull(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns the database entity based on the sync type as "Pull" and status as "active"  .
        Example :
            get_pending_sync_pull()
        '''
        result = self.collection.find({"status": {"$in": [re.compile(
            "active", re.IGNORECASE)]}, "sync_type": {"$in": [re.compile("pull", re.IGNORECASE)]}})
        if not result:
            return result
        else:
            list = []
            for rec in result:
                list.append(self.decrypt(rec))
        return list

    def get_pending_sync_push(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns the database entity based on the sync type as "push" and status as "active"  .
        Example :
            get_pending_sync_push()
        '''
        result = self.collection.find({"status": {"$in": [re.compile("active", re.IGNORECASE)]},
                                       "sync_type": {"$in": [re.compile("push", re.IGNORECASE)]}})
        if not result:
            return result
        else:
            list = []
            for rec in result:
                list.append(self.decrypt(rec))
        return list

    def init_status_details(self, object_id, file_list):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            SyncRequest stored in the database.
            param2 : file_list (list) : This parameter takes list of sync request "status" details/
            in a file .
        Returns:
                Returns the count of the successful records updated.
        Example :
            init_status_details(id, file_list)
        '''
        result = self.collection.update_one({"_id": ObjectId(object_id)},
                                            {"$set": json.loads(file_list)}, upsert=False)
        return result.modified_count

    def update_step_status(self, object_id, file_name, file_num, status):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            SyncRequest stored in the database.
            param2 : file_name (string) : This parameter takes name of the file which has \
            sync request "status" details.
            param3 : file_num (integer) : This parameter takes unique number of file.
            param4 : status (string) : It can be "New"/"compared" /"processed "/"success" /"failed".
        Returns:
                Returns the count of the successful records updated.
        Example :
            update_step_status(id,file_name)
        '''
        set_node = '"file_list.' + file_num + "."
        data = set_node + 'file_status' + '":"' + status + '",'
        data = '{' + data[:-1] + '}'
        result = self.collection.update_one({"_id": ObjectId(str(object_id))},
                                            {"$set": json.loads(data)}, upsert=False)
        return result.modified_count
