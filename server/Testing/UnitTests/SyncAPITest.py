
import unittest
import requests

from GetAuthToken import getToken
import json
from settings import mongodb,unittest_test_url
from DBUtil import Sync,Versions
import verifyResponse

Syncdb=Sync.Sync(mongodb)
Baseurl = unittest_test_url+"sync/"
header = {'content-type': "application/json",
                   'token':str(getToken())}
class SyncViewAllTest(unittest.TestCase):
    sync_id=None;
    def runTest(self):
        url=Baseurl+"view/all"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Sync view all test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        data=json_data.get("data").get("data")
        rec=data[0]
        SyncViewAllTest.sync_id=rec.get("sync_id")
                
class GetBySyncIdTest(unittest.TestCase):
    
    def runTest(self):
        if SyncViewAllTest.sync_id:
            url=Baseurl+"view/syncid/"+SyncViewAllTest.sync_id
        else:
            url=Baseurl+"view/syncid/dummy"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Sync_id  test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)    
                
def CleanDB():
    print "--------------------------------------------------------------------------------------------------------"
    print "--------------------------------------------------------------------------------------------------------"     
        
def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(SyncViewAllTest())
    suite.addTest(GetBySyncIdTest())
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


