from werkzeug import secure_filename
from urlparse import urlparse
from bson.json_util import dumps
from flask import Blueprint, jsonify, request
from DBUtil import Build, Users, SystemDetails,State,Config
from settings import mongodb, default_nexus_container_name, temp_files_full_path
from Services import StateHelperService,BuildHelperService,HelperServices
from Services.AppInitServices import authService
import os
import json
# blueprint declaration
buildAPI = Blueprint('buildAPI', __name__)

# get global db connection
db = mongodb
buildDB = Build.Build()
userDB = Users.Users(db)
systemDetailsDB = SystemDetails.SystemDetails(db)
stateDb=State.State(mongodb)
configDb=Config.Config(mongodb)




'''
INPUT REQUEST:
{ 
    "_id" : ObjectId("5abbc6749e53f700787d3997"), 
    "status" : "1",
    "file_size" : "4.0K", 
    "type" : "url", 
    "file_path" : "http://illin4490:8081/nexus/content/repositories/yum-test/com/amdocs/core/crm/crm-playbooks/10.2.4-1620/crm-playbooks-10.2.4-1620.tar",
    "build_number": 22, 
    "package_name" : "crm-playbooks-10.2.4-1620.tar", 
    "package_type" : "tar", 
    "parent_entity_id" : "5abbbf5ff13a94007945f01a",   
    "additional_artifacts" : {
        "artifacts" : [
            {
                "repo_id" : "yum-test", 
                "package" : "com.amdocs.core.crm", 
                "file_name" : "amdocs-crm-admin_cluster_top-1-10.2.0.3.106.rpm", 
                "artifact" : "amdocs-crm-admin_cluster_top-1", 
                "relative_path" : "yum-test/com/amdocs/core/crm/amdocs-crm-admin_cluster_top-1/10.2.0.3.106", 
                "version" : "10.2.0.3.106", 
                "type" : "rpm",
                 "classifier" : "1"
            }
        ], 
        "repo_provider" : "Yum"
    }, 
    "additional_info" : {
        "repo_id" : "yum-test", 
        "package" : "com.amdocs.core.crm", 
        "file_name" : "crm-playbooks-10.2.4-1620.tar", 
        "artifact" : "crm-playbooks", 
        "relative_path" : "yum-test/com/amdocs/core/crm/crm-playbooks/10.2.4-1620", 
        "version" : "10.2.4-1620"
       
    }, 
    "state_details": { # CONSIDERED ONLY IF create_state_ind == true
        "name": "Test",#OPTIONAL #AUTO GENERATED
        "approval_status":"Tested", # OPTIONAL #DEFAULT :Created
        "deployment_field": {"kuk": "hellow"} # OPTIONAL
    }
}


RESPONSE :

{
    "message": "Build and State added successfully",
    "data": {
        "build_id": "5a3bc9c1f913e748d40b16fe",
        "state_id": "5a3bc9c2f913e748d40b16ff",
        "state_data": {
            "build_id": "5a3bc9c1f913e748d40b16fe",
            "name": "test du 30 State-548",
            "deployment_field": {
                "fields": [
                    {
                        "default_value": "2017-10-18T18:30:00.000Z",
                        "is_mandatory": true,
                        "order_id": 0,
                        "input_type": "date",
                        "tooltip": "hkhk",
                        "input_name": "kuk"
                    },
                    {
                        "order_id": 1,
                        "input_type": "text",
                        "default_value": "fgh",
                        "input_name": "hg",
                        "tooltip": "gfh"
                    },
                    {
                        "order_id": 2,
                        "input_type": "password",
                        "default_value": "fhg",
                        "input_name": "fhghgh",
                        "tooltip": "gfh"
                    },
                    {
                        "order_id": 3,
                        "input_type": "email",
                        "default_value": "gfh@df.com",
                        "input_name": "fhg",
                        "tooltip": "df"
                    },
                    {
                        "order_id": 4,
                        "input_type": "date",
                        "default_value": "2017-10-11T18:30:00.000Z",
                        "input_name": "sdf",
                        "tooltip": "sdfd"
                    },
                    {
                        "order_id": 5,
                        "input_type": "checkbox",
                        "valid_values": [
                            "dsfdfd",
                            "sdfdf"
                        ],
                        "input_name": "sdfdfdsfdfdsfds",
                        "tooltip": "dsfd"
                    },
                    {
                        "default_value": "dsfdf",
                        "order_id": 6,
                        "input_type": "dropdown",
                        "tooltip": "dsfd",
                        "valid_values": [
                            "dsfdf"
                        ],
                        "input_name": "sdfdfdfdsfds"
                    },
                    {
                        "order_id": 7,
                        "input_type": "radio",
                        "valid_values": [
                            "sdfdf",
                            "dsfdf"
                        ],
                        "input_name": "sdfdsfdsfdsfdsf",
                        "tooltip": "sdfdf"
                    }
                ],
                "_id": {
                    "$oid": "5a3bc9c2f913e748d40b1700"
                },
                "parent_entity_id": "5a3bc9c2f913e748d40b16ff"
            },
            "parent_entity_id": "59ddcf802646eb006a6c7707",
            "build": {
                "status": "1",
                "build_date": {
                    "$date": 1513887513000
                },
                "build_number": 12,
                "package_name": "amdocs_data_loader_ga_1_8_18_8.zip",
                "package_type": "zip",
                "parent_entity_id": "59ddcf802646eb006a6c7707",
                "file_path": "http://illin4467:8081/nexus/content/repositories/vp_builds/amdocs/infra/db/amdocs_data_loader/ga_1_8_18/amdocs_data_loader-ga_1_8_18-8.zip",
                "file_size": "4.0K",
                "_id": {
                    "$oid": "5a3bc9c1f913e748d40b16fe"
                },
                "type": "url",
                "additional_info": {
                    "repo_id": "vp_builds",
                    "package": "amdocs.infra.db",
                    "file_name": "amdocs_data_loader-ga_1_8_18-8.zip",
                    "artifact": "amdocs_data_loader",
                    "relative_path": "vp_builds/amdocs/infra/db/amdocs_data_loader/ga_1_8_18",
                    "version": "ga_1_8_18"
                }
            },
            "_id": {
                "$oid": "5a3bc9c2f913e748d40b16ff"
            },
            "type": "dustate",
            "approval_status": "Created"
        }
    },
    "result": "success"
}
'''


@buildAPI.route('/build/add', methods=['POST'])
@buildAPI.route('/versions/build/add', methods=['POST'])
@authService.unauthorized
def add_build():
    try:
        state_details=None
        new_state_id=None
        new_build_id=None
        new_build = request.get_json()
        directory_to_import_from =None
        
        #IN CASE THIS METHOD IS GETTING CALLED FROM upload_build()
        if not new_build : 
            new_build = request.data # Used by upload_build()
            directory_to_import_from = new_build.get("directory_to_import_from")
            new_build.pop("directory_to_import_from")
        if "version_id" in new_build.keys():  # PATCH FOR VERSION ID
            if "parent_entity_id" not in new_build.keys():
                new_build["parent_entity_id"] = new_build["version_id"]
            new_build.pop("version_id")
        state_details=new_build.get("state_details",None)
        new_build_id = BuildHelperService.add_update_build(new_build, new_build.get("parent_entity_id"), directory_to_import_from)
        if str(new_build_id) not in ["1","0"] and state_details is not None:
            state_details["parent_entity_id"]=new_build["parent_entity_id"]
            state_details["build_id"]=new_build_id                
            new_state_id = StateHelperService.generate_new_state(state_details)
            return jsonify(json.loads(dumps({"result": "success", "message": "Build and State added successfully", "data": {"build_id": new_build_id,\
                "state_id":new_state_id,"state_data":stateDb.get_state_by_id(new_state_id, True)}}))), 200
        else:    
            if str(new_build_id) == "1":
                return jsonify(json.loads(dumps({"result": "success", "message": "Build updated successfully", "data": {"id": new_build_id}}))), 200
            elif str(new_build_id) == "0":
                return jsonify(json.loads(dumps({"result": "success", "message": "No changes found", "data": {"id": new_build_id}}))), 200                
            else:
                return jsonify(json.loads(dumps({"result": "success", "message": "Build added successfully", "data": {"build_id": new_build_id}}))), 200
    except Exception as e:  # catch *all* exceptions
        if str(new_state_id).lower() not in ["none","1","0"]:
            StateHelperService.delete_state(new_state_id,False)
        if str(new_build_id).lower() not in ["none","1","0"]:
            buildDB.delete_build(new_build_id)    
        raise e


@buildAPI.route('/build/update', methods=['PUT'])
@authService.unauthorized
def update_build():
    request_build_details = request.get_json() 
    if not request_build_details.get("_id"):
        build_details = buildDB.get_build_by_number(
            str(request_build_details.get("parent_entity_id")), request_build_details.get("build_number"), True)
        if build_details is not None:
            if build_details.get("_id"):
                request_build_details["_id"] = {"oid": str(build_details.get("_id"))}
            else:
                raise Exception(
                    "Unable to find a build id for parent_entity_id" + str(request_build_details.get("parent_entity_id")))
        else:
            raise Exception("Unable to find a build details for build number " + str(request_build_details.get(
                "build_number")) + " and parent_entity_id " + str(request_build_details.get("parent_entity_id")))
    else:
        if request_build_details.get("parent_entity_id"):
            HelperServices.get_details_of_parent_entity_id(request_build_details.get("parent_entity_id"))        
    result = BuildHelperService.add_update_build(request_build_details, request_build_details.get("parent_entity_id"), None)
    return jsonify(json.loads(dumps({"result": "success", "message": "Build updated successfully", "data": {"id":result}}))), 200
    



@buildAPI.route('/build/view/<string:oid>', methods=['GET'])
@authService.unauthorized
def get_build(oid):
    build=buildDB.get_build(oid)
    actual_host = bool(request.args.get('actual_host', False))
    '''
    if actual_host is True, the hostname in the file_path replaced with the hostname mentioned in the SystemDetails collection 
    provided the hostname in build and default_nexus_container_name is same.  
    '''
    if build.get("file_path",None) and (actual_host):
        if urlparse(build.get("file_path")).hostname == default_nexus_container_name :
            build["file_path"]=build.get("file_path").replace(urlparse(build.get("file_path")).\
                                                              hostname,systemDetailsDB.get_system_details_single().get("hostname"))
    return jsonify(json.loads(dumps({"result": "success", "data": build}))), 200

'''

Now from 3.2.3 we have repository plugins. So one DU can have Jfrog and other can have Nexus.
Its tiresome to upload a build independently and then then add a build to dpm with another api.
Why not handle both at once

Postman:
        artifact_file : File to upload
        build_details : A file containing the build detais.Should be json. Contents is Repository Specific
CURL:
    curl --verbose -F 'build_details=@jsonfile.txt' -F 'artifact_file=@test.pdf' http://localhost:8000/build/upload
    
PLEASE NOTE :
    It wont work for nexus2 and nexus 3 as the keyargs["file_to_upload"] = join(keyargs["directory_to_import_from"],relative_path,fileName)
    But file is saved at keyargs["file_to_upload"] = join(keyargs["directory_to_import_from"])
'''
@buildAPI.route('/build/upload', methods=['POST'])
@authService.unauthorized
def upload_build():
    try:
        artifact_file = request.files['artifact_file']
    except Exception:
        raise ValueError("Please provide artifact_file")
    try:
        build_details = request.files['build_details']
    except Exception:
        raise ValueError("Please provide build_details")
    artifact_file_filename = secure_filename(artifact_file.filename)
    artifact_file_filename = str(temp_files_full_path + artifact_file_filename)
    artifact_file.save(artifact_file_filename)
    build_details_filename = secure_filename(build_details.filename)
    build_details_filename = str(temp_files_full_path + build_details_filename)
    build_details.save(build_details_filename)
    try:
        build_details = json.loads(open(build_details_filename).read())
        build_details["directory_to_import_from"] = temp_files_full_path
        request.data =  build_details   
        return add_build()
    finally:
        try:
            os.remove(artifact_file_filename)
            os.remove(build_details_filename)
        except Exception:
            pass


@buildAPI.route('/tool/update/buildmarkup', methods=['POST'])
@authService.unauthorized
def update_build_markup():
    try:
        update_build_markup = request.get_json()
    except Exception:
        raise ValueError("Please provide build Ids")
    request_build_details = request.get_json()
    version_build_dic = request_build_details.get("updateMarkupBuild")
    if  request_build_details.get("updateMarkupBuild"):
        for version_id in version_build_dic.keys():
            for build in version_build_dic[version_id]:
                result = BuildHelperService.add_update_build(build,
                                                             version_id,
                                                             None)
    else:
        return jsonify(
            json.loads(
                dumps({"result": "success", "message": "Build Not updated", "data": {"id": update_build_markup}}))), 200
    return jsonify(
        json.loads(
            dumps({"result": "success", "message": "Build  updated", "data": {"id": update_build_markup}}))), 200


