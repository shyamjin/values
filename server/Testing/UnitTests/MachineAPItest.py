
import unittest
import requests

from GetAuthToken import getToken
import json
from settings import mongodb,unittest_test_url
from DBUtil import Machine,Accounts,MachineType,Users,UserFavoriteMachine
import verifyResponse

UsersDb=Users.Users(mongodb)
AccountsDb=Accounts.Accounts()
MachineTypeDb=MachineType.MachineType(mongodb)
Machinedb=Machine.Machine(mongodb)
UserFavoriteMachineDb=UserFavoriteMachine.UserFavoriteMachine(mongodb)
Baseurl = unittest_test_url+"machine/"
header = {'content-type': "application/json",
                   'token':str(getToken())}
class AddMachineTest(unittest.TestCase):
    oid=None;
    machine_name="UnitTestMachine"
    tag="test"
    def runTest(self):
        url=Baseurl+"new"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Create Machine test"
        payload={"permitted_users":["all"],
                 "included_in":[],
                 "permitted_teams":[],
                 "port":22,
                 "shell_type":"",
                 "reload_command":"",
                 "tag":["test"],
                 "fav":False,
                 "auth_type":"password",
                 "machine_name":"UnitTestMachine",
                 "ip":"10.19.87.107",
                 "host":"vptestind01",
                 "username":"root",
                 "password":"root123",
                 "machine_type":str(MachineTypeDb.get_machine_type_by_name("ST").get("_id")),
                 "account_id":str(AccountsDb.get_account_by_name("Test").get("_id")),
                 "status":"1",
                 "steps_to_auth":[]}

        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        AddMachineTest.oid = str(json_data.get("data").get("id"))

class UpdateMachineTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"update"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Update Machine test"
        payload={"_id":{"oid":AddMachineTest.oid},
                 "machine_name":"UnitTestMachine",
                 "host":"vptestind01",
                 "ip":"10.19.87.107",
                 "username":"root",
                 "shell_type":"",
                 "reload_command":"",
                 "tag":[],
                 "auth_type":"password",
                 "machine_type":str(MachineTypeDb.get_machine_type_by_name("Production").get("_id")),
                 "password":"root123",
                 "port":22,
                 "account_id":str(AccountsDb.get_account_by_name("Test").get("_id")),
                 "permitted_teams":[],
                 "included_in":[],
                 "steps_to_auth":[]}
        
        response = requests.request("PUT", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        
        
        
class AddFavMachineTest(unittest.TestCase):
    oid=None
    def runTest(self):
        url=Baseurl+"fav/new"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Add Fav Machine test"
        payload={"user_id":str(UsersDb.get_user_by_name("SuperAdmin")),
                 "machine_id":AddMachineTest.oid,
                 "status":1}
        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        AddFavMachineTest.oid = str(json_data.get("data").get("_id"))

class GetUserFavMachineTest(unittest.TestCase):
    oid=None
    def runTest(self):
        url=Baseurl+"fav/user/"+str(UsersDb.get_user_by_name("SuperAdmin"))
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get User Fav Machine test"
        response = requests.request("GET", url,headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        
class GetUserFavByMachineIdMachineTest(unittest.TestCase):
    oid=None
    def runTest(self):
        url=Baseurl+"fav/machine/"+AddMachineTest.oid+"/user/"+str(UsersDb.get_user_by_name("SuperAdmin"))
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get User Fav by Machine Id Machine test"
        response = requests.request("GET", url,headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
    
class DeleteFavMachineTest(unittest.TestCase):
    oid=None
    def runTest(self):
        url=Baseurl+"fav/delete/"+AddFavMachineTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Delete Fav Machine test"
        response = requests.request("DELETE", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)

class GetAllMachineTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/all"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get all Machine test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)                

class GetByIdMachineTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/"+AddMachineTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Id Machine test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)    
        
class GetAllTypeMachineTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"type/all"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get all type Machine test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)                

class PingMachineTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"test"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For ping Machine test"
        payload ={"machine_name":"UnitTestMachine",
                  "host":"vptestind01",
                  "ip":"10.19.87.107",
                  "username":"root",
                  "shell_type":"",
                  "reload_command":"",
                  "auth_type":"password",
                  "machine_type":str(MachineTypeDb.get_machine_type_by_name("Production").get("_id")),
                  "password":"root123",
                  "port":22,
                  "account_id":str(AccountsDb.get_account_by_name("Test").get("_id")),
                  "steps_to_auth":[]}
        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)                

class DeleteMachineTest(unittest.TestCase):
     
    def runTest(self):
        url=Baseurl+"remove/"+AddMachineTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Delete Machine test"
        response = requests.request("DELETE", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response) 
        
class SearchManchineByTag(unittest.TestCase):
     
    def runTest(self):
        url=Baseurl+"search/tag/"+AddMachineTest.tag
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Search Machine by tag"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response) 
                
class SearchManchineByName(unittest.TestCase):
     
    def runTest(self):
        url=Baseurl+"search/name/"+AddMachineTest.machine_name
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Search Machine by name"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response) 
                                
        
def CleanDB():
    print "--------------------------------------------------------------------------------------------------------"
    print "Cleaning Database"
    if AddMachineTest.oid is not None:
        Machinedb.DeleteDocument(AddMachineTest.oid)
    if AddFavMachineTest.oid is not None:
        UserFavoriteMachineDb.delete_user_favorite_machine(AddFavMachineTest.oid)
    print "--------------------------------------------------------------------------------------------------------"     
        
def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(AddMachineTest())
    suite.addTest(UpdateMachineTest())
    suite.addTest(AddFavMachineTest())
    suite.addTest(GetUserFavMachineTest())
    suite.addTest(GetUserFavByMachineIdMachineTest())
    suite.addTest(DeleteFavMachineTest())
    suite.addTest(GetAllMachineTest())
    suite.addTest(GetByIdMachineTest())
    suite.addTest(GetAllTypeMachineTest())
    suite.addTest(PingMachineTest())
    suite.addTest(DeleteMachineTest())
    suite.addTest(SearchManchineByTag())
    suite.addTest(SearchManchineByName())
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

