from datetime import datetime

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class ToolsOnMachine(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for ToolsOnMachine.
    '''

    def __init__(self, db):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.ToolsOnMachine
        # indexes
        self.collection.create_index(
            [('parent_entity_id', ASCENDING), ('machine_id', ASCENDING)], unique=True)
    '''
    tools on machine contains entries of tool and DUs installed on the machine
    '''

    def get_tools_on_machine_all(self,show_active=True):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns the database entities existing for ToolsOnMachine.
        Example :
            get_tools_on_machine_all()
        '''
        if show_active:
            return self.collection.find({"status": "1"})
        return self.collection.find({})

    def get_tools_on_machine_by_parent_entity_id(self, parent_entity_id,show_active=True):
        '''
        General description:

        Args:
            param1 : parent_entity_id(object) : This is the unique id of the\
            Tool stored in the database.
        Returns:
                Returns the database entity based on the parent_entity_id.
        Example :
            get_tools_on_machine_by_parent_entity_id(parent_entity_id)
        '''
        if show_active:
            return self.collection.find(
            {"parent_entity_id": parent_entity_id, "status": "1"})
        return self.collection.find(
            {"parent_entity_id": parent_entity_id})

    def get_tools_on_machine_by_machine_id(self, machineid):
        '''
        General description:

        Args:
            param1 : machineid(object) : This is the unique id of the\
            machine stored in the database.
        Returns:
                Returns the database entity based on the machineid.
        Example :
            get_tools_on_machine_by_machine_id(machineid)
        '''
        return self.collection.find({"machine_id": machineid, "status": "1"}) 
    
    
    def get_by_machine_group_id(self, machine_group_id):
        '''
        General description:

        Args:
            param1 : machine_group_id(object) : This is the unique id of the\
            machine group stored in the database.
        Returns:
                Returns the database entity based on the machine_group_id.
        Example :
            get_by_machine_group_id(machine_group_id)
        '''
        return self.collection.find({"machine_group_id": machine_group_id, "status": "1"})         

    def get_tools_on_machine_by_machine_id_and_parent_entity_id(self, machineid, parent_entity_id,show_active=False):
        '''
        General description:

        Args:
            param 1 : machineid (object) : This is the unique id of the\
            machine stored in the database.

            param 2 : parent_entity_id(object) : This is the unique id of the\
            Tool stored in the database.
        Returns:
                Returns the database entity based on the machineid.
        Example :
            get_tools_on_machine_by_machine_id_and_parent_entity_id(machineid , parent_entity_id)
        '''
        if show_active:
            return self.collection.find_one(
            {"machine_id": machineid, "parent_entity_id": parent_entity_id, "status": "1"})
        return self.collection.find_one(
            {"machine_id": machineid, "parent_entity_id": parent_entity_id})
        


    def get_tools_on_machine_by_filter(self, machine_id=None, parent_entity_id=None,\
                                        build_id=None,deployment_request_id=None,is_active=True):
        '''
        General description:

        Args:
            param 1 : machineid (object) : This is the machineid name of the\
            machine stored in the database.

            param 2 : parent_entity_id(object) : This is the unique id of the\
            Tool stored in the database.

             param 3 : build_id (object) : This is the unique id of the\
            build stored in the database.
             
             param 4 : deployment_id (object) : This is the unique id of the\
            deployment stored in the database.
            
            param 5 : is_active (boolean) : This is the indicator if we need only active records
        Returns:
                Returns the database entity based on the host.
        Example :
            get_tools_on_machine_by_filter(machineid , parent_entity_id, build_id,deployment_request_id,is_active)
        '''
        filter_req={} 
        if machine_id : filter_req["machine_id"]=machine_id
        if parent_entity_id : filter_req["parent_entity_id"]=parent_entity_id
        if build_id : filter_req["build_id"]=build_id
        if deployment_request_id : filter_req["deployment_request_id"]=deployment_request_id
        if is_active:filter_req["status"]="1"
        return self.collection.find_one(filter_req)        
    
    def get_tools_on_machine_by_host_parent_entity_id_and_build_id(self, machineid, parent_entity_id, build_id):
        '''
        General description:

        Args:
            param 1 : host (object) : This is the host name of the\
            machine stored in the database.

            param 2 : parent_entity_id(object) : This is the unique id of the\
            Tool stored in the database.

             param 3 : build_id (object) : This is the unique id of the\
            build stored in the database.
        Returns:
                Returns the database entity based on the host.
        Example :
            get_tools_on_machine_by_machine_id_and_parent_entity_id(host , parent_entity_id, build_if)
        '''
        tool = self.collection.find_one(
            {"host": machineid, "parent_entity_id": parent_entity_id, "build_id": build_id, "status": "1"})
        return tool
    
    def get_tools_on_machine_by_machine_by_condition(self, condition, condition_value):
        '''
        General description:

        Args:
            param1 : condition(string) : This determines the condition on which the\
            ToolsOnMachine will be fetched from database.

            param 2:  condition_value(list) : This parameter full fills the condition on which the\
            ToolsOnMachine will be fetched from database. Its a kind of list.
        Returns:
                Returns the database entity based on the condition.
        Example :
            get_tools_on_machine_by_machine_by_condition(condition,condition_value)
        '''
        return self.collection.find({condition: {"$in": [str(condition_value)]}})

    def add_tool_on_machine(self, json_entry):
        '''
        General description:

        Args:
            param1 : new_tool(JSON) : This is the parameter which has details \
            for new ToolOnMachine .
        Returns:
              Returns the id of the newly created ToolOnMachine in the database.
        Example :
             add_tool_on_machine(json_entry)
        '''
        json_entry["create_date"] = datetime.now()
        json_entry["update_date"] = datetime.now()
        result = self.collection.insert_one(json_entry)
        return str(result.inserted_id)

    def update_tools_on_machine(self, tool):
        '''
        General description:

        Args:
            param1 : tool (JSON) : This is the parameter which has details of ToolOnMachine.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_tools_on_machine(tool)
        '''
        json_new_entry = {}
        for key in tool.keys():
            if key != "_id":
                json_new_entry[key] = tool[key]
        json_new_entry["update_date"] = datetime.now()
        result = self.collection.update_one({"_id": ObjectId(tool["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def update_hostname(self, machine_id, hostname):
        result = self.collection.update_many({"machine_id": machine_id}, {
                                             "$set": {"host": hostname}}, upsert=False)
        return result.modified_count

    def delete_tools_by_machine_id(self, machine_id):
        '''
        General description:

        Args:
           param1 : machine_id(object) : This is the unique id of the\
            Machine based on which ToolOnMachine will be deleted.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_tools_by_machine_id(id)
        '''
        result = self.collection.delete_many({"machine_id": machine_id})
        return result.deleted_count
