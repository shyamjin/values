
import re
from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
import DeploymentUnitApprovalStatus , DeploymentFields,Build,DeploymentUnitSet, DeploymentUnit
from datetime import datetime
class State(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for State.
    '''
    
    def __init__(self, db):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.State
        self.deploymentunitapprovalstatusdb=DeploymentUnitApprovalStatus.DeploymentUnitApprovalStatus()
        self.DeploymentFieldsdb=DeploymentFields.DeploymentFields(db)
        self.buildDb=Build.Build()
        # indexes
        self.collection.create_index(
            [('name', ASCENDING), ('parent_entity_id', ASCENDING)], unique=True)

    def get_state_all(self,is_all_details=False,type_filter=None,parent_filter=None, skip=0, limit=0,additional_filters={}):
        '''
        General description:
            
            param1 : get_all_details(string) :This is the parameter which determines \
            whether all state details should be visible to user or not.\
            This has two values - True /False .
            
            param 2 : skip (integer) : This is the count of the\
            State to be skipped.

            param 3 : limit (integer) : This is the count of the\
            State to be limited from the database .
        Returns:
                Returns the database entities existing for State based on status filter \
                skip count ,limit count and filer_required .
        Example :
            get_state_all(True, skip,limit)
        '''
        # default value of limit and skip is set in respective APIs
        # in DAO skip=0 , limit =0 means it will send all documents
        condition_to_filter={}
        if additional_filters:
            condition_to_filter.update(additional_filters)
        if type_filter:
            condition_to_filter["type"] =  {"$in": type_filter}
        
        if parent_filter:
            condition_to_filter["parent_entity_id"] =  {"$in": parent_filter}
            
        if len(condition_to_filter.keys()) > 0:
            count = self.collection.find(condition_to_filter).skip(
                skip).limit(limit).count()
            if count < 1:
                skip = 0
            states=self.collection.find(condition_to_filter).skip(skip).limit(limit)
            final_states=[]
            for state in states:
                state=self.get_basic_state_details(state)
                if is_all_details == True and states is not []:
                    state= self.get_state_details(state)
                final_states.append(state)
            return final_states
        else:
            count = self.collection.find().skip(skip).limit(limit).count()
            if count < 1:
                skip = 0
            states=self.collection.find().skip(skip).limit(limit)
            final_states=[]
            for state in states:
                state=self.get_basic_state_details(state)
                if is_all_details == True and states is not []:
                    state= self.get_state_details(state)
                final_states.append(state)
            return final_states        

    def get_state_by_id(self, object_id , is_all_details=False,only_build_number=False):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            state stored in the database.

            param2 : get_all_details(string) :This is the parameter which determines \
            whether all state details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the state id and\
                is_all_details parameter.
        Example :
            get_state_by_id(id ,True)
        '''
        state = self.collection.find_one({"_id": ObjectId(str(object_id))})
        if state is not None:
            state=self.get_basic_state_details(state)
        if is_all_details == True and state is not None:
            state = self.get_state_details(state,only_build_number)
        return state
    
    def get_state_by_name(self, state_name , is_all_details=False,only_build_number=False):
        '''
        General description:

        Args:
            param1 : state_name : This is the name of the\
            state stored in the database.

            param2 : get_all_details(string) :This is the parameter which determines \
            whether all state details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the state name and\
                is_all_details parameter.
        Example :
            get_state_by_name(state_name ,True)
        '''
        states = self.collection.find({"name": re.compile(state_name, re.IGNORECASE)})
        final_states=[]
        for state in states:
            state=self.get_basic_state_details(state)
            if is_all_details == True and state is not None:
                state = self.get_state_details(state,only_build_number)
            final_states.append(state)
        return final_states
    
      
    
    def get_state_by_parent_entity_id_name(self,state_name,parent_entity_id , is_all_details=False):
        '''
        General description:

        Args:
            param1 : state_name : This is the name of the\
            state stored in the database.
            
            param2 : object_id(parent_entity_id) : This is the parent_entity_id of the\
            state stored in the database.
            
            param3 : get_all_details(string) :This is the parameter which determines \
            whether all state details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the state name and\
                is_all_details parameter.
        Example :
            get_state_by_parent_entity_id_name(state_name,parent_entity_id ,True)
        '''
        state = self.collection.find_one({"name": re.compile(str(state_name), re.IGNORECASE) , "parent_entity_id": str(parent_entity_id)})
        if state is not None:
            state=self.get_basic_state_details(state)
        if is_all_details == True and state is not None:
            state= self.get_state_details(state)
        return state

    def get_state_details(self, state,only_build_number=False):
        '''
        General description:

        Args:
            param 1 : state(JSON) : This is the parameter which has details \
            for state .
        Returns:
                Returns the database entity based on the state details ,state
        Example :
            get_state_details(state)
        '''
        
        #IF ITS DU STATE
        state["deployment_field"] =self.DeploymentFieldsdb.GetDeploymentFields(str(state.get("_id")))
        if state.get("build_id"):      
            state["build"]=self.buildDb.get_build_by_id(state.get("build_id"), True, only_build_number)
        #IF ITS DU SET STATE
        du_states=[]
        for rec in state.get("states",[]) :
            du_states.append(self.get_state_by_id(rec, True,only_build_number))
        if len(du_states) >0 : # SHOULD NOT BE RETURNED FOR DU STATE
            state["states"] = du_states
              
        return state
    
    def get_state_by_parent_entity_id(self, parent_entity_id , is_all_details = False,only_build_number=False):
        '''
        General description:

        Args:
            param1 : object_id(parent_entity_id) : This is the parent_entity_id of the\
            state stored in the database.
            
            param2 : get_all_details(string) :This is the parameter which determines \
            whether all state details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entities based on the parent_entity_id
        Example :
            get_state_by_parent_entity_id(parent_entity_id , True)
        '''
        states = self.collection.find({"parent_entity_id": str(parent_entity_id)})
        final_states=[]
        for state in states:
            state=self.get_basic_state_details(state)
            if is_all_details == True and states is not []:
                state= self.get_state_details(state,only_build_number)
            final_states.append(state)
        return final_states
    def add_state(self, new_state):
        '''
        General description:

        Args:
            param1 : new_state(JSON) : This is the parameter which has details \
            for new state .
        Returns:
              Returns the id of the newly created state in the database.
        Example :
             add_state(new_state)
        '''
        new_state=self.encrypt(new_state)
        result = self.collection.insert_one(new_state)
        return str(result.inserted_id)

    def update_state(self, state):
        '''
        General description:

        Args:
            param1 : state (JSON) : This is the parameter which has details of state.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_state(state)
        '''
        json_new_entry = {}
        for key in state.keys():
            if key != "_id":
                json_new_entry[key] = state[key]
        json_new_entry=self.encrypt(json_new_entry)        
        result = self.collection.update_one({"_id": ObjectId(state["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_state(self, object_id):
        '''
        General description:

        Args:
           param1 : object_id(object) : This is the unique id of the\
            state stored in the database.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_state(id)
        '''
        return self.collection.delete_one({"_id": ObjectId(object_id)}).deleted_count
        
    def delete_state_by_parent_entity_id(self, parent_entity_id):
        '''
        General description:

        Args:
           param1 : parent_entity_id(object) : This is the unique id of the\
            state stored in the database.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_state_by_parent_entity_id(id)
        '''
        result = self.collection.delete_many({"parent_entity_id": parent_entity_id})
        return result.deleted_count

        
    def encrypt (self , state):
        print "encrypt data"
        return state
        
    def decypt (self , state):
        print "decypt data"
        return state
    
    def get_basic_state_details (self , state):
        '''
        General description:

        Args:
           param1 : state(object) : This is the state stored in the database.
        Returns:
              Returns updated state details.
        Example :
             get_basic_state_details(state)
        '''
        if (state.get("approval_status") is not None):
            app_status = self.deploymentunitapprovalstatusdb.GetDeploymentUnitApprovalStatusById(state.get("approval_status"))
            if not app_status : raise Exception("approval_status with _id: "+str(state.get("approval_status"))+" was not found in database")
            state["approval_status"]=app_status.get("name")
        return state
    
    def add_state_details_for_sync(self,state_data):
        '''
        General description:

        Args:
           param1 : state(object) : This is the state stored in the database.
        Returns:
              Returns updated state details.
        Example :
             add_state_details_for_sync(state)
        '''
        if state_data:
            state_data["deployment_field"] =self.DeploymentFieldsdb.GetDeploymentFields(str(state_data.get("_id")))
            if state_data.get("deployment_field"):  
                if "_id" in state_data["deployment_field"].keys():
                    state_data["deployment_field"].pop("_id")
            if state_data.get("build_id"):      
                state_data["build"]=self.buildDb.get_build_by_id(state_data.get("build_id"), False)
                if state_data.get("build"):  
                    state_data["build_id"]=state_data["build"].get("build_number")
                    state_data["build"]["build_date"] = str(state_data["build"].get("build_date"))
                    state_data.pop("build")
                else:
                    raise Exception ("Build details were not found for build_id: "+str(state_data.get("build_id")))            
        return state_data
        
    def get_state_data_for_sync(self,state):
        '''
        General description:

        Args:
           param1 : state(object) : This is the state stored in the database.
        Returns:
              Returns updated state details.
        Example :
             get_state_data_for_sync(state)
        '''
        record={}        
        record["state_data"] = self.add_state_details_for_sync(state)
        # _id is used in self.add_state_details_for_sync
        if "_id" in state.keys():
            record["source_state_id"] = str(state.get("_id"))
            state.pop("_id")        
        return record    