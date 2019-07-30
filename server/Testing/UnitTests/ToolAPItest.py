
import unittest
import requests

from GetAuthToken import getToken
import json
from settings import mongodb,unittest_test_url
from DBUtil import Tool,Versions
import verifyResponse

Tooldb=Tool.Tool(mongodb)
Versionsdb=Versions.Versions(mongodb)
Baseurl = unittest_test_url+"tool/"
header = {'content-type': "application/json",
                   'token':str(getToken())}
class AddToolTest(unittest.TestCase):
    oid=None;
    version_id=None
    def runTest(self):
        url=Baseurl+"add"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Create tool test"
        payload={"name":"UnitTestTool","tag":[],
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

        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        AddToolTest.oid = str(json_data.get("data").get("_id"))
        AddToolTest.version_id = str(json_data.get("data").get("version_id"))

class UpdateToolTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"update"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Update tool test"
        payload={"_id":{"oid":AddToolTest.oid},
                "name":"UnitTestTool","tag":[],
                "support_details":"TEST@TEST.TEST1",
                 "description":"TEST123",
                 "version":[{
                     "_id":{"oid":AddToolTest.version_id},
                     "version_date":"2018-02-16 14:44:47.021 ",
                            "version_number":"3",
                            "gitlab_branch":"",
                            "tool_id":AddToolTest.oid,
                            "status":"1",
                            "branch_tag":"Branch"
                          }],
                  "status":"1"
                            }
        
        response = requests.request("PUT", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)

class DepricateToolTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"update"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Deprecate tool test"
        payload={"_id":{"oid":AddToolTest.oid},
                "name":"UnitTestTool","tag":[],
                "support_details":"TEST@TEST.TEST1",
                 "description":"TEST123",
                 "version":[{
                     "_id":{"oid":AddToolTest.version_id},
                     "version_date":"2018-02-16 14:44:47.021 ",
                            "version_number":"3",
                            "gitlab_branch":"",
                            "tool_id":AddToolTest.oid,
                            "status":"1",
                            "branch_tag":"Branch"
                          }],
                  "status":"3"
                            }
        response = requests.request("PUT", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)        

class GetAllToolTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"all"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get all tool test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)                

class GetByIdToolTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/"+AddToolTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Id tool test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)    
        
class GetByVerIdToolTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/version/"+AddToolTest.version_id
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by version Id tool test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)              


class GetByVerAndMachineIdToolTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/version/"+AddToolTest.version_id+"/prevversion/"+AddToolTest.version_id+"/machine/"+AddToolTest.version_id
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by version Id tool test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)


class GetByTagToolTest(unittest.TestCase):
     
    def runTest(self):
        url=Baseurl+"search/tag/test"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Tag tool test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response) 
                
def CleanDB():
    print "--------------------------------------------------------------------------------------------------------"
    print "Cleaning Database"
    if AddToolTest.oid is not None:
        result = Tooldb.delete_tool(AddToolTest.oid)
    if AddToolTest.version_id is not None:
        result = Versionsdb.delete_version(AddToolTest.version_id)
    print "--------------------------------------------------------------------------------------------------------"     
        
def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(AddToolTest())
    suite.addTest(UpdateToolTest())
    suite.addTest(DepricateToolTest())
    suite.addTest(GetAllToolTest())
    suite.addTest(GetByIdToolTest())
    suite.addTest(GetByVerIdToolTest())
    suite.addTest(GetByVerAndMachineIdToolTest())
    suite.addTest(GetByTagToolTest())
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


