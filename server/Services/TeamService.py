'''
Created on Apr 27, 2017

@author: pdinda
'''

'''
    This Class is responsible to loop over Teams and refresh a static array static_users
    This array is later used by the project to manage the data available to users 
'''

import logging
from threading import Lock
from autologging import logged
from bson.objectid import ObjectId
from DBUtil import Versions, Tool, \
    Tags, ToolSet, \
    DeploymentUnitSet, DeploymentUnit, \
    Users, Teams, Machine, MachineGroups, Role
from settings import mongodb



# STORE IN STATIC MEMORY
static_users = {}  # DATA OF USERS MAPPED HERE <---
static_teams = {}  # DATA OF TEAMS MAPPED HERE <---
static_tags = []


locker = Lock()


def synchronized(lock):
    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap

@logged(logging.getLogger("TeamService"))
class TeamService(object):

    # Init's Data
    def __init__(self):

        self.versionsDB = Versions.Versions(mongodb)
        self.toolDB = Tool.Tool(mongodb)
        self.tagDB = Tags.Tags()
        self.toolsetdb = ToolSet.ToolSet(mongodb)
        self.deploymentunitsetdb = DeploymentUnitSet.DeploymentUnitSet()
        self.deploymentunitdb = DeploymentUnit.DeploymentUnit()
        self.teamDB = Teams.Teams(mongodb)
        self.machineDB = Machine.Machine(mongodb)
        self.machinegroupsDB = MachineGroups.MachineGroups(mongodb)
        self.toolsetdb = ToolSet.ToolSet(mongodb)
        self.userdb = Users.Users(mongodb)
        self.roledb = Role.Role(mongodb)

    @synchronized(locker)
    def generate_details(self):

        global static_users, static_teams, static_tags
        '''
        This method is responsible to generate reference data used by the system to allow api's data 
        '''

        print "Loading data for users in memory..."
        
        
       
        
        
        #ALL DATA
        all_machine_groups_data=list(self.machinegroupsDB.get_all_machine_groups())
        all_machine_data=list(self.machineDB.GetMachines())
        all_tool_set_data=list(self.toolsetdb.get_all_tool_set())
        all_du_set_data=list(self.deploymentunitsetdb.GetAllDeploymentUnitSet())
        all_tool_data=list(self.toolDB.get_tools_all())
        all_du_data=list(self.deploymentunitdb.GetAllDeploymentUnits())
        all_user_data=list(self.userdb.get_all_users())
        
                
        #GET ALL TO BE USED IDS
        # THESE HAVE STR IDS
        all_tag_ids=self.tagDB.GetAllTagIds()
        all_tool_ids=[]
        all_tool_set_ids=[]
        all_du_ids=[]
        all_du_set_ids=[]
        all_machine_ids=[]
        all_machine_group_ids=[]
        
        # THESE LIST CONTAIN ALL IDS FROM DATABASE
        #THESE HAVE OBJECT IDS
        all_parent_entity_id_list = []      
        all_parent_entity_set_id_list = []  
        all_machine_id_list = []
        all_machine_group_id_list = []
        
        
        
        for rec in all_machine_groups_data:
            all_machine_group_ids.append(str(rec["_id"]))    
            all_machine_group_id_list.append(rec["_id"])
            
        for rec in all_machine_data:
            all_machine_ids.append(str(rec["_id"]))    
            all_machine_id_list.append(rec["_id"])    
            
        for rec in all_tool_set_data:
            all_tool_set_ids.append(str(rec["_id"]))    
            all_parent_entity_set_id_list.append(rec["_id"])      
            
        for rec in all_du_set_data:
            all_du_set_ids.append(str(rec["_id"]))    
            all_parent_entity_set_id_list.append(rec["_id"])       

        for rec in all_tool_data:
            all_tool_ids.append(str(rec["_id"]))    
            all_parent_entity_id_list.append(rec["_id"]) 
            
        for rec in all_du_data:
            all_du_ids.append(str(rec["_id"]))    
            all_parent_entity_id_list.append(rec["_id"])     
            
        ################## WORKING PER TEAM HERE ####################
        # 1)Loop over all teams to get related data
        for team_details in self.teamDB.get_all_teams():

            # THESE LIST CONTAIN ALL IDS FROM DATABASE FOR THIS TEAM
            tag_id_list = []
            parent_entity_tag_list = []
            parent_entity_set_tag_list = []
            parent_entity_id_list = []
            parent_entity_set_id_list = []
            machine_id_list = []
            machine_group_id_list = []
            distribution_list_list = []

            # LOAD LIST FROM TEAM REC
            if team_details.get("tag_id_list"):
                if "all" in team_details.get("tag_id_list"):
                    tag_id_list.extend(all_tag_ids)
                else:
                    tag_id_list.extend(team_details["tag_id_list"])

            if team_details.get("parent_entity_tag_list"):
                if "all" in team_details.get("parent_entity_tag_list"):
                    parent_entity_tag_list.extend(all_tag_ids)
                else:
                    parent_entity_tag_list.extend(
                        team_details["parent_entity_tag_list"])

            if team_details.get("parent_entity_set_tag_list"):
                if "all" in team_details.get("parent_entity_set_tag_list"):
                    parent_entity_set_tag_list.extend(all_tag_ids)
                else:
                    parent_entity_set_tag_list.extend(
                        team_details["parent_entity_set_tag_list"])

            if team_details.get("parent_entity_id_tool_list"):
                if "all" in team_details.get("parent_entity_id_tool_list"):
                    parent_entity_id_list.extend(all_tool_ids)
                else:
                    parent_entity_id_list.extend(
                        team_details["parent_entity_id_tool_list"])

            if team_details.get("parent_entity_id_du_list"):
                if "all" in team_details.get("parent_entity_id_du_list"):
                    parent_entity_id_list.extend(all_du_ids)
                else:
                    parent_entity_id_list.extend(
                        team_details["parent_entity_id_du_list"])

            if team_details.get("parent_entity_tool_set_id_list"):
                if "all" in team_details.get("parent_entity_tool_set_id_list"):
                    parent_entity_set_id_list.extend(all_tool_set_ids)
                else:
                    parent_entity_set_id_list.extend(
                        team_details["parent_entity_tool_set_id_list"])

            if team_details.get("parent_entity_du_set_id_list"):
                if "all" in team_details.get("parent_entity_du_set_id_list"):
                    parent_entity_set_id_list.extend(all_du_set_ids)
                else:
                    parent_entity_set_id_list.extend(
                        team_details["parent_entity_du_set_id_list"])

            if team_details.get("machine_id_list"):
                if "all" in team_details.get("machine_id_list"):
                    machine_id_list.extend(all_machine_ids)
                else:
                    machine_id_list.extend(team_details["machine_id_list"])

            if team_details.get("machine_group_id_list"):
                if "all" in team_details.get("machine_group_id_list"):
                    machine_group_id_list.extend(all_machine_group_ids)
                else:
                    machine_group_id_list.extend(
                        team_details["machine_group_id_list"])

            if team_details.get("distribution_list"):
                distribution_list_list.append(
                    team_details.get("distribution_list"))

            # 2)Step 2 Create required lists

            '''
            GET BY  tag_id_list OR machine_group_id_list
            
            
            Duplication    user is assigned to a machine and the team that user is assigned to the machine 
                         there is no logical issue but this might cause issue in the backend 
                         the service handling the permissions knows to ignore duplication            
            '''

            # GET MACHINE GROUP BY TAG
            for machines in all_machine_groups_data:
                if machines.get("tag") and len(machines.get("tag")) > 0:
                    if len(list(set(tag_id_list) & set(machines["tag"]))) > 0:
                        machine_group_id_list.append(str(machines["_id"]))
                        if machines.get("machine_id_list") and type(machines.get("machine_id_list")) is list and len(machines.get("machine_id_list")) > 0:
                            machine_id_list.extend(machines["machine_id_list"])
                    # stuti
                    static_tags.extend(machines["tag"])

                if machines.get("_id") in machine_group_id_list:
                    if machines.get("machine_id_list") and type(machines.get("machine_id_list")) is list and len(machines.get("machine_id_list")) > 0:
                        machine_id_list.extend(machines["machine_id_list"])

            # GET MACHINE BY TAG
            for machine in all_machine_data:
                if machine.get("tag") and len(machine.get("tag")) > 0:
                    if len(list(set(tag_id_list) & set(machine["tag"]))) > 0:
                        machine_id_list.append(machine["_id"])
                    # stuti
                    static_tags.extend(machine["tag"])

            '''
            GET BY  tag_id_list OR parent_entity_set_tag_list
            '''
            appended_tag_set_list_for_parent = []
            appended_tag_set_list_for_parent.extend(tag_id_list)
            appended_tag_set_list_for_parent.extend(parent_entity_set_tag_list)

            # GET TOOL BY TAG
            for toolSet in all_tool_set_data:
                if toolSet.get("tag") and len(toolSet.get("tag")) > 0:
                    if len(list(set(appended_tag_set_list_for_parent) & set(self.tagDB.get_tag_ids_from_given_ids_list(toolSet.get("tag"))))) > 0:
                        parent_entity_set_id_list.append(str(toolSet["_id"]))
                        for tool in toolSet.get("tool_set"):
                            if "tool_id" in tool.keys():
                                parent_entity_id_list.append(
                                    tool.get("tool_id"))
                    # stuti
                    static_tags.extend(
                        self.tagDB.get_tag_ids_from_given_ids_list(toolSet["tag"]))

            # GET DU BY TAG
            for duSet in all_du_set_data:
                if duSet.get("tag") and len(duSet.get("tag")) > 0:
                    if len(list(set(appended_tag_set_list_for_parent) & set(self.tagDB.get_tag_ids_from_given_ids_list(duSet.get("tag"))))) > 0:
                        parent_entity_set_id_list.append(str(duSet["_id"]))
                        for du in duSet.get("du_set"):
                            if "du_id" in du.keys():
                                parent_entity_id_list.append(du.get("du_id"))
                    # stuti
                    static_tags.extend(
                        self.tagDB.get_tag_ids_from_given_ids_list(duSet["tag"]))

            '''
            GET BY tag_id_list OR  parent_entity_tag_list
            '''

            appended_tag_list_for_parent = []
            appended_tag_list_for_parent.extend(tag_id_list)
            appended_tag_list_for_parent.extend(parent_entity_tag_list)
            # GET TOOL BY TAG
            for tool in all_tool_data:
                if tool.get("tag") and len(tool.get("tag")) > 0:
                    if len(list(set(appended_tag_list_for_parent) & set(tool["tag"]))) > 0:
                        parent_entity_id_list.append(str(tool["_id"]))
                    # stuti
                    static_tags.extend(tool["tag"])

            # GET DU BY TAG
            for du in all_du_data:
                if du.get("tag") and len(du.get("tag")) > 0:
                    if len(list(set(appended_tag_list_for_parent) & set(self.tagDB.get_tag_ids_from_given_ids_list(du.get("tag"))))) > 0:
                        parent_entity_id_list.append(str(du["_id"]))
                    # stuti
                    static_tags.extend(
                        self.tagDB.get_tag_ids_from_given_ids_list(du["tag"]))

            # CONVERT TO IDS
            for idx, item in enumerate(parent_entity_id_list):
                parent_entity_id_list[idx] = ObjectId(item)
            for idx, item in enumerate(parent_entity_set_id_list):
                parent_entity_set_id_list[idx] = ObjectId(item)
            for idx, item in enumerate(machine_id_list):
                machine_id_list[idx] = ObjectId(item)
            for idx, item in enumerate(machine_group_id_list):
                machine_group_id_list[idx] = ObjectId(item)

            static_teams[str(team_details["_id"])] = {"parent_entity_id_list": parent_entity_id_list,
                                                      "parent_entity_set_id_list": parent_entity_set_id_list,
                                                      "machine_id_list": machine_id_list,
                                                      "machine_group_id_list": machine_group_id_list,
                                                      "distribution_list_list": distribution_list_list}

        ################## WORKING ALL PERMISSION HERE ####################

        # CONVERT TO IDS
        for idx, item in enumerate(static_tags):
            static_tags[idx] = ObjectId(item)

        ################## WORKING PER USER HERE ####################
        # CREATE USER DATA
        for user_detail in all_user_data:
            static_users[str(user_detail["_id"])] = {"parent_entity_id_list": [],
                                                     "parent_entity_set_id_list": [],
                                                     "machine_id_list": [],
                                                     "machine_group_id_list": [],
                                                     "distribution_list_list": []}

            skip_role = ["admin", "superadmin"]
            user = self.userdb.get_user_by_id(str(user_detail["_id"]), False)
            roleId = user["roleid"]
            result = self.roledb.get_role_by_id(roleId, False)
            # IS USER IS ALLOWED EVERTHING

            # ADD DISTRIBUTION LIST
            for team_detail in self.teamDB.get_team_by_user(str(user_detail["_id"])):
                static_users[str(user_detail["_id"])]["distribution_list_list"].extend(
                    static_teams[str(team_detail["_id"])]["distribution_list_list"])
            if user_detail.get("email"):
                static_users[str(user_detail["_id"])]["distribution_list_list"].append(
                    user_detail.get("email"))

            # ADD
            if result["name"].lower() in skip_role:
                static_users[str(user_detail["_id"])]["parent_entity_id_list"].extend(
                    all_parent_entity_id_list)
                static_users[str(user_detail["_id"])]["parent_entity_set_id_list"].extend(
                    all_parent_entity_set_id_list)
                static_users[str(user_detail["_id"])]["machine_id_list"].extend(
                    all_machine_id_list)
                static_users[str(user_detail["_id"])]["machine_group_id_list"].extend(
                    all_machine_group_id_list)
            else:
                # MAP USER AS PER PERMISSION
                for team_detail in self.teamDB.get_team_by_user(str(user_detail["_id"])):
                    static_users[str(user_detail["_id"])]["parent_entity_id_list"].extend(
                        static_teams[str(team_detail["_id"])]["parent_entity_id_list"])
                    static_users[str(user_detail["_id"])]["parent_entity_set_id_list"].extend(
                        static_teams[str(team_detail["_id"])]["parent_entity_set_id_list"])
                    static_users[str(user_detail["_id"])]["machine_id_list"].extend(
                        static_teams[str(team_detail["_id"])]["machine_id_list"])
                    static_users[str(user_detail["_id"])]["machine_group_id_list"].extend(
                        static_teams[str(team_detail["_id"])]["machine_group_id_list"])

                # HANDLE MACHINE  LEVEL permitted_users list
                '''
                Conflicts  in case user is assigned to a machine, but team is not assigned to a machine
                             or In case team is assigned to a machine, but user is not assigned to a machine.
                In both cases system will do aggregation of all permission so in both cases user will have
                              the ability to perform actions on machine
        
                '''
                ################## WORKING PER USER HERE.SPECIAL HANDLING FOR permitted_users in machineDb ####################
                for machine in all_machine_data:
                    if machine.get("permitted_users") and (len(list(set([str(user_detail["_id"]), "all", "All"]) & set(machine.get("permitted_users")))) > 0):
                        if str(user_detail["_id"]) in static_users.keys():
                            static_users[str(user_detail["_id"])]["machine_id_list"].append(
                                ObjectId(str(machine["_id"])))

        print "loaded data for users in memory..."

    def get_user_permissions(self, user_id):
        '''
        Return permissions data for given user 
        '''
        global static_users
        return static_users.get(user_id)

    def get_team_permissions(self, team_id):
        '''
        Return permissions data for given team 
        '''
        global static_teams
        return static_teams.get(team_id)

    # stuti
    def get_active_tags(self):
        '''
        Return permissions data for given team 
        '''
        global static_tags
        return static_tags
