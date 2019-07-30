import unittest
import requests

from GetAuthToken import getToken
import json
from settings import mongodb,unittest_test_url
from DBUtil import DeploymentUnit
import verifyResponse

DeploymentUnitDb=DeploymentUnit.DeploymentUnit()
Baseurl = unittest_test_url+"deploymentunit/"
header = {'content-type': "application/json",
                   'token':str(getToken())}
class AddDuTest(unittest.TestCase):
    
    oid=None;
    def runTest(self):
        url=Baseurl+"new"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Create Du test"
        payload={"name":"TestDU",
                 "type":"Fast Track",
                 "tag":[],"release_notes":"",
                 "branch":"","pre_requiests":[],
                 "deployment_field":{"fields":[]},
                 "approval_status":"Created",
                 "approval_list":[{"approval_status":"Created",
                                   "approved_by":"Admin",
                                   "approved_date":"2018-02-20T09:36:19.512Z"}]}
        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        AddDuTest.oid = str(json_data.get("data").get("_id"))

class UpdateDuTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"update"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Update Du test"
        payload={"_id":{"oid":AddDuTest.oid},
                 "name":"TestDU",
                 "type":"Version",
                 "tag":[],
                 "release_notes":"",
                 "branch":"",
                 "pre_requiests":[],
                 "deployment_field":{"fields":[]}}
        
        response = requests.request("PUT", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)

class GetAllDuTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"all"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get all Du test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)                

class GetByIdDuTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/"+AddDuTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Id Du test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)    
        

class GetByMachineIdDuTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/"+AddDuTest.oid+"/machine/"+AddDuTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Machine Du test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)


class GetByNameDuTest(unittest.TestCase):
     
    def runTest(self):
        url=Baseurl+"search/name/TestDU"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Name Du test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response) 

class GetByTagDuTest(unittest.TestCase):
     
    def runTest(self):
        url=Baseurl+"search/tag/testtagforunittest"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Tag Du test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response) 
        
class DeleteDuTest(unittest.TestCase):
     
    def runTest(self):
        url=Baseurl+"delete/"+AddDuTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Deleting Du test"
        response = requests.request("DELETE", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response) 
                        
def CleanDB():
    print "--------------------------------------------------------------------------------------------------------"
    print "Cleaning Database"
    if AddDuTest.oid is not None:
        DeploymentUnitDb.DeleteDeploymentUnit(AddDuTest.oid)
    print "--------------------------------------------------------------------------------------------------------"     
        
def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(AddDuTest())
    suite.addTest(UpdateDuTest())
    suite.addTest(GetAllDuTest())
    suite.addTest(GetByIdDuTest())
    suite.addTest(GetByMachineIdDuTest())
    suite.addTest(GetByNameDuTest())
    suite.addTest(GetByTagDuTest())
    suite.addTest(DeleteDuTest())
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

