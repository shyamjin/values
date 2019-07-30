'''
Created on Aug 4, 2016

@author: pdinda
'''
from datetime import datetime
import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class DistributionMachine(DBUtil):
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
        self.collection = db.DistributionMachine
        # indexes
        self.collection.create_index([('machine_id', ASCENDING)], unique=True)

    def GetDistributionMachineAll(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns all Database entities of all the existing DistributionMachine
        Example :
             GetDistributionMachineAll(id)
        '''
        return self.collection.find()

    def GetDistributionMachineRequest(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            DistributionMachine stored in the database.
        Returns:
                Returns Database entity by the id of the DistributionMachine.
        Example :
             GetDistributionMachineRequest(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def GetDistributionMachineRequestByMachineId(self, machine_id):
        '''
        General description:
        Args:
            param1 (machine_id) : This is the unique id of the\
            DistributionMachine stored in the database.
        Returns:
                Returns Database entity by the id of the DistributionMachine.
        Example :
             GetDistributionMachineRequestByMachineId(machine_id)
        '''
        return self.collection.find_one({"machine_id": machine_id})

    def GetDistributionMachineRequestByHost(self, host):
        '''
        General description:
        Args:
            param1 (host) : This is the host of the\
            DistributionMachine stored in the database.
        Returns:
                Returns Database entity of the DistributionMachine.
        Example :
             GetDistributionMachineRequestByHost(host)
        '''
        return self.collection.find({"host": re.compile(host, re.IGNORECASE)})

    def AddDistributionMachineRequests(self, newCloneRequest):
        '''
        General description:
        Args:
            param1 (newCloneRequest) : This is the parameter which has the details of the\
            DistributionMachine to be added in the database.
        Returns:
                Returns the id of the newly created DistributionMachine from the database.
        Example :
             AddDistributionMachineRequests(newCloneRequest)
        '''
        newCloneRequest["create_date"] = datetime.now()
        newCloneRequest["update_date"] = datetime.now()
        result = self.collection.insert_one(newCloneRequest)
        return str(result.inserted_id)

    def UpdateDistributionMachineRequest(self, deployment_request):
        '''
        General description:
        Args:
            param1 (deployment_request) : This is the parameter which has the details of the\
            DistributionMachine to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the DistributionMachine.
        Example :
             UpdateDistributionMachineRequest(deployment_request)
        '''
        jsonnewEntry = {}
        for key in deployment_request.keys():
            if key != "_id":
                jsonnewEntry[key] = deployment_request[key]
        result = self.collection.update_one({"_id": ObjectId(
            deployment_request["_id"]["oid"])}, {"$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def GetAllDistributionMachineRequests(self, status=None, object_id=None):
        '''
        General description:
        Args:param1 (status) : This is the parameter of the\
            DistributionMachine stored in the database which give the status of DistributionMachine.
            param2 (object_id) : This is the unique id of the\
            DistributionMachine stored in the database.
        Returns:
                Returns Database entity by the id and status of the DistributionMachine.
        Example :
             GetAllDistributionMachineRequests(id,none)
        '''
        if status and object_id:
            return self.collection.find({"_id": ObjectId(object_id), "status": re.compile(status, re.IGNORECASE)})
        elif status:
            return self.collection.find({"status": re.compile(status, re.IGNORECASE)})
        elif object_id:
            self.GetDistributionMachineRequest(str(object_id))
        else:
            return self.collection.find()

    def CancelDistributionMachineRequests(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            DistributionMachine stored in the database.
        Returns:
                Returns the count of the records cancled successfully\
                for the given id of the DistributionMachine
        Example :
             CancelDistributionMachineRequests(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def update_hostname(self, machine_id, hostname):
        result = self.collection.update_many({"machine_id": machine_id}, {
                                             "$set": {"host": hostname}}, upsert=False)
        return result.modified_count

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
