'''
#########################################################################################
STRUCTURE OF DEPLOYMENT UNIT for GUI : WE WILL RECEIVE AND SEND DATA IN THIS FORMAT TO GUI
#########################################################################################

{
    "status": "1",
    "tag": [
        "AAM",
        "KAM"
    ],
    "name": "Test Du",
    "type": "Fast Track",
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
    "build": [
        {
            "status": "1",
            "build_number": 1,
            "package_name": "du_1_1.zip",
            "package_type": "zip",
            "file_size": "6.6 MB",
            "type": "url",
            "file_path": "http://abcmd:8000/ac_rebuild_map-ga_9-37.zip"
        },
        {
            "status": "1",
            "build_number": 1,
            "package_name": "du_1_1.zip",
            "package_type": "zip",
            "file_size": "6.6 MB",
            "type": "url",
            "file_path": "http://abcmd:8000/ac_rebuild_map-ga_9-37.zip"
        }
    ],
    "deployment_field": {"fields": [
        {
            "default_value": "123",
            "is_mandatory": "true",
            "order_id": "1",
            "input_type": "text",
            "tooltip": "This account name which will be presented in a reports",
            "input_name": "site_name"
        },
          {
            "default_value": "123",
            "is_mandatory": "true",
            "order_id": "1",
            "input_type": "text",
            "tooltip": "This account name which will be presented in a reports",
            "input_name": "site_name"
        }
    ]},
    "allow_build_download": "true",
    "release_notes": "This is a test version"
}

#########################################################################################
STRUCTURE OF DEPLOYMENT UNIT in Server: WE WILL SAVE DATA IN MONGO IN THIS FORMAT
#########################################################################################

{
    "status": "1",
    "tag": [
        "58738ed17fe7b979008b26e7",
        "58738ed17fe7b979008b26e7"
    ],
    "name": "Test Du",
    "type": "58738ed17fe7b979008b26efd",
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
    "build": [ # BUILD IS PRESENT IN BUILDS COLLECTION
        {
            "status": "1",
            "build_number": 1,
            "package_name": "du_1_1.zip",
            "package_type": "zip",
            "file_size": "6.6 MB",
            "type": "url",
            "file_path": "http://abcmd:8000/ac_rebuild_map-ga_9-37.zip"
        },
        {
            "status": "1",
            "build_number": 1,
            "package_name": "du_1_1.zip",
            "package_type": "zip",
            "file_size": "6.6 MB",
            "type": "url",
            "file_path": "http://abcmd:8000/ac_rebuild_map-ga_9-37.zip"
        }
    ],
    "deployment_field": {"fields": [ # DEPLOYMENT FIELDS IS PRESENT IN Deployment Field COLLECTION
        {
            "default_value": "123",
            "is_mandatory": "true",
            "order_id": "1",
            "input_type": "text",
            "tooltip": "This account name which will be presented in a reports",
            "input_name": "site_name"
        },
          {
            "default_value": "123",
            "is_mandatory": "true",
            "order_id": "1",
            "input_type": "text",
            "tooltip": "This account name which will be presented in a reports",
            "input_name": "site_name"
        }
    ]},
    "allow_build_download": "true",
    "release_notes": "This is a test version"
}


'''

from datetime import datetime
import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

import Build
from DBUtil import DBUtil
import DeploymentFields
import DeploymentUnitApprovalStatus
import DeploymentUnitSet
import DeploymentUnitType
import Tags
import State
from settings import mongodb


class DeploymentUnit(DBUtil):
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
        self.collection = db.DeploymentUnit
        self.deploymentUnitApprovalStatusDB = DeploymentUnitApprovalStatus.DeploymentUnitApprovalStatus()
        self.tagDB = Tags.Tags()
        self.buildDB = Build.Build()
        self.deploymentFieldsDB = DeploymentFields.DeploymentFields(db)
        self.deploymentUnitTypeDB = DeploymentUnitType.DeploymentUnitType()
        self.statedb=State.State(db)
        # self.deploymentUnitSetDB = DeploymentUnitSet.DeploymentUnitSet()
        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def GetDeploymentUnitDetails(self, record,only_build_number=False, only_basic_details=None):
        '''
        General description:
        Args:
            param1 (record) : This is the DeploymentUnit Id which is stored in database
        Returns:
                Returns Database entity of record for the given DeploymentUnit
        Example :
            GetDeploymentUnitDetails(record)
        '''
        if record:
            build = self.buildDB.get_active_build(str(record["_id"]),only_build_number)
            if build is not None and build.count() > 0:
                record["build"] = build
            else:
                record["build"] = None
            if only_basic_details is None:
                deployment_field = self.deploymentFieldsDB.GetDeploymentFields(
                    str(record["_id"]))
                if deployment_field is not None:
                    if deployment_field.get("fields") and len(deployment_field.get("fields")) > 0:
                        if len(deployment_field.get("fields")[0]) > 0:
                            record["deployment_field"] = deployment_field
                        else:
                            record["deployment_field"] = None
                    else:
                        record["deployment_field"] = None
                else:
                    record["deployment_field"] = None
                state=self.statedb.get_state_by_parent_entity_id(record.get("_id"), True,only_build_number)
                record["state"]=state
        return record

    def GetDeploymentUnitBasicDetails(self, record, only_basic_details=None):
        '''
        General description:
        Args:
            param1 (record) : This is the DeploymentUnit Id which is stored in database
        Returns:
                Returns Database entity of record for the given DeploymentUnit
        Example :
            GetDeploymentUnitBasicDetails(record)
        '''
        if record:
            if only_basic_details is None:
                included_in_du_set = []
                deploymentUnitSetDB = DeploymentUnitSet.DeploymentUnitSet()
                for duSetdata in deploymentUnitSetDB.GetDeploymentUnitSetByCondition("du_set.du_id", str(record["_id"])):
                    included_in_du_set.append(
                        {"du_set_id": str(duSetdata["_id"]), "du_set_name": str(duSetdata.get("name"))})
                record["included_in"] = included_in_du_set
            if record.get("tag"):
                record["tag"] = self.tagDB.get_tag_names_from_given_ids_list(
                    record["tag"])
            if record.get("type"):
                record["type"] = self.deploymentUnitTypeDB.GetDeploymentUnitTypeById(record["type"])[
                    "name"]
        return record

    def GetAllDuIds(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns list of all Du ids.
        Example :
            get_tag_ids()
        '''
        dus = self.collection.find()
        du_ids_list = []
        for du in dus:
            du_ids_list.append(str(du["_id"]))
        return du_ids_list

    def GetAllDeploymentUnits(self, stat_filter_input=None,deployment_unit_type_filter =None,is_all_details=False, filter_required=None, skip=0, limit=0, only_basic_details=None):
        # default value of limit and skip is set in respective APIs
        # in DAO skip=0 , limit =0 means it will send all documents
        deployment_type_filter = []
        search_input = {}
        if deployment_unit_type_filter:
            for rec in list(self.deploymentUnitTypeDB.GetDeploymentUnitType()):
                deployment_type_filter.append((str(rec["_id"]), rec["name"]))
            mapping = deployment_type_filter
            for k, v in mapping:
                deployment_unit_type_filter = [
                    w.replace(v, k) for w in deployment_unit_type_filter]
            search_input["type"] = {"$in": deployment_unit_type_filter}
        if stat_filter_input:
            mapping = [('active', '1'), ('deleted', '0')]
            for k, v in mapping:
                stat_filter_input = [w.replace(k, v)
                                     for w in stat_filter_input]
            search_input["status"] = {"$in": stat_filter_input}
        rawDeploymentUnit = []

        if filter_required:
            search_input.update(filter_required)
        count = self.collection.find(search_input).skip(
            skip).limit(limit).count()
        if count < 1:
            skip = 0
        # entities_projected = {"_id": 1, "name": 1, "tag": 1, "logo": 1, "thumbnail_logo": 1, "type" : 1, "release_notes" : 1, "status" : 1}
        if only_basic_details is True:
            for record in self.collection.find(search_input).skip(skip).limit(limit):
                record = self.GetDeploymentUnitBasicDetails(record, True)
                if is_all_details:
                    record = self.GetDeploymentUnitDetails(record, True)
                rawDeploymentUnit.append(record)
        else:
            for record in self.collection.find(search_input).skip(skip).limit(limit):
                record = self.GetDeploymentUnitBasicDetails(record)
                if is_all_details:
                    record = self.GetDeploymentUnitDetails(record)
                rawDeploymentUnit.append(record)
        return rawDeploymentUnit

    def GetDeploymentUnitById(self, duid, isAllDetails=False,only_build_number=False,get_basic_deatils = True, keys_to_include = None):
        '''
        General description:

        Args:
             param1 (duid) : This is the unique id of the\
            DeploymentRequest stored in the database.

            param2: is_all_details(string) :This is the parameter which determines \
            whether all DeploymentRequest should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the DeploymentRequest and\
                is_all_details parameter.
        Example :
            GetDeploymentUnitById(duid ,True)
        '''
        if keys_to_include:
            deployment_unit = self.collection.find_one({"_id": ObjectId(duid)},keys_to_include)
        else:  
            deployment_unit = self.collection.find_one({"_id": ObjectId(duid)})
        if get_basic_deatils and deployment_unit:
            deployment_unit = self.GetDeploymentUnitBasicDetails(
                deployment_unit)
        if isAllDetails and deployment_unit is not None:
            deployment_unit = self.GetDeploymentUnitDetails(deployment_unit,only_build_number)
        return deployment_unit

    def GetDeploymentUnitByName(self, name, isAllDetails=False):
        '''
        General description:

        Args:
             param1 (name) : This is the name of the\
            DeploymentRequest stored in the database.

            param2: is_all_details(string) :This is the parameter which determines \
            whether all DeploymentRequest should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the DeploymentRequest and\
                is_all_details parameter.
        Example :
            GetDeploymentUnitByname(name,True)
        '''
        deployment_unit = (self.collection.find_one(
            {"name": re.compile('^' + re.escape(name) + '$', re.IGNORECASE)}))
        if deployment_unit:
            deployment_unit = self.GetDeploymentUnitBasicDetails(
                deployment_unit)
        if isAllDetails and deployment_unit is not None:
            deployment_unit = self.GetDeploymentUnitDetails(deployment_unit)
        return deployment_unit

    def GetDeploymentUnitByTag(self, tag, isAllDetails=False):
        '''
        General description:

        Args:
             param1 (tag) : This is the tag of the\
            DeploymentRequest stored in the database.

            param2: is_all_details(string) :This is the parameter which determines \
            whether all DeploymentRequest should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the DeploymentRequest and\
                is_all_details parameter.
        Example :
            GetDeploymentUnitByTag(tag,True)
        '''

        tag_name = self.tagDB.get_tag_by_name(tag)
        deploymentUnit=[]
        if tag_name:
            deploymentUnit = self.collection.find({"tag": re.compile(
                '^' + re.escape(str(tag_name["_id"])) + '$', re.IGNORECASE)})
        rawDeploymentUnit = []
        for record in deploymentUnit:
            record = self.GetDeploymentUnitBasicDetails(record)
            if isAllDetails:
                record = self.GetDeploymentUnitDetails(record)
            rawDeploymentUnit.append(record)
        return rawDeploymentUnit

    def AddDeploymentUnit(self, newDeploymentUnit):
        '''
        General description:
        Args:
            param1 (newDeploymentUnit) : This is the parameter which has the details of the\
            DeploymentUnit to be added in the database.
        Returns:
                Returns the id of the newly created DeploymentUnit from the database.
        Example :
             AddDeploymentUnit(DeploymentUnit)
        '''
        result = self.collection.insert_one(newDeploymentUnit)
        return str(result.inserted_id)

    def UpdateDeploymentUnit(self, deploymentUnit):
        '''
        General description:
        Args:
            param1 (deploymentUnit) : This is the parameter which has the details of the\
            deploymentUnit to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the deploymentUnit.
        Example :
             UpdateDeploymentUnit(deploymentUnit)
        '''
        jsonnewEntry = {}
        for key in deploymentUnit.keys():
            if key != "_id":
                jsonnewEntry[key] = deploymentUnit[key]
        result = self.collection.update_one({"_id": ObjectId(
            deploymentUnit["_id"]["oid"])}, {"$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def DeleteDeploymentUnit(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            DeploymentUnit stored in the database.
        Returns:
                Returns the count of the records deleted successfully\
                for the given id of the DeploymentUnit.
        Example :
             DeleteDeploymentUnit(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def add_du_logo(self, short_path, thumbnail_path, object_id):
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

    def get_dus_to_sync(self):
        dus_to_consider = []
        all_dus = self.GetAllDeploymentUnits(['active'],None, True)
        if not all_dus:
            return all_dus
        for du in all_dus:
            record = {}
            if du.get("build"):
                builds = []
                for build in du.get("build"):
                    build = self.trim_data_for_sync(build)
                    if build.get("build_date"):
                        build["build_date"] = str(build["build_date"])
                    builds.append(build)
                du["build"] = builds
            if du.get("deployment_field"):
                du["deployment_field"] = self.trim_data_for_sync(
                    du.get("deployment_field"))
            if "_id" in du.keys():
                record["source_du_id"] = str(du.get("_id"))
                du.pop("_id")
            if du.get("state"):
                du.pop("state")
            record["du_data"] = du
            dus_to_consider.append(record)
        return dus_to_consider
    
    
    def trim_data_for_sync(self, data):
        '''
        General description:
        Args:
           param1 : data (JSON) : This is the parameter which has details of\
           Tool in JSON object.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             trim_data_for_sync(data)
        '''
        if data:
            if "_id" in data.keys():
                data.pop("_id")
            if "version_id" in data.keys():  # TODO REMOVE LATER.Not required from 2.0.3
                data.pop("version_id")
            if "parent_entity_id" in data.keys():
                data.pop("parent_entity_id")
        return data

    def GetDeploymentUnitByFA(self, faName):        
        return self.collection.find({ "flexible_attributes."+faName : {"$exists": True}})


    def get_du_deatils_for_api(self,rec,add_dep_fields = True , add_builds = True, add_states = True):
        du = self.GetDeploymentUnitById(
                    str(rec.get("du_id")), False,False,False,{"_id":1,"build":1,"name":1,"type":1,"flexible_attributes":1})
        du["type"] = self.deploymentUnitTypeDB.GetDeploymentUnitTypeById(du["type"])[
                "name"]
        du["dependent"] = rec.get("dependent")
        du["order"] = rec.get("order")        
        if add_dep_fields:
            deployment_field = self.deploymentFieldsDB.GetDeploymentFields(str(du["_id"]))
            if deployment_field is not None:
                if deployment_field.get("fields") and len(deployment_field.get("fields")) > 0:
                    if len(deployment_field.get("fields")[0]) > 0:
                        du["deployment_field"] = deployment_field
                    else:
                        du["deployment_field"] = None
                else:
                    du["deployment_field"] = None
            else:
                du["deployment_field"] = None         
        if add_builds:               
            build = self.buildDB.get_active_build(str(du["_id"]),True)
            if build is not None and build.count() > 0:
                du["build"] = build
            else:
                du["build"] = None
        if add_states:
            du["states"] = self.statedb.get_state_by_parent_entity_id(str(du["_id"]),True,True)        
        return du    
    