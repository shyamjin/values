"""
.. module:: InitDataHelper
   :platform: Unix, Windows
   :synopsis: Some data is required to run Deployment Manager for the first time.
       DPM is in 5 flavor dpm_lite,dpm_account,dpm_master,edpm_lite,edpm. Which flavor is installed is decided by global variable "edpm_type" defined in settings.py
       According to edpm_type,data from one of the following files :InitData, InitDataLite,InitDataAccount,InitDataEDpmLite,InitDataEDpmAccount is populated on collection
.. moduleauthor:: name <email@amdocs.com>

"""
import json
import random
import string
import socket

from bson.objectid import ObjectId
from DBUtil  import Teams, Users, FlexibleAttributes, Config,ExitPointPlugins, Repository
from DBUtil.InitData import InitSlamData,InitDataCommon
from Services import PasswordHelper
from settings import onDockerInd, dpm_type, dpm_version, dpm_port, key, pipeline, build, build_date,hostname,ip,account_name


# DECIDE WHICH FILE TO RUN
if dpm_type.lower() in ["dpm_lite","edpm_lite"]:
    from DBUtil.InitData import InitDataLite
    dynamicInstanceOfInitData = InitDataLite
elif dpm_type.lower() in ["dpm_account","edpm"]:
    from DBUtil.InitData import InitDataAccount
    dynamicInstanceOfInitData = InitDataAccount
elif dpm_type.lower() == "dpm_master":
    from DBUtil.InitData import InitData
    dynamicInstanceOfInitData = InitData
else:
    raise ValueError("Invalid DPM type found")

print "### INIT DATA WILL RUN FOR " + str(dynamicInstanceOfInitData) + " ###"


# lists to store objects
roleobjects = []
permissionobjects = []
routeobjects = []

# Key-ValueMaps to store the Roles and corresponding ObjectsIds
RoleObjMap = {}
# Key-ValueMaps to store the Permissions and corresponding ObjectsIds
PermObjMap = {}
RolePermissionGroupObjMap = {}
RouteObjMap = {}


class InitDataHelper():

    def __init__(self, db):
        # Populate Data for Permissions Table
        self.populate_permissions_data(db)
        # Populate Data for Routes Table
        self.populate_routes_data(db)
        # Populate Data for Permission Group Table
        self.populate_permission_group_data(db)
        # Populate Data for Roles Table
        self.populate_roles_data(db)
        # Populate Data for Accounts Table
        self.populate_account_data(db)
        # Populate Data for Users Table
        self.populate_user_data(db)
        # Populate Data for Config Table
        self.populate_config_data(db)
        # Populate Data for EmailTemplate Table
        self.populate_email_template_data(db)
        # Populate Data for MachineType Table
        self.populate_machine_type_data(db)
        # Update OnDockerInd when dpm is up
        self.populate_system_data(db)
        # Populate Data for DeploymentUnitType
        self.populate_du_type_data(db)
        # Populate Data for DeploymentUnitApprovalStatus
        self.populate_du_approval_sts_data(db)
        # Populate Data for Reports
        self.populate_reports_data(db)
        # Populate Data for Reports
        self.populate_reports_int_data(db)
        # Create Team For Guests
        self.create_guest_team(db)
        # Generate Access token for DPMsysCI
        self.create_token_for_ci(db)
        # Populate Data for FlexibleAttributes
        self.populate_fa_data(db)
        # Populate Data for Plugin
        self.populate_plugins_data(db)
        # Populate Data for FlexibleAttributes
        self.populate_repository_data(db)
    
    def create_guest_team(self, db):
        '''
        General description: Create Team For Guests 
        Args:
            param1 (db) : Database instance.
        Returns:
                None
        '''
        try:
            teamDB = Teams.Teams(db)
            if teamDB.get_team_by_name("Guest_Team") is None:
                userDB = Users.Users(db)
                teamDetails = {}
                teamDetails["team_name"] = "Guest_Team"
                teamDetails["description"] = "This team has view access to all the tools, Du, tool set and Du set"
                teamDetails["distribution_list"] = ""
                try:
                    teamDetails["users_id_list"] = [
                        userDB.get_user_by_name("Guest")]
                except:
                    raise ValueError("Guest User does not exist")
                teamDetails["tag_id_list"] = []
                teamDetails["parent_entity_tag_list"] = []
                teamDetails["parent_entity_set_tag_list"] = []
                teamDetails["parent_entity_id_tool_list"] = []
                teamDetails["parent_entity_id_du_list"] = []
                teamDetails["parent_entity_tool_set_id_list"] = []
                teamDetails["parent_entity_du_set_id_list"] = []
                teamDetails["machine_id_list"] = []
                teamDetails["machine_group_id_list"] = []
                new_team_id = teamDB.add_team(teamDetails)
                print "Guest Team Created Sucessfull with Team Id" + new_team_id
            else:
                print "Guest Team already exists"
        except:
            raise ValueError("Unable to create Guest Team")

    def create_token_for_ci(self, db):
        '''
        General description: Create Team For Guests 
        Args:
            param1 (db) : Database instance.
        Returns:
                None
        '''
        try:
            userDB = Users.Users(db)
            data = userDB.get_user("DPMsysCI", False)
            if data and not data.get("access_token"):
                data1 = {}
                data1["_id"] = {"oid": str(data["_id"])}
                data1["access_token"] = ''.join(random.SystemRandom().choice(
                    string.ascii_uppercase + string.digits) for _ in range(25))
                data1["access_exp_date"] = "2100-01-01T00:00:00"
                userDB.update_user(data1)
        except Exception:
            raise ValueError("Unable to create access token for DPMsysCI")

    def populate_system_data(self, db):
        '''
        General description: populate initial mandatory data to SystemDetails collection
        Args:
            param1 (db) : Database instance.
        Returns:
                None
        '''
        self.collection = db.SystemDetails  # Set Collection as SystemDetails
        if socket.gethostname().find('.') >= 0:
            host = socket.gethostname()
        else:
            host = socket.gethostbyaddr(socket.gethostname())[0]
        ip_address = socket.gethostbyname(host)
        
        if hostname.lower() <> "none":
            host = hostname
        if ip.lower() <> "none":
            ip_address = ip    
        
        is_found = self.get_single_record()
        if is_found is None:
            is_found = {}
            is_found["ondockerInd"] = str(onDockerInd)
            is_found["ip"] = ip_address
            is_found["hostname"] = host
            is_found["account_name"] = "Test"
            is_found["created_by"] = "Self"
            # need to get details
            is_found["dpm_type"] = dpm_type
            is_found["dpm_version"] = dpm_version
            is_found["port"] = dpm_port
            is_found["pipeline"] = pipeline
            is_found["build"] = build
            is_found["build_date"] = build_date
            if dpm_type.lower() in ("dpm_lite", "dpm_account", "dpm_master"):
                is_found["homepage"] = "dashboard"
            else:
                is_found["homepage"] = "duDashboard"
            updated = self.insert_record(is_found)
        else:
            is_found["ondockerInd"] = str(onDockerInd)
            is_found["dpm_type"] = dpm_type
            is_found["dpm_version"] = dpm_version
            is_found["port"] = dpm_port
            is_found["pipeline"] = pipeline
            is_found["build"] = build
            is_found["build_date"] = build_date
            if account_name.lower() <> "none":
                is_found["account_name"] = account_name
            if dpm_type.lower() in ("dpm_lite", "dpm_account", "dpm_master"):
                is_found["homepage"] = "dashboard"
            else:
                is_found["homepage"] = "duDashboard"
            updated = self.update_record(is_found)
        # print PermObjMap
            if updated:
                print "SystemDetails updated!!"
            elif updated == 0:
                print "SystemDetails Not changed!!"
            else:
                raise ValueError("Unable to update SystemDetails ")
            
            
        '''
        As we are taking input of hostname from env 
        if the current dpm version is <> dpm_master or dpm_account its safe to assume that
        the account in Accounts collect is only 1 record with value Test
        '''    
        self.collection = db.Accounts  # Set Collection as Accounts
        if self.get_all_count() == 1 and account_name.lower() <> "none"\
         and dpm_type not in ("dpm_account", "dpm_master"):
            is_found = self.get_single_record()
            if is_found:
                is_found["name"] = account_name
                updated = self.update_record(is_found)
                if updated:
                    print "Account Name updated!!"
                elif updated == 0:
                    print "Account Name Not changed!!"
                else:
                    raise ValueError("Unable to update Account Name in Accounts collection ")
                
    def populate_permissions_data(self, db):
        self.collection = db.Permissions  # Set Collection as Permissions
        # Loop over the Permissions list and insert into the role collection if
        # not present
        for permName in InitDataCommon.PERMISSIONS:
            IsFound = self.get_record_by_name(permName["name"])
            if IsFound is None:
                objectid = str(self.insert_record(permName))
                permissionobjects.append(objectid)
                PermObjMap[permName["name"]] = objectid
            else:
                PermObjMap[permName["name"]] = IsFound["_id"]
                # print PermObjMap[permName["name"]]
                # PermObjMap[permName["name"]]
        count = self.get_all_count()
        # print PermObjMap
        if count >= len(InitDataCommon.PERMISSIONS):
            print "Permissions data Populated Successful"
        else:
            raise ValueError("Insufficient Permission detected. " + str(
                len(InitDataCommon.PERMISSIONS) - count) + " entries are missing")

    def populate_routes_data(self, db):
        self.collection = db.Routes  # Set Collection as Permissions
        # Loop over the Permissions list and insert into the role collection if
        # not present
        for routeName in InitDataCommon.ROUTES:
            IsFound = self.get_record_by_name(routeName["name"])
            if IsFound is None:
                objectid = str(self.insert_record(routeName))
                routeobjects.append(objectid)
                RouteObjMap[routeName["name"]] = objectid
            else:
                RouteObjMap[routeName["name"]] = IsFound["_id"]
        count = self.get_all_count()
        if count >= len(InitDataCommon.ROUTES):
            print "Routes data Populated Successful"
        else:
            raise ValueError("Insufficient Routes detected. " + str(
                len(InitDataCommon.ROUTES) - count) + " entries are missing")

    def populate_permission_group_data(self, db):
        self.collection = db.PermissionGroup
        self.PermCollection = db.Permissions
        self.RoutesCollection = db.Routes
        for record in InitDataCommon.PERMISSION_GROUPS:
            if PermObjMap:
                perList = []
                permissionssArr = record["permissions"]
                # routesArr=routesArr[0]
                for url in permissionssArr:
                    result = self.PermCollection.find_one({"name": url})
                    if result is not None:
                        perList.append(str(result["_id"]))
                    else:
                        raise ValueError("Error while creating Permission group :" + record.get(
                            "groupname") + " .Permission :" + url + " was not found in Permissions collection.")
                record["permissions"] = perList
            if RouteObjMap:
                routeList = []
                routesArr = record["routes"]
                # routesArr=routesArr[0]
                for url in routesArr:
                    result = self.RoutesCollection.find_one({"name": url})
                    if result is not None:
                        routeList.append(str(result["_id"]))
                    else:
                        raise ValueError("Error while creating Permission group :" + record.get(
                            "groupname") + " .Route :" + url + " was not found in Routes collection.")
                record["routes"] = routeList
            IsFound = self.getPermGroupsByName(record["groupname"])
            if IsFound:
                record["_id"] = str(IsFound["_id"])
                self.update_record(record)
                RolePermissionGroupObjMap[record["groupname"]] = id
            else:
                RolePermissionGroupObjMap[record["groupname"]] = self.insert_record(
                    record)
        count = self.get_all_count()
        if count >= len(InitDataCommon.PERMISSION_GROUPS):
            print "PermissionGroup data Populated Successful"
        else:
            raise ValueError("Insufficient Permission group detected. " + str(len(
                InitDataCommon.PERMISSION_GROUPS) - count) + " entries are missing")

    def populate_roles_data(self, db):
        self.collection = db.Role  # Set Collection as Role
        self.PermissionGroupCollection = db.PermissionGroup

        # Loop over the roles list and insert into the role collection if not
        # present
        for rec in dynamicInstanceOfInitData.ROLE_GROUPING:
            # print roleName["name"]
            IsFound = self.get_record_by_name(rec["name"])
            # print RolePermissionGroupObjMap
            if IsFound is None:
                permissionArr = []
                if rec.get("permissiongroup") is not None:
                    for pergroup in rec["permissiongroup"]:
                        result = self.PermissionGroupCollection.find_one(
                            {"groupname": pergroup})
                        if result is not None:
                            permissionArr.append(str(result["_id"]))
                rec["permissiongroup"] = permissionArr
                self.insert_record(rec)
        count = self.get_all_count()
        if count >= len(dynamicInstanceOfInitData.ROLE_GROUPING):
            print "Roles data Populated Successful"
        else:
            raise ValueError("Insufficient Roles detected. " + str(
                len(dynamicInstanceOfInitData.ROLE_GROUPING) - count) + " entries are missing")

    def populate_user_data(self, db):
        self.collection = db.Users  # Set Collection as Role
        self.RoleCollection = db.Role  # Set Collection as Role
        self.AccountsCollection = db.Accounts
        passwordHelper = PasswordHelper.PasswordHelper(key)
        # Loop over the roles list and insert into the role collection if not
        # present
        for rec in dynamicInstanceOfInitData.USERS:
            # print roleName["name"]
            IsFound = self.get_record_from_user(rec["user"])
            # print RolePermissionGroupObjMap
            if IsFound is None:
                rec["roleid"] = str(self.RoleCollection.find_one(
                    {"name": rec["roleid"]})["_id"])
                rec["accountid"] = str(self.AccountsCollection.find_one(
                    {"name": rec["accountid"]})["_id"])
                rec["password"] = passwordHelper.encrypt(rec["password"])
                self.insert_record(rec)
        count = self.get_all_count()
        if count >= len(dynamicInstanceOfInitData.USERS):
            print "Users data Populated Successful"
        else:
            raise ValueError("Insufficient Users detected. " + str(
                len(dynamicInstanceOfInitData.users) - count) + " entries are missing")

    def populate_config_data(self, db):
        self.collection = db.Config  # Set Collection as Config
        # 525
        self.configdb = Config.Config(db)
        # Loop over the configuration data list and insert into the Config
        # collection if not present
        for configDetail in dynamicInstanceOfInitData.CONFIG_DATA:
            IsFound = self.get_record_by_name(configDetail["name"])
            if IsFound is None:
                # 525
                configDetail = self.configdb.encrypt(configDetail)
                self.insert_record(configDetail)
        count = self.get_all_count()
        if count >= len(dynamicInstanceOfInitData.CONFIG_DATA):
            print "Config data Populated Successful"
        else:
            raise ValueError("Insufficient Config detected. " + str(
                len(dynamicInstanceOfInitData.CONFIG_DATA) - count) + " entries are missing")

    def populate_email_template_data(self, db):
        self.collection = db.EmailTemplate  # Set Collection as EmailTemplate
        # Loop over the EmailTemplate list and insert into the EmailTemplate
        # collection if not present
        for EmailTemplate in InitDataCommon.EMAIL_TEMPLATE:
            IsFound = self.get_record_by_template_id(EmailTemplate["templateid"])
            if IsFound is None:
                self.insert_record(EmailTemplate)
        count = self.get_all_count()
        if count >= len(InitDataCommon.EMAIL_TEMPLATE):
            print "EmailTemplate data Populated Successful"
        else:
            raise ValueError("Insufficient EmailTemplate detected. " + str(
                len(InitDataCommon.EMAIL_TEMPLATE) - count) + " entries are missing")

    def populate_machine_type_data(self, db):
        self.collection = db.MachineType  # Set Collection as MachineType
        # Loop over the MachineType list and insert into the MachineType
        # collection if not present
        for type in InitDataCommon.MACHINE_TYPE:
            IsFound = self.get_record_by_type(type["type"])
            if IsFound is None:
                self.insert_record(type)
        count = self.get_all_count()
        if count >= len(InitDataCommon.MACHINE_TYPE):
            print "MachineType data Populated Successful"
        else:
            raise ValueError("Insufficient MachineType detected. " + str(
                len(InitDataCommon.MACHINE_TYPE) - count) + " entries are missing")

    def populate_account_data(self, db):
        self.collection = db.Accounts  # Set Collection as Accounts
        for acc in InitDataCommon.ACCOUNT:
            IsFound = self.get_record_by_name(acc["name"])
            if IsFound is None:
                self.insert_record(acc)
        count = self.get_all_count()
        if count >= len(InitDataCommon.ACCOUNT):
            print "Account data Populated Successful"
        else:
            raise ValueError("Insufficient Account detected. " + str(
                len(InitDataCommon.ACCOUNT) - count) + " entries are missing")

    def Roles_DataReloadToDefault(self, db):
        self.collection = db.Role  # Set Collection as Role
        self.PermissionGroupCollection = db.PermissionGroup

        # Loop over the roles list and insert into the role collection if not
        # present
        for rec in dynamicInstanceOfInitData.ROLE_GROUPING:
            # print roleName["name"]
            IsFound = self.get_record_by_name(rec["name"])
            # print RolePermissionGroupObjMap
            permissionArr = []
            if rec.get("permissiongroup") is not None:
                for pergroup in rec["permissiongroup"]:
                    result = self.PermissionGroupCollection.find_one(
                        {"groupname": pergroup})
                    if result is not None:
                        permissionArr.append(str(result["_id"]))
            rec["permissiongroup"] = permissionArr
            if IsFound is None:
                self.insert_record(rec)
            else:
                IsFound["_id"] = {"oid": str(IsFound["_id"])}
                IsFound["permissiongroup"] = rec["permissiongroup"]
                self.UpdateRole(IsFound)
        print "Roles data Populated Successful"

    def populate_du_type_data(self, db):
        self.collection = db.DeploymentUnitType  # Set Collection as DeploymentUnitType
        for rec in InitDataCommon.DEPLOYMENT_UNIT_TYPE:
            IsFound = self.get_record_by_name(rec["name"])
            if IsFound is None:
                self.insert_record(rec)
        count = self.get_all_count()
        if count >= len(InitDataCommon.DEPLOYMENT_UNIT_TYPE):
            print "DeploymentUnitType data Populated Successful"
        else:
            raise ValueError("Insufficient DeploymentUnitType detected. " + str(len(
                InitDataCommon.DEPLOYMENT_UNIT_TYPE) - count) + " entries are missing")

    def populate_du_approval_sts_data(self, db):
        # Set Collection as DeploymentUnitApprovalStatus
        self.collection = db.DeploymentUnitApprovalStatus
        for rec in InitDataCommon.DEPLOYMENT_UNIT_APPROVAL_STATUS:
            IsFound = self.get_record_by_name(rec["name"])
            if IsFound is None:
                self.insert_record(rec)
        count = self.get_all_count()
        if count >= len(InitDataCommon.DEPLOYMENT_UNIT_APPROVAL_STATUS):
            print "DeploymentUnitApprovalStatus data Populated Successful"
        else:
            raise ValueError("Insufficient DeploymentUnitApprovalStatus detected. " + str(len(

                dynamicInstanceOfInitData.myDeploymentUnitApprovalStatus) - count) + " entries are missing")

    def populate_reports_data(self, db):
        self.collection = db.SystemDetails  # Set Collection as Permissions
        sys_details = self.get_single_record()
        host_name = str(sys_details.get("hostname"))
        self.collection = db.Reports  # Set Collection as Reports
        for rec in InitSlamData.reports:
            IsFound = self.get_record_by_name(rec.get("name"))
            if IsFound is None:
                rec["url"] = rec.get("url").replace("hostname", host_name)
                self.insert_record(rec)
        count = self.get_all_count()
        if count >= len(InitSlamData.reports):
            print "Reports Populated Successful"
        else:
            raise ValueError("Insufficient Reports detected. " + str(len(
                InitSlamData.reports) - count) + " entries are missing")

    def populate_reports_int_data(self, db):
        mycollections = []
        for rec in InitSlamData.reports_data:
            mycollections.append(rec.get("collection_name"))
            if rec.get("collection_name") and rec.get("collection_name") not in (db.collection_names()):
                self.collection = db[rec["collection_name"]]
                rec.pop("collection_name")
                self.insert_record(rec)
        if set(mycollections).issubset(db.collection_names()):
            print "ReportsData data Populated Successful"
        else:
            raise ValueError("Insufficient ReportsData detected. " + str(len(
                mycollections) - len(list(set(db.collection_names()) & set(mycollections)))) + " entries are missing")



    def populate_fa_data(self, db):
        # Set Collection as FlexibleAttributes
        array_to_parse=InitDataCommon.FLEX_ATTRIBUTES
        self.collection = FlexibleAttributes.FlexibleAttributes()
        for rec in array_to_parse:
            IsFound = self.collection.get_by_name_and_entity(rec["name"],rec["entity"])
            if IsFound is None:
                self.collection.add(rec)
        count = self.collection.get_all()
        if count >= len(array_to_parse):
            print "FlexibleAttributes data Populated Successful"
        else:
            raise ValueError("Insufficient FlexibleAttributes detected. " + str(len(
                array_to_parse) - count) + " entries are missing")

    def populate_plugins_data(self, db):
        # Set Collection as ExitPointPlugins
        array_to_parse=InitDataCommon.EXITPOINTPLUGINS
        self.collection = ExitPointPlugins.ExitPointPlugins() 
        for rec in array_to_parse:
            if (self.collection.get_by_plugin_name(rec["plugin_name"]) is None\
                 and  self.collection.get_by_repo_provider(rec.get("repo_provider",str(None))) is None):
                self.collection.add(rec)
        count = self.collection.get_all()
        if count >= len(array_to_parse):
            print "ExitPointPlugins data Populated Successful"
        else:
            raise ValueError("Insufficient ExitPointPlugins detected. " + str(len(
                array_to_parse) - count) + " entries are missing")            
            
    def populate_repository_data(self, db):
        # Set Collection as ExitPointPlugins
        array_to_parse=InitDataCommon.REPOSITORY_DATA
        self.collection = Repository.Repository() 
        for rec in array_to_parse:
            if self.collection.get_repository_by_name(rec.get("name")) is None:
                self.collection.add(rec)
        count = self.collection.get_all()
        if count >= len(array_to_parse):
            print "Repository data Populated Successful"
        else:
            raise ValueError("Insufficient Repository data detected. " + str(len(
                array_to_parse) - count) + " entries are missing")                    
            
################################################## HELPER METHODS ######################################################

    def update_record(self, sysdetails):
        jsonnewEntry = {}
        for key in sysdetails.keys():
            if key != "_id":
                jsonnewEntry[key] = sysdetails[key]
        result = self.collection.update_one({"_id": ObjectId(str(sysdetails["_id"]))}, {
                                            "$set": jsonnewEntry}, upsert=False)
        return result.modified_count
    
    def get_single_record(self):
        return (self.collection.find_one())

    def get_record_by_name(self, roleName):
            return (self.collection.find_one({"name": roleName}))
    
    def get_record_from_user(self, user):
        return (self.collection.find_one({"user": user}))
    
    def get_record_by_id(self, roleId):
        return (self.collection.find_one({"_id": ObjectId(roleId)}))
    
    def get_record_by_template_id(self, templateid):
        return (self.collection.find_one({"templateid": templateid}))
    
    def get_record_by_type(self, type_received):
        return (self.collection.find_one({"type": type_received}))
    
    def get_all_count(self):
        return (self.collection.find().count())
    
    def insert_record(self, per):
        result = self.collection.insert_one(per)
        return(result.inserted_id)
    
    
    def getPermGroupsByName(self, groupName):
        result = self.collection.find_one({"groupname": groupName})
        return result
    
    def getRoutesGroupsByName(self, routes_group):
        result = self.collection.find_one({"routes_group": routes_group})
        return result
    
    def push_entry_to_record(self, roleobj, permissiongroupobj):
        result = self.collection.update_one({"_id": ObjectId(roleobj)}, {
                                            "$push": permissiongroupobj})
        return result
    
    def UpdateRole(self, roleData):
        permissiongroup_list = None
        jsonEntry = '{'
        for key in roleData.keys():
            if key != "_id":
                if isinstance(roleData[key], (list)) and key == "permissiongroup":
                    permissiongroup_list = roleData[key]
    
                else:
                    jsonEntry += '"' + key + '":"' + roleData[key] + '",'
        jsonEntry = jsonEntry[:-1] + '}'
        data = json.loads(jsonEntry)
        if permissiongroup_list is not None:
            data["permissiongroup"] = permissiongroup_list
        result = self.collection.update_one(
            {"_id": ObjectId(roleData["_id"]["oid"])}, {"$set": data}, upsert=False)
        return result.modified_count            