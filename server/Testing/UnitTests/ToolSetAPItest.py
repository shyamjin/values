import unittest
import requests

from GetAuthToken import getToken
import json
from settings import mongodb,unittest_test_url
from DBUtil import Tool,ToolSet,Versions
import verifyResponse


ToolDb=Tool.Tool(mongodb)
VersionsDb=Versions.Versions(mongodb)
ToolSetDb=ToolSet.ToolSet(mongodb)
Baseurl = unittest_test_url+"toolset/"
header = {'content-type': "application/json",
                   'token':str(getToken())}
class AddToolSetTest(unittest.TestCase):
    
    ToolSetoid=None;
    Tooloid1=None;
    Veroid1=None;
    Tooloid2=None;
    Veroid2=None;
    def runTest(self):
        CreateToolForToolSet()
        url=Baseurl+"add"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Create ToolSet test"
        payload={"tool_set":[{"tool_id":AddToolSetTest.Tooloid1,
                              "status":"1",
                              "tool_name":"UnitTestTool2",
                              "tool_version":"UnitTestTool2 TEST",
                              "version_id":AddToolSetTest.Veroid1,
                              "version_name":"1","version_number":"TEST"},
                             {"tool_id":AddToolSetTest.Tooloid2,
                              "status":"1",
                              "tool_name":"UnitTestTool3",
                              "tool_version":"UnitTestTool3 TEST",
                              "version_id":AddToolSetTest.Veroid2,
                              "version_name":"1",
                              "version_number":"TEST"}],
                 "name":"UnitTestToolSetTest",
                 "description":"",
                 "tag":[]}
        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        AddToolSetTest.ToolSetoid = str(json_data.get("data").get("_id"))

class UpdateToolSetTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"update"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Update ToolSet test"
        payload={"_id":{"oid":AddToolSetTest.ToolSetoid},
                 "name":"UnitTestToolSetTest",
                 "description":"will describe later",
                 "tag":[],"logo":"/static/files/logos/default_u.png",
                 "tool_set":[{"tool_id":AddToolSetTest.Tooloid1,
                              "status":"1",
                              "tool_name":"UnitTestTool2",
                              "version_name":"1",
                              "version_id":AddToolSetTest.Veroid1,
                              "version_number":"TEST",
                              "tool_version":"UnitTestTool2 TEST"},
                             {"tool_id":AddToolSetTest.Tooloid2,
                              "status":"1",
                              "tool_name":"UnitTestTool3",
                              "version_name":"1",
                              "version_id":AddToolSetTest.Veroid2,
                              "version_number":"TEST",
                              "tool_version":"UnitTestTool3 TEST"}]}
        
        response = requests.request("PUT", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)

class GetAllToolSetTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"all"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get all ToolSet test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)                

class GetByIdToolSetTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/"+AddToolSetTest.ToolSetoid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Id ToolSet test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)    

class DeleteToolSetTest(unittest.TestCase):
     
    def runTest(self):
        url=Baseurl+"delete/"+AddToolSetTest.ToolSetoid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Deleting ToolSet test"
        response = requests.request("DELETE", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response) 
                        
def CleanDB():
    print "--------------------------------------------------------------------------------------------------------"
    print "Cleaning Database"
    if AddToolSetTest.ToolSetoid is not None:
        ToolSetDb.delete_tool_set(AddToolSetTest.ToolSetoid)
    if AddToolSetTest.Tooloid1 is not None:
        ToolDb.delete_tool(AddToolSetTest.Tooloid1)
    if AddToolSetTest.Tooloid2 is not None:
        ToolDb.delete_tool(AddToolSetTest.Tooloid2)
    if AddToolSetTest.Veroid1 is not None:
        result = VersionsDb.delete_version(AddToolSetTest.Veroid1)
    if AddToolSetTest.Veroid2 is not None:
        result = VersionsDb.delete_version(AddToolSetTest.Veroid2)
    print "--------------------------------------------------------------------------------------------------------"     
        
def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(AddToolSetTest())
    suite.addTest(UpdateToolSetTest())
    suite.addTest(GetAllToolSetTest())
    suite.addTest(GetByIdToolSetTest())
    suite.addTest(DeleteToolSetTest())
    return suite

def CreateToolForToolSet():
    url=unittest_test_url+"tool/add"
    payload1={"name":"UnitTestTool2","tag":[],
                 "support_details":"TEST@TEST.TEST",
                 "description":"TEST",
                 "version":{"version_date":"2018-02-16 14:44:47.021 ",
                            "version_name":"1",
                            "version_number":"TEST",
                            "pre_requiests":[],
                            "branch_tag":
                            "Branch","gitlab_repo":"",
                            "gitlab_branch":"",
                            "jenkins_job":"",
                            "document":{"documents":[]},
                            "backward_compatible":"no",
                            "release_notes":"",
                            "mps_certified":[],
                            "deployment_field":{"fields":[]},"dependent_tools":[]}}
    payload2={"name":"UnitTestTool3","tag":[],
                 "support_details":"TEST@TEST.TEST",
                 "description":"TEST",
                 "version":{"version_date":"2018-02-16 14:44:47.021 ",
                            "version_name":"1",
                            "version_number":"TEST",
                            "pre_requiests":[],
                            "branch_tag":
                            "Branch","gitlab_repo":"",
                            "gitlab_branch":"",
                            "jenkins_job":"",
                            "document":{"documents":[]},
                            "backward_compatible":"no",
                            "release_notes":"",
                            "mps_certified":[],
                            "deployment_field":{"fields":[]},"dependent_tools":[]}}
    response = requests.request("POST", url, data=json.dumps(payload1), headers=header,verify=False)
    json_data = json.loads(response.text)
    AddToolSetTest.Tooloid1 = str(json_data.get("data").get("_id"))
    AddToolSetTest.Veroid1 = str(json_data.get("data").get("version_id"))
    response = requests.request("POST", url, data=json.dumps(payload2), headers=header,verify=False)
    json_data = json.loads(response.text)
    AddToolSetTest.Tooloid2 = str(json_data.get("data").get("_id"))
    AddToolSetTest.Veroid2 = str(json_data.get("data").get("version_id"))

def main():  
    runner = unittest.TextTestRunner()
    test_suite = suite()
    result =runner.run (test_suite)
    CleanDB()
    if "errors=0" not in str(result):
        raise Exception("UnitTest for "+str(__name__)+" has failed")    
if __name__ == '__main__':
    main()      


