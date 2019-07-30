from bson.objectid import ObjectId
from pymongo import ASCENDING
import re
from DBUtil import DBUtil
from settings import key
import Machine


class MachineGroups(DBUtil):
    '''
        General description:

       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for MachineGroups.
    '''

    def __init__(self, db):
        '''
           General description:
           This function initializes the database variables and \
           index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.MachineGroups
        self.machineDB = Machine.Machine(db)
        # indexes
        self.collection.create_index([('group_name', ASCENDING)], unique=True)

    def machine_groups_by_name(self, name):
        '''
        General description:
        Args:
            param1: name(string) : This is the MachineGroup Name
        Returns:
                Returns Database entity of MachineGroup for the given Machine Group Name
        Example :
            machine_groups_by_name("TestGroup")
        '''
        return self.collection.find_one({"group_name": re.compile('^' + re.escape(name) + '$', re.IGNORECASE)})

    def get_machine_groups(self, object_id, is_all_details=False):
        '''
        General description:
        Args:
            param1 (object_id) : This is the MachineGroup Id which is stored in database
        Returns:
                Returns Database entity of MachineGroup for the given Machine Group Id
        Example :
            get_machine_groups(id)
        '''
        machine_group_details=self.collection.find_one({"_id": ObjectId(str(object_id))})
        if is_all_details == True and machine_group_details is not None:
            self.get_state_details(machine_group_details)
        return machine_group_details 
    
    def get_details(self,machine_group_details):
        machine_group_details["machine_deatils"]=[]
        for machine in machine_group_details.get("machine_id_list"):
            machine_group_details["machine_deatils"].append(self.machineDB.GetMachine(machine))

    def GetAllMachineGroupIds(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns list of all machine group ids.
        Example :
            get_tag_ids()
        '''
        machinegroups = self.collection.find()
        machinegroup_ids_list = []
        for machinegroup in machinegroups:
            machinegroup_ids_list.append(str(machinegroup["_id"]))
        return machinegroup_ids_list

    def get_machine_group_by_machine(self, machine_id):
        '''
        General description:
        Args:
            param1 (machine_id) : This is the machine_id which is part of a machine group.
        Returns:
                Returns Database entity of MachineGroup for the given machine_id
        Example :
             get_machine_group_by_machine(id)
        '''
        return self.collection.find({"machine_id_list": machine_id})

    def get_all_machine_groups(self, filter_required=None):
        '''
        General description:
        Args:
            param1 (filter_required) : This is the parameter using\
            which we can filter different machine groups.
            It can be machine group name or Machine ID .
        Returns:
                Returns Database entity of MachineGroup for the given filters
        Example :
             get_all_machine_groups(name) or get_all_machine_groups(machineID)
        '''
        if filter_required:
            return self.collection.find(filter_required)
        else:
            return self.collection.find()
    
    def get_machine_group_by_name(self, name):
        '''
        General description:
        Args:
            param1 (filter_required) : This is the parameter using\
            which we can filter different machine groups.
            It can be machine group name or Machine ID .
        Returns:
                Returns Database entity of MachineGroup for the given filters
        Example :
             get_all_machine_groups(name) or get_all_machine_groups(machineID)
        '''
        return self.collection.find_one({"group_name":name})        
    def add_machine_groups(self, group):
        '''
        General description:
        Args:
            param1 (group) : This is the parameter which has the details for \
            the new machine group to be added in database.
        Returns:
                Returns Database entity id of the new MachineGroup created
        Example :
             add_machine_groups(group)
        '''
        result = self.collection.insert_one(group)
        return str(result.inserted_id)

    def add_to_machine_groups(self, object_id, id_machine):
        '''
        General description:
        Args:
            param1 (object_id) : This is the id of the existing machine\
            group which we have to update.

            param2 (id_machine) : This is the machine ID of the \
            existing machine we wish to add to a MachineGroup.
        Returns:
                Returns the count of records that has been \
                updated successfully for a given MachineGroup .
        Example :
             add_to_machine_groups(id, id_machine)
        '''
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$push": {"machine_id_list": id_machine}})
        return result.modified_count

    def remove_from_machine_groups(self, object_id, id_machine):
        '''
        General description:
        Args:
            param1 (object_id) : This is the id of the existing\
            machine group which we have to remove.

            param2 (id_machine) : This is the machine ID which belongs to this Machine Group .
        Returns:
                Returns the count of records that has been updated /removed\
                successfully for a given MachineGroup .
        Example :
             remove_from_machine_groups(id, id_machine)
        '''
        result = self.collection.update_many(
            {"machine_id_list": id_machine}, {"$pull": {"machine_id_list": id_machine}})
        return result.modified_count

    def remove_machine_from_all_groups(self, id_machine):
        '''
        General description:
        Args:       
            param1 (id_machine) : This is the machine ID which we want to remove .
        Returns:
                Returns the count of records that has been updated /removed\
                successfully for a given MachineGroup .
        Example :
             remove_machine_from_all_groups(id, id_machine)
        '''
        result = self.collection.update(
            {}, {"$pull": {"machine_id_list": id_machine}})
        return result

    def update_machine_groups(self, group):
        '''
        General description:
        Args:
            param1 (group) : This is the group details of the existing machine \
            group which we have to update.Its a JSON object.
        Returns:
                Returns the count of records that has been updated \
                successfully for a given MachineGroup .
        Example :
             update_machine_groups(group)
        '''
        json_new_entry = {}
        for key in group.keys():
            if key != "_id":
                json_new_entry[key] = group[key]
        result = self.collection.update_one({"_id": ObjectId(group["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_machine_groups(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the ID of the existing \
            machine group which we have to delete.
        Returns:
                Returns the count of records that has been deleted \
                successfully for a given MachineGroup .
        Example :
             delete_machine_groups(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count
    def GetMachineGroupByFA(self, faName):        
        return self.collection.find({ "flexible_attributes."+faName : {"$exists": True}})