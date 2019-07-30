
import unittest
import requests
import string
import random
from GetAuthToken import getToken
import json
from settings import mongodb,unittest_test_url
from DBUtil import ProposedTools
import verifyResponse


proposedToolsDB=ProposedTools.ProposedTools()
Baseurl = unittest_test_url+"proposed/tool/"
header = {'content-type': "application/json",
                   'token':str(getToken())}
payload={
                "name": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(50)),
                "support_details": "vpadmin@amdocs.com",
                "description": "Test Desc",
                "request_reason": "Test Reason",
                "version": {
                    "version_name": "ga",
                    "version_number": "1.0"
                }
                 }
class AddProposedToolTest(unittest.TestCase):
    oid=None;
    global payload
    def runTest(self):
        url=Baseurl+"new"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Create Proposed Tool test"
        
        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        AddProposedToolTest.oid = str(json_data.get("data").get("_id"))
        
class ApproveProposedToolTest(unittest.TestCase):
    oid=None;
    global payload
    def runTest(self):
        url=Baseurl+"approve"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Create Proposed Tool test"
        payload["_id"]=AddProposedToolTest.oid
        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        AddProposedToolTest.oid = str(json_data.get("data").get("_id"))        

class GetAllProposedToolTest(unittest.TestCase):    
    def runTest(self):
        url=Baseurl+"view/all"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For all proposed tools test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)  
        
class GetProposedToolByIdTest(unittest.TestCase):    
    def runTest(self):
        url=Baseurl+"view/"+AddProposedToolTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Id PT test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)  
        
class RemoveProposedToolByIdTest(unittest.TestCase):    
    def runTest(self):
        url=Baseurl+"delete/"+AddProposedToolTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Delete by Id PT test"
        response = requests.request("DELETE", url, headers=header,verify=False)
        verifyResponse.NegativeTesting(response, None)          
        
def CleanDB():
    print "--------------------------------------------------------------------------------------------------------"
    print "Cleaning Database"
    if AddProposedToolTest.oid is not None:
        proposedToolsDB.delete(AddProposedToolTest.oid)
    print "--------------------------------------------------------------------------------------------------------"     
        
def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(AddProposedToolTest())
    suite.addTest(GetAllProposedToolTest())
    suite.addTest(GetProposedToolByIdTest())
    suite.addTest(ApproveProposedToolTest())
    suite.addTest(RemoveProposedToolByIdTest())
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

