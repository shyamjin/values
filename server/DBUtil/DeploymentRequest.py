from datetime import datetime
import json
from bson.objectid import ObjectId
from pymongo import DESCENDING
from DBUtil import DBUtil
import Machine
from Services import PasswordHelper
import Tool ,State
import Versions
from settings import key


class DeploymentRequest(DBUtil):
    '''
        General description:

       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for  DeploymentRequest.
    '''

    def __init__(self, db):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.DeploymentRequest
        self.machineDB = Machine.Machine(db)
        self.versionsDB = Versions.Versions(db)
        self.toolDB = Tool.Tool(db)
        self.passHelper = PasswordHelper.PasswordHelper(key)
        self.statedb =  State.State(db)
        # indexes
        # self.collection.create_index([('catalog_name', ASCENDING)])

    def get_dp_req_dts(self, deploymentDetails):
        '''
        General description:
        Args:
            param1 : deploymentDetails(JSON) : This is the parameter which has details like \
            password /input_value .
        Returns:
                Returns Database entity by the deploymentDetails \
                of the DeploymentRequest.
        '''
        if deploymentDetails.get("tool_deployment_value") and len(deploymentDetails.get("tool_deployment_value")) > 0:
            tool_deployment_value = []
            for data in deploymentDetails["tool_deployment_value"]:
                if "input_type" in data.keys() and str(data["input_type"]) in ["password"]:
                    data["input_value"] = self.passHelper.decrypt(
                        data["input_value"])
                tool_deployment_value.append(data)
            deploymentDetails["tool_deployment_value"] = tool_deployment_value
        if deploymentDetails.get("state_id"):   
            deploymentDetails["state"]=self.statedb.get_state_by_id(deploymentDetails.get("state_id"), False)  
        else:
            deploymentDetails["state"]=None      
        return deploymentDetails

    def set_dp_req_dts(self, deploymentDetails):
        '''
        General description:
        Args:
            param1 deploymentDetails(JSON) : This is the JSON object which has details like \
            password /input_value  .
        Returns:
                Returns Database entity by the deploymentDetails\
                of the DeploymentRequest.

        '''
        if deploymentDetails.get("tool_deployment_value") and len(deploymentDetails.get("tool_deployment_value")) > 0:
            tool_deployment_value = []
            for data in deploymentDetails["tool_deployment_value"]:
                keys_to_check = ["input_name", "input_type", "input_value"]
                keys_whose_value_cannot_empty = ["input_name", "input_type"]
                for key in keys_to_check:
                    if key not in data.keys():
                        raise ValueError(
                            "Deployment field key: " + key + " was not found for:" + data.get("input_name"))
                    if key in keys_whose_value_cannot_empty and not data.get(key):
                        raise ValueError("Deployment field key: " + key +
                                         " cannot have empty value")
                if "input_type" in data.keys() and str(data["input_type"]) in ["password"]:
                    data["input_value"] = self.passHelper.encrypt(
                        data["input_value"])
                tool_deployment_value.append(data)
            deploymentDetails["tool_deployment_value"] = tool_deployment_value
        return deploymentDetails

    def GetDeploymentRequestAll(self, filter_required={}, skip=0, limit=0):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities of all the existing DeploymentRequest
        Example :
             GetDeploymentRequestAll(id)
        '''
        if filter_required or filter_required=={}:
            count = self.collection.find(filter_required).sort(
                    [['_id', DESCENDING]]).skip(skip).limit(limit).count()
            if count < 1:
                skip = 0
            return self.collection.find(filter_required).sort([['_id', DESCENDING]]).skip(skip).limit(limit)
        else:
            count = self.collection.find().sort(
                [['_id', DESCENDING]]).skip(skip).limit(limit).count()
            if count < 1:
                skip = 0
            return self.collection.find().sort([['_id', DESCENDING]]).skip(skip).limit(limit)

    def GetDeploymentRequest(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            DeploymentRequest stored in the database.
        Returns:
                Returns Database entity by the id of the DeploymentRequest.
        Example :
             GetDeploymentRequest(id)
        '''
        result = self.collection.find_one({"_id": ObjectId(object_id)})
        if not result:
            return result
        else:
            return self.get_dp_req_dts(result)

    def AddDeploymentRequest(self, newDeploymentRequest):
        '''
        General description:
        Args:
            param1 (DeploymentRequest) : This is the parameter which has the details of the\
            DeploymentRequest to be added in the database.
        Returns:
                Returns the id of the newly created DeploymentRequest from the database.
        Example :
             AddDeploymentRequest(DeploymentRequest)
        '''
        newDeploymentRequest["status"] = "New"
        newDeploymentRequest["retry_count"] = 0
        newDeploymentRequest["status_message"] = "The request is accepted"
        newDeploymentRequest["logs"] = []
        newDeploymentRequest["current_step_id"] = 0
        newDeploymentRequest["create_date"] = datetime.now()
        newDeploymentRequest["update_date"] = datetime.now()
        try:
            # fix by Surendra
            if newDeploymentRequest.get("scheduled_date"):
                newDeploymentRequest["scheduled_date"] = datetime.strptime(
                    str(newDeploymentRequest.get("scheduled_date")).split(".")[0].replace("T"," "), "%Y-%m-%d %H:%M:%S")
            else:
                newDeploymentRequest["scheduled_date"] = datetime.now()
        except Exception as e:
            raise Exception("Given scheduled_date is invalid")
        newDeploymentRequest = self.set_dp_req_dts(newDeploymentRequest)
        result = self.collection.insert_one(newDeploymentRequest)
        return str(result.inserted_id)

    def UpdateDeploymentRequest(self, deployment_request):
        '''
        General description:
        Args:
            param1 (deployment_request) : This is the parameter which has the details of the\
            deployment_request to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the deployment_request
        Example :
             UpdateDeploymentRequest(deployment_request)
        '''
        jsonnewEntry = {}
        for key in deployment_request.keys():
            if key != "_id":
                jsonnewEntry[key] = deployment_request[key]
        jsonnewEntry["update_date"] = datetime.now()
        jsonnewEntry = self.set_dp_req_dts(jsonnewEntry)
        result = self.collection.update_one({"_id": ObjectId(
            deployment_request["_id"]["oid"])}, {"$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def UpdateDeploymentRequestStatus(self, object_id, status, message):
        '''
        General description:
        Args:
            param1 (deployment_request) : This is the parameter which has the details of the\
            deployment_request to be updated in the database.
            param2( status):This is the parameter which is given the status of the deployment_request.
            param3(  message):This is the parameter which is given the  message.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the deployment_request
        Example :
             UpdateDeploymentRequestStatus(bject_id, status, message)
        '''
        jsonEntry = {}
        jsonEntry["status"] = status
        jsonEntry["status_message"] = message
        jsonEntry["update_date"] = datetime.now()
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": jsonEntry}, upsert=False)
        return result.modified_count

    def UpdateDeploymentRequestTime(self, object_id, type):
        '''
        General description:
        Args:
             param1 (object_id) : This is the unique id of the\
            DeploymentRequest stored in the database.
            param2(  type):This is the parameter which is given the  type of DeploymentRequest.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the deployment_request
        Example :
             UpdateDeploymentRequestStatus(bject_id, type)
        '''
        jsonEntry = {}
        jsonEntry[type] = datetime.now()
        jsonEntry["update_date"] = datetime.now()
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": jsonEntry}, upsert=False)
        return result.modified_count

    def CancelDeploymentRequest(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            DeploymentRequest stored in the database.
        Returns:
                Returns Cancel Database entity by the id of the DeploymentRequest.
        Example :
             CancelDeploymentRequest(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

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
        set_node = 'step_details.$.'
        data = {}
        for attr in kwargs:
            kwargsValue = str(kwargs[attr])
            kwargsValue = kwargsValue.replace("'", "")
            kwargsValue = kwargsValue.replace('"', "")
            data[set_node + attr] = kwargsValue
        result = self.collection.update_one({"_id": ObjectId(object_id), "step_details.step_id": str(
            step_id)}, {"$set": data}, upsert=False)
        return result.modified_count

    def UpdateRequestDetails(self, object_id, **kwargs):
        '''
        General description:
        Args:
        param1 (object_id) : This is the unique id of the existing \
            Request stored in the database.

        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the Request.
        Example :
             UpdateRequestDetails(id,step_id,kwargs)
        '''
        data = {}
        for attr in kwargs:
            kwargsValue = str(kwargs[attr])
            kwargsValue = kwargsValue.replace("'", "")
            kwargsValue = kwargsValue.replace('"', "")
            data[attr] = kwargsValue
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": data}, upsert=False)
        return result.modified_count

    def UpdateNestedStepDetails(self, object_id, step_id, nested_current_step_id, **kwargs):
        '''
        General description:
        Args:
        param1 (object_id) : This is the unique id of the existing \
            Request stored in the database.
            param2 (step_id) : This is the step id of the existing \
            Request stored in the database.
             param2 (nested_current_step_id) : This is the current step id of the existing \
            Request stored in the database.
            param3 (kwargs) : This is the parameter which has the details of the\
            kwargs to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the Request.
        Example :
             UpdateRequestDetails(id,step_id,kwargs)
        '''
        set_node = 'step_details.$.nested_step_details.' + \
            str(nested_current_step_id) + '.'
        data = {}
        for attr in kwargs:
            kwargsValue = str(kwargs[attr])
            kwargsValue = kwargsValue.replace("'", "")
            kwargsValue = kwargsValue.replace('"', "")
            data[set_node + attr] = kwargsValue
        result = self.collection.update_one({"_id": ObjectId(
            object_id), "step_details.step_id": str(step_id)}, {"$set": data}, upsert=False)
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

    def StepDetailsCount(self, object_id):
        '''
          General description:
        Args:
        param1 (object_id) : This is the unique id of the existing \
            Request stored in the database.

        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the Request.
        Example :
             StepDetailsCount(id)
        '''
        # find a better way to get length of step_details[]
        return self.collection.find_one({"_id": ObjectId(object_id)}).step_details.length

    def addDeploymentSteps(self, object_id, steps):
        '''
        General description:
        Args: param1 (object_id) : This is the unique id of the existing \
            Request stored in the database.

            param2 (steps) : This is the parameter which has the details of
           steps to be added in database.
        Returns:
                Returns Database entity id of the new DeploymentSteps
        Example :
             addDeploymentSteps(object_id,steps)
        '''
        self.collection.update({"_id": ObjectId(object_id)}, {'$push': {'step_details': {'$each': steps}}}
                               )
    def getRandomDepReqForUnitTest(self):
        return self.collection.find_one({})