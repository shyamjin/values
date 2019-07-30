'''
Created on Dec 18, 2017

@author: pdinda
'''
import traceback,RepositoryHelperService
from DBUtil import Config, Build,Versions,DeploymentUnitSet,DeploymentUnit,DeploymentUnitType,Tool,Tags,\
        State,Teams,DeploymentRequest,Machine, DeploymentFields
from settings import mongodb
from Services import HelperServices,TeamService,BuildHelperService,\
    FlexibleAttributesHelper

tagDB = Tags.Tags()
versionsDB = Versions.Versions(mongodb)
configdb = Config.Config(mongodb)
buildsDB = Build.Build()
deploymentunitsetdb = DeploymentUnitSet.DeploymentUnitSet()
deploymentunitdb = DeploymentUnit.DeploymentUnit()
deploymentUnitTypedb = DeploymentUnitType.DeploymentUnitType()
toolDB = Tool.Tool(mongodb)
teamService = TeamService.TeamService()
statedb=State.State(mongodb)
teamsdb=Teams.Teams(mongodb)
deploymentrequestdb=DeploymentRequest.DeploymentRequest(mongodb)
machinedb=Machine.Machine(mongodb)
deploymentFieldsDB = DeploymentFields.DeploymentFields(mongodb)

def delete_du(du_id , validation_indicator=True):
    """Start Du Deletion"""
    # MAINTAIN THE DELETED TOOLS
    deleted_dus = []
    deleted_builds = []

    dudata = {}
    try:
        du = deploymentunitdb.GetDeploymentUnitById(du_id, False)
        if not du:
            raise ValueError("No such du was found with id:" + du)
        if validation_indicator == True :
            dusets = deploymentunitsetdb.GetAllDeploymentUnitSet(False, {"du_set.du_id": {"$in" : [str(du_id)]}})
            present_in_duset=[]
            for duset in dusets:
                if duset.get("name") not in present_in_duset:
                    present_in_duset.append(duset.get("name")) 
            all_deployments=deploymentrequestdb.GetDeploymentRequestAll({"parent_entity_id": {"$in": [str(du_id)]}})
            present_in_deployment=[]
            for dep in all_deployments:
                machine=machinedb.GetMachine(dep.get("machine_id"))
                if machine:
                    if machine.get("machine_name") not in present_in_deployment:
                        present_in_deployment.append(machine.get("machine_name")) 
            teams = teamsdb.get_teams_by_filter(str(du_id))
            present_in_teams=[]
            for team in teams :
                if team.get("team_name") not in present_in_teams:
                    present_in_teams.append(team.get("team_name"))
            err=""
            if len(present_in_duset)>0: 
                err="The Du cannot be deleted as it is present in Du Package: " + (','.join(map(str, present_in_duset)))
            if len(present_in_deployment)>0:
                if len(err)>0: 
                    err=err + " and has been deployed in machines: " + (','.join(map(str, present_in_deployment)))
                else:
                    err="The Du cannot be delete as it has been deployed in machines: " + (','.join(map(str, present_in_deployment)))
            if len(present_in_teams)>0 :
                if len(err)>0: 
                    err=err + " and is the part of teams: " +  (','.join(map(str, present_in_teams)))
                else:
                    err="The Du cannot be deleted as it is the part of the teams : " + (','.join(map(str, present_in_teams)))
            if len(err)>0:
                raise ValueError (err)
        
        dudata["_id"] = {}
        dudata["_id"]["oid"] = str(du_id)
        dudata["status"] = "0"
        if str(du.get("status")) <> "0":
            deldu = deploymentunitdb.UpdateDeploymentUnit(dudata)
            if deldu in [None, 0]:
                raise Exception("Unable to delete tool " + str(du_id))
            else:
                dudata["status"] = du.get("status")
                deleted_dus.append(dudata)
            builds = buildsDB.get_active_build(
                du_id)
            if builds:
                for build in builds:
                    if str(build.get("status")) <> "0":
                        Buildupdate = {}
                        Buildupdate["_id"] = {}
                        Buildupdate["_id"]["oid"] = str(
                            build.get("_id"))
                        Buildupdate["status"] = "0"
                        delbuild = buildsDB.update_build(
                            Buildupdate)
                        if delbuild in [None, 0]:
                            raise Exception(
                                "Unable to delete build " + str(build.get("_id")))
                        else:
                            deleted_builds.append(Buildupdate)
        statedb.delete_state_by_parent_entity_id(str(du_id))                    
        return {"result": "success", "message": "du was deleted"}
    except Exception as e_value:  # catch *all* exceptions
        for rec in deleted_dus:
            rec["status"] = "1"
            deploymentunitdb.UpdateDeploymentUnit(rec)
        for rec in deleted_builds:
            rec["status"] = "1"
            buildsDB.update_build(rec)
        traceback.print_exc()
        return {"result": "failed", "message": str(e_value)}
    
def delete_du_set(duset_id,validation_indicator=True):
    """Start DuSet Deletion"""
    if validation_indicator is False :
        try:
            statedb.delete_state_by_parent_entity_id(str(duset_id))
            deploymentunitsetdb.DeleteDeploymentUnitSet(str(duset_id))
            return {"result": "success", "message": "DuSet was deleted"}
        except Exception as e_value:  # catch *all* exceptions
            return {"result": "failed", "message": str(e_value)}    
    else:
        if not deploymentunitsetdb.GetDeploymentUnitSetById(str(duset_id), False):
            raise ValueError ("No such Du Package was found")
        states= statedb.get_state_by_parent_entity_id(str(duset_id), False)
        present_in_states=[]
        for state in states:
            if state.get("name") not in present_in_states:
                present_in_states.append(state.get("name"))
        teams=teamsdb.get_teams_by_filter(str(duset_id))
        present_in_teams=[]
        for team in teams:
            if team.get("team_name") not in present_in_teams:
                present_in_teams.append(team.get("team_name"))
        err=""
        if len(present_in_states)>0: 
            err="The DU Package cannot be delete as it is present in States: " + (','.join(map(str, present_in_states)))
        if len(present_in_teams)>0:
            if len(present_in_states)>0: 
                err=err + " and Teams: " + (','.join(map(str, present_in_teams)))
            else:
                err="The DU Package cannot be delete as it is present in Teams: " + (','.join(map(str, present_in_teams)))
        if len(err)>0:
            raise ValueError (err)
        return deploymentunitsetdb.DeleteDeploymentUnitSet(str(duset_id))

def add_update_du_set(deploymentUnitSetData, deployment_unit_set_id=None, logo_path=None, logo_full_path=None,directory_to_import_from=None):
    """Add update DeploymentUnitSet data"""
    
    # Mandatory Keys
    keys_to_validate=["name","du_set"]
    for key in keys_to_validate:
        if not deploymentUnitSetData.get(key): raise Exception ("mandatory key: "+ key+" is missing in DU details")
    if (deploymentUnitSetData.get("name")):
        HelperServices.validate_name(deploymentUnitSetData.get("name"),"deploymentunit package name")
    verify_du_set_data(deploymentUnitSetData)
    verify_du_and_du_set_data(deploymentUnitSetData)
   
    #ADD LOGO
    deploymentUnitSetData = HelperServices.add_update_logo(
            deploymentUnitSetData, logo_path, logo_full_path, directory_to_import_from)
    
    #TRIM NOT REQUIRED DATA
    deploymentUnitSetData = trim_du_duset_data(deploymentUnitSetData)
        
    #VALIDATION    
    if deployment_unit_set_id:
        existing_du_set_details = deploymentunitsetdb.GetDeploymentUnitSetById(
                                 deployment_unit_set_id, False)
        if not existing_du_set_details:
            raise Exception("No such DeploymentUnit Set was found with _id: ")  
    else:
        #TRY TO SEARCH WITH NAME
        existing_du_set=deploymentunitsetdb.GetDeploymentUnitSetByName(deploymentUnitSetData.get("name"),False)
        if  existing_du_set:
            deployment_unit_set_id=str(existing_du_set["_id"])
                    
    if deployment_unit_set_id:    
        deploymentUnitSetData["_id"] = {}
        deploymentUnitSetData["_id"]["oid"] = deployment_unit_set_id
        result = deploymentunitsetdb.UpdateDeploymentUnitSet(
            deploymentUnitSetData)
    else:
        add_missing_attributes_for_duset(deploymentUnitSetData)
        result = deploymentunitsetdb.AddNewDeploymentUnitSet(
            deploymentUnitSetData)
    if result is None:
        raise Exception("Unable to create/update DeploymentUnit Set")
    else:
        # RELOAD TEAM PERMISSIONS
        teamService.generate_details()
    return str(result)

def trim_du_duset_data(data):
    """Trim trim_du_duset_data"""
    keys_to_remove = ["deployment_field", "build", "operation",\
                      "approval_list","approval_status"]
    for key in keys_to_remove:
        if key in data.keys():
            data.pop(key)
    return data

def add_missing_attributes_for_duset(deployment_unit_set_data):
    input_as_array=["pre_requiests","tag"]
    input_as_string=["release_notes"]    
    for rec in input_as_array: 
        if rec not in deployment_unit_set_data.keys() or deployment_unit_set_data.get(rec) is None : deployment_unit_set_data[rec]=[]
    for rec in input_as_string: 
        if rec not in deployment_unit_set_data.keys() or deployment_unit_set_data.get(rec) is None : deployment_unit_set_data[rec]=""
   
def add_missing_attributes_for_du(deployment_unit_data):
    input_as_array=["pre_requiests","tag","included_in"]
    input_as_string=["branch","release_notes"]    
    for rec in input_as_array: 
        if rec not in deployment_unit_data.keys() or deployment_unit_data.get(rec) is None : deployment_unit_data[rec]=[]
    for rec in input_as_string: 
        if rec not in deployment_unit_data.keys() or deployment_unit_data.get(rec) is None : deployment_unit_data[rec]=""
           
               
    

def add_update_du(deploymentUnitData, deploymentUnitId=None, logo_path=None, directory_to_import_from=None, full_logo_path=None,handle_dependencies=True):
    
    """Add update DeploymentUnit data"""
    # Mandatory Keys
    keys_to_validate=["name"]
    for key in keys_to_validate:
        if not deploymentUnitData.get(key): raise Exception ("mandatory key: "+ key+" is missing in DU details")
       
       
    buildData = None
    deploymentFeildData = None
    result = None
    transaction_type = None
    if not deploymentUnitId:
        transaction_type = "new"
        
    # preparing deploymentUnit data
    if deploymentUnitData.get("build") is not None:
        buildData = deploymentUnitData.get("build")
    if deploymentUnitData.get("deployment_field") is not None:
        deploymentFeildData = deploymentUnitData.get("deployment_field")[
            "fields"]
        
    #VALIDATION                
    if deploymentUnitId:
        if not deploymentunitdb.GetDeploymentUnitById(deploymentUnitId):
            raise ValueError("No DU with this _id is found in database")
    else:
        #TRY TO SEARCH WITH NAME
        existing_du=deploymentunitdb.GetDeploymentUnitByName(deploymentUnitData.get("name"))
        if  existing_du:
            deploymentUnitId=str(existing_du["_id"])
    #VALIDATIONS FOR NEW DU
    if not deploymentUnitId:         
        keys_to_validate=["type"]
        for key in keys_to_validate:
            if not deploymentUnitData.get(key): raise Exception ("mandatory key: "+ key+" is missing in du details")
        add_missing_attributes_for_du(deploymentUnitData)
    if deploymentUnitData.get("name"):
        HelperServices.validate_name(deploymentUnitData.get("name"),"deploymentunit name") 
    if deploymentUnitData.get("flexible_attributes"):
        FlexibleAttributesHelper.validate_entity_value("DeploymentUnit", deploymentUnitData.get("flexible_attributes"))    
    deploymentUnitData = verify_du_and_du_set_data(deploymentUnitData)

    deploymentUnitData = HelperServices.add_update_logo(
        deploymentUnitData, logo_path, full_logo_path, directory_to_import_from)
    
    #TRIM NOT REQUIRED DATA
    deploymentUnitData = trim_du_duset_data(deploymentUnitData)

    if deploymentUnitData.get("repository_to_use"):
        if not RepositoryHelperService.check_if_repo_exists_by_name(deploymentUnitData.get("repository_to_use")):
            raise Exception(deploymentUnitData.get("repository_to_use") + ": No such repository exists")
    
    # ADD UPDATE DATA
    if deploymentUnitId:
        deploymentUnitData["_id"] = {"oid": deploymentUnitId}
        result = deploymentunitdb.UpdateDeploymentUnit(deploymentUnitData)
    else:
        deploymentUnitData["status"] = "1"
        result = deploymentunitdb.AddDeploymentUnit(deploymentUnitData)
        deploymentUnitId = result
    if result is None:
        raise Exception(
            "Unable to create/update deploymentUnit " + deploymentUnitData["name"])
    else:
        # RELOAD TEAM PERMISSIONS
        teamService.generate_details()
    if handle_dependencies: 
        dep_fields_result = None   
        try:    
            if buildData is not None:
                for build in buildData:
                    build["parent_entity_type"] = "du"
                    BuildHelperService.add_update_build(build, deploymentUnitId, None)
            # preparing deployment_field data
            # if duDatabackup.get("deployment_field") is not None:
            if deploymentFeildData is not None:
                dep_fields_result = HelperServices.add_update_deployment_fields(
                        deploymentFeildData, deploymentUnitId)
            
            #SET DU AS UPDATED if either of dep fields or build is updated
            if transaction_type <> "new" and str(result) == "0" \
            and  str(dep_fields_result) == "1": 
                result = "1" 
        except Exception as e:     
            if transaction_type == "new":    
                deploymentunitdb.DeleteDeploymentUnit(deploymentUnitId)
                buildsDB.delete_build_by_parent_entitity_id(deploymentUnitId)
                deploymentFieldsDB.delete_dep_field_by_parent_entity_id(deploymentUnitId)
            return e                    
    return str(result)


def verify_du_and_du_set_data(myData):
    """Verify DuSetData"""
    if myData.get("tag"):
        myData["tag"] = tagDB.get_tag_ids_from_given_ids_list(myData["tag"])
    if myData.get("type"):
        du_type = deploymentUnitTypedb.GetDeploymentUnitTypeByName(
            myData["type"])
        if not du_type:
            raise Exception("No such type was found:"+str(myData["type"]))
        else:
            myData["type"] = str(du_type["_id"])
    return myData

def verify_du_set_data(deploymentUnitSetData):
    """Verify DeploymentUnitSetData"""
    dus_added=[]
    if deploymentUnitSetData.get("du_set") and len(deploymentUnitSetData.get("du_set")) > 0:
        for rec in deploymentUnitSetData.get("du_set"):
            if str(rec.get("dependent")).lower() not in ["true", "false"]:
                raise ValueError(
                    "Value dependent was not fount for du_id:" + rec.get("du_id") + " in input request")
            # dependent IS ALWAYS STRING TYPE
            rec["dependent"] = str(rec.get("dependent")).lower()
            if not rec.get("order"):
                raise ValueError(
                    "Value order was not fount for du_id:" + rec.get("du_id") + " in input request")
            rec["order"] = int(rec.get("order"))  # ORDER IS ALWAYS INT TYPE
            du = deploymentunitdb.GetDeploymentUnitById(
                str(rec.get("du_id")), True)
            if not du:
                raise ValueError("DeploymentUnit with _id:" +
                                 rec.get("du_id") + " was not found in database")
            else:
                if rec.get("du_id") not in dus_added:
                    dus_added.append(rec.get("du_id"))
                else:
                    raise Exception("Du with _id: "+rec.get("du_id")+" was found twice in du_set list")    
    else:
        raise ValueError(
            "Specifying at least one Deployment Unit in the DeploymentUnit Set is mandatory")
    return deploymentUnitSetData


def check_if_du_exists(du_data):
    """Check if tool data dependent data exists in database"""
    local_du = deploymentunitdb.GetDeploymentUnitByName(du_data["name"])
    if local_du is not None:
        raise Exception("DU already exists")


def validate_du_data(du_data=None):
    """Validate a du_data Data"""
    if not du_data:
        raise Exception("du_data is missing")
    if du_data.get("operation") != "delete":
        if du_data.get("deployment_field"):
            if not du_data.get("deployment_field").get("fields") or len(du_data.get("deployment_field").get("fields")) < 1:
                raise Exception("deployment_field has no fields")        

def validate_duset_data(duset_data=None):
    """Validate a du_data Data"""
    if not duset_data:
        raise Exception("duset_data is missing")
    if not duset_data.get("name"):
        raise Exception("duset_data.name is missing")
    if not duset_data.get("du_set") and len(duset_data.get("du_set",[]))<1:
        raise Exception("duset_data.du_set is missing")
    return