from datetime import datetime
import json
import re

from bson.objectid import ObjectId
from pymongo import DESCENDING

from DBUtil import DBUtil


class CloneRequest(DBUtil):
    '''
        General description:

       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for CloneRequest.
    '''

    def __init__(self, db):
        '''
           General description:
           This function initializes the database variables and \
           index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.CloneRequest
        # indexes
        # self.collection.create_index([('catalog_name', ASCENDING)])

    def GetCloneRequestAll(self):
        '''
        General description:
        Args:
           no args
        Returns:
                Returns all Database entity by the id of the CloneRequest.
        Example :
             GetCloneRequestAll()
        '''
        return self.collection.find().sort([['_id', DESCENDING]])

    def GetCloneRequest(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            CloneRequest stored in the database.
        Returns:
                Returns Database entity by the id of theCloneRequest
        Example :
             GetCloneRequest(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def GetCloneRequestbymachineandtype(self, machine_id, type):
        '''
        General description:
        Args:
            param1 (machine_id) : This is the machine id of the\
            CloneRequest stored in the database.
            param1 (type) : This is the type of the\
            CloneRequest stored in the database.
        Returns:
                Returns type and machine_id of theCloneRequest
        Example :
             GetCloneRequestbymachineandtype(machine_id, type)
        '''
        return self.collection.find_one({"machine_id": machine_id, "type": type})

    def AddCloneRequest(self, newCloneRequest, request_type="clone"):
        '''
        General description:
        Args:
            param1 (newCloneRequest) : This is the parameter which has the details for \
            the new CloneRequest to be added in database.
             param2  type(string) :This is the parameter which determines \
            type

        Returns:
                Returns Database entity id of the new CloneRequest created
        Example :
             AddCloneRequest(newCloneRequest,None)
        '''
        newCloneRequest["status"] = "New"
        newCloneRequest["type"] = request_type
        newCloneRequest["status_message"] = "The clone request is accepted"
        newCloneRequest["create_date"] = datetime.now()
        newCloneRequest["current_step_id"] = 0
        newCloneRequest["execution_count"] = 0
        newCloneRequest["retry_count"] = 0
        newCloneRequest["step_details"] = ""
        newCloneRequest["logs"] = []
        result = self.collection.insert_one(newCloneRequest)
        return str(result.inserted_id)

    def UpdateCloneRequest(self, deployment_request):
        '''
        General description:
        Args:
            param1 (deployment_request) : This is the deployment_request details of the existing CloneRequest \
         which we have to update.Its a JSON object.
        Returns:
                Returns the count of records that has been updated \
                successfully for a given CloneRequest .
        Example :
             uUpdateCloneRequest(deployment_request)
        '''
        jsonnewEntry = {}
        for key in deployment_request.keys():
            if key != "_id":
                jsonnewEntry[key] = deployment_request[key]
        result = self.collection.update_one({"_id": ObjectId(
            deployment_request["_id"]["oid"])}, {"$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def UpdateRequestDetails(self, object_id, **kwargs):
        '''
        General description:
        Args:
        param1 (object_id) : This is the unique id of the existing \
            Request stored in the database.
            param2 (kwargs) : This is the parameter which has the details of the\
            kwargs to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the Request.
        Example :
             UpdateRequestDetails(id,kwargs)
        '''
        data = ""
        jsonnewEntry = {}
        for key in kwargs.keys():
            if key != "_id":
                jsonnewEntry[key] = kwargs[key]
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def UpdateStepDetails(self, object_id, step_id, **kwargs):
        '''
        General description:
        Args:
        param1 (object_id) : This is the unique id of the existing \
            Request stored in the database.
            param2 (step_id) : This is the step id of the existing \
            Request stored in the database.
            param3 (kwargs) : This is the parameter which has the details of the\
            kwargs to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the Request.
        Example :
             UpdateRequestDetails(id,step_id,kwargs)
        '''
        set_node = '"step_details.$.'
        data = ""
        for attr in kwargs:
            kwargsValue = str(kwargs[attr])
            kwargsValue = kwargsValue.replace("'", "")
            kwargsValue = kwargsValue.replace('"', "")
            data = data + set_node + attr + '":"' + kwargsValue + '",'
        data = '{' + data[:-1] + '}'
        result = self.collection.update_one({"_id": ObjectId(object_id), "step_details.step_id": str(
            step_id)}, {"$set": json.loads(data, strict=False)}, upsert=False)
        return result.modified_count

    def updateToolList(self, object_id, version_id, **kwargs):
        '''
        General description:
        Args:
        param1 (object_id) : This is the unique id of the existing \
            Request stored in the database.
            param2 (version_id) : This is the version id of the existing \
            Request stored in the database.
            param3 (kwargs) : This is the parameter which has the details of the\
            kwargs to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the Request.
        Example :
             UpdateRequestDetails(id,version_id,kwargs)
        '''
        set_node = '"tool_list.$.'
        data = ""
        for attr in kwargs:
            kwargsValue = str(kwargs[attr])
            kwargsValue = kwargsValue.replace("'", "")
            kwargsValue = kwargsValue.replace('"', "")
            data = data + set_node + attr + '":"' + kwargsValue + '",'
        data = '{' + data[:-1] + '}'
        result = self.collection.update_one({"_id": ObjectId(object_id), "tool_list.version_id": str(
            version_id)}, {"$set": json.loads(data, strict=False)}, upsert=False)
        return result.modified_count

    def UpdateToolStepDetails(self, object_id, step_id, version_id, tool_step_id, **kwargs):
        '''
        General description:
        Args:
        param1 (object_id) : This is the unique id of the existing \
            Request stored in the database.
             param2 (step_id) : This is the step id of the existing \
            Request stored in the database.
            param3 (version_id) : This is the version id of the existing \
            Request stored in the database.
            param3 (kwargs) : This is the parameter which has the details of the\
            kwargs to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the Request.
        Example :
             UpdateRequestDetails(id,step_id,version_id,kwargs)
        '''
        set_node = '"step_details.$.tool_step_details.' + \
            str(version_id) + '.' + str(tool_step_id) + '.'
        data = ""
        for attr in kwargs:
            kwargsValue = str(kwargs[attr])
            kwargsValue = kwargsValue.replace("'", "")
            kwargsValue = kwargsValue.replace('"', "")
            data = data + set_node + attr + '":"' + kwargsValue + '",'
        data = '{' + data[:-1] + '}'
        result = self.collection.update_one({"_id": ObjectId(object_id), "step_details.step_id": str(
            step_id)}, {"$set": json.loads(data, strict=False)}, upsert=False)
        return result.modified_count

    def InitStatusDetails(self, object_id, step_details):
        '''
           General description:
        Args:
        param1 (object_id) : This is the unique id of the existing \
            Request stored in the database.
        param2  step_details(string):this parameter has a details of steps.   
          Returns: This function initializes the object_id and 
           step_details
        '''
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": json.loads(step_details)}, upsert=False)
        return result.modified_count

    def CancelCloneRequest(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the ID of the existing \
            CloneRequest which we have to Cancel.
        Returns:
                Returns the count of records that has been Canceled \
                successfully for a given CloneRequest.
        Example :
             delete_machine_groups(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def GetNewPendingCloneRequests(self):
        '''
        General description:
        Args:
           No args
        Returns:
                Returns Database entity of CloneRequests .
        Example :
            GetNewPendingCloneRequests(id)
        '''
        return self.collection.find({"status": {"$in": [re.compile("new", re.IGNORECASE), re.compile("Retry", re.IGNORECASE)]}, "type": {"$in": [re.compile("Clone", re.IGNORECASE), re.compile("ImportTool", re.IGNORECASE), re.compile("UpdateTool", re.IGNORECASE)]}})

    def GetCloneRequestsByMachineId(self, machine_id):
        '''
        General description:
        Args:
            param1 (machine_id) : This is the Machine Id which is stored in database
        Returns:
                Returns Database entity of CloneRequest for the given Machine  Id
        Example :
            GetCloneRequestsByMachineId(id)
        '''
        return self.collection.find({"machine_id": machine_id})

    def clone_order(self, json):
        '''
        General description:
        Args:
            param1:json
        Returns:deployement order converted to int type

        '''
        """
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2"."""
        try:
            return int(json['clone_order'])
        except KeyError:
            return 0
