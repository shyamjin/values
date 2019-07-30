'''
#########################################################################################
STRUCTURE OF DEPLOYMENT SET for GUI : WE WILL RECEIVE AND SEND DATA IN THIS FORMAT TO GUI
#########################################################################################

{
    "name": "Test Du",
    "id": "ads8978asd",
    "du_set": [
        {
            "du_id": "575807a5f37d66d77783b2a3",
            "dependent": "false",
            "order": "1"
        },
        {
            "du_id": "5779f5b4f37d669f1e1501fe",
            "dependent": "true",
            "order": "2"
        }
    ],
    "pre_requiests": [
        {
            "version": "1.7",
            "name": "java"
        },
        {
            "version": "2.6",
            "name": "python"
        }
    ],
    "tag": [
         "Hello",
         "Hi"
    ],
    "size": "15 mb",
    "release_notes": "This is a test version"
    
}

#########################################################################################
STRUCTURE OF DEPLOYMENT SET in server : WE WILL SAVE DATA IN MONGO IN THIS FORMAT
#########################################################################################

{
    "name": "Test Du",
    "id": "ads8978asd",
    "du_set": [
        {
            "du_id": "575807a5f37d66d77783b2a3",
            "dependent": "false",
            "order": "1"
        },
        {
            "du_id": "5779f5b4f37d669f1e1501fe",
            "dependent": "true",
            "order": "2"
        }
    ],
    "pre_requiests": [
        {
            "version": "1.7",
            "name": "java"
        },
        {
            "version": "2.6",
            "name": "python"
        }
    ],
    "tag": [
        "58738ed17fe7b979008b26e7",
        "5874d60b63d0c00050b8fff0"
    ],
    "size": "15 mb",
    "release_notes": "This is a test version"
    
}


'''

import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
import DeploymentUnit,Build,DeploymentUnitType,DeploymentFields,DeploymentUnitApprovalStatus,Tags,State
from settings import mongodb

class DeploymentUnitSet(DBUtil):
    '''
        General description:

       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for PermissionGroup.
    '''
    
    def __init__(self):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''

        db = mongodb
        DBUtil.__init__(self, db)
        self.collection = db.DeploymentUnitSet
        self.DeploymentUnitDB = DeploymentUnit.DeploymentUnit()
        self.tagDB = Tags.Tags()
        self.deploymentUnitApprovalStatusDB = DeploymentUnitApprovalStatus.DeploymentUnitApprovalStatus()
        self.statedb=State.State(db)
        self.buildDB = Build.Build()
        self.deploymentUnitTypeDB = DeploymentUnitType.DeploymentUnitType()
        
        # indexes
        
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def GetAllDuSetIds(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns list of all du set ids.
        Example :
            get_tag_ids()
        '''
        dusets = self.collection.find()
        duset_ids_list = []
        for duset in dusets:
            duset_ids_list.append(str(duset["_id"]))
        return duset_ids_list

    def getMandatoryDetails(self, record):
        '''
        General description:
        Args:
            param1 (record) : This is the parameter which has details of\
           DeploymentUnitApprovalStatus
        Returns:
                Returns Database entity by the record of the DeploymentUnitApprovalStatus.
        Example :
             getMandatoryDetails(record)
        '''
        if record:
            if record.get("tag"):
                record["tag"] = self.tagDB.get_tag_names_from_given_ids_list(
                    record["tag"])
            if record.get("type"):
                record["type"] = self.deploymentUnitTypeDB.GetDeploymentUnitTypeById(record["type"])[
                    "name"]

        return record

    def GetDeploymentUnitSetDetails(self, record,only_build_number=False):
        '''
        General description:
        Args:
            param1 (record) : This is the parameter which has details of\
           DeploymentUnitApprovalStatus
        Returns:
                Returns Database entity by the record of the DeploymentUnitApprovalStatus.
        Example :
             GetDeploymentUnitSetDetails(record)
        '''
        if record:
            if record.get("du_set"):
                du_details = []
                for rec in record.get("du_set"):
                    du = self.DeploymentUnitDB.GetDeploymentUnitById(
                        str(rec.get("du_id")), True,only_build_number)
                    du["dependent"] = rec.get("dependent")
                    du["order"] = rec.get("order")
                    du_details.append(du)
                record["du_set_details"] = du_details
            state=self.statedb.get_state_by_parent_entity_id(record.get("_id"), True,only_build_number)
            record["state"]=state
        return record
    
    
    def GetAllDeploymentUnitSet(self,isAllDetails=False, filter_required=None, skip=0, limit=0):
        '''
        General description:
        Args:
             param1 : get_all_details(string) :This is the parameter which determines \
            whether all DeploymentUnitSet details should be visible to user or not.\
            This has two values - True /False .
            param2 : filter_required(string) :This is the parameter which determines \
            whether filter_required to user or not.

        Returns:
                Returns Database entity based on filter_required of the DeploymentUnitApprovalStatus.
        Example :
             GetAllDeploymentUnitSet(True,None)
        '''
        # default value of limit and skip is set in respective APIs
        # in DAO skip=0 , limit =0 means it will send all documents
        search_input = {}
        if filter_required:
            search_input.update(filter_required)
            count = self.collection.find(search_input).skip(
                skip).limit(limit).count()
            if count < 1:
                skip = 0
            results = self.collection.find(
                search_input).skip(skip).limit(limit)
        else:
            count = self.collection.find().skip(skip).limit(limit).count()
            if count < 1:
                skip = 0
            results = self.collection.find().skip(skip).limit(limit)

        listOfDeploymentUnitSet = []
        for deployment_unit_set in results:
            deployment_unit_set = self.getMandatoryDetails(deployment_unit_set)
            if isAllDetails:
                deployment_unit_set = self.GetDeploymentUnitSetDetails(
                    deployment_unit_set)
            listOfDeploymentUnitSet.append(deployment_unit_set)
        return listOfDeploymentUnitSet

    def GetDeploymentUnitSetById(self, duid, isAllDetails=False, only_build_number=False):
        '''
        General description:
        Args: param 1 : duid(object) : This is the unique id of the\
            DeploymentUnitSet stored in the database.
             param2 : get_all_details(string) :This is the parameter which determines \
            whether all DeploymentUnitSet details should be visible to user or not.\
            This has two values - True /False .

        Returns:
                Returns Database entity by the duid of the DeploymentUnitApprovalStatus.
        Example :
             GetDeploymentUnitSetById(duid,True)
        '''
        deployment_unit_set = self.collection.find_one({"_id": ObjectId(duid)})
        deployment_unit_set = self.getMandatoryDetails(deployment_unit_set)
        if isAllDetails:
            deployment_unit_set = self.GetDeploymentUnitSetDetails(
                deployment_unit_set,only_build_number)
        return deployment_unit_set
    
       
    def GetDeploymentUnitSetBuildsById(self, duid):
        data=self.GetDeploymentUnitSetById(duid, False, False)
        if data.get("du_set"):
            du_details = []
            for rec in data.get("du_set"):du_details.append(self.DeploymentUnitDB.get_du_deatils_for_api(rec,True,True,False))
            data["du_set_details"] = du_details
            data.pop("du_set")
        return data    
    
    def GetDeploymentUnitSetStatesById(self, duid):
        data=self.GetDeploymentUnitSetById(duid, False, False)
        if data.get("du_set"):
            du_details = []
            for rec in data.get("du_set"):
                du_details.append(self.DeploymentUnitDB.get_du_deatils_for_api(rec,False,False,True))   
        data["du_set_details"] = du_details
        data.pop("du_set") 
        return data    
    

    def GetDeploymentUnitSetByName(self, text, isAllDetails=False):
        '''
        General description:
        Args: param 1 : text(object) : This is the parameter of the\
            DeploymentUnitSet stored in the database.
             param2 : get_all_details(string) :This is the parameter which determines \
            whether all DeploymentUnitSet details should be visible to user or not.\
            This has two values - True /False .

        Returns:
                Returns Database entity based on text of the DeploymentUnitApprovalStatus.
        Example :
             GetDeploymentUnitSetByName(text,True)
        '''
        deployment_unit_set = self.collection.find_one(
            {"name": re.compile('^' + re.escape(text) + '$', re.IGNORECASE)})
        deployment_unit_set = self.getMandatoryDetails(deployment_unit_set)
        if isAllDetails:
            deployment_unit_set = self.GetDeploymentUnitSetDetails(
                deployment_unit_set)
        return deployment_unit_set

    def GetDeploymentUnitSetByTag(self, tag, isAllDetails=False):
        '''
        General description:

        Args:
            param 1: tag(string) :This is the parameter which \
            has the unique tag names for the existing DeploymentUnitSet in the database.
            param2 : get_all_details(string) :This is the parameter which determines \
            whether all DeploymentUnitSet details should be visible to user or not.\
            This has two values - True /False .

            Returns:
                Returns the existing database entity based on the DeploymentUnitSet Tags \
                from the DeploymentUnitSet database.
        Example :
            GetDeploymentUnitSetByTag(tag,true)
        '''
        listOfDeploymentUnitSet = []
        for deployment_unit_set in self.collection.find({"tag": re.compile('^' + re.escape(tag) + '$', re.IGNORECASE)}):
            deployment_unit_set = self.getMandatoryDetails(deployment_unit_set)
            if isAllDetails:
                deployment_unit_set = self.GetDeploymentUnitSetDetails(
                    deployment_unit_set)
            listOfDeploymentUnitSet.append(deployment_unit_set)
        return listOfDeploymentUnitSet

    def GetDeploymentUnitSetByCondition(self, condition, conditionValue):
        '''
        General description:

        Args:
            param 1: condition(string) :This is the parameter which \
            has the unique condition for the existing DeploymentUnitSet in the database.
            param2 : conditionValue(string) :This is the parameter which determines \
            conditionValue.

            Returns:
                Returns the existing database entity based on the DeploymentUnitSet condition \
                from the DeploymentUnitSet database.
        Example :
            GetDeploymentUnitSetByCondition(condition, conditionValue)
        '''

        return self.collection.find({condition: {"$in": [str(conditionValue)]}})

    def AddNewDeploymentUnitSet(self, newDeploymentUnitSet):
        '''
        General description:
        Args:
            param1 (newDeploymentUnitSet) : This is the parameter which has the details of the\
            newDeploymentUnitSet to be added in the database.
        Returns:
                Returns the id of the newly created newDeploymentUnitSet from the database.
        Example :
             AddNewDeploymentUnitSet(newDeploymentUnitSet)
        '''
        result = self.collection.insert_one(newDeploymentUnitSet)
        return str(result.inserted_id)

    def UpdateDeploymentUnitSet(self, deploymentUnitSet):
        '''
        General description:
        Args:
            param1 (deploymentUnitSet) : This is the parameter which has the details of the\
            MediaFiles to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given deploymentUnitSet
        Example :
             UpdateDeploymentUnitSet(deploymentUnitSet)
        '''
        jsonnewEntry = {}
        for key in deploymentUnitSet.keys():
            if key != "_id":
                jsonnewEntry[key] = deploymentUnitSet[key]
        result = self.collection.update_one({"_id": ObjectId(
            deploymentUnitSet["_id"]["oid"])}, {"$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def DeleteDeploymentUnitSet(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            DeploymentUnitSet stored in the database.
        Returns:
                Returns the count of the records deleted successfully\
                for the given id of the DeploymentUnitSet.
        Example :
             DeleteDeploymentUnitSet(id)
        '''
        return self.collection.delete_one({"_id": ObjectId(object_id)}).deleted_count

    def add_du_set_logo(self, short_path, thumbnail_path, object_id):
        '''
        General description:

        Args:
            param 1 : object_id(object) : This is the unique id of the\
            Tool stored in the database.

            param 2 : short_path(string) : This is the parameter which has details \
            for path where the logo file is present for a tool .

            param 3 : thumbnail_path(string) : This is the parameter which has details \
            for path where the thumbnail logo file is present for a tool
        Returns:
              Returns the count of the successful records updated.
        Example :
             add_tool_logo(id ,short_path,thumbnail_path )
        '''
        result = self.collection.update_one({"_id": ObjectId(object_id)},
                                            {"$set": {"logo": short_path,
                                                      "thumbnail_logo": thumbnail_path}})
        return result.modified_count

    def parse_du_set_data_for_sync(self,du_set):
        if du_set.get("du_set"):
            du_set_det =[]
            for record in du_set.get("du_set"):
                du=self.DeploymentUnitDB.GetDeploymentUnitById(record.get("du_id"), False);
                if du:
                    record["du_id"] = du.get("name")
                    du_set_det.append(record)
                else:
                    raise ValueError ("Du with id : "+record.get("du_id")+" not present in the Database")
            du_set["du_set"] =du_set_det
        for key in ["state","_id"]:    
            if du_set.get(key) is not None:
                du_set.pop(key)
        
            
    def get_du_sets_to_sync(self):
        du_sets_to_consider = []
        not_exported_du_set_names = []
        not_exported_du_set_names_and_reason = []
        all_du_sets = self.GetAllDeploymentUnitSet()
        for du_set in all_du_sets:
            record = {}
            try:
                if "_id" in du_set.keys():
                    record["source_du_set_id"] = str(du_set.get("_id"))
                self.parse_du_set_data_for_sync(du_set)
                record["duset_data"] = du_set 
                du_sets_to_consider.append(record)
            except Exception as e:  
                not_exported_du_set_names_and_reason.append(du_set.get("name") + " with error :" + str(e))
                not_exported_du_set_names.append(du_set.get("name"))               
        return du_sets_to_consider,not_exported_du_set_names,not_exported_du_set_names_and_reason
    