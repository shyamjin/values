import unittest
import requests
import time

from GetAuthToken import getToken
import json
from settings import mongodb,unittest_test_url
from DBUtil import DeploymentRequest
import verifyResponse

DeploymentRequestdb=DeploymentRequest.DeploymentRequest(mongodb)
Baseurl = unittest_test_url+"deploymentrequest/"

header = {'content-type': "application/json",
                   'token':str(getToken())}

class GetAllDepReqTest(unittest.TestCase):
    def runTest(self):
        url=Baseurl+"all"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get all Deployment Request test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)            

class GetByIdDepReqTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/"+str(DeploymentRequestdb.getRandomDepReqForUnitTest().get("_id"))
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Id Deployment Request test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)    

class RetryDepGroupReqTest(unittest.TestCase):
    def runTest(self):
        DepReq=DeploymentRequestdb.getRandomDepReqForUnitTest()
        url=Baseurl+"retry"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Save Deployment Group Request test"
        payload={"_id":{"oid":str(DepReq.get("_id"))}}
        response = requests.request("PUT", url, data=json.dumps(payload), headers=header,verify=False)
        if (DepReq.get("status")=="Failed"):
            verifyResponse.PositiveTesting(response)
        else:
            verifyResponse.NegativeTesting(response, "The request is not in failed status")


def CleanDB():
    print "--------------------------------------------------------------------------------------------------------"
    print "--------------------------------------------------------------------------------------------------------"     
            
def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(GetAllDepReqTest())
    suite.addTest(GetByIdDepReqTest())
    suite.addTest(RetryDepGroupReqTest())

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

