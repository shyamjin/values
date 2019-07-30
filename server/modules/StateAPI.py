import json
import re
from bson.json_util import dumps
from flasgger import swag_from, validate, ValidationError
from flask import Blueprint, jsonify, request
from DBUtil import State,DeploymentUnitApprovalStatus,DeploymentFields,DeploymentUnit,DeploymentUnitSet,Build
from Services import HelperServices,StateHelperService
from Services.AppInitServices import authService
from settings import mongodb, relative_path


# blueprint declaration
stateAPI = Blueprint('stateAPI', __name__)
# get global db connection
db = mongodb

# collection
statedb = State.State(db)
deploymentUnitApprovalStatusdb=DeploymentUnitApprovalStatus.DeploymentUnitApprovalStatus()
deploymentFieldsdb=DeploymentFields.DeploymentFields(db)
deploymentUnitdb=DeploymentUnit.DeploymentUnit()
deploymentUnitSetdb=DeploymentUnitSet.DeploymentUnitSet()
buildDB = Build.Build()


'''
{
    "data": {
        "page_total": 2,
        "total": 2,
        "data": [
            {
                "build_id": "59fae88cf6a8881077056569",
                "name": "Test 100 State-539",
                "parent_entity_id": "59fac998721561006abadb9b",
                "parent_entity_name": "Test 100",
                "_id": {
                    "$oid": "5a3b9b16f913e73f0852811c"
                },
                "type": "dustate",
                "approval_status": "Created"
            },
            {
                "name": "sfdf",
                "parent_entity_id": "5a31307293f4850065519eca",
                "states": [
                    "5a3b9b16f913e73f0852811c"
                ],
                "parent_entity_name": "JIn Test",
                "_id": {
                    "$oid": "5a3b9b16f913e73f0852811e"
                },
                "type": "dusetstate",
                "approval_status": "Tested"
            }
        ],
        "page": 0
    },
    "result": "success"
}
'''

@stateAPI.route('/state/all/', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/StateAPI/getAllStates.yml')
def get_all_states(): 
    
    type_filter=[]
    approval_status_filter = []
    parent_filter = []
    du_filter = []
    build_id_filter = []
    state_name_filter = []
    if request.args.get('type', None):
        type_filter = request.args.get('type', None).split(",")
        if "any" in type_filter:
            type_filter = None
    if request.args.get('build_id', None):
        build_id_filter = request.args.get('build_id', None).split(",")
        if "any" in build_id_filter:
            build_id_filter = None
    if request.args.get('name', None):
        state_name_filter = request.args.get('name', None).split(",")
        if "any" in state_name_filter:
            state_name_filter = None
    if request.args.get('approval_status', None):
        approval_status_filter = request.args.get('approval_status', None).split(",")  
        if "any" in approval_status_filter:
            approval_status_filter = None
    if request.args.get('parent_entity_id', None):
        parent_filter = request.args.get('parent_entity_id', None).split(",")  
        if "any" in parent_filter:
            parent_filter = None
    if request.args.get('du_id', None):
        du_filter = request.args.get('du_id', None).split(",")  
        if "any" in du_filter:
            du_filter = None     
    limit = int(request.args.get('perpage', "30"))
    page = int(request.args.get('page', "0"))
    skip = page * limit
    filter_req={}
    if state_name_filter:
        list_of_names = []
        for name in state_name_filter: list_of_names.append(re.compile(name, re.IGNORECASE)) 
        filter_req.update({"name": {"$in": list_of_names}})
    if build_id_filter:
        filter_req.update({"build_id": {"$in": build_id_filter}})  
    states = statedb.get_state_all(False,type_filter,parent_filter,skip,limit,filter_req)        
    total_count_of_state_in_page=0
    total_count_of_state_in_db=len(list(statedb.get_state_all(False,type_filter)))        
    final_data = []        
    for state in states:
        if(HelperServices.filter_handler(state,approval_status_filter,[state.get("approval_status")],"approval_status")):
            continue
        StateHelperService.get_names_from_ids(state , False)
        total_count_of_state_in_page+=1                    
        if len(du_filter) > 0:                
            for state_id in state["states"]:
                state_data = statedb.get_state_by_id(state_id, True)                                    
                if state_data["parent_entity_id"] in du_filter:
                    if state not in final_data:
                        final_data.append(state)
        else:
            final_data.append(state)        
    return jsonify(json.loads(dumps({"result": "success", "data": {"data": final_data,"page": page, "total": total_count_of_state_in_db, "page_total": total_count_of_state_in_page}}))), 200

'''
DU STATE
{
    "name": "Test",# OPTIONAL # AUTO GENERATED
    "parent_entity_id": "59ddcf802646eb006a6c7707",
    "build_id": "59fae87df6a8881077056568",
    "approval_status": "Created",
    "deployment_field": {"fields": [{
        "default_value": "2017-10-18T18:30:00.000Z",
        "is_mandatory": true,
        "order_id": 0,
        "input_type": "date",
        "tooltip": "hkhk",
        "input_name": "kuk"
    }]}
}


DU PACKAGE STATE
{
    "name":"sfdf",# OPTIONAL # AUTO GENERATED
    "parent_entity_id": "5a31307293f4850065519eca",
    "approval_status": "Tested",# OPTIONAL # AUTO ASSIGNED AS 'CREATED'
    "states": [
        {
            "build_id":"59fae88cf6a8881077056569",
            "name":"Hello"
        },
        {
            "build_id":"59fae88cf6a8881077056569",
            "name":"",# OPTIONAL # AUTO GENERATED
            "deployment_field":{"hi":"hellow"} #OPTIONAL
        }
    ]
}
'''
@stateAPI.route('/state/add', methods=['POST'])
@authService.authorized
@swag_from(relative_path + '/swgger/StateAPI/addStates.yml')
def add_state():
    try:
        state_id=None
        deployment_fields_data=None
        deployment_fields_id=None
        states_to_rollback=[]
        parent_entity_id_list=[]  
        data = request.json
        validate(data, 'State', relative_path +
                 '/swgger/StateAPI/addStates.yml')
        state_data = request.get_json()
        StateHelperService.check_state_mandate_fields(state_data)
        if state_data.get("deployment_field") and len(state_data.get("deployment_field").get("fields",[])) > 0:
            deployment_fields_data=state_data.get("deployment_field")
        else:deployment_fields_data=deploymentFieldsdb.GetDeploymentFields(state_data.get("parent_entity_id"))
        for idx, item in enumerate(state_data.get("states",[])):
            if isinstance(item,dict):
                build_details=buildDB.get_build_by_id(item.get("build_id"), False)
                if build_details:
                    state_data["states"][idx]=StateHelperService.generate_new_state({"build_id":str(build_details.get("_id")),\
           "name":item.get("name"),"parent_entity_id":build_details.get("parent_entity_id"),"deployment_field":item.get("deployment_field")})
                    parent_entity_id_list.append(build_details.get("parent_entity_id"))
                    states_to_rollback.append(state_data["states"][idx])
                else:
                    raise Exception("Invalid build_id:"+str(item.get("build_id")))    
            elif statedb.get_state_by_id(item):
                parent_entity_id_list.append(statedb.get_state_by_id(item).get("parent_entity_id"))
            else:
                raise Exception("Invalid build_id/state_id: "+item) 
        duplicates=[x for x in parent_entity_id_list if parent_entity_id_list.count(x) > 1]    
        if  len(duplicates) >0:
            raise Exception("More than one state request was found for parent_entity_id:"+",".join(list(set(duplicates))))                  
        state_id = StateHelperService.add_update_state(state_data, None)        
        if deployment_fields_data:
            deployment_fields_id=HelperServices.add_update_deployment_fields(deployment_fields_data.get("fields"), str(state_id))        
        return jsonify(json.loads(dumps({"result": "success", "message": "State created successfully", "data": {"_id": state_id }}))), 200
    except Exception as e:  # catch *all* exceptions
        for new_state_id in states_to_rollback:
            StateHelperService.delete_state(new_state_id)
        if state_id is not None:
            StateHelperService.delete_state(state_id)
        if deployment_fields_id is not None:
            deploymentFieldsdb.DeleteDeploymentFields(deployment_fields_id)
        raise e


'''
DU STATE
{
    "_id":{"oid":"5a31307293f4850065519eca"},
    "approval_status": "Created",
    "deployment_field": {"fields": [{
        "default_value": "2017-10-18T18:30:00.000Z",
        "is_mandatory": true,
        "order_id": 0,
        "input_type": "date",
        "tooltip": "hkhk",
        "input_name": "kuk"
    }]}
}


DU PACKAGE STATE
{
    "_id":{"oid":"5a31307293f4850065519eca"},
    "approval_status": "Tested"    
}
'''
@stateAPI.route('/state/update', methods=['PUT'])
@authService.authorized
@swag_from(relative_path + '/swgger/StateAPI/updateState.yml')
def update_state():
    deployment_fields_data=None
    keys_allowed_to_update=["deployment_field","approval_status","_id"]
    data = request.json
    validate(data, 'UpdateStateData', relative_path +
             '/swgger/StateAPI/updateState.yml')
    state = request.get_json()
    for key in state.keys():
        if key not in keys_allowed_to_update:
            state.pop(key)            
    if(state.get("deployment_field") is not None):
        deployment_fields_data=state.get("deployment_field")       
    StateHelperService.add_update_state(state, state.get("_id").get("oid"))        
    if(deployment_fields_data is not None):
        HelperServices.add_update_deployment_fields(deployment_fields_data.get("fields"), str(state.get("_id").get("oid")))
    return jsonify(json.loads(dumps({"result": "success", "message": "State was updated successfully"}))), 200

'''
DU STATE

{
    "data": {
        "build_id": "59fae88cf6a8881077056569",
        "parent_entity_name": "Test 100",
        "name": "Test 100 State 1",
        "deployment_field": {
            "fields": [],
            "_id": {"$oid": "5a337de9256527006c43fb66"},
            "parent_entity_id": "5a337de9256527006c43fb65"
        },
        "parent_entity_id": "59fac998721561006abadb9b",
        "build": {
            "status": "1",
            "build_date": {"$date": 1498056529999},
            "build_number": 290,
            "package_name": "usage_hourly_processing_statistics_ga_9_18.zip",
            "package_type": "zip",
            "parent_entity_id": "59fac998721561006abadb9b",
            "additional_info": {
                "repo_id": "vp_builds",
                "package": "amdocs.reports",
                "file_name": "usage_hourly_processing_statistics-ga_9-18.zip",
                "artifact": "usage_hourly_processing_statistics",
                "relative_path": "vp_builds/amdocs/reports/usage_hourly_processing_statistics/ga_9",
                "version": "ga_9",
                "release_notes": "urly_processing_statistics_ga_9_18"
            },
            "file_size": "20K",
            "_id": {"$oid": "59fae88cf6a8881077056569"},
            "type": "url",
            "file_path": "http://illin4490:8081/nexus/service/local/repositories/vp_builds/content/test/test/1/test-1.zip"
        },
        "_id": {"$oid": "5a337de9256527006c43fb65"},
        "type": "dustate",
        "approval_status": "Created"
    },
    "result": "success"
}

DU SET STATE

{
    "data": {
        "name": "Jin DUSET StateSet",
        "deployment_field": null,
        "parent_entity_id": "5a31307293f4850065519eca",
        "states": [
            {
                "build_id": "59fae88cf6a8881077056569",
                "name": "Test 100 State 1",
                "deployment_field": {
                    "fields": [],
                    "_id": {"$oid": "5a337de9256527006c43fb66"},
                    "parent_entity_id": "5a337de9256527006c43fb65"
                },
                "parent_entity_id": "59fac998721561006abadb9b",
                "build": {
                    "status": "1",
                    "build_date": {"$date": 1498056529999},
                    "build_number": 290,
                    "package_name": "usage_hourly_processing_statistics_ga_9_18.zip",
                    "package_type": "zip",
                    "parent_entity_id": "59fac998721561006abadb9b",
                    "additional_info": {
                        "repo_id": "vp_builds",
                        "package": "amdocs.reports",
                        "file_name": "usage_hourly_processing_statistics-ga_9-18.zip",
                        "artifact": "usage_hourly_processing_statistics",
                        "relative_path": "vp_builds/amdocs/reports/usage_hourly_processing_statistics/ga_9",
                        "version": "ga_9",
                        "release_notes": "urly_processing_statistics_ga_9_18"
                    },
                    "file_size": "20K",
                    "_id": {"$oid": "59fae88cf6a8881077056569"},
                    "type": "url",
                    "file_path": "http://illin4490:8081/nexus/service/local/repositories/vp_builds/content/test/test/1/test-1.zip"
                },
                "_id": {"$oid": "5a337de9256527006c43fb65"},
                "type": "dustate",
                "approval_status": "Created"
            },
            {
                "build_id": "59fae88cf6a8881077056569",
                "name": "Test 100 State 2",
                "deployment_field": {
                    "fields": [],
                    "_id": {"$oid": "5a337df6256527006c43fb68"},
                    "parent_entity_id": "5a337df6256527006c43fb67"
                },
                "parent_entity_id": "59fac998721561006abadb9b",
                "build": {
                    "status": "1",
                    "build_date": {"$date": 1498056529999},
                    "build_number": 290,
                    "package_name": "usage_hourly_processing_statistics_ga_9_18.zip",
                    "package_type": "zip",
                    "parent_entity_id": "59fac998721561006abadb9b",
                    "additional_info": {
                        "repo_id": "vp_builds",
                        "package": "amdocs.reports",
                        "file_name": "usage_hourly_processing_statistics-ga_9-18.zip",
                        "artifact": "usage_hourly_processing_statistics",
                        "relative_path": "vp_builds/amdocs/reports/usage_hourly_processing_statistics/ga_9",
                        "version": "ga_9",
                        "release_notes": "urly_processing_statistics_ga_9_18"
                    },
                    "file_size": "20K",
                    "_id": {"$oid": "59fae88cf6a8881077056569"},
                    "type": "url",
                    "file_path": "http://illin4490:8081/nexus/service/local/repositories/vp_builds/content/test/test/1/test-1.zip"
                },
                "_id": {"$oid": "5a337df6256527006c43fb67"},
                "type": "dustate",
                "approval_status": "Created"
            }
        ],
        "parent_entity_name": "JIn Test",
        "_id": {"$oid": "5a337e10256527006c43fb69"},
        "type": "dusetstate",
        "approval_status": "Tested"
    },
    "result": "success"
}

'''

@stateAPI.route('/state/view/<string:state_id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/StateAPI/getStateById.yml')
def get_state_id(state_id):    
    state = statedb.get_state_by_id(state_id, True)
    StateHelperService.get_names_from_ids(state , True)
    return jsonify(json.loads(dumps({"result": "success", "data": state}))), 200
    
@stateAPI.route('/state/view/parent/<string:parent_entity_id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/StateAPI/getStateByParentEntityId.yml')
def get_state_parent_entity_id(parent_entity_id):
    states = statedb.get_state_by_parent_entity_id(parent_entity_id,True)
    final_state=[]
    for state in states:
        StateHelperService.get_names_from_ids(state , True)
        final_state.append(state)
    return jsonify(json.loads(dumps({"result": "success", "data": states}))), 200

@stateAPI.route('/state/view/parent/<string:parent_entity_id>/name/<string:name>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/StateAPI/getStateByParentEntityIdName.yml')
def get_state_parent_entity_id_name(parent_entity_id,name):
    state = statedb.get_state_by_parent_entity_id_name(name, parent_entity_id, True)
    StateHelperService.get_names_from_ids(state ,True)
    return jsonify(json.loads(dumps({"result": "success", "data": state}))), 200


@stateAPI.route('/state/delete/<string:state_id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/StateAPI/deleteStateByStateId.yml')
def delete_state(state_id):
    res=StateHelperService.delete_state(state_id)
    deploymentFieldsdb.delete_dep_field_by_parent_entity_id(state_id)
    if(res is 1):  
        return jsonify(json.loads(dumps({"result": "success" ,"message": "State deleted"}))), 200
    else:
        raise Exception ("Unable to delete the state : "+state_id)
