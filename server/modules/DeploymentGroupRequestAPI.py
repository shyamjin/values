import copy
from datetime import datetime
import traceback,json
from bson.json_util import dumps
from flasgger import swag_from, validate
from flask_restplus import Resource
from flask import Blueprint, jsonify, request
from DBUtil import DeploymentRequest, DeploymentRequestGroup, Machine,\
 Versions, MachineGroups, ToolSet, Tool, Counter,Build,DeploymentUnit,DeploymentUnitSet,Users,State
from Services import DeploymentRequestService,\
    HelperServices, BuildHelperService, DeploymentHelperService,StateHelperService,\
    CustomClassLoaderService
from Services.AppInitServices import authService
from settings import mongodb, relative_path
from modules.apimodels.Restplus import api, header_parser
from modules.apimodels import DeploymentGroupModel


# blueprint declaration
deploymentgrouprequestAPI = Blueprint('deploymentgrouprequestAPI', __name__)
#restplus
deploymentgrouprequestAPINs = api.namespace('deploymentrequestgroup', \
                                            description='Group Deployment Operations',path="/deploymentrequest/group")

# get global db connection
db = mongodb

# collections
deploymentRequestDB = DeploymentRequest.DeploymentRequest(db)
deploymentRequestGroupDB = DeploymentRequestGroup.DeploymentRequestGroup(db)
machineDB = Machine.Machine(db)
versionsDB = Versions.Versions(db)
machinegroupsDB = MachineGroups.MachineGroups(db)
toolSetDB = ToolSet.ToolSet(db)
deploymentRequestService = DeploymentRequestService.DeploymentRequestService(db)
toolDB = Tool.Tool(db)
CounterDB = Counter.Counter(db)
buildDB = Build.Build()
deploymentUnitdb=DeploymentUnit.DeploymentUnit()
deploymentUnitSetdb=DeploymentUnitSet.DeploymentUnitSet()
userDB = Users.Users(db)
statedb = State.State(db)


@deploymentgrouprequestAPI.route('/deploymentrequest/group/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentGroupRequestAPI/getAllGroupDeploymentRequests.yml')
def getAllGroupDeploymentRequests():
    
    list = {}
    filter_condition = {}
    parent_entity_id_list = []
    if request.args.get('scheduled_date', None):
        start_date = datetime.strptime(
            request.args.get('scheduled_date', None).split(".")[0], "%Y-%m-%d")
        end_date_str = request.args.get('scheduled_date') + " 23:59:59" 
        end_date = datetime.strptime(
            end_date_str.split(".")[0], "%Y-%m-%d %H:%M:%S")
        filter_condition["scheduled_date"] = {'$gt': start_date, '$lt': end_date}
    if request.args.get('create_date', None):
        start_date = datetime.strptime(
            request.args.get('create_date', None).split(".")[0], "%Y-%m-%d")
        end_date_str = request.args.get('create_date') + " 23:59:59" 
        end_date = datetime.strptime(
            end_date_str.split(".")[0], "%Y-%m-%d %H:%M:%S")
        filter_condition["create_date"] = {'$gt': start_date, '$lt': end_date}
    if request.args.get('machine_id', None):
        machine_list = request.args.get("machine_id").split(",")
        filter_condition["details.machine_id"] = {"$in" : machine_list}
    if request.args.get('requested_by', None):
        requested_by_list = request.args.get("requested_by").split(",")
        filter_condition["requested_by"] = {"$in" : requested_by_list}
    if request.args.get('du_id', None):
        parent_entity_id_list = request.args.get("du_id").split()
    limit = int(request.args.get('perpage', "50"))
    page = int(request.args.get('page', "0"))
    skip = page * limit        
    detailsRequired = str(request.args.get('details', 'false')).lower() == "true"
    sortedRequired = str(request.args.get('sorted', 'false')).lower() == "true"
    deployment_request_group_list = deploymentRequestGroupDB.get_all_group_deployment_request(
        filter_condition,{"_id":1,"create_date":1,"name":1,"status":1}, parent_entity_id_list, detailsRequired, skip, limit)
    total_count_of_dep_in_page = len(deployment_request_group_list)
    total_count_of_dep_in_db = deploymentRequestGroupDB.get_all_group_depreq_count()
    data = {"list": deployment_request_group_list, "requests_count": {},
                                                                            "total": total_count_of_dep_in_db,
                                                                            "page_total": total_count_of_dep_in_page, 
                                                                            "page": page}
    if sortedRequired:
        for rec in deployment_request_group_list:
            if str(rec['_id'].generation_time.replace(tzinfo=None).date()) not in list.keys():
                list[str(rec['_id'].generation_time.replace(
                    tzinfo=None).date())] = []
                list[str(rec['_id'].generation_time.replace(
                    tzinfo=None).date())].append(rec)
            else:
                list[str(rec['_id'].generation_time.replace(
                    tzinfo=None).date())].append(rec)

                # NEW FORMAT FOR NEW GUI
        data["list"] = list

    return jsonify(json.loads(dumps({"result": "success", "data": data}))), 200


@deploymentgrouprequestAPI.route('/deploymentrequest/group/saved/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentGroupRequestAPI/get_all_saved_group_deployment_requests.yml')
def get_all_saved_group_deployment_requests():
        deployment_request_group_list = deploymentRequestGroupDB.get_all_saved_group_deployment_request()
        deployment_request_group_list_final = {}
        deployment_request_group_list_final["toolgroup"] = {}
        deployment_request_group_list_final["dugroup"] = {}
        
        for rec in deployment_request_group_list:                        
            if rec["deployment_type"] == 'toolgroup':
                if str(rec['_id'].generation_time.replace(tzinfo=None).date()) not in deployment_request_group_list_final["toolgroup"].keys():
                    deployment_request_group_list_final["toolgroup"][str(rec['_id'].generation_time.replace(
                        tzinfo=None).date())] = []
                    deployment_request_group_list_final["toolgroup"][str(rec['_id'].generation_time.replace(
                        tzinfo=None).date())].append(rec)
                else:
                    deployment_request_group_list_final["toolgroup"][str(rec['_id'].generation_time.replace(
                        tzinfo=None).date())].append(rec)                    
            else:
                if str(rec['_id'].generation_time.replace(tzinfo=None).date()) not in deployment_request_group_list_final["dugroup"].keys():
                    deployment_request_group_list_final["dugroup"][str(rec['_id'].generation_time.replace(
                        tzinfo=None).date())] = []
                    deployment_request_group_list_final["dugroup"][str(rec['_id'].generation_time.replace(
                        tzinfo=None).date())].append(rec)
                else:
                    deployment_request_group_list_final["dugroup"][str(rec['_id'].generation_time.replace(
                        tzinfo=None).date())].append(rec)                
        return jsonify(json.loads(dumps({"result": "success", "data": {"list": deployment_request_group_list_final, "requests_count": {"saved": deployment_request_group_list.count()}}}))), 200


@deploymentgrouprequestAPI.route('/deploymentrequest/group/saved/view/<string:group_id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentGroupRequestAPI/get_saved_group_deployment_request_by_id.yml')
def get_saved_group_deployment_request_by_id(group_id):
    return jsonify(json.loads(dumps({"result": "success", "data": deploymentRequestGroupDB.get_group_deployment_request(group_id,False,False)}))), 200


@deploymentgrouprequestAPI.route('/deploymentrequest/group/saved/add', methods=['POST'])
@authService.authorized
def add_saved_group_deployment_requests():
    request_data = request.get_json()
    request_data["status"] = "Saved"
    if "name" not in request_data.keys():
        request_data["name"] = "Deployment Group " + \
            CounterDB.get_counter()
    return jsonify(json.loads(dumps({"result": "success", "data": deploymentRequestGroupDB.add_request(request_data)}))), 200


@deploymentgrouprequestAPI.route('/deploymentrequest/group/saved/update', methods=['PUT'])
@authService.authorized
def update_saved_group_deployment_requests():
    request_data = request.get_json()
    if request_data.get("_id") is None:
        raise ValueError("Required filed _id was no found in request")
    request_data["status"] = "Saved"
    dep_grp_data = deploymentRequestGroupDB.get_group_deployment_request(
        request_data["_id"]["oid"],False,False)
    if dep_grp_data and str(dep_grp_data.get("status")).lower() == "saved":
        if deploymentRequestGroupDB.upd_group_depreq(request_data) == 1:
            return jsonify(json.loads(dumps({"result": "success", "message": "The request was updated successfully", "data": 1}))), 200
        else:
            raise ValueError("No difference found")
    else:
        if not dep_grp_data:
            raise ValueError("No such request found")
        else:
            raise ValueError(
                "Cannot update this record as its not in Saved status")

@deploymentgrouprequestAPI.route('/deploymentrequest/group/saved/delete/<string:group_id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentGroupRequestAPI/delete_saved_group_deployment_requests.yml')
def delete_saved_group_deployment_requests(group_id):
    return jsonify(json.loads(dumps({"result": "success", "data": deploymentRequestGroupDB.cancel_grpdep_req(group_id)}))), 200


@deploymentgrouprequestAPI.route('/deploymentrequest/group/view/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentGroupRequestAPI/getGroupDeploymentRequestByID.yml')
def getGroupDeploymentRequestByID(id):
    deployment_request_group_data = deploymentRequestGroupDB.get_group_deployment_request(
        str(id), True,False)

    if not deployment_request_group_data:
        raise ValueError("GroupDeployment request with _id: " +
                         id + " was not found in database")
    # ADD STATUS COUNT FOR INNER DEPLOYMENTS# INITIALIZE COUNT
    innerFailedCount = 0
    innerInprogressCount = 0
    innerCompletedCount = 0
    innerRetryCount = 0
    innerNewCount = 0
    inner_skipped_count = 0
    for inner_rec in deployment_request_group_data.get("details"):
        # SET STATUS COUNT
        if "Retry".lower() in str(inner_rec.get("status")).lower():
            innerRetryCount = innerRetryCount + 1
        elif "Failed".lower() in str(inner_rec.get("status")).lower():
            innerFailedCount = innerFailedCount + 1
        elif "Done".lower() in str(inner_rec.get("status")).lower():
            if str(inner_rec.get("skipped_ind",False)).lower() == "true":
                inner_skipped_count+=1
            else:    
                innerCompletedCount = innerCompletedCount + 1
        elif "Processing".lower() in str(inner_rec.get("status")).lower():
            innerInprogressCount = innerInprogressCount + 1
        elif "New".lower() in str(inner_rec.get("status")).lower():
            innerNewCount = innerNewCount + 1

    deployment_request_group_data["requests_count"] = {"failed": innerFailedCount,
                                                       "inprogress": innerInprogressCount,
                                                       "retry": innerRetryCount,
                                                       "new": innerNewCount,
                                                       "done": innerCompletedCount,
                                                       "skipped":inner_skipped_count}
    
    #CHECK if revert undeploy is allowed
    DeploymentHelperService.check_if_revert_undeploy_allwed_for_group(deployment_request_group_data)
    if deployment_request_group_data.get("package_state_id"):
        package_state = statedb.get_state_by_id(deployment_request_group_data.get("package_state_id"), False)
        if package_state:deployment_request_group_data["package_state_name"] = package_state["name"]
        if deployment_request_group_data.get("parent_entity_set_id"):
                du_package = deploymentUnitSetdb.GetDeploymentUnitSetById(deployment_request_group_data.get("parent_entity_set_id"), False)
                if du_package:deployment_request_group_data["parent_entity_set_name"] = du_package["name"]
    return jsonify(json.loads(dumps({"result": "success", "data": deployment_request_group_data}))), 200


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")


'''FORMAT
{"deployment_requests": [{
    "parent_entity_id": "59fac998721561006abadb9b",
    "requested_by": "Admin",
    "request_type": "deploy",
    "deployment_type": "dugroup",
    "requests": [{
        "machine_id": "5a292a95f913e733dc0e8520",
        "tool_deployment_value": [
            {
                "input_name": "gfh",
                "input_type": "text",
                "input_value": "gfh",
                "order_id": 0
            }
        ],
        "warning_flag": false
    }],
    "scheduled_date": "2017-12-11T10:03:18.043Z"
}]}
'''
@deploymentgrouprequestAPI.route('/deploymentrequest/group/add', methods=['POST'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentGroupRequestAPI/addGroupDeploymentRequest.yml')
def addGroupDeploymentRequest():
    requests_list = []
    newGroupDeploymentRequest = request.get_json()
    for rec in newGroupDeploymentRequest.get(
            "deployment_requests"):
        outerRequest = copy.deepcopy(rec)
        if "requests" in outerRequest.keys():
            innerRequest = None
            innerRequest = outerRequest.get("requests")
            if innerRequest and type(innerRequest) is list:
                outerRequest.pop("requests")
                for innerData in innerRequest:
                    finalData = None
                    finalData = copy.deepcopy(outerRequest)
                    finalData.update(innerData)
                    requests_list.append(finalData)                      
            else:
                raise Exception("requests should be of type list")
        else:
            raise Exception(
                "List of requests machines was not found in given input")
    return jsonify(json.loads(dumps({"result": "success", "message": "New GroupDeployment request has been added successfully",\
                   "data": {"id": add_request(requests_list)}}))), 200

def verify_deployment_request(req):
    # CHECK IF parent_entity_id is valid
    parent_entity = HelperServices.get_details_of_parent_entity_id(req.get("parent_entity_id"))
    deployer_module="Plugins.deploymentPlugins."+parent_entity.get("deployer_to_use")
    class_obj=CustomClassLoaderService.get_class(deployer_module)
    if "verify_deployment_request" in dir(class_obj):       
        method = getattr(class_obj(None),"verify_deployment_request") # MEDHOD NAME
        keyargs={"input_dep_request_dict":req}
        method(**keyargs)

def verify_group_deployment_request(group_request):
    # CHECK IF parent_entity_id is valid
    parent_entity = HelperServices.get_details_of_parent_entity_id(group_request[0].get("parent_entity_id"))
    deployer_module="Plugins.deploymentPlugins."+parent_entity.get("deployer_to_use")
    class_obj=CustomClassLoaderService.get_class(deployer_module)
    if "verify_group_deployment_request" in dir(class_obj):
        method = getattr(class_obj(None),"verify_group_deployment_request") # MEDHOD NAME
        keyargs={"input_group_dep_request_dict":group_request}
        method(**keyargs)
    else:
        print "Skipping step : verify group deployment request as method doesn't exists in "+parent_entity.get("deployer_to_use")
def add_request(requests_list):
    ids_list=[]
    group_status_details = []
    try:
        #Check while adding new group deployment req to database    
        verify_group_deployment_request(requests_list)
        for req in requests_list:            
            for rec in ["requested_by","parent_entity_id","deployment_type",\
                        "scheduled_date" ,"request_type"]:
                if not rec in req.keys(): raise ValueError("Mandatory key: "+rec+" was not found in request")
            finalData = handle_dependent_and_order(req) #ADD MMISSING DEPLOYMENT ORDER
            #CHECK if build_id is valid or assign new build
            get_build_for_parent(finalData)            
            #Check while adding new deployment req to database    
            verify_deployment_request(req)
            
            
        #START ADDING
        for req in requests_list:   
            try:
                dep_id=str(deploymentRequestDB.AddDeploymentRequest(req))
            except Exception as ex:
                if req.get("parent_entity_id"): 
                    parent_details = HelperServices.get_details_of_parent_entity_id(req.get("parent_entity_id"))
                    if parent_details:
                        raise Exception("For entity "+str(parent_details.get("name","Unknown"))+" :"+str(ex))
                raise ex        
       
            ids_list.append(dep_id)
            group_status_details.append({"deployment_id": dep_id, "machine_id": req.get(
                                "machine_id"), "status": "New", "status_message": "The request is accepted",\
                                "deployment_order": int(req.get("deployment_order")), "dependent": req.get("dependent")})
        newGroupDeploymentRequest = {
            "deployment_type": str(req.get("deployment_type")).lower(), "details": group_status_details,\
             "requested_by": req.get("requested_by"), "name": "Deployment Group " + CounterDB.get_counter(),\
              "scheduled_date": req.get("scheduled_date"),"request_type":str(req.get("request_type"))}
        
        if req.get("callback_url"):
            newGroupDeploymentRequest["callback"]= { "callback_url": str(req.get("callback_url")) }
        # ADD ADDITIONAL KEYS    
        for key_to_add in ["parent_entity_set_id","package_state_id","machine_group_id"]:
            if key_to_add in req.keys(): newGroupDeploymentRequest[key_to_add]=str(req.get(key_to_add))
        return deploymentRequestGroupDB.add_new_grp_depreq(newGroupDeploymentRequest)
    except Exception as e:  # catch *all* exceptions
        print "Error :" + str(e)
        traceback.print_exc()
        # REMOVE ALREADY ADDED REQUESTS
        for rec in ids_list:
            deploymentRequestDB.CancelDeploymentRequest(rec)
        raise e       
        

def get_build_for_parent(finalData):
    build_details=BuildHelperService.get_build_for_parent(finalData.get("parent_entity_id"),\
                                                       finalData.get("build_id"), finalData.get("state_id"),finalData.get("build_number"))
    if build_details:
        finalData["build_id"]=str(build_details["_id"])
        finalData["build_number"]=build_details["build_number"]
    else:
        raise Exception("Unable to find build details for parent_entity_id: "\
                        +str(finalData.get("parent_entity_id")))   
        
def handle_dependent_and_order(newDeploymentRequest):
    deployment_type = str(newDeploymentRequest.get("deployment_type")).lower()
    if deployment_type in ["none", None, ""]:
        raise ValueError("Request is missing value for deployment_type")
    if newDeploymentRequest.get("deployment_order") is None:
        newDeploymentRequest["deployment_order"] = 0
    if newDeploymentRequest.get("dependent") is None:
        newDeploymentRequest["dependent"] = "false"
    return newDeploymentRequest


@deploymentgrouprequestAPI.route('/deploymentrequest/group/retry', methods=['PUT'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentGroupRequestAPI/retryGroupDeploymentRequest.yml')
def retryGroupDeploymentRequest():
    data = request.json
    validate(data, 'Retry', relative_path +
             '/swgger/DeploymentGroupRequestAPI/retryGroupDeploymentRequest.yml')
    DeploymentRequest = request.get_json()
    dep_id = DeploymentRequest.get("_id")
    if dep_id is None:
        raise Exception("_id is missing")
    oid = dep_id.get("oid")
    if oid is None:
        raise Exception("oid is missing")
    data = deploymentRequestGroupDB.get_group_deployment_request(str(oid), False,False)
    details = data.get("details")
    if data is None:
        raise Exception("Request was not found")
    if data.get('status').lower() != 'failed':
        raise Exception("Only failed request can be retried")
    retryCount = data.get("retry_count")
    if retryCount is None:
        retryCount = "1"
    else:
        retryCount = str(int(retryCount) + 1)
    data = {}
    data["_id"] = DeploymentRequest["_id"]
    data["retry_count"] = retryCount
    data["status"] = "Retry"  # GETS UPDATED WITH METHOD
    # update_DeploymentGroups
    updated = deploymentRequestGroupDB.upd_group_depreq(data)

    # UPDATE INDIVIDUAL REQUESTS
    for rec in details:
        if str(rec.get("status")).lower() in ["Failed".lower()]:
            updated = deploymentRequestService.retryDeploymentRequest(
                str(rec["deployment_id"]))
    return jsonify(json.loads(dumps({"result": "success", "message": "The request was updated successfully", "data": updated}))), 200
    
'''FORMAT
{
"machine_group_id":"5a69e45e505d83006cfd3587",
"package_state_id":"5a55f1ad4bcb0f006a2fbfb8",
"skip_dep_ind":true
"check_matching_ind":true
}
'''    
   
'''
TODO : As discussed with Rabiaa we are currently not saving "dependent" and "order" in du package state entity.
SO the use case were we have a du in du package state but not in a du package we will have order as 0 ande deplendent as false
'''   
   
@deploymentgrouprequestAPINs.route('/machinegroup/new', methods=['POST'])
class CreateGDByGroupIds(Resource):
    @api.expect(header_parser,DeploymentGroupModel.du_grp_machine_grp_create_request, validate=True)
    @api.marshal_with(DeploymentGroupModel.du_grp_create_response)
    @authService.authorized
    def post(self):
        """
        Create new Group Dep definition
        """
        requests_list = []
        
        #GET LOGGEDIN USER
        requested_by=userDB.get_user_by_id(authService.get_userid_by_auth_token(), False)["user"]
        
        #VALIDATIONS
        request_details = request.get_json()
        
        # get machine group
        machine_group_id=request_details.get("machine_group_id")
        machine_group_name=request_details.get("machine_group_name")
        if machine_group_id:
            machine_group_details=machinegroupsDB.get_machine_groups(machine_group_id,False)
            if not machine_group_details:
                raise Exception("Machine Group with _id: "+machine_group_id+" was not in database")
        elif machine_group_name:
            machine_group_details=machinegroupsDB.get_machine_group_by_name(machine_group_name)
            if not machine_group_details:
                raise Exception("Machine Group with group_name: "+machine_group_name+" was not found in database")
        else :
            raise Exception("Mandatory parameter : machine_group_id or machine_group_name was not provided")
        
        # get package state
        package_state_id=request_details.get("package_state_id")
        package_state_name=request_details.get("package_state_name")
        if package_state_id:
            package_state_details = statedb.get_state_by_id(package_state_id, True)
            if not package_state_details:
                raise Exception("Package State with _id: "+package_state_id+" was not found in database")
        elif package_state_name:
            package_state_details = statedb.get_state_by_name(package_state_name, True)
            if not package_state_details:
                raise Exception("Package State with name: "+package_state_name+" was not found in database")
            if len(package_state_details) > 1:
                raise Exception("Package State with name: "+package_state_name+" has more than one entries in database")
            else:
                package_state_details = package_state_details[0]                
        else :
            raise Exception("Mandatory parameter : package_state_id or package_state_name was not provided")
        if len(package_state_details.get("states",[])) < 0 or package_state_details.get("type") <> "dusetstate":
            raise Exception("State with _id: "+package_state_id+" is invalid du package state")
        du_set_details=deploymentUnitSetdb.GetDeploymentUnitSetById(package_state_details.get("parent_entity_id"), False)
        if not du_set_details:
            raise Exception("DU Package with _id: "+str(package_state_details.get("parent_entity_id"))+" was not in database")
        
        scheduled_date = str(datetime.now())
        #CREATE OUTER LIST OF DUS
        for state in package_state_details.get("states"):
            
            if not deploymentUnitdb.GetDeploymentUnitById(state["parent_entity_id"]):
                raise Exception("DU with _id: "+str(state.get("parent_entity_id"))+" was not in database")
                
            #CRAETE INNER LIST OF MACHINES
            for machine in machine_group_details["machine_id_list"]:
                inner_data = {"request_type": "deploy","deployment_type": "dugroup",\
                        "requested_by":requested_by,"parent_entity_id":state["parent_entity_id"],"state_id":str(state["_id"]),
                        "machine_id":machine,"warning_flag": False,"tool_deployment_value":[],"scheduled_date":scheduled_date,"parent_entity_set_id":package_state_details.get("parent_entity_id")}
                if state.get("deployment_field"):
                    for dep_field in state.get("deployment_field").get("fields"):
                        if dep_field.get("default_value"):
                            inner_data["tool_deployment_value"].append({"input_name": dep_field.get("input_name"),\
                                "input_type": dep_field.get("input_type"),"input_value": dep_field.get("default_value"),\
                                "order_id": dep_field.get("order_id")})                
                inner_data.update(request_details) 
                requests_list.append(inner_data)  
        
               
        return {"result": "success", "message": "New GroupDeployment request has been added successfully",\
                       "data": {"_id": add_request(requests_list)}}, 200    
                       

@deploymentgrouprequestAPINs.route('/add/undeploy', methods=['POST'])
class undeploy_group_deployment_request(Resource):
    @api.expect(header_parser,DeploymentGroupModel.undeploy_group_deployment_request_input, validate=True)
    @api.marshal_with(DeploymentGroupModel.du_grp_create_response)
    @authService.authorized
    def post(self):
        data = request.json
        oid=data.get("_id").get("oid")
        dep_req=deploymentRequestGroupDB.get_group_deployment_request(str(oid), True ,True)
        request_list= dep_req.get("requested_deployment_ids_data")
        keys_to_pop=["machine_name","create_date","update_date","execution_count",\
                     "status_message","status","start_time","_id","step_details",\
                     "current_step_id","retry_count","end_time"]
        requested_by=userDB.get_user_by_id(authService.get_userid_by_auth_token(), False).get("user")
        for key in keys_to_pop:
            for idx, item in enumerate(request_list):     
                if key in request_list[idx].keys() :
                    request_list[idx].pop(key)
                request_list[idx]["requested_by"]= requested_by
                request_list[idx]["request_type"]= "undeploy" 
        return {"result": "success", "message": "New GroupDeployment request has been added successfully",\
                       "data": {"_id": add_request(request_list)}}, 200            
  
@deploymentgrouprequestAPI.route('/deploymentrequest/group/view/revert/<string:oid>', methods=['GET'])
@authService.authorized
def get_deployment_request_group_by_id_for_revert(oid):
    dep_grp_req=deploymentRequestGroupDB.get_group_deployment_request(str(oid), False,False)
    du_package_id=dep_grp_req.get("parent_entity_set_id")
    deployed_set_stateId=statedb.get_state_by_id(dep_grp_req.get("package_state_id"), False).get("_id")
    data=deploymentUnitSetdb.GetDeploymentUnitSetById(str(du_package_id), True)
    states=[]
    if data.get("state"):
        for state in data.get("state"):
            if (deployed_set_stateId.generation_time.replace(tzinfo=None) > state.get("_id").generation_time.replace(tzinfo=None)) : 
                states.append(StateHelperService.get_names_from_ids(state,True)) 
        data["state"]= states 
        return jsonify(json.loads(dumps({"result": "success", "data":data }))), 200         
        
        

