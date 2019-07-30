from datetime import datetime
import re
from concurrent.futures import ThreadPoolExecutor,wait
from bson.objectid import ObjectId
from pymongo import DESCENDING
from DBUtil import DBUtil
import DeploymentRequest
import Machine
import Versions
import Tool
import DeploymentUnit
import State



class DeploymentRequestGroup(DBUtil):
    '''                                                                                   
      General description:                                                              

     This class has definition for functions that provides add /update/ delete \        
     / search by entities in database for DeploymentRequestGroup.                       
    '''

    def __init__(self, db):
        '''                                                                    
         General description :                                               
         This function initializes the database variables and \              
         index to refer in functions.                                        
        '''
        DBUtil.__init__(self, db)
        self.collection = db.DeploymentRequestGroup
        self.deploymentRequestDb = DeploymentRequest.DeploymentRequest(db)
        self.machineDB = Machine.Machine(db)
        self.versionsDB = Versions.Versions(db)
        self.toolDB = Tool.Tool(db)
        self.deploymentUnitDB = DeploymentUnit.DeploymentUnit()
        self.deploymentRequestDbCollection = db.DeploymentRequest
        self.statedb = State.State(db)
        # indexes
        # self.collection.create_index([('catalog_name', ASCENDING)])

    def get_dep_req_details(self, rec, add_dep_data=False):
        '''
        General description:
        Args:
            param1 (rec) : This is the unique id of the \
            DeploymentRequest  unit stored in the database.
            add_dep_data(string) :This is the parameter which determines \
            whether all DeploymentRequest add_dep_data should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns Database entity by the parent_entity_id of the DeploymentRequest.
        Example :
             get_dep_req_details(parent_entity_id,False)
        '''
        requested_deployment_ids_data = []
        futures = []
        details = []
        pool = ThreadPoolExecutor(4,__name__+".get_dep_req_details")        
        for depRec in rec.get("details"):futures.append(pool.submit(self.get_details,depRec))
        wait(futures)
        for future in futures: # CHECK EXCEPTIONS
            if future.exception(): 
                raise future.exception()
            else: 
                depRec,dep_data = future.result()
                details.append(depRec)
                if add_dep_data:requested_deployment_ids_data.append(dep_data)
        if add_dep_data:rec["requested_deployment_ids_data"] = requested_deployment_ids_data
        rec["details"] = details
        return rec
    
    
    def get_details(self,depRec):
        dep_data = self.deploymentRequestDb.GetDeploymentRequest(
                str(depRec.get("deployment_id")))
        if dep_data:
            if "logs" in dep_data.keys():dep_data.pop("logs")
            depRec["build_id"] = dep_data.get("build_id")
            depRec["build_number"] = dep_data.get("build_number")
            if dep_data.get("machine_id"):
                machineData = self.machineDB.GetMachine(dep_data["machine_id"])
                if machineData and machineData.get("machine_name"):
                    depRec["machine_name"] = machineData["machine_name"]
                    dep_data["machine_name"] = machineData["machine_name"]
            if dep_data.get("parent_entity_id"):
                version_data = self.versionsDB.get_version(dep_data.get("parent_entity_id"), False)
                if version_data:
                    if version_data.get("version_name"):
                        depRec["version_name"] = version_data["version_name"]
                        dep_data["version_name"] = version_data["version_name"]
                    if version_data.get("version_number"):
                        depRec["version_number"] = version_data["version_number"]
                        dep_data["version_number"] = version_data["version_number"]
                    if version_data.get("tool_id"):
                        toolData = self.toolDB.get_tool_by_id(
                            version_data.get("tool_id"), False)
                        if toolData:
                            depRec["parent_entity_id"] = str(toolData["_id"])
                            if toolData.get("name"):
                                depRec["parent_entity_name"] = toolData["name"]
                                dep_data["parent_entity_name"] = toolData["name"]
                else:                
                    du_data = self.deploymentUnitDB.GetDeploymentUnitById(
                        dep_data["parent_entity_id"], False)
                    if du_data:
                        depRec["parent_entity_id"] = str(du_data["_id"])
                        depRec["parent_entity_name"] = du_data["name"]
                        dep_data["parent_entity_name"] = du_data["name"]
            if dep_data.get("state_id"):
                state = self.statedb.get_state_by_id(dep_data.get("state_id"), False)
                if state: depRec["state"] = state                                      
                            
        return  depRec,dep_data        

    def get_all_group_deployment_request(self, filter_condition,exclude_key_list, parent_entity_id_list, isAllDetails, skip=0, limit=0):
        '''
        General description:

        Args:

            param1: get_all_details(string) :This is the parameter which determines \
            whether all DeploymentRequest should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the DeploymentRequest and\
                is_all_details parameter.
        Example :
            get_all_group_deployment_request(id ,True)
        '''
        result = self.collection.find({"$and" : [{"status": {"$nin": [re.compile(
            "Saved", re.IGNORECASE)]}}, filter_condition]},exclude_key_list).skip(skip).limit(limit).sort([['_id', DESCENDING]])

        deployment_groups_data = []
        for rec in result:  # ALL DEPLOYMENT GROUPS HERE
            if len(parent_entity_id_list)>0:
                for dep_id in rec.get("details"):                                     
                    deployment_id = dep_id.get("deployment_id")
                    data = self.deploymentRequestDbCollection.find_one({"$and" : [
                        {"_id" : ObjectId(deployment_id)},
                        {"parent_entity_id" : {"$in" : parent_entity_id_list}}
                        ]
                    })
                    if data is not None:
                        deployment_groups_data.append(rec)
            else:
                deployment_groups_data.append(rec)
        return deployment_groups_data

    def get_all_saved_group_deployment_request(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities of all the all_saved_group_deployment_request
        Example :
             get_all_saved_group_deployment_request(id)
        '''
        return self.collection.find({"status": {"$in": [re.compile("Saved", re.IGNORECASE)]}}).sort([['_id', DESCENDING]])

    def get_group_deployment_request(self, object_id, isAllDetails = False ,add_dep_data = False):
        '''
        General description:

        Args:
             param1 (object_id) : This is the unique id of the\
            DeploymentRequest stored in the database.

            param2: get_all_details(string) :This is the parameter which determines \
            whether all DeploymentRequest should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the DeploymentRequest and\
                is_all_details parameter.
        Example :
            get_group_deployment_request(id ,True)
        '''

        result = self.collection.find_one({"_id": ObjectId(str(object_id))})
        if isAllDetails and result is not None:
            result = self.get_dep_req_details(result, add_dep_data)
        return result

    def get_grp_depreq_by_inner_depreq_ids(self, object_id,is_completed=False):
        '''
        General description:

        Args:
             param1 (object_id) : This is the unique id of the\
            DeploymentRequest stored in the database.


        Returns:
                Returns the database entity based on the DeploymentRequest.

        Example :
            get_grp_depreq_by_inner_depreq_ids(object_id ,True)
        '''
        if is_completed:
            return self.collection.find_one({"status":re.compile("done", re.IGNORECASE),\
                                             "details.deployment_id": {"$in": [str(object_id)]}}) 
        return self.collection.find_one({"details.deployment_id": {"$in": [str(object_id)]}})

    def get_pending_grp_depreq(self):
        '''
        General description:

        Args:
            no args

        Returns:
                Returns the database entity based on the DeploymentRequest.

        Example :
            get_pending_grp_depreq(id)
        '''
        return self.collection.aggregate([{"$match": {"status": {"$in": [re.compile("New", re.IGNORECASE), re.compile("Retry", re.IGNORECASE), re.compile("Processing", re.IGNORECASE)]}, "$or": [{"scheduled_date": {"$lte": datetime.now()}}, {"scheduled_date": None}, {"scheduled_date": {"$exists": False}}]}}, {"$group": {"_id": "$requested_by", "object_id": {"$min": "$_id"}}}])

    def add_new_grp_depreq(self, new_group_deployment_request):
        '''
        General description:
        Args:
            param1 (new_group_deployment_request) : This is the parameter which has the details of the\
            newGroupDeploymentRequest to be added in the database.
        Returns:
                Returns the id of the newly created DeploymentRequest from the database.
        Example :
             add_new_grp_depreq(new_group_deployment_request)
        '''
        new_group_deployment_request["status"] = "New"
        new_group_deployment_request["status_message"] = "The request is accepted"
        new_group_deployment_request["retry_count"] = 0
        try:
            # fix by Surendra
            if new_group_deployment_request.get("scheduled_date"):
                new_group_deployment_request["scheduled_date"] = datetime.strptime(
                    str(new_group_deployment_request.get("scheduled_date")).split(".")[0].replace("T"," "), "%Y-%m-%d %H:%M:%S")
            else:
                new_group_deployment_request["scheduled_date"] = datetime.now()
        except Exception as e:
            raise Exception("Given scheduled_date is invalid")
        return self.add_request(new_group_deployment_request)

    def add_request(self, new_group_deployment_request):
        '''
        General description:
        Args:
            param1 (new_group_deployment_request) : This is the parameter which has the details of the\
          DeploymentRequest to be added in the database.
        Returns:
                Returns the id of the newly created DeploymentRequest from the database.
        Example :
            add_request(new_group_deployment_request)
        '''
        new_group_deployment_request["create_date"] = datetime.now()
        new_group_deployment_request["update_date"] = datetime.now()
        result = self.collection.insert_one(new_group_deployment_request)
        return str(result.inserted_id)

    def upd_group_depreq(self, deployment_request):
        '''
        General description:
        Args:
            param1 (deployment_request) : This is the parameter which has the details of the\
            deployment_request to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the deployment_request.
        Example :
             upd_group_depreq(deployment_request)
        '''
        jsonnewEntry = {}
        for key in deployment_request.keys():
            if key != "_id":
                jsonnewEntry[key] = deployment_request[key]
        jsonnewEntry["update_date"] = datetime.now()
        result = self.collection.update_one({"_id": ObjectId(
            deployment_request["_id"]["oid"])}, {"$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def upd_group_depreq_sts(self, object_id, status, message):
        '''
        General description:
        Args:
        param1 (object_id) : This is the unique id of the\
            DeploymentRequest stored in the database.

             param2: status(string) :This is the parameter which determines \
            whether all DeploymentRequest should be visible to user or not.\
            This has two values - True /False .
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the deployment_request.
        Example :
             upd_group_depreq_sts(deployment_request,true)
        '''
        jsonEntry = {}
        jsonEntry["status"] = status
        jsonEntry["status_message"] = message
        jsonEntry["update_date"] = datetime.now()
        self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": jsonEntry}, upsert=False)

    def cancel_grpdep_req(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            DeploymentRequest stored in the database.
        Returns:
                Returns the count of the records Canceled successfully\
                for the given id of the DeploymentRequest.
        Example :
             cancel_grpdep_req(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count
    
    def get_all_group_depreq_count(self):
        '''
        General description:        
        Returns:
                Returns the count of all non saved records in DeploymentRequestGroup                
        Example :
             GetAllGroupDeploymentRequestCount()
        '''
        result = self.collection.find({"$and" : [{"status": {"$nin": [re.compile("Saved", re.IGNORECASE)]}}]}).sort([['_id', DESCENDING]])
        count=0;
        for rec in result:
            count=count+1;
        return count
    
    def get_all_group_deployment_request_by_condition(self, filter_condition,limit=None):
        '''
        General description:
        Args:

            param1: filter_condition(json) :Condition to filter
            This has two values - True /False .
        Returns:
                Returns the database entity based on the filter_condition 
        Example :
            get_all_group_deployment_request_by_condition(id ,filter_condition)
        '''
        if limit:
            return self.collection.find(filter_condition).sort([['_id', DESCENDING]]).limit(limit)
        else:
            return self.collection.find(filter_condition).sort([['_id', DESCENDING]])
            
