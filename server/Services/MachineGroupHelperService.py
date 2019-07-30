from DBUtil import Machine, Users, MachineGroups, Tags
from settings import mongodb
from Services import HelperServices,TeamService,FlexibleAttributesHelper

db = mongodb

# collections
machineDB = Machine.Machine(db)
tagDB = Tags.Tags()
userdb = Users.Users(db)
machinegroupsDB = MachineGroups.MachineGroups(db)
teamService = TeamService.TeamService()


def add_missing_machine_group_attr(machine_group_details,is_new_machine=True):
    if is_new_machine:
        if not machine_group_details.get("description") or machine_group_details.get("description") is None:
            machine_group_details["description"] = ""

def validate_machine_group(machine_group_details):
    keys_to_validate=["group_name","machine_id_list"]
    for key in keys_to_validate:
        if not machine_group_details.get(key):
            raise Exception ("Mandatory Field: "+ (str(key).replace('_', ' ')).upper()+" is missing")
    if "," in  machine_group_details.get("group_name"):
        raise Exception ("Field: "+ (str("group_name").replace('_', ' ')).upper()+" cannot contain comma")       
    if (machine_group_details.get("group_name") and machine_group_details.get("machine_id_list")) is None:
            raise Exception("Mandatory fields to create a new group was not found.")
    HelperServices.validate_name(machine_group_details.get("group_name"),"machine group name") 
    if len(machine_group_details.get("machine_id_list",[]))<1:
        raise Exception("atleast one machine is required in group")
    for machine_id in machine_group_details["machine_id_list"]:
        if machineDB.GetMachine(machine_id) is None:
            raise Exception("Machine with _id : " + machine_id + " not exists")
    if machine_group_details.get("flexible_attributes"):
        FlexibleAttributesHelper.validate_entity_value("MachineGroup", machine_group_details.get("flexible_attributes"))

def add_update_machinegroups(machine_group_details,group_machine_id=None):
    
    validate_machine_group(machine_group_details)
    # EXISTING MACHINE
    if group_machine_id:
        if machinegroupsDB.get_machine_groups(group_machine_id) is None:
            raise Exception("Machinegroup with _id : " + group_machine_id + " not exists")
        existing_machine_group_detail = machinegroupsDB.machine_groups_by_name(machine_group_details.get("group_name"))
        if existing_machine_group_detail and str(existing_machine_group_detail["_id"]) <> str(group_machine_id):
            raise Exception("Failed as duplicate machinegroup was found")
        machine_group_details["_id"] = {}
        machine_group_details["_id"]["oid"] = group_machine_id
        group_machine_id = machinegroupsDB.update_machine_groups(machine_group_details)   
    elif machinegroupsDB.machine_groups_by_name(machine_group_details.get("group_name")):
        machine_group_details["_id"] = {}
        machine_group_details["_id"]["oid"] = str(machinegroupsDB.machine_groups_by_name(machine_group_details.get("group_name"))["_id"])
        group_machine_id = machinegroupsDB.update_machine_groups(machine_group_details)   
    else:
        #NEW MACHINE GROUP
        add_missing_machine_group_attr(machine_group_details,True)
        group_machine_id = machinegroupsDB.add_machine_groups(machine_group_details)   
        
    # RELOAD TEAM PERMISSIONS
    teamService.generate_details()
    return group_machine_id