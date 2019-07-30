import traceback,csv,json,os
from bson.json_util import dumps
from flasgger import swag_from, validate
from flask import Blueprint, jsonify, request
from DBUtil import Users, Accounts, Role, UserFavoriteMachine, Emails, PermissionGroup, Teams, SystemDetails, Machine,Config
from Services import Mailer, TeamService, HelperServices
from Services.SpecialUsers import SpecialUsers
from Services.UserRoles import UserRoles
from Services.AppInitServices import authService
from settings import mongodb, dpm_type, relative_path, import_full_path
from werkzeug import secure_filename
from flask_restplus import Resource
from modules.apimodels import UserModel
from modules.apimodels.Restplus import api, header_parser
from Services import LdapHelper
from datetime import datetime, timedelta
import re
from Services.HelperServices import genrate_random_key
# blueprint declaration
userAPI = Blueprint('userAPI', __name__)
userAPINs = api.namespace('user', description='User Operations')

# get global db connection
db = mongodb
accountDB = Accounts.Accounts()
userdb = Users.Users(db)
roledb = Role.Role(db)
machineFavDb = UserFavoriteMachine.UserFavoriteMachine(db)
emaildb = Emails.Emails(db)
perGroup = PermissionGroup.PermissionGroup(db)
teamDB = Teams.Teams(db)
mailer = Mailer.Mailer()
systemDetailsDB = SystemDetails.SystemDetails(db)
teamService = TeamService.TeamService()
machine_db = Machine.Machine(db)
configDb = Config.Config(db)



@userAPINs.route('/new', methods=['POST'])
class addNewUser(Resource):
    @api.expect(header_parser,UserModel.add_user_input_model,validate=True)
    @api.marshal_with(UserModel.add_user_response_model)
    @authService.authorized 
    def post(self):
        user = request.get_json()
        HelperServices.validate_name(user.get("user"),"username")
        user_id = authService.get_userid_by_auth_token()
        if user_id is None:
            raise Exception("Token verification failed")
        loggedInUser = userdb.get_user_by_id(user_id, False)
        loggedInUserRole = roledb.get_role_by_id(loggedInUser["roleid"], True)
        if loggedInUserRole["name"].lower() == "superadmin":
            pass
        else:
            newUserRole = roledb.get_role_by_id(user.get("roleid"), False)
            if newUserRole["name"].lower() == "superadmin":
                raise ValueError(
                    "Only SuperAdmin can create a SuperAdmin user")
            else:
                pass
        if (user.get("employeeid") and user.get("user") and user.get("email") and user.get("accountid"))is None:
            raise Exception("Mandatory fields to create a new user was not found.")
        if userdb.get_user(user.get("user"), False) is not None:
            raise Exception("User already exists")
        if accountDB.get_account(user.get("accountid")) is None:
            raise Exception("Account does not exists")
        addData = {"user": user.get("user").lower(), "status": "active"}
        if user.get("roleid") is None:
            addData["roleid"] = str(
                roledb.get_role_by_name('Guest', False)["_id"])
        else:
            if roledb.get_role_by_id(user.get("roleid"), False) is None:
                raise Exception("Role does not exists")
        user.update(addData)
        passw = genrate_random_key()
        user["password"] = passw
        result = userdb.add_user(user)
        if user.get("included_in"):
            for team_id in user["included_in"]:
                teamDB.add_user_to_team(team_id, str(result))
        try:
            systemdetails = systemDetailsDB.get_system_details_single()
            mailer.send_html_notification(user.get("email"), None, None, 14, {
                                          "name": user.get("user"), "password": passw, "machine_host": systemdetails.get("hostname")})
            teamService.generate_details()
        except Exception as e:
            traceback.print_exc()
        return {"result": "success", "message": "A new user was created..Token was generated", "data": {"Token": authService.generate_auth_token(str(result))}}, 200


@userAPINs.route('/update', methods=['PUT'])
class updateUser(Resource):
    @api.expect(header_parser,UserModel.update_user_input_model,validate=True)
    @api.marshal_with(UserModel.update_user_response_model)
    @authService.authorized 
    def put(self):
        user_data = request.get_json()
        if user_data.get("user"):
            HelperServices.validate_name(user_data.get("user"),"username")
        if user_data.get("_id"):
            user_id = user_data["_id"]["oid"]
        if user_data.get("roleid") is not None:
            if roledb.get_role_by_id(user_data.get("roleid"), False) is None:
                raise Exception("Role does not exists")
        # other way is to get account id from GUI
        if user_data.get("accountid") is not None:
            if accountDB.get_account(user_data.get("accountid")) is None:
                raise Exception("Account does not exists")
        auth_user_id = authService.get_userid_by_auth_token()
        if auth_user_id is None:
            raise Exception("Token verification failed")
        loggedInUser = userdb.get_user_by_id(auth_user_id, False)
        loggedInUserRole = roledb.get_role_by_id(loggedInUser["roleid"], True)
        if loggedInUserRole["name"].lower() == "superadmin":
            pass
        else:
            newUserRole = roledb.get_role_by_id(user_data.get("roleid"), False)
            if newUserRole["name"].lower() == "superadmin":
                raise ValueError(
                    "Only SuperAdmin can update role to SuperAdmin")
            else:
                pass

        for group in teamDB.get_team_by_user(user_id):
            teamDB.remove_user_from_team(str(group["_id"]), user_id)
        
        if user_data.get("included_in"):
            for group_id in user_data.get("included_in"):
                teamDB.add_user_to_team(group_id, user_id)
        updated = userdb.update_user(user_data)

        if updated == 1:
            teamService.generate_details()
            return {"result": "success", "message": "User was updated", "data": updated}, 200
        else:
            raise Exception("User was not updated.")

@userAPINs.route('/change/password', methods=['PUT'])
class updateUserPassword(Resource):
    @api.expect(header_parser,UserModel.update_password_input_model,validate=True)
    @api.marshal_with(UserModel.update_user_response_model)
    @authService.authorized 
    def put(self):
        user_data = request.get_json()
        data = {}
        if user_data.get("_id") is None:
            raise Exception("_id not found")
        else:
            data["_id"] = user_data["_id"]
        if user_data.get("password") is None:
            raise Exception("password not found")
        else:
            data["password"] = user_data["password"]
        user = userdb.get_user_by_id(
                user_data.get("_id").get("oid"), True)
        if not user:
            raise Exception("No such user was found")    
        if str(userdb.get_user_by_id(authService.get_userid_by_auth_token(), True)["role_details"]["name"]).lower() not in ["superadmin","admin"]:
            if user["user"] <> userdb.get_user_by_id(authService.get_userid_by_auth_token(), True)["user"]:
                raise Exception("You are only allowed to change your own password")
        updated = userdb.update_user(data)
        try:
            mailer.send_html_notification(user.get("email"), None, None, 1,
                                           {"name": user.get("user")})
        except Exception as e:  # catch *all* exceptions
            print "Failed to save email" + str(e)
        if updated == 1:
            user_update_data = {
                "_id" : user_data.get("_id"),
                "isfirstlogin" : "false"
            }
            userdb.update_user(user_update_data)
            invalidate_temp_password(userdb.get_user_by_id(user_data.get("_id").get("oid"), True))
            return {"result": "success", "message": "Password was updated", "data": updated}, 200
        else:
            raise Exception("Password was not updated")

@userAPINs.route('/generateaccesstoken', methods=['PUT'])
class generateAccessToken(Resource):
    @api.expect(header_parser,UserModel.gen_accestoken_input_model,validate=True)
    @api.marshal_with(UserModel.gen_accestoken_response_model)
    @authService.authorized
    def put(self):
        user_data = request.get_json()
        access_token = userdb.add_user_access_token(
            user_data.get("_id").get("oid"), user_data.get("access_exp_date"))
        return {"result": "success", "message": "Access token was generated", "data": access_token}, 200

@userAPINs.route('/deleteaccesstoken/<string:id>', methods=['DELETE'])
class deleteaccesstoken(Resource):
    @api.param('id', 'User Id')
    @api.marshal_with(UserModel.update_user_response_model)
    @authService.authorized
    def delete(self,id):
        isDeleted = userdb.delete_user_access_token(id)
        if isDeleted == 1:
            return {"result": "success", "message": "Access token was deleted", "data": isDeleted}, 200
        else:
            raise Exception( "No Access token found for the User")           


@userAPI.route('/user/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/UserAPI/getUsers.yml')
def getUsers():
    user_data = []
    user_list = userdb.get_all_users()
    record = {}
    for record in user_list:
        roleid = record["roleid"]
        record['rolename'] = "Not Found"
        role = roledb.get_role_name_by_id(roleid)
        if role:
            if role.get("name"):
                record['rolename'] = roledb.get_role_name_by_id(roleid)[
                    "name"]
        record["password"] = ""
        user_data.append(record)
        GroupsForUser = teamDB.get_team_by_user(str(record["_id"]))
        included_in = []
        for group in GroupsForUser:
            temp_group = teamDB.get_user_groups_for_view(group["_id"])
            included_in.append(temp_group)
        record["included_in"] = included_in
    return jsonify(json.loads(dumps({"result": "success", "data": user_data}))), 200


@userAPI.route('/user/view/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/UserAPI/getUserById.yml')
def getUserById(id):
    user_list = userdb.get_user_by_id(id, False)
    if user_list is None:
        raise Exception ("User is not found")
    user_list["password"] = ""
    user_list['rolename'] = "Not Found"
    role = roledb.get_role_name_by_id(user_list['roleid'])
    if role:
        if role.get("name"):
            user_list['rolename'] = roledb.get_role_name_by_id(
                user_list['roleid'])["name"]
    user_list["account_details"] = accountDB.get_account(
        user_list["accountid"])
    GroupsForUser = teamDB.get_team_by_user(str(user_list["_id"]))
    included_in = []
    for group in GroupsForUser:
        temp_group = teamDB.get_user_groups_for_view(group["_id"])
        included_in.append(temp_group)
    user_list["included_in"] = included_in
    return jsonify(json.loads(dumps({"result": "success", "data": user_list}))), 200


@userAPI.route('/user/name/<string:name>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/UserAPI/getUserByName.yml')
def getUserByName(name):
    user_list = userdb.get_user(name, False)
    if user_list is None:
        raise Exception ("User is not found")
    user_list["password"] = ""
    user_list['rolename'] = roledb.get_role_name_by_id(
        user_list['roleid'])["name"]
    user_list["account_details"] = accountDB.get_account(
        user_list["accountid"])
    return jsonify(json.loads(dumps({"result": "success", "data": user_list}))), 200


@userAPI.route('/guipermissions', methods=['GET'])
@authService.unauthorized
@swag_from(relative_path + '/swgger/UserAPI/getGuiPermissionsByUserId.yml')
def getGuiPermissionsByUserId():
    showDetails = request.headers.get("detail")
    superAdmin = False
    user_id = authService.get_userid_by_auth_token()
    user = userdb.get_user_by_id(user_id, False)
    role_list = roledb.get_role_by_id(user["roleid"], True)
    in_user = 'SuperAdmin'
    if dpm_type.lower() == "dpm_master":
        if role_list["name"].lower() == in_user.lower():
            superAdmin = True
    if role_list is not None:
        if role_list.get("permissiongroup_details") is not None:
            if showDetails == "True":
                if superAdmin:
                    data = perGroup.get_all_group_permission(True)
                else:
                    data = role_list["permissiongroup_details"]
            else:
                if superAdmin:
                    role_list["permissiongroup_details"] = perGroup.get_all_group_permission(
                        True)
                list = []
                for rec in role_list.get("permissiongroup_details"):
                    for recInner in rec["routes_details"]:
                        list.append(recInner["name"])
                return jsonify(json.loads(dumps({"result": "success", "data": list}))), 200
        else:
            raise Exception ("No data found")
    else:
        raise Exception ("Role with id :" + user["roleid"] + "was not found")
    return jsonify(json.loads(dumps({"result": "success", "data": data}))), 200

@userAPI.route('/user/auth', methods=['POST'])
@authService.unauthorized
@swag_from(relative_path + '/swgger/UserAPI/genAuth.yml')
def genAuth():
    data = request.json
    validate(data, 'User', relative_path + '/swgger/UserAPI/genAuth.yml')
    user = request.json.get('user')
    password = request.json.get('password')
    print " The user: "+user+" is trying to log in."
    response= user_login(user,password)
    print " The user: "+user+" has logged in."
    return response

@userAPI.route('/user/basicauth', methods=['POST'])
@authService.unauthorized
@swag_from(relative_path + '/swgger/UserAPI/userBasicAuth.yml')
def genBasicAuth():
    user = request.authorization.username
    password = request.authorization.password
    print " The user: "+user+" is trying to log in."
    response= user_login(user,password)
    print " The user: "+user+" has logged in."
    return response
def user_login(user,password):    
    if is_ldap_enabled() and not is_special_user(user):
        user_db_details = auth_with_ldap(password, user)
    else:
        user_db_details = auth_with_db(user,password)
    update_user_last_login(user_db_details)
    user_db_details=invalidate_temp_password(user_db_details)
    return create_auth_response(user,user_db_details), 200

def auth_with_db(user,password):
    user_db_details = userdb.get_user(user, False)
    if user_db_details:
        if user_db_details["status"].lower() != "active":
            raise Exception("Invalid credentials")
        elif str(password) != str(user_db_details["password"]):
            if datetime.strptime(user_db_details.get("temp_pass_expiry",(datetime.now()-timedelta(hours=1)).isoformat()), "%Y-%m-%dT%H:%M:%S.%f") > datetime.now():
                if str(user_db_details.get("temp_password",""))=="":
                    raise Exception("Invalid credentials")
                if str(user_db_details.get("temp_password",""))!=str(password):
                    raise Exception("Invalid credentials")
            else:
                raise Exception("Invalid credentials")
        else:
            temp_pass_expiry=(datetime.now()-timedelta(hours=1)).isoformat()
            user_db_details["temp_password"]=""
            user_db_details["temp_pass_expiry"]=temp_pass_expiry
    else:
        raise Exception("Invalid credentials")
    return user_db_details


def auth_with_ldap(password, user):
    print "LDAP authentication for: " + user
    user_ldap_data = LdapHelper.get_user(user, password)
    if user_ldap_data:
        user_role = get_user_role_based_on_ldap_groups(user_ldap_data)
        user_full_name = user_ldap_data.get("name")[0]
        user_db_details = authService.create_or_update_user(user, user_full_name, user_role)
    else:
        raise Exception("Invalid credentials")
    return user_db_details

def invalidate_temp_password(user_db_details):
    temp_pass_expiry=(datetime.now()-timedelta(hours=1)).isoformat()
    data={}
    
    if datetime.strptime(user_db_details.get("temp_pass_expiry",(datetime.now()-timedelta(hours=1)).isoformat()), "%Y-%m-%dT%H:%M:%S.%f") > datetime.now():
        data = {"_id": {"oid": user_db_details["_id"]}, "temp_password": "", "temp_pass_expiry":temp_pass_expiry,"isfirstlogin" : "true"}
        user_db_details["isfirstlogin"]="true"
    else:
        data = {"_id": {"oid": user_db_details["_id"]}, "temp_password": "", "temp_pass_expiry":temp_pass_expiry,"isfirstlogin" : user_db_details.get("isfirstlogin","true")}
        user_db_details["isfirstlogin"]=user_db_details.get("isfirstlogin","true")
    userdb.update_user(data)
    return user_db_details
    
def get_user_role_based_on_ldap_groups(user_ldap_data):
    auth_service_settings = configDb.getConfigByName('AuthService')
    user_groups = set(get_user_ldap_groups(user_ldap_data))
    if auth_service_settings:
        if auth_service_settings.get("operator_role_groups"):
            operator_role_groups = str(auth_service_settings.get("operator_role_groups")).split(',')
            if any(elem in operator_role_groups for elem in user_groups):
                return UserRoles.Operator.name
        if auth_service_settings.get("admin_role_groups"):
            admin_role_groups = str(auth_service_settings.get("admin_role_groups")).split(',')
            if any(elem in admin_role_groups for elem in user_groups):
                return UserRoles.Admin.name

    return UserRoles.Guest.name


def get_user_ldap_groups(user_ldap_data):
    groups = []
    for group in user_ldap_data.get("memberOf"):
        m = re.search('CN=(\w+)[,$]', group)
        if m:
            groups.append(m.group(1))
    return groups


def create_auth_response(user,user_db_details):
    return jsonify(json.loads(dumps({"result": "success",
                    "message": "Token was generated for existing user found",
                    "data": {"Token": authService.generate_auth_token(str(user_db_details["_id"])),
                             "user": user_db_details.get("user", None),
                             "email": user_db_details.get("email", None),
                             "lastloggedin": user_db_details.get("lastloggedin", None),
                             "isfirstlogin": user_db_details.get("isfirstlogin", user_db_details.get("isfirstlogin","true")),
                             "homepage": authService.get_default_home_page(user)
                             }
                    })))


def update_user_last_login(user_db_details):
    localtime = datetime.now().isoformat()
    userdb.update_user(
        {"_id": {"oid": str(user_db_details.get("_id"))}, "lastloggedin": localtime})


def is_special_user(user):
    return SpecialUsers.has_name(user)


def is_ldap_enabled():
    auth_service_settings = configDb.getConfigByName('AuthService')
    return auth_service_settings and str(auth_service_settings.get("enable_ldap")).lower() == "true"


@userAPINs.route('/forgotPassword', methods=['POST'])
class userForgotPassword(Resource):
    @api.expect(header_parser,UserModel.ForgotPassword_input_model,validate=True)
    @api.marshal_with(UserModel.ForgotPassword_response_model)
    @authService.unauthorized
    def post(self):
        if is_ldap_enabled() and is_special_user(request.json.get('user')):
            return authService.reset_pass(request)
        else:
            raise Exception ("Password reset is not allowed for the specified user")


@userAPINs.route('/logout', methods=['POST'])
class genLogout(Resource):
    @api.marshal_with(UserModel.logout_response_model)
    @authService.authorized
    def post(self):
        token,user=authService.invalidate()
        print " The user: "+user+" has been logged out. Reason: User Request."
        return {"result": "success", "data": {"Token":token}}, 200


@userAPINs.route('/auth/verify', methods=['POST'])
class verifyAuth(Resource):
    @api.expect(header_parser,UserModel.auth_verify_input_model,validate=True)
    @api.marshal_with(UserModel.auth_verify_response_model)
    @authService.unauthorized
    def post(self):
        token = request.json.get('token')
        if not authService.verify_auth_token(token, True):
            raise Exception ("Invalid Token")
        else:
            return {"result": "success", "message": "Valid Token"}, 200


@userAPI.route('/user/import', methods=['POST'])
@authService.authorized
def Upload_CsvFile():
    # This is the path to the upload directory
    try:
        # Get the name of the uploaded file
        file = request.files['file']
        if file is None:
            raise ValueError("No file selected")
        filename = ('.' in file.filename and
                    file.filename.rsplit('.', 1)[1] in ['csv'])
        if filename not in [True]:
            raise Exception ("Invalid file .Please select file of type 'csv'")
        # Check if the file is one of the allowed types/extensions
        if file and filename:
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            file_path = str(import_full_path + '/' + filename)
            file.save(file_path)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    reader = csv.reader(f)
                    index = 0
                    status = 0
                    variable = []
                    for row in reader:

                        flag = 0
                        index = index + 1
                        if index is 1:
                            if len(row) is 6 and row[0] in "username" and row[1] in "password" and row[2] in "employeeid" and row[3] in "role" and row[4] in "email" and row[5] in "account":
                                status = 1
                            else:
                                variable2 = ""
                                variable.append(index)
                                raise Exception ("Header Validation failed.")
                        else:
                            if len(row) is 6 and not (row[0].isspace() or row[0] is '') and not (row[1].isspace() or row[1] is '') and not (row[2].isspace() or row[2] is '') and not (row[3].isspace() or row[3] is '') and not (row[4].isspace() or row[4] is '') and not (row[5].isspace() or row[5] is ''):
                                role_data = roledb.get_role_by_name(row[3], False)
                                account_data = accountDB.get_account_by_name(row[5])
                                if role_data is None and account_data is None:
                                    variable2 = ""
                                    variable2 = variable2 + "Row no " + \
                                        str(index) + \
                                        ":Role, Account not present, "
                                    variable.append(variable2)
                                elif role_data is None and account_data is not None:                                    
                                    variable2 = ""
                                    variable2 = variable2 + "Row no " + \
                                        str(index) + \
                                        ":Role not present, "
                                    variable.append(variable2)
                                elif role_data is not None and account_data is None:                                    
                                    variable2 = ""
                                    variable2 = variable2 + "Row no " + \
                                        str(index) + \
                                        ":Account not present, "
                                    variable.append(variable2)
                                else:
                                    # Check if the user with the same username already exists                                    
                                    if userdb.is_duplicate(row[0]) is False:
                                        try:
                                            data = {}
                                            variable2 = ""
                                            data["user"] = row[0]
                                            # data["machine_name"] = row[0]
                                            data["accountid"] = str(
                                                accountDB.get_account_by_name(row[5])["_id"])
                                            data["password"] = row[1]
                                            data["employeeid"] = row[2]                                            
                                            data["email"] = row[4]
                                            data["roleid"] = str(
                                                roledb.get_role_by_name(row[3], False)["_id"])
                                            data["status"] = "active"
                                            env_id = userdb.add_user(data)
                                            variable2 = variable2 + "Row no " + \
                                                str(index) + ": User with username :" + \
                                                data["user"] + \
                                                " created"
                                            variable.append(variable2)
                                        except Exception as e:  # catch *all* exceptions
                                            print "Error :" + str(e)
                                            traceback.print_exc()
                                            raise Exception ("Failed to create new user at row no " + str(index))
                                    else:
                                        variable2 = ""                                        
                                        variable2 = variable2 + "Row no " + \
                                            str(index) + ": User with username :" + \
                                            str(str(row[0])) + \
                                            " already exists "     
                                        variable.append(variable2)                                   
                            else:
                                variable2 = ""
                                variable2 = variable2 + \
                                    "Row no " + str(index) + ":"
                                if (row[0].isspace() or row[0] is ''):
                                    variable2 = variable2 + "username,"
                                if (row[1].isspace() or row[1] is ''):
                                    variable2 = variable2 + "password,"
                                if (row[2].isspace() or row[2] is ''):
                                    variable2 = variable2 + "employeeid,"
                                if (row[3].isspace() or row[3] is ''):
                                    variable2 = variable2 + "role,"
                                if (row[4].isspace() or row[4] is ''):
                                    variable2 = variable2 + "email, "
                                if (row[5].isspace() or row[5] is ''):
                                    variable2 = variable2 + "account,"
                                variable2 = variable2[:-1]
                                variable2 = variable2 + " not found"
                                variable.append(variable2)
                # RELOAD TEAM PERMISSIONS
                teamService.generate_details()
                return jsonify(json.loads(dumps({"result": "success", "message": "File has been uploaded", "data": variable}))), 200
            else:
                raise Exception("Unable to upload file")
    finally:
        try:
            f.close()
            os.remove(file_path)
        except Exception as e:
            print e