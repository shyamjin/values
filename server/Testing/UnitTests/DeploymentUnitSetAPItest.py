import unittest
import requests

from GetAuthToken import getToken
import json
from settings import mongodb,unittest_test_url
from DBUtil import DeploymentUnit,DeploymentUnitSet
import verifyResponse


DeploymentUnitDb=DeploymentUnit.DeploymentUnit()

DeploymentUnitSetDb=DeploymentUnitSet.DeploymentUnitSet()
Baseurl = unittest_test_url+"deploymentunitset/"
header = {'content-type': "application/json",
                   'token':str(getToken())}
class AddDuSetTest(unittest.TestCase):
    
    DuSetoid=None;
    Duoid1=None;
    Duoid2=None;
    def runTest(self):
        CreateDuForDuSet()
        url=Baseurl+"new"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Create DuSet test"
        payload={"du_set":[{"du_id":AddDuSetTest.Duoid1,
                            "dependent":"false",
                            "order":1},
                           {"du_id":AddDuSetTest.Duoid2,
                            "dependent":"false","order":2}],
                 "name":"UnitTestDuSet","tag":[],
                 "release_notes":"","pre_requiests":[],
                 "approval_status":"Created",
                 "approval_list":[{"approval_status":"Created",
                                   "approved_by":"SuperAdmin",
                                   "approved_date":"2018-02-20T15:21:38.199Z"}]}
        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        AddDuSetTest.DuSetoid = str(json_data.get("data").get("_id"))

class UpdateDuSetTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"update"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Update DuSet test"
        payload={"_id":{"oid":AddDuSetTest.DuSetoid},
                 "du_set":[{"du_id":AddDuSetTest.Duoid1,
                            "dependent":"false","order":1},
                           {"du_id":AddDuSetTest.Duoid2,
                            "dependent":"false","order":2}],
                 "name":"UnitTestDuSet","tag":[],
                 "logo":"/static/files/logos/default_u.png",
                 "release_notes":"Yet to be released",
                 "pre_requiests":[]}
        
        response = requests.request("PUT", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)

class GetAllDuSetTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"all"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get all DuSet test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)                

class GetByIdDuSetTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/"+AddDuSetTest.DuSetoid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Id DuSet test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)    

class DeleteDuSetTest(unittest.TestCase):
     
    def runTest(self):
        url=Baseurl+"delete/"+AddDuSetTest.DuSetoid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Deleting DuSet test"
        response = requests.request("DELETE", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response) 
                        
def CleanDB():
    print "--------------------------------------------------------------------------------------------------------"
    print "Cleaning Database"
    if AddDuSetTest.DuSetoid is not None:
        DeploymentUnitSetDb.DeleteDeploymentUnitSet(AddDuSetTest.DuSetoid)
    if AddDuSetTest.Duoid1 is not None:
        DeploymentUnitDb.DeleteDeploymentUnit(AddDuSetTest.Duoid1)
    if AddDuSetTest.Duoid2 is not None:
        DeploymentUnitDb.DeleteDeploymentUnit(AddDuSetTest.Duoid2)
    print "--------------------------------------------------------------------------------------------------------"     
        
def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(AddDuSetTest())
    suite.addTest(UpdateDuSetTest())
    suite.addTest(GetAllDuSetTest())
    suite.addTest(GetByIdDuSetTest())
    suite.addTest(DeleteDuSetTest())
    return suite

def CreateDuForDuSet():
    url=unittest_test_url+"deploymentunit/new"
    payload1={"name":"TestDU1",
             "type":"Fast Track",
             "tag":[],"release_notes":"",
             "branch":"","pre_requiests":[],
             "deployment_field":{"fields":[]},
             "approval_status":"Created",
             "approval_list":[{"approval_status":"Created",
                               "approved_by":"Admin",
                               "approved_date":"2018-02-20T09:36:19.512Z"}]}
    payload2={"name":"TestDU2",
             "type":"Fast Track",
             "tag":[],"release_notes":"",
             "branch":"","pre_requiests":[],
             "deployment_field":{"fields":[]},
             "approval_status":"Created",
             "approval_list":[{"approval_status":"Created",
                               "approved_by":"Admin",
                               "approved_date":"2018-02-20T09:36:19.512Z"}]}
    response = requests.request("POST", url, data=json.dumps(payload1), headers=header,verify=False)
    json_data = json.loads(response.text)
    AddDuSetTest.Duoid1 = str(json_data.get("data").get("_id"))
    response = requests.request("POST", url, data=json.dumps(payload2), headers=header,verify=False)
    json_data = json.loads(response.text)
    AddDuSetTest.Duoid2 = str(json_data.get("data").get("_id"))

def main():  
    runner = unittest.TextTestRunner()
    test_suite = suite()
    result =runner.run (test_suite)
    CleanDB()
    if "errors=0" not in str(result):
        raise Exception("UnitTest for "+str(__name__)+" has failed")
    
    
if __name__ == '__main__':
    main()      


