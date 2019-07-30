import json
import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
from Services import PasswordHelper
import Users
import Role
from settings import key
import Tags


class Machine(DBUtil):
    def __init__(self, db):
        DBUtil.__init__(self, db)
        self.collection = db.Machine
        self.passHelper = PasswordHelper.PasswordHelper(key)
        self.userdb = Users.Users(db)
        self.roleDb = Role.Role(db)
        self.tagDB = Tags.Tags()
        # indexes
        self.collection.create_index(
            [('username', ASCENDING), ('host', ASCENDING)], unique=True)
        # THERE IS NO POINT KEEPING USERNAME AS INDEX AS IT IS ENCRYPTED AND CHANGES EVERYTIME
        # WE WILL HAVE TO ADD THIS VALIDATION ON CODE LEVEL IN DEF  is_machine_duplicate

    def decrypt(self, machineDetails):
        if machineDetails.get("username") is not None:
            machineDetails["username"] = self.passHelper.decrypt(
                machineDetails["username"])
        if machineDetails.get("password") is not None:
            machineDetails["password"] = self.passHelper.decrypt(
                machineDetails["password"])

        if machineDetails.get("steps_to_auth") and len(machineDetails.get("steps_to_auth")) > 0:
            steps_to_auth = []
            for data in machineDetails["steps_to_auth"]:
                if data.get("username"):
                    data["username"] = self.passHelper.decrypt(
                        data["username"])
                if data.get("password"):
                    data["password"] = self.passHelper.decrypt(
                        data["password"])
                steps_to_auth.append(data)
            machineDetails["steps_to_auth"] = steps_to_auth
        return machineDetails

    def encrypt(self, machineDetails):
        if machineDetails.get("username") is not None:
            machineDetails["username"] = self.passHelper.encrypt(
                machineDetails["username"])
        if machineDetails.get("password") is not None:
            machineDetails["password"] = self.passHelper.encrypt(
                machineDetails["password"])

        if machineDetails.get("steps_to_auth") and len(machineDetails.get("steps_to_auth")) > 0:
            steps_to_auth = []
            for data in machineDetails["steps_to_auth"]:
                if data.get("username"):
                    data["username"] = self.passHelper.encrypt(
                        data["username"])
                if data.get("password"):
                    data["password"] = self.passHelper.encrypt(
                        data["password"])
                steps_to_auth.append(data)
            machineDetails["steps_to_auth"] = steps_to_auth
        return machineDetails

    def GetMachines(self, filter_required=None, skip=0, limit=0):
        if filter_required:
            return self.collection.find(filter_required).skip(
            skip).limit(limit)
        else:
            return self.collection.find().skip(
            skip).limit(limit)

    def GetAllMachineIds(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns list of all machine ids.
        Example :
            get_tag_ids()
        '''
        machines = self.collection.find()
        machine_ids_list = []
        for machine in machines:
            machine_ids_list.append(str(machine["_id"]))
        return machine_ids_list

    def GetMachine(self, object_id):
        result = self.collection.find_one({"_id": ObjectId(object_id)})
        if not result:
            return result
        else:
            return self.decrypt(result)

    def is_machine_duplicate(self, username, host, machine_name, addition_type, machine_id_to_exclude=None):
        duplicate_machine = []
        if str(addition_type).lower() == "new":
            machines = self.GetMachines()
        elif str(addition_type).lower() == "update":
            machines = self.GetMachines(
                {"_id": {"$not": {"$eq": ObjectId(machine_id_to_exclude)}}})
        else:
            raise ValueError("Invalid type")
        for machine in machines:
            machine = self.decrypt(machine)
            if str(username + "@" + host).lower() in [str(str(machine.get("username")) + "@" + str(machine.get("host"))).lower()]:
                if machine_name.lower() == machine.get("machine_name").lower():
                    duplicate_machine.append(machine.get("machine_name"))               
        if str(addition_type).lower() == "new" and len(duplicate_machine) > 0:
            return ",".join(duplicate_machine)
        elif str(addition_type).lower() == "update" and len(duplicate_machine) >= 1:
            return ",".join(duplicate_machine)
        return None

    def GetMachinebyIp(self, ip):
        result = self.collection.find_one({"ip": ip})
        if not result:
            return result
        else:
            return self.decrypt(result)

    def get_machine_by_user_and_host(self,username,host):
        result = self.collection.find(
            {"host": re.compile(host, re.IGNORECASE)})
        for machine in result:
            machine = self.decrypt(machine)
            if username == machine.get("username"):
                return machine
        return None
         

    def get_machine_by_permitted_user(self, user_id):
        return self.collection.find({"permitted_users": user_id})

    def AddMachine(self, machineDetails):
        machineDetails["status"] = "1"
        machineDetails = self.encrypt(machineDetails)
        result = self.collection.insert_one(machineDetails)
        return str(result.inserted_id)

    def UpdateMachine(self, machineDetails):
        jsonnewEntry = {}
        for key in machineDetails.keys():
            if key != "_id":
                jsonnewEntry[key] = machineDetails[key]
        jsonnewEntry = self.encrypt(jsonnewEntry)
        result = self.collection.update_one({"_id": ObjectId(
            machineDetails["_id"]["oid"])}, {"$set": jsonnewEntry}, upsert=False)
        if machineDetails.get("included_in") is not None:
            self.collection.update_one({"_id": ObjectId(machineDetails["_id"]["oid"])}, {
                                       "$unset": {"included_in": machineDetails.get("included_in")}})
        return result.modified_count


    def DisableMachine(self, object_id):
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": {"status": "0"}})
        return result.modified_count

    def DeleteDocument(self, object_id):
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return str(result.deleted_count)

    def UpdateUserDetailsOnMachine(self, object_id, username, userpass):
        username = self.passHelper.encrypt(username)
        userpass = self.passHelper.encrypt(userpass)
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": {"username": username, "password": userpass}})
        return result.modified_count

    def UpdateUserTypeOnMachine(self, object_id, usertype):
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": {"user_type": usertype}})
        return result.modified_count

    def AddUserPermissionToMachine(self, object_id, per_id):
        self.collection.update_one({"_id": ObjectId(object_id)}, {
                                   "$pull": {"permitted_users": "all"}})
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$push": {"permitted_users": per_id}})
        return result.modified_count

    def RemoveUserPermissionToMachine(self, object_id, per_id):
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$pull": {"permitted_users": per_id}})
        return result.modified_count
    
    def get_machine_by_tag(self, tag):
        '''
        General description:

        Args:
            param 1: tag(string) :This is the parameter which \
            has the unique tag names for the existing Machine in the database.
            Returns:
                Returns the existing database entity based on the Machine Tags \
                from the Machine database.
        Example :
            get_machine_by_tag(tag)
        '''
        tag_name = self.tagDB.get_tag_by_name(tag)
        machine =[]
        if tag_name:
            machine = self.collection.find({"tag": re.compile(
                '^' + re.escape(str(tag_name["_id"])) + '$', re.IGNORECASE)})
        final_machines=[]
        for rec in machine:
            final_machines.append(self.decrypt(rec))
        return final_machines
    
    def GetMachinebyName(self, machine_name):
        result = self.collection.find({"machine_name": {"$regex": str(machine_name), "$options": "i"}})
        final_machines=[]
        for rec in result:
            final_machines.append(self.decrypt(rec))
        return final_machines        
    
    def GetMachineByFA(self, faName):        
        return self.collection.find({ "flexible_attributes."+faName : {"$exists": True}})