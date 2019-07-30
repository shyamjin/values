import unittest
import requests

from GetAuthToken import getToken
import json
from settings import mongodb,unittest_test_url
from DBUtil import MachineGroups,Accounts,Users,MachineType,Machine
import verifyResponse

UsersDb=Users.Users(mongodb)
AccountsDb=Accounts.Accounts()
MachineDb=Machine.Machine(mongodb)
MachineTypeDb=MachineType.MachineType(mongodb)
MachineGroupdb=MachineGroups.MachineGroups(mongodb)
Baseurl = unittest_test_url+"machinegroups/"
header = {'content-type': "application/json",
                   'token':str(getToken())}
class AddMachineGroupTest(unittest.TestCase):
    oid=None;
    MacOid1=None;
    MacOid2=None
    def runTest(self):
        CreateMachinesForMachineGroup()
        url=Baseurl+"add"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Create MachineGroup test"
        payload={"group_name":"UnitTestMachineGroup",
                 "machine_id_list":[AddMachineGroupTest.MacOid1,
                                    AddMachineGroupTest.MacOid2]}
        response = requests.request("POST", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        json_data = json.loads(response.text)
        AddMachineGroupTest.oid = str(json_data.get("data").get("id"))

class UpdateMachineGroupTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"update"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Update MachineGroup test"
        payload={"_id":{"oid":AddMachineGroupTest.oid},
                 "group_name":"UnitTestMachineGroup",
                 "description":"Test",
                 "machine_id_list":[AddMachineGroupTest.MacOid1,
                                    AddMachineGroupTest.MacOid2]}
        
        response = requests.request("PUT", url, data=json.dumps(payload), headers=header,verify=False)
        verifyResponse.PositiveTesting(response)
        

class GetAllMachineGroupTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get all MachineGroup test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)                

class GetByIdMachineGroupTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/"+AddMachineGroupTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Id MachineGroup test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)    
     
class GetByNameMachineGroupTest(unittest.TestCase):
    
    def runTest(self):
        url=Baseurl+"view/name/UnitTestMachineGroup"
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Get by Name MachineGroup test"
        response = requests.request("GET", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response)               

class DeleteMachineGroupTest(unittest.TestCase):
     
    def runTest(self):
        url=Baseurl+"delete/"+AddMachineGroupTest.oid
        print "--------------------------------------------------------------------------------------------------------"
        print "Calling API :"+url + " For Delete MachineGroup test"
        response = requests.request("DELETE", url, headers=header,verify=False)
        verifyResponse.PositiveTesting(response) 
 
def CreateMachinesForMachineGroup():
    url=unittest_test_url+"machine/new"
    payload1={"permitted_users":["all"],
                 "included_in":[],
                 "permitted_teams":[],
                 "port":22,
                 "shell_type":"",
                 "reload_command":"",
                 "tag":[],"fav":False,
                 "auth_type":"password",
                 "machine_name":"TestMachine3",
                 "ip":"10.19.87.07",
                 "host":"vptest",
                 "username":"rot",
                 "password":"rot123",
                 "machine_type":str(MachineTypeDb.get_machine_type_by_name("ST").get("_id")),
                 "account_id":str(AccountsDb.get_account_by_name("Test").get("_id")),
                 "status":"1",
                 "steps_to_auth":[]}
    
    payload2={"permitted_users":["all"],
                 "included_in":[],
                 "permitted_teams":[],
                 "port":22,
                 "shell_type":"",
                 "reload_command":"",
                 "tag":[],"fav":False,
                 "auth_type":"password",
                 "machine_name":"TestMachine4",
                 "ip":"10.19.87.1",
                 "host":"vptest",
                 "username":"roo",
                 "password":"root1",
                 "machine_type":str(MachineTypeDb.get_machine_type_by_name("ST").get("_id")),
                 "account_id":str(AccountsDb.get_account_by_name("Test").get("_id")),
                 "status":"1",
                 "steps_to_auth":[]}
    response = requests.request("POST", url, data=json.dumps(payload1), headers=header,verify=False)
    json_data = json.loads(response.text)
    if(response.status_code!=200):
        print "FAILURE"
        raise Exception(str(response.text))
    AddMachineGroupTest.MacOid1 = str(json_data.get("data").get("id"))
    response = requests.request("POST", url, data=json.dumps(payload2), headers=header,verify=False)
    json_data = json.loads(response.text)
    if(response.status_code!=200):
        print "FAILURE"
        raise Exception(str(response.text))
    AddMachineGroupTest.MacOid2 = str(json_data.get("data").get("id"))  
    
                 
def CleanDB():
    print "--------------------------------------------------------------------------------------------------------"
    print "Cleaning Database"
    if AddMachineGroupTest.oid is not None:
        MachineGroupdb.delete_machine_groups(AddMachineGroupTest.oid)
    if AddMachineGroupTest.MacOid1 is not None:
        MachineDb.DeleteDocument(AddMachineGroupTest.MacOid1)
    if AddMachineGroupTest.MacOid2 is not None:
        MachineDb.DeleteDocument(AddMachineGroupTest.MacOid2)
    print "--------------------------------------------------------------------------------------------------------"     
        
def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(AddMachineGroupTest())
    suite.addTest(UpdateMachineGroupTest())
    suite.addTest(GetAllMachineGroupTest())
    suite.addTest(GetByIdMachineGroupTest())
    suite.addTest(GetByNameMachineGroupTest())
    suite.addTest(DeleteMachineGroupTest())

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

