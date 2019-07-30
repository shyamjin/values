from bson.objectid import ObjectId
from pymongo import ASCENDING
from DBUtil import DBUtil
import Config
from settings import mongodb



class SystemDetails(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for SystemDetails.
    '''

    def __init__(self, db):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.SystemDetails
        self.configDb=Config.Config(mongodb)
        # indexes
        # self.collection.create_index([('version_id', ASCENDING)], unique=False)
        self.collection.create_index([('ip', ASCENDING)], unique=True)
        self.collection.create_index([('hostname', ASCENDING)], unique=True)

    def get_system_details_single(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns the database entities existing for SystemDetails.
        Example :
            get_system_details_single()
        '''
        sys_details=self.collection.find_one()
        sys_details["allow_new_tools"]=False
        proposed_tool_support_email=self.configDb.getConfigByName("ProposedToolService")
        if proposed_tool_support_email and proposed_tool_support_email.get("enable","false") == "true":
            sys_details["allow_new_tools"]=True
        return  sys_details
            

    def add_system_details(self, new_environment):
        '''
        General description:

        Args:
            param1 : new_environment(JSON) : This is the parameter which has details \
            for new environment .
        Returns:
              Returns the id of the newly created SystemDetails the database.
        Example :
             add_system_details(new_environment)
        '''
        result = self.collection.insert_one(new_environment)
        return str(result.inserted_id)

    def update_system_details(self, machine):
        '''
        General description:

        Args:
            param1 : machine(JSON) : This is the parameter which has details of machine.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_system_details(machine)
        '''
        json_new_entry = {}
        for key in machine.keys():
            if key != "_id":
                json_new_entry[key] = machine[key]
        result = self.collection.update_one({"_id": ObjectId(machine["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count
