'''
Created on Jun 3, 2016

@author: PDINDA
'''

from datetime import datetime
import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
import SystemDetails


class Sync(DBUtil):
    '''
        General description:
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for Sync.
    '''

    def __init__(self, db):
        '''
            General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.Sync
        self.system_details_db = SystemDetails.SystemDetails(db)

        # indexes
        # self.collection.create_index([('_id', ASCENDING)], unique=True,)

    def add_sync(self, data):
        '''
        General description:

        Args:
            param1: data (JSON) : This is the parameter which has the details of the\
            Sync to be added in the database.Its a JSON object.
        Returns:
                Returns the id of the newly created Sync from the database.
        Example :
             add_sync(data)
        '''
        if data.get("status") is None:
            data["status"] = "new"
        data["updated_time"] = datetime.now()
        data["created_time"] = datetime.now()
        if data.get("source_dpm_version") and len(data.get("source_dpm_version")) > 0:
            self.system_detail = self.system_details_db.get_system_details_single()
            if self.system_detail and self.system_detail.get("dpm_version"):
                if data.get("source_dpm_version") <> self.system_detail.get("dpm_version"):
                    data["warning_message"] = 'This sync might fail as the DPM \
                                               version is expected to be :' + data.get(
                        "source_dpm_version") + \
                        ". Current DPM version is :" + \
                        self.system_detail.get(
                        "dpm_version")
        result = self.collection.insert_one(data)
        return(result.inserted_id)

    def sync_all(self):
        '''
        General description::
        Retrieves from DB all the sync
        Args:
             No Arguments
        Returns:
                Returns all the existing Database entities  \
                of the Sync.
        Example :
             sync_all()
        '''
        return self.collection.find()

    def update_sync(self, sync):
        '''
        General description:

        Args:
            param1: sync(JSON) : This is the parameter which has the details of the\
            Sync to be added in the database.Its a JSON object.
        Returns:
               Returns the count of the records updated successfully \
               for Sync.
        Example :
            update_sync(sync)
        '''
        json_new_entry = {}
        for key in sync.keys():
            if key != "_id":
                json_new_entry[key] = sync[key]
        result = self.collection.update_one({"_id": ObjectId(sync["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def update_sync_status(self, object_id, status, message):
        '''
        General description:

        Args:
            param1: object_id(object) : This is the unique id of the\
            Sync stored in the database.
            param2: status(string) : It can be "New"/"compared" /"processed "/"success" /"failed".
            param2: message(string) : This is the parameter which has the details of the\
            status of the Sync .It either has update successful \
            or no changes found to be updated.
        Returns:
               Returns the count of the records updated successfully \
               for Sync.
        Example :
            update_sync_status(id,status, message)
        '''
        json_entry = {}
        json_entry["status"] = status
        json_entry["status_message"] = message
        json_entry["updated_time"] = datetime.now()
        self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": json_entry}, upsert=False)

    def update_add_processed_by_sync_id(self, sync_id):
        '''
        General description:

        Args:
            param1: sync_id(str) : This is the unique id of the\
            Sync stored in the database.            
        Returns:
               Returns the count of the records updated successfully \
               for Sync.
        Example :
            update_sync_status(sync_id)
        '''
        json_entry = {}
        json_entry["processed_additional_data"] = True
        json_entry["updated_time"] = datetime.now()
        self.collection.update_many({"sync_id": sync_id}, {"$set": json_entry}, upsert=False)

    def remove_sync(self, object_id):
        '''
        General description:
        Args:
            param1: object_id (object) : This is the unique id of the\
            Sync stored in the database.
        Returns:
                Returns the count of the records deleted successfully \
                for the given id .
        Example :
             remove_sync(id)
        '''
        return (self.collection.delete_one({"_id": ObjectId(object_id)}))
    
    def remove_sync_by_sync_id(self, sync_id):
        '''
        General description:
        Args:
            param1: object_id (object) : This is the unique id of the\
            Sync stored in the database.
        Returns:
                Returns the count of the records deleted successfully \
                for the given id .
        Example :
             remove_sync(id)
        '''
        return (self.collection.delete_many({"sync_id": sync_id}))

    def get_sync_by_id(self, object_id):
        '''
        General description:
        Args:
            param1: object_id(object) : This is the existing unique sync id of the\
            Sync stored in the database.
        Returns:
                Returns the database entity based on the sync id .
        Example :
             get_sync_by_id(id)
        '''
        return (self.collection.find_one({"_id": ObjectId(object_id)}))

    def get_sync_type(self, sync_type):
        '''
        General description:
        Args:
            param1:sync_type (string) : This is the type of sync causing service.
            Its vales can be (Push / Pull / Manual )
        Returns:
                Returns the database entity based on the sync type.
        Example :
             get_sync_by_id(sync_type)
        '''
        return (self.collection.find_one({"type": sync_type}))

    def get_sync_by_sync_id(self, sync_id,skip=0,limit=0):
        '''
        General description:
        Args:
            param 1 :sync_id (string) : This is the existing unique sync id of the\
            Sync stored in the database.
            
            param 2 : skip (integer) : This is the count of the\
            Sync req to be skipped.

            param 3 : limit (integer) : This is the count of the\
            Sync req to be limited from the database .
        Returns:
                Returns the database entity based on the sync status .
        Example :
            get_sync_by_sync_id(sync_id)
        '''
        return self.collection.find({"sync_id": sync_id}).skip(skip).limit(limit)
    
    def get_sync_by_filter(self, filter_condition={},skip=0,limit=0):
        '''
        General description:
        Args:
            param 1 :filter (Json) : filter condition.
            
            param 2 : skip (integer) : This is the count of the\
            Sync req to be skipped.

            param 3 : limit (integer) : This is the count of the\
            Sync req to be limited from the database .
        Returns:
                Returns the database entity based on the sync status .
        Example :
            get_sync_by_sync_id(sync_id)
        '''
        return self.collection.find(filter_condition).skip(skip).limit(limit)
    
    def get_pending_sync_to_compare(self):
        '''
        General description:
        Args:
            No Argument.
        Returns:
                Returns the database entity based on the sync status  .
        Example :
            get_pending_sync_to_compare()
        '''
        regx1 = re.compile("new", re.IGNORECASE)
        regx2 = re.compile("retry", re.IGNORECASE)
        result = self.collection.find({"status": {"$in":[regx1,regx2]}}).sort(
            [("created_time", ASCENDING)]).limit(1)
        if result.count() > 0:
            sync_id = result[0]["sync_id"]
        else:
            return None
        if sync_id:
            return self.collection.find({"status": {"$in":[regx1,regx2]},
                                         "sync_id": sync_id}).sort([("process_order", ASCENDING)])
        else:
            return None

    def get_sync_by_sync_id_and_name(self, sync_id, condition, name):
        '''
        General description:
        Args:
            param1; sync_id (object) : This is the existing unique sync id of the\
            Sync stored in the database.
            param2 (name) : This is the existing unique name of the\
            tool stored in the database.
        Returns:
                Returns the database entity based on the sync id and tool name.
        Example :
            get_sync_by_sync_id_and_tool_name(sync_id, name)
        '''
        return self.collection.find({"sync_id": sync_id, condition: re.compile(name, re.IGNORECASE)})

    def get_pending_sync_to_process(self):
        '''
        General description:
        Args:
            No Argument.
        Returns:
                Returns the database entity based on the sync status .
        Example :
            get_pending_sync_to_process()
        '''
        result = self.collection.find({"status": re.compile(
            "compared", re.IGNORECASE)}).sort([("created_time", ASCENDING)]).limit(1)
        if result.count() > 0:
            sync_id = result[0]["sync_id"]
        else:
            return None
        if sync_id:
            return self.collection.find({"status": re.compile("compared", re.IGNORECASE),
                                         "sync_id": sync_id}).sort([("process_order", ASCENDING)])
        else:
            return None
      
    def get_distinct_sync_id_by_status(self,status=""):
        '''
        General description::
        Retrieves distinct sync_id list based on status

        Args:
             No Arguments
        Returns:
                Returns all distinct sync_id list based on status
        Example :
             get_distinct_sync_id_by_status(success)
        '''
        return self.collection.distinct("sync_id",{"status": {"$regex": status, "$options": "i"}})
      

    def get_distinct_sync_id_pending_callback(self):
        '''
        General description::
        Retrieves distinct sync_ids with pending callback

        Args:
             No Arguments
        Returns:
                Returns distinct sync_ids with pending callback
        Example :
             get_distinct_sync_id_pending_callback()
        '''
        sync_ids=self.collection.distinct("sync_id",{"status": {"$in": ["failed","success"]},\
                            "callback_status": {"$nin": ["failed","success","skipped"]}})
        final_list=[]
        for sync_id in sync_ids:
            if self.collection.find({"sync_id":sync_id}).count() == self.collection.find({"sync_id":sync_id,\
                            "status": {"$in": ["failed","success"]}}).count() :
                final_list.append(sync_id)                                                                                       
        return final_list            
    
    def update_callback_status_by_sync_id(self, sync_id,callback_status,callback_status_reason):
        '''
        General description:

        Args:
            param1: sync_id(str) : This is the unique id of the\
            Sync stored in the database.
            param1: callback_status(str) : Callback Status
            param1: callback_status_reason(str) : Reason for Callback Status  
        Returns:
               Returns the count of the records updated successfully \
               for Sync.
        Example :
            update_callback_status_by_sync_id(sync_id,callback_status,callback_status_reason)
        '''
        json_entry = {}
        json_entry["callback_status"] = callback_status
        json_entry["callback_status_reason"] = callback_status_reason
        self.collection.update_many({"sync_id": sync_id}, {"$set": json_entry}, upsert=False)
        
    def get_sync_data_for_sync_all(self,sync_id):
        syncs = self.collection.find({"sync_id": sync_id})
        date=None
        status="success"
        for sync in syncs:
            date=sync.get("date")
            if sync.get("status").lower() == "failed":
                status="failed"
                break
            elif not(sync.get("status").lower() == "success" or sync.get("status").lower() == "skipped"):
                status="running"
        return  {"sync_id":sync_id , "date" : date , "status" : status}
    
    def sync_distinct_status(self,sync_id):
        '''
        General description::
        Retrieves from DB all the avalibale status for a sync

        Args:
             No Arguments
        Returns:
                Returns all the existing Database entities  \
                of the Sync.
        Example :
             sync_distict_status()
        '''
        return self.collection.distinct("status",{"sync_id":sync_id })
                 
            