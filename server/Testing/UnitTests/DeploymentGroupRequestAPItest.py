import unittest
import requests
import time

from GetAuthToken import getToken
import json
from settings import mongodb,unittest_test_url
from DBUtil import DeploymentRequestGroup,MachineType,Machine,Versions,Tool,Config,Build,MachineGroups,DeploymentUnitSet
import verifyResponse

DeploymentUnitSetDb=DeploymentUnitSet.DeploymentUnitSet()
MachineGroupsDb=MachineGroups.MachineGroups(mongodb)
BuildDb=Build.Build()
ToolDb=Tool.Tool(mongodb)
ConfigDb = Config.Config(mongodb)
MachineDb=Machine.Machine(mongodb)
MachineTypeDb=MachineType.MachineType(mongodb)
VersionsDb=Versions.Versions(mongodb)
DeploymentRequestGroupdb=DeploymentRequestGroup.DeploymentRequestGroup(mongodb)
Baseurl = unittest_test_url+"deploymentrequest/group/"

header = {'content-type': "application/json",
                   'token':str(getToken())}
class AddDepGroupReqTest(unittest.TestCase):
    oid=None;
    def runTest(self):
        url=Baseurl+"add"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Create Deployment Group Request test"
        payload={"deployment_requests":[{"parent_entity_id":str(VersionsDb.get_last_active_version_by_tool_id(str(ToolDb.get_tool_by_name("jTrace").get("_id")),False).get("_id")),
                                         "requested_by":"SuperAdmin",
                                         "request_type":"deploy",
                                         "deployment_type":"toolgroup",
                                         "callback_url": "http://localhost:3000/groupdu",
                                         "requests":[{"machine_id":str(MachineDb.GetMachinebyName("root@1.1.1.1")[0].get("_id")),
                                                      "tool_deployment_value":[{"input_name":"debug_host",
                                                                                "input_type":"text",
                                                                                "input_value":"TEST",
                                                                                "order_id":1},
                                                                               {"input_name":"debug_port",
                                                                                "input_type":"text",
                                                                                "input_value":"8899",
                                                                                "order_id":2}],"warning_flag":False,
                                                      "skip_dep_ind":False}],
                                         "scheduled_date":"2018-02-27T08:48:47.222Z",
                                         "build_number":20,
                                         "build_id": str(BuildDb.get_active_build_for_unittest(str(VersionsDb.get_last_active_version_by_tool_id(str(ToolDb.get_tool_by_name("jTrace").get("_id")),False).get("_id"))))}]}
        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        AddDepGroupReqTest.oid = str(json_data.get("data").get("id"))
        enable_callback = ConfigDb.getConfigByName('DeploymentRequestService').get("enable_callback")
        if enable_callback == "false" or not enable_callback:
            return
        callback_url = DeploymentRequestGroupdb.get_group_deployment_request(AddDepGroupReqTest.oid).get("callback").get("callback_url")
        assert callback_url == payload.get("deployment_requests")[0].get("callback_url"), "FAILURE: Callback URL did not register to database. Response is " + str(response.text)

class SaveDepGroupReqTest(unittest.TestCase):
    oid=None;
    def runTest(self):
        url=Baseurl+"saved/add"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Save Deployment Group Request test"
        payload = {"deployment_type":"toolgroup",
                   "data":[{"tool_id":str(ToolDb.get_tool_by_name("jTrace").get("_id")),
                            "tool_name":"jTrace",
                            "version_number":"0.1.0",
                            "tool_deployment_value":[{"default_value":"",
                                                      "is_mandatory":True,
                                                      "order_id":1,
                                                      "input_type":"text",
                                                      "tooltip":"",
                                                      "input_name":"debug_host"},
                                                     {"default_value":"8899",
                                                      "is_mandatory":True,
                                                      "order_id":2,
                                                      "input_type":"text",
                                                      "tooltip":"",
                                                      "input_name":"debug_port"}],
                            "build_number":20,
                            "build_id":str(BuildDb.get_active_build_for_unittest(str(VersionsDb.get_last_active_version_by_tool_id(str(ToolDb.get_tool_by_name("jTrace").get("_id")),False).get("_id")))),
                            "requests":[{"tool_name":"jTrace",
                                         "tool_deployment_value":[{"default_value":"wte",
                                                                   "is_mandatory":True,
                                                                   "order_id":1,
                                                                   "input_type":"text",
                                                                   "tooltip":"",
                                                                   "input_name":"debug_host"},
                                                                  {"default_value":"8899",
                                                                   "is_mandatory":True,
                                                                   "order_id":2,
                                                                   "input_type":"text",
                                                                   "tooltip":"",
                                                                   "input_name":"debug_port"}],
                                         "machine_id":str(MachineDb.GetMachinebyName("root@1.1.1.1")[0].get("_id")),
                                         "machine_name":"root@1.1.1.1","skip_deployment":False,
                                         "is_build_already_deployed":False,"isDefault":True,
                                         "isCopiedToAllMachines":False,
                                         "warning_flag":False}],
                            "version_id":str(VersionsDb.get_last_active_version_by_tool_id(str(ToolDb.get_tool_by_name("jTrace").get("_id")),False).get("_id"))}]}
        
        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        SaveDepGroupReqTest.oid = str(json_data.get("data"))
        
class CreateDepGrpReqByGrpIdTest(unittest.TestCase):
    oid=None;
    def runTest(self):
        url=Baseurl+"machinegroup/new"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Create Deployment Group Request test"
        payload={
                "machine_group_id":str(MachineGroupsDb.get_machine_group_by_name("TestMachineGroup1").get("_id")),
                "parent_entity_set_id":str(DeploymentUnitSetDb.GetDeploymentUnitSetByName("Test Du Package", False).get("_id")),                "skip_dep_ind":True,
                "machine_matching_ind":True
                }
        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        CreateDepGrpReqByGrpIdTest.oid = str(json_data.get("data").get("id"))


class UpdateSaveDepGroupReqTest(unittest.TestCase):
    def runTest(self):
        url=Baseurl+"saved/update"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Save Deployment Group Request test"
        payload = {"_id":{"oid":SaveDepGroupReqTest.oid},"deployment_type":"toolgroup",
           "data":[{"tool_id":str(ToolDb.get_tool_by_name("jTrace").get("_id")),
                    "tool_name":"jTrace",
                    "version_number":"0.1.0",
                    "tool_deployment_value":[{"default_value":"",
                                              "is_mandatory":True,
                                              "order_id":1,
                                              "input_type":"text",
                                              "tooltip":"",
                                              "input_name":"debug_host"},
                                             {"default_value":"8899",
                                              "is_mandatory":True,
                                              "order_id":2,
                                              "input_type":"text",
                                              "tooltip":"",
                                              "input_name":"debug_port"}],
                    "build_number":20,
                    "build_id":str(BuildDb.get_active_build_for_unittest(str(VersionsDb.get_last_active_version_by_tool_id(str(ToolDb.get_tool_by_name("jTrace").get("_id")),False).get("_id")))),
                    "requests":[{"tool_name":"jTrace",
                                 "tool_deployment_value":[{"default_value":"wte",
                                                           "is_mandatory":True,
                                                           "order_id":1,
                                                           "input_type":"text",
                                                           "tooltip":"",
                                                           "input_name":"debug_host"},
                                                          {"default_value":"8899",
                                                           "is_mandatory":True,
                                                           "order_id":2,
                                                           "input_type":"text",
                                                           "tooltip":"",
                                                           "input_name":"debug_port"}],
                                 "machine_id":str(MachineDb.GetMachinebyName("root@1.1.1.1")[0].get("_id")),
                                 "machine_name":"root@1.1.1.1","skip_deployment":False,
                                 "is_build_already_deployed":False,"isDefault":True,
                                 "isCopiedToAllMachines":False,
                                 "warning_flag":True}],
                    "version_id":str(VersionsDb.get_last_active_version_by_tool_id(str(ToolDb.get_tool_by_name("jTrace").get("_id")),False).get("_id"))}]}
        response = requests.request("PUT", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        

class RetryDepGroupReqTest(unittest.TestCase):
    def runTest(self):
        url=Baseurl+"retry"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Save Deployment Group Request test"
        payload={"_id":{"oid":AddDepGroupReqTest.oid}}
        response = requests.request("PUT", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.NegativeTesting(response, "Only failed request can be retried")
        
class GetAllDepGroupReqTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"all"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get all Deployment Group Request test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)                
        
class GetAllSavedDepGroupReqTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"saved/all"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get all Saved Deployment Group Request test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)                

class GetByIdDepGroupReqTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/"+AddDepGroupReqTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Id Deployment Group Request test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)    

class GetByIdSavedDepGroupReqTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"saved/view/"+AddDepGroupReqTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Id Saved Deployment Group Request test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)    
     
class GetByNameDepGroupReqTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/name/UnitTestDepGroupReq"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Name Deployment Group Request test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)               


def CleanDB():
    print "--------------------------------------------------------------------------------------------------------"
    print "--------------------------------------------------------------------------------------------------------"     
            
def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(AddDepGroupReqTest())
    suite.addTest(SaveDepGroupReqTest())
    suite.addTest(CreateDepGrpReqByGrpIdTest())
    suite.addTest(UpdateSaveDepGroupReqTest())
    suite.addTest(RetryDepGroupReqTest())
    suite.addTest(GetAllDepGroupReqTest())
    suite.addTest(GetAllSavedDepGroupReqTest())
    suite.addTest(GetByIdDepGroupReqTest())
    suite.addTest(GetByIdSavedDepGroupReqTest())

    return suite

def main():  
    runner = unittest.TextTestRunner()
    test_suite = suite()
    result =runner.run (test_suite)
    CleanDB()
    if "errors=0" not in str(result):
        raise Exception("UnitTest for "+str(__name__)+" has failed")
    
if __name__ == '__main__':
    main()

