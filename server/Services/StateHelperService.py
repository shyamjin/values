'''
Created on Dec 18, 2017

@author: pdinda
'''
import traceback
from DBUtil import  DeploymentFields,  DeploymentUnitApprovalStatus, State,DeploymentUnitSet,DeploymentUnit,Counter,DeploymentRequest,Machine
from settings import mongodb
from Services import HelperServices

statedb=State.State(mongodb)
deploymentUnitApprovalStatusdb = DeploymentUnitApprovalStatus.DeploymentUnitApprovalStatus()
deploymentFieldsDB = DeploymentFields.DeploymentFields(mongodb)
deploymentunitsetdb = DeploymentUnitSet.DeploymentUnitSet()
deploymentunitdb = DeploymentUnit.DeploymentUnit()
counterDB = Counter.Counter(mongodb)
deploymentrequestdb=DeploymentRequest.DeploymentRequest(mongodb)
machinedb=Machine.Machine(mongodb)




def generate_new_state(details):
    # details has "deployment_field":{"hi":"hellow"} which is handled below
    state_id=None
    deployment_fields_id=None
    dep_fields=None
    try:
        state={"type":"dustate","build_id":details.get("build_id"),\
               "name":details.get("name"),"parent_entity_id":details.get("parent_entity_id")\
               ,"approval_status":"Created"}# DATA VERIFIED IN add_update_state
        if details.get("deployment_field") and len(details.get("deployment_field").get("fields",[])) > 0:
            dep_fields = details.get("deployment_field")                 
        else:dep_fields=deploymentFieldsDB.GetDeploymentFields(details.get("parent_entity_id"))
        state_id=add_update_state(state,None)
        if dep_fields:
            deployment_fields_id =  HelperServices.add_update_deployment_fields(dep_fields.get("fields"),state_id)
        return state_id
    except Exception as e:  # catch *all* exceptions
        traceback.print_exc()
        if state_id is not None:
            delete_state(state_id)
        if deployment_fields_id is not None:
            deploymentFieldsDB.DeleteDeploymentFields(deployment_fields_id)    
        raise e    
    
def add_update_state(state_data, state_Id):
    """Add update DeploymentUnit data"""
    if state_data.get("approval_status"):
        approval_status=deploymentUnitApprovalStatusdb.GetDeploymentUnitApprovalStatusByName(state_data.get("approval_status"))
        if approval_status:state_data["approval_status"]  = str(approval_status.get("_id"))
        else:
            raise Exception ("The approval status provided is not correct")
    if not state_Id:
        # MANDATORY ATTRIBUTES
        for rec in ["parent_entity_id","approval_status"]:
            if not state_data.get(rec):
                raise Exception(rec+" is not provided")
        state_data=trim_state_data(state_data)
        existing_du=deploymentunitdb.GetDeploymentUnitById(state_data.get("parent_entity_id"))
        existing_du_set=deploymentunitsetdb.GetDeploymentUnitSetById(state_data.get("parent_entity_id"))
        if existing_du:         
            state_data["type"]="dustate";
            if not state_data.get("name"):
                state_data["name"]=existing_du.get("name")+" State-"+str(counterDB.get_counter())
            # MANDATORY ATTRIBUTES
            for rec in ["build_id"]:
                if not state_data.get(rec):
                    raise Exception(rec+" is not provided")
        elif existing_du_set:
            state_data["type"]="dusetstate";
            if not state_data.get("name"):
                state_data["name"]=existing_du_set.get("name")+" Package State-"+str(counterDB.get_counter())
            # MANDATORY ATTRIBUTES
            for rec in ["states"]:
                if not state_data.get(rec):
                    raise Exception(rec+" is not provided")                     
        else:
            raise Exception("parent_entity_id provided is neither du or duPackage")
        HelperServices.validate_name(state_data.get("name"),"state name")
        existing_state=statedb.get_state_by_parent_entity_id_name(state_data.get("name"), state_data.get("parent_entity_id"),False)  
        if existing_state:
            if(state_data.get("type")=="dustate"):
                raise Exception("Duplicate state error, state '"+existing_state.get("name")+"' already present with same name for this Du")
            else:
                raise Exception("Duplicate state error, state '"+existing_state.get("name")+"' already present with same name for this DuSet")
        result = statedb.add_state(state_data)
    # ADD UPDATE DATA
    if state_Id:
        if state_data.get("name") is not None:
            prev_data=statedb.get_state_by_id(state_Id,False)
            duplicate=statedb.get_state_by_parent_entity_id_name(state_data.get("name"), prev_data.get("parent_entity_id"),False)
            if not(duplicate is None or str(duplicate.get("_id")) == str(state_Id)):
                raise Exception("Duplicate state error, state already present with same name") 
        state_data["_id"] = {"oid": state_Id}
        state_data=trim_state_data(state_data)
        result = statedb.update_state(state_data)
    if result is None:
        raise Exception(
            "Unable to create/update state")
    return result

def trim_state_data(state_data):
    """Trim state data"""
    keys_to_remove = ["deployment_field","operation"]
    for key in keys_to_remove:
        if key in state_data.keys():
            state_data.pop(key)
    return state_data

def check_state_mandate_fields(state_data):
    if not state_data.get("name"):
        raise ValueError(
            "Mandatory attribute name not found.")
    if not state_data.get("parent_entity_id"):
        raise ValueError(
            "Mandatory attribute parent_entity_id not found.")   
    if not state_data.get("build_id") and len(state_data.get("states",[]))<1:
        raise ValueError(
            "Mandatory attribute build_id/states not found.")
        
def delete_state(state_id,validation_indicator=True):
    """Start State Deletion"""
    if validation_indicator is False:
        try:
            statedb.delete_state(str(state_id))
            return {"result": "success", "message": "State was deleted"}
        except Exception as e_value:  # catch *all* exceptions
            return {"result": "failed", "message": str(e_value)}
    else:
        state = statedb.get_state_by_id(str(state_id))
        if state is None:
            raise ValueError ("No such state was found")
        dusetstates = statedb.get_state_all(False, None, None, 0, 0, {"states": {"$in": [str(state_id)]}})
        present_in_dusetstate=[]
        for dusetstate in dusetstates:
            if dusetstate.get("name") not in present_in_dusetstate:
                present_in_dusetstate.append(dusetstate.get("name")) 
        all_deployments=deploymentrequestdb.GetDeploymentRequestAll({"$or":[{"state_id": {"$in": [str(state_id)]}},\
                                                                            {"package_state_id": {"$in": [str(state_id)]}}]})    
        present_in_deployment=[]
        for dep in all_deployments:
            machine=machinedb.GetMachine(dep.get("machine_id"))
            if machine:
                if machine.get("machine_name") not in present_in_deployment:
                    present_in_deployment.append(machine.get("machine_name")) 
        err=""
        if len(present_in_dusetstate)>0: 
            err="The state cannot be deleted as the state is present in Du package state: " + (','.join(map(str, present_in_dusetstate)))
        if len(present_in_deployment)>0:
            if len(present_in_dusetstate)>0: 
                err=err + " and has been deployed in machines: " + (','.join(map(str, present_in_deployment)))
            else:
                err="The DU Package cannot be delete as it has been deployed in machines: " + (','.join(map(str, present_in_deployment)))
        if len(err)>0:
            raise ValueError (err)
        return statedb.delete_state(str(state_id))
 
def get_names_from_ids(state , is_state_details=False,states=None):
    if state is not None:
        state["parent_entity_name"],state["parent_entity_type"]=get_parent_name_from_id(state.get("parent_entity_id"),True)        
        if state.get("type") == "dusetstate":
            if is_state_details:
                temp_states=[]
                for rec in state.get("states") :  
                    rec["parent_entity_name"],rec["parent_entity_type"]=get_parent_name_from_id(rec.get("parent_entity_id"),True)
                    temp_states.append(rec) 
                state["states"]=temp_states     
    if type(states) == list:
        states.append(state)
    else:
        return state  

def get_parent_name_from_id(parent_entity_id,add_type_ind = False):
    du=deploymentunitdb.GetDeploymentUnitById(parent_entity_id)
    if du :
        if add_type_ind:
            return du.get("name"),du.get("type")
        return du.get("name")
    duset=deploymentunitsetdb.GetDeploymentUnitSetById(parent_entity_id)
    if duset:
        if add_type_ind:
            return duset.get("name"),duset.get("type")
        return duset.get("name")
    raise Exception("Given parent_entity_id: "+parent_entity_id + " was not found in DB")    

def get_parent_id_from_name(parent_entity_id):
    du=deploymentunitdb.GetDeploymentUnitByName(parent_entity_id)
    if du :
        return str(du.get("_id"))
    duset=deploymentunitsetdb.GetDeploymentUnitSetByName(parent_entity_id)
    if duset:
        return str(duset.get("_id"))
    raise Exception("Given parent_entity_id: "+parent_entity_id + " was not found in DB")    

def convert_parent_names_to_ids(state , is_state_details=False):
    #state.get("parent_entity_id") is the name of parent here
    if state is not None:
        state["parent_entity_id"] = get_parent_id_from_name(state.get("parent_entity_id"))
        if not state.get("parent_entity_id"):
            raise Exception("State with given parent_entity_id: "+state.get("parent_entity_id") +" was not found")
        if state.get("states"):
            if is_state_details:
                states=[]
                for rec in state.get("states") :
                    rec["parent_entity_id"] = get_parent_id_from_name(rec.get("parent_entity_id")) 
                    states.append(rec) 
                state["states"]=states   
    return state    

def convert_parent_to_states(state):
    if state is not None:
        if state.get("states"):
            states=[]
            for rec in state.get("states") :
                inner_state=statedb.get_state_by_parent_entity_id_name(rec.get("name"),rec.get("parent_entity_id") , False)
                if inner_state:
                    states.append(str(inner_state.get("_id")))
                else:
                    raise Exception("State with given parent_entity_id: "+rec.get("parent_entity_id") + " and State Name: "+rec.get("name")+" was not found")
            state["states"]=states    
    return state    

def convert_parent_ids_to_name(state_data):
    #state.get("parent_entity_id") is the id of parent here
    if state_data:
        state_data["parent_entity_id"]=get_parent_name_from_id(state_data.get("parent_entity_id"))
        if not state_data.get("parent_entity_id"):
            raise Exception("State with given parent_entity_id: "+state_data.get("parent_entity_id") +" was not found")
        if(state_data.get("states")):
            childstates=[]
            for rec in state_data.get("states"):
                childstate={}
                child_state_data=statedb.get_state_by_id(rec, False)
                if not child_state_data:
                    raise Exception("State with given _id: "+rec +" was not found")
                childstate["name"] = child_state_data.get("name")
                childstate["parent_entity_id"]=get_parent_name_from_id(child_state_data.get("parent_entity_id")) 
                childstates.append(childstate)
            state_data["states"]=childstates
  