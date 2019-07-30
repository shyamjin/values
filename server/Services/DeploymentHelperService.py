'''
Created on Mar 8, 2018

@author: pdinda
'''
from DBUtil import DeploymentRequest, ToolsOnMachine,Build, State, DeploymentUnitSet
from settings import mongodb
statedb = State.State(mongodb)
deploymentUnitSetdb=DeploymentUnitSet.DeploymentUnitSet()


deploymentRequestDb = DeploymentRequest.DeploymentRequest(mongodb)
toolsonmachinedb = ToolsOnMachine.ToolsOnMachine(mongodb)
buildDB = Build.Build()

def check_if_revert_undeploy_allwed_for_group(deployment_request_group_data):
    """This def is responsible to decide if a Group Deployment is valid to Revert or un deploy"""
    deployment_request_group_data["allow_revert"] = False
    deployment_request_group_data["allow_undeploy"] = False 
    deployment_request_group_data["allow_retry"] = False    
    try:        
        #DECIDE IF RETRY IS ALLOWED
        # IF one of the deployments of this request is failed it should be allowed to retry
        if str(deployment_request_group_data.get("status")).lower() == "failed":    
            deployment_request_group_data["allow_retry"] = True         
        elif str(deployment_request_group_data.get("status")).lower() == "done":
            # I REQUEST CAN BE ALLOWED TO UNDEPLOYED ONLY IF IT WAS DEPLOYED OR REDEPLOYED
            if deployment_request_group_data.get("request_type").lower() not in ["undeploy"]:
                deployment_request_group_data["allow_undeploy"] = True
            # REVERT IS ALLOWED ONLY IF IT WAS DEPLOYED USING PACKAGE STATE for DU_GROUP
            if deployment_request_group_data.get("package_state_id") is not None or deployment_request_group_data.get("parent_entity_set_id") is not None:                                
                # do this if deployed with specified state                
                du_package_id = deployment_request_group_data.get("parent_entity_set_id")                
                deployed_set_state = statedb.get_state_by_id(deployment_request_group_data.get("package_state_id"), False)
                all_set_states = statedb.get_state_by_parent_entity_id(du_package_id, False)
                for state in all_set_states:
                        if (deployed_set_state.get("_id").generation_time.replace(tzinfo=None) > state.get("_id").generation_time.replace(tzinfo=None)):
                            deployment_request_group_data["allow_revert"] = True
                            break                                                           
            # do this if deployed with specified builds
            for dep in deployment_request_group_data.get("details"):
                dep_details=deploymentRequestDb.GetDeploymentRequest(dep.get("deployment_id"))
                # IF THE DEP REQUEST IS NOT PRESENT WE CANNOT SUPPORT ANYTHING
                if not dep_details:raise Exception("")
                # IF THERE WAS A DEPLOYMENT WITH EXACT SAME DETAILS ONLY deployment_id will be diffrent.We cannot allow this situation
                if not toolsonmachinedb.get_tools_on_machine_by_filter\
                            (dep_details.get("machine_id"), dep_details.get("parent_entity_id"), dep_details.get("build_id"),dep.get("deployment_id")):
                    raise Exception("")          
    except Exception:  # catch *all* exceptions
        deployment_request_group_data["allow_revert"] = False
        deployment_request_group_data["allow_undeploy"] = False 
    return deployment_request_group_data
