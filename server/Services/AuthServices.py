from functools import wraps
import logging,json,copy
import threading
import time
from flask.wrappers import Response
from datetime import datetime, timedelta
from Crypto.PublicKey import RSA
from autologging import logged, TRACE
from flask import request
import jwt
import traceback
from bson.json_util import dumps
from DBUtil import Users, Permissions, Role, PermissionGroup, Accounts, Config, SystemDetails, Teams,Auditing
from Services import PasswordHelper, Mailer, TeamService
from Services.UserRoles import UserRoles
from settings import dpm_type
from collections import OrderedDict
from Services.HelperServices import genrate_random_key
from concurrent.futures import ThreadPoolExecutor

@logged(logging.getLogger("AuthRequestService"))
class AuthRequestService(object):

    # Init's Data
    def __init__(self, db, key):
        self.RSAKEY = RSA.generate(1024)
        self.SECRET_KEY = self.RSAKEY.exportKey('PEM')
        self.SECRET_PUBLIC_KEY = self.RSAKEY.publickey().exportKey('PEM')
        self.ENCRYPTION_METHOD = 'RS512'
        # WE WILL VERIFY EXPIRATION BY OURSELVES
        self.JWT_OPTIONS = {'verify_exp': False, }
        self.userdb = Users.Users(db)
        self.auditdb = Auditing.Auditing()
        self.roledb = Role.Role(db)
        self.passHelper = PasswordHelper.PasswordHelper(key)
        self.permissiondb = Permissions.Permissions(db)
        self.permissiongroupdb = PermissionGroup.PermissionGroup(db)
        self.accountDB = Accounts.Accounts()
        self.configdb = Config.Config(db)
        self.systemDetailsDB = SystemDetails.SystemDetails(db)
        self.configdbData = self.configdb.getConfigByName("AuthService")  # 6 is for AuthRequestService configuration
        self.auditing_config = self.configdb.getConfigByName("AuditingServices")  # 6 is for AuthRequestService configuration
        self.mailer = Mailer.Mailer()
        self.validTokens = {}
        self.teamService = TeamService.TeamService()
        self.collection = db.SystemDetails  # Set Collection as Permissions
        self.teamsdb = Teams.Teams(db)
        if self.configdbData is not None:
            if self.configdbData.get("expiration") is not None:
                self.expiration = int(self.configdbData.get("expiration"))
            else:
                raise Exception(
                    "Config AuthService does not have expiration set")
            if self.configdbData.get("email_domain") is not None:
                self.email_domain = str(self.configdbData.get("email_domain"))
            else:
                raise Exception(
                    "Config AuthService does not have email_domain set")
            self.allow_multi_user_session = self.configdbData.get("allow_multi_user_session","false")        
        else:
            raise Exception("Config was not found for Authorization services")

        # ADD DEAMON THREAD TO REMOVE IN VALID TOKENS AUTOMATICALLY
        pool = ThreadPoolExecutor(2,__name__+".__init__")
        pool.submit(self.removeInvalidTokens)
        pool.submit(self.check_if_user_logged_in_from_last_6_months)
   
        
        
    def check_if_user_logged_in_from_last_6_months(self):
        while True:
            for user in self.userdb.get_all_users():
                if user.get("lastloggedin") and user.get("status").lower() == "active" :
                    last_login_date = user.get("lastloggedin").split("T")[0]
                    formatted_date = datetime.strptime(last_login_date, "%Y-%m-%d")
                    if (formatted_date + timedelta(days = 182)) < datetime.now():
                        message = " The user: "+user["user"]+" has not logged in since 6 months. The user is marked suspended"
                        print message
                        self.mark_user_as_inactive(str(user["_id"]),message)    
            time.sleep(3600)  # 60 Min
    
    def mark_user_as_inactive(self,user_id,message):
        self.userdb.update_user_status(user_id, "suspended",message)


    # RUNS IN THREAD AND REMOVES INVALID TOKEN
    def removeInvalidTokens(self):
        """This method Removes Invalid Tokens from Memory"""
        while True:
            for token in self.validTokens.keys():
                if self.hasTokenExpired(token):
                    print " The user: "+self.userdb.get_user_by_id(self.validTokens[token]["user_id"]).get("user")+" has been logged out. Reason: Session Timeout."
                    self.RemoveTokenFromMem(str(token))
            time.sleep(10)  # 10 SEC

    # CHECKS IF THE GIVEN TOKEN HAS EXPIRED
    def hasTokenExpired(self, token):
        """This method Checks whether the Token is valid or is invalid"""
        return int((datetime.now() - self.validTokens.get(token).get("time")).total_seconds()) \
            > int(self.expiration)

    # GENRATES A NEW TOKEN TO REQUESTER
    def generate_auth_token(self, user_id, expiration=6000):
        """This method generates the authentication token"""
        data = {'id': user_id, "source_ip": str(request.remote_addr), "first_login_time": str(
            datetime.now())} if user_id is not None else {}
        result = jwt.encode(data, self.SECRET_KEY,
                            algorithm=self.ENCRYPTION_METHOD)
        if user_id is not None:
            self.AddTokenToMem(str(result),user_id,str(request.remote_addr))
        return result

    # REMOVES THE TOKEN PASSED IN HEADER AND CREATES A DUMMY TOKEN AND RETURNS
    # IT BACK
    def invalidate(self):
        """This method removes the token passed in headers and returns a dummy token"""
        if 'token' not in request.headers:
                    # Unauthorized
            raise ValueError("No token in header")
        token = request.headers["Token"]
        user=None
        if token in self.validTokens:
            user=self.userdb.get_user_by_id(self.validTokens[token]["user_id"]).get("user")
            self.RemoveTokenFromMem(str(token))
        return_token = self.generate_auth_token(None, 0)
        return return_token,user
        
    # ADD A TOKEN GENRATED BY generate_auth_token to APP MEMORY
    def AddTokenToMem(self, token,user_id,source_ip):
        """ This method adds a TOKEN to APP memory"""
        now = datetime.now()
        delta = timedelta(0, self.expiration)
        t = now.time()
        today = datetime.today()
        if self.allow_multi_user_session.lower() == "false":
            self.remove_previous_sessions_of_user(user_id)
        self.validTokens[token] = {"time":(datetime.combine(today, t) + delta),"user_id":user_id,"source_ip":source_ip}
        
    # A USER IS ALLOWED TO HAVE ONLY ONE VALID SESSION    
    def remove_previous_sessions_of_user(self,user_id):
        for rec in copy.deepcopy(self.validTokens):
            if  str(user_id) ==  str(self.validTokens[rec].get("user_id")):
                self.validTokens.pop(rec)    

    # REMOVE A TOKEN GENERATED BY generate_auth_token to APP MEMORY
    def RemoveTokenFromMem(self, token):
        """This method removes TOKEN from APP Memory"""
        if self.validTokens.get(token):
            self.validTokens.pop(token)

    # CHECK IF TOKEN IS VALID.IF VALID INCREASE TOKEN VAIDITY BY
    # self.expiration seconds.IN INVALID REMOVE IT FROM APP MEMORY
    def check_validToken(self, token):
        """ This method Checks if the TOKEN is valid then increase """ + \
            """its validity else it removes it from memory"""
        try:
            result = jwt.decode(token, self.SECRET_PUBLIC_KEY, options=self.JWT_OPTIONS, algorithms=[
                self.ENCRYPTION_METHOD])
            if self.hasTokenExpired(token):
                self.RemoveTokenFromMem(str(token))
            else:
                now = datetime.now()
                delta = timedelta(0, self.expiration)
                t = now.time()
                today = datetime.today()
                self.validTokens[str(token)] = {"time":(
                    datetime.combine(today, t) + delta),"user_id":result["id"],"source_ip":result["source_ip"]}
        except Exception:
            self.RemoveTokenFromMem(str(token))


    def get_user_details(self, token,return_user_id=False):        
        try:
            token, type_of_token = self.getToken(request)
            if type_of_token == 'Token':
                user_id = self.verify_auth_token(token, True)
            elif type_of_token == 'Access_Token':
                user_id = self.verify_access_token(token, True)
            user = self.userdb.get_user_by_id(user_id, False)
            if user is not None:
                if return_user_id:
                    return str(user["_id"])
            return  user   
        except Exception:
            return None  # valid token, but expired
        
    # INTERNALLY CALLS check_validToken
    # CHECKS USER ROUTES AND PERMISSIONS
    def verify_auth_token(self, token, returnUser=False):
        """This method checks ROutes and permissions if the token is valid"""
        # REMOVE ALL INVALID TOKENS
        self.check_validToken(token)
        try:
            data = jwt.decode(token, self.SECRET_PUBLIC_KEY, options=self.JWT_OPTIONS, algorithms=[
                self.ENCRYPTION_METHOD])
        except Exception:
            self.invalidate()
            return None  # valid token, but expired
        if not self.validTokens.get(token):
            print "The token is invalid.User will be logged out"
            return None
        user = self.userdb.get_user_by_id(data['id'], False)
        if user is not None:
            if returnUser:
                return str(user["_id"])
            result = self.authPermissions(user)
            return result
        else:
            return None

    def verify_access_token(self, token, returnUser=False):
        """This method verifiey the access token"""
        user = self.userdb.get_user_by_access_token(token, False)
        if user is not None:
            if returnUser:
                return str(user["_id"])
            result = self.authPermissions(user)
            return result
        else:
            return None

    def get_userid_by_auth_token(self):
        """This method fetches the USERID by decrypting the AUTH_TOKEN"""
        token, type_of_token = self.getToken(request)
        if not token:
            raise ValueError("No token in header")
        if type_of_token == 'Token':
            return self.verify_auth_token(token, True)
        elif type_of_token == 'Access_Token':
            return self.verify_access_token(token, True)

    def getToken(self, request):
        if request.headers.get("Token"):
            return request.headers.get("Token"), "Token"
        elif request.headers.get("Access_Token"):
            return request.headers.get("Access_Token"), "Access_Token"
        else:
            return None, None

    def record(self,fn,user_id,*args, **kwargs):
        now = datetime.now()
        if str(self.auditing_config.get("enable")).lower() <> "true":
            return fn(*args, **kwargs)
        try:
    #         data = {"user":self.userdb.get_user_by_id(user_id, False)["user"],"remote_addr":str(request.remote_addr),"headers":str(request.headers),\
    #                 "url":str(request.base_url),"end_point":str(request.endpoint),
    #                "request_type":str(request.method),"client_info":str(request.user_agent),"args":str(request.view_args),"data":str(request.data)}
    
            data = {"remote_addr":str(request.remote_addr),"headers":str(request.headers),\
                    "url":str(request.path),"end_point":str(request.endpoint),
                   "request_type":str(request.method),"client_info":str(request.user_agent),"requested_at" :now }
            
            user_details = self.userdb.get_user_by_id(user_id, False)
            if user_details : 
                data["user"]=user_details["user"]
                data["role_id"]= user_details["roleid"]
                data["api_type"] = "Authorized"
                
            else : 
                data["api_type"] = "Unauthorized"
            
            oid=self.auditdb.add(data)
            
            try:
                response = fn(*args, **kwargs)
            except Exception as e:  # catch ValidationError exceptions
                data["response"]=str(e).replace("$oid","oid").replace("$date","date")
                data["response_status_code"]=404
                self.auditdb.update(data, oid)
                logging.log(logging.ERROR,"^^^^^^^^ ERROR STACK TRACE --> "+str(data.get("user","NA"))+" "+str(request.remote_addr)+" "+str(request.method)+" "+ str(request.path)+" "+str(data.get("response_status_code"))+" ^^^^^^^^")
                traceback.print_exc()
                logging.log(logging.ERROR,"^^^^^^^^^^^^^^^^^^^^^^      ^^^^^^^^^^^^^^^^^^^^^^^ ")
                raise e
            try:
                data["response"]=response[0]
                
                # NEED IF AS SOMETIMES MULTIPLE IF"S GET USED
                if type(data["response"]) == Response:
                    data["response"]=str(data["response"].data).replace("$oid","oid").replace("$date","date")
                if type(data["response"]) == OrderedDict:
                    data["response"]=dict(data["response"])
                if type(data["response"]) == dict:
                    data["response"]=dumps(data["response"]).replace("$oid","oid").replace("$date","date")
                if type(data["response"]) == str:
                    data["response"]=data["response"].replace("$oid","oid").replace("$date","date")    
                data["response_status_code"]=response[1]            
            except Exception:
                pass    
            finally:
                try:
                    data["response"]=json.loads(data.get("response"))
                except:
                    pass
                try:
                    self.auditdb.update(data, oid)                
                except:
                    pass
                return response
        finally:
            try:
                logging.log(TRACE,str(data.get("user","NA"))+" "+str(request.remote_addr)+" "+str(request.method)+" "+ str(request.path)+" "+str(data.get("response_status_code"))+" in "+str((datetime.now()-now).total_seconds() * 1000) + " ms")
            except:
                pass
            
    
    def authorized(self, fn):
        @wraps(fn)
        def _wrap(*args, **kwargs):
            user_id = None
            token, type_of_token = self.getToken(request)
            if not token:
                raise Exception("Missing Authorization Token")
            if type_of_token == 'Token':
                user_id = self.verify_auth_token(token, False)
            elif type_of_token == 'Access_Token':
                user_id = self.verify_access_token(token, False)
            if not user_id:
                raise Exception( "Invalid token or Unauthorized access to: "\
                                +str(self.get_required_Permission_goup_for_url(request.url)))
            else: 
                return self.record(fn,self.get_user_details(token, True),*args, **kwargs)
        return _wrap
    
    def unauthorized(self, fn):
        @wraps(fn)
        def _wrap(*args, **kwargs):
            return self.record(fn,None,*args, **kwargs)
        return _wrap

    def authPermissions(self, user):
        """This method Checks the auth permissions for a valid user"""
        grouplist = []
        permlist = []
        if user is not None:
            roleId = user["roleid"]
            result = self.roledb.get_role_by_id(roleId, False)
            if dpm_type.lower() == "dpm_master":
                in_user = 'SuperAdmin'
                if result["name"].lower() == in_user.lower():
                    return True
            for permissiongroup in result["permissiongroup"]:
                grouplist.append(permissiongroup)
            for record in grouplist:
                # print record
                result = self.permissiongroupdb.get_group_permission_by_id(
                    record, False)
                for eachperm in result["permissions"]:
                    permlist.append(eachperm)
            for record in permlist:
                result = self.permissiondb.get_permission_by_id(record)
                urlPartsCount = len(result["name"].split('~'))
                count = 0
                for rec in result["name"].split('~'):
                    if rec in request.url:
                        count = count + 1
                if urlPartsCount == count:
                    return True
            return None

    def get_required_Permission_goup_for_url(self, url):
        '''Search through all permission and fet relevant permission group'''
        
        for grp in self.permissiongroupdb.get_all_group_permission(True):
            for record in grp["permissions"]:
                result = self.permissiondb.get_permission_by_id(record)
                urlPartsCount = len(result["name"].split('~'))
                count = 0
                for rec in result["name"].split('~'):
                    if rec in request.url:
                        count = count + 1
                if urlPartsCount == count:
                    return grp.get("groupname")
        return None   


    def create_or_update_user(self, user_name, user_full_name, user_role):
        """This method Checks if user exists else creates a new user with role as GUEST"""
        # Check if user exists .Create new user with Role 'Guest' if not
        # exists
        user_name = user_name.lower()
        user_db_details = self.userdb.get_user(user_name, False)
        if user_db_details is None:
            systemdetails = self.systemDetailsDB.get_system_details_single()
            account_details = self.accountDB.get_account_by_name(systemdetails.get("account_name"))
            if not account_details:
                raise Exception("Unable to find account with name: " + systemdetails.get("account_name"))
            user = {"user": user_name, "full_name": user_full_name, "password": genrate_random_key(), "isfirstlogin": "false", "status": "active", "roleid": str(
                self.roledb.get_role_by_name(user_role, False)["_id"]), \
                       "accountid": str(account_details["_id"]), \
                       "email": user_name + self.email_domain, "employeeid": "0", "ldap_user": True}
            user_id = self.userdb.add_user(user)
            if user_role == UserRoles.Guest.name:
                guest_team = self.teamsdb.get_team_by_name("Guest_Team")
                if guest_team:
                    guest_team["_id"]={"oid":str(guest_team["_id"])}
                    guest_team["users_id_list"].append(str(user_id))
                    self.teamsdb.update_team(guest_team)

            self.teamService.generate_details()
            user_db_details = self.userdb.get_user(user_name, False)
        else:
            if user_full_name != user_db_details.get("full_name") or user_role != self.roledb.get_role_by_id(user_db_details.get("roleid"), False)["name"]:
                user_db_details["full_name"] = user_full_name
                user_db_details["roleid"] = str(self.roledb.get_role_by_name(user_role, False)["_id"])
                self.userdb.update_user(user_db_details)
        return user_db_details

    def reset_pass(self, request):
        """This method allows user to reset the password"""
        if request.json.get('user') is None:
            raise Exception ("Expected request input 'user' " +
                            "was not found in request")
        result = self.userdb.get_user(request.json.get('user'), False)
        if result is None:
            raise Exception ("No such user was found")
        elif result.get("email") is None:
            raise Exception ("No email id was found for user")
        if result["status"].lower() != "active":
            raise Exception ("User is not active")
        else:
            temp_password = genrate_random_key()
            temp_pass_expiry=(datetime.now()+timedelta(hours=12)).isoformat()
            data = {"_id": {"oid": str(result["_id"])}, "temp_password": temp_password, "temp_pass_expiry":temp_pass_expiry}
            self.userdb.update_user(data)
            try:
                systemdetails = self.systemDetailsDB.get_system_details_single()
                self.mailer.send_html_notification(result["email"],
                                                   None, None, 8,
                                                   {"name": result["user"],
                                                    "pass":temp_password,"temp_pass_expiry":temp_pass_expiry})
            except Exception as e:
                traceback.print_exc()
            self.remove_previous_sessions_of_user(result["_id"])
            return {"result": "success",
                            "message": "You password has been reset. " +
                            " New password will be emailed at "
                            + result["email"]
                            }, 200

    def get_default_home_page(self, user):
        try:
            home_page = None
            temp_user_data = {}
            temp_user_data = self.userdb.get_user(user, False)
            user_id = str(temp_user_data.get("_id"))
            teams = []
            teams = self.teamsdb.get_team_by_user(user_id)
            if "homepage" in temp_user_data.keys():
                home_page = temp_user_data["homepage"]
            elif teams.count() > 0:
                toolDashboardFlag = 0
                duDashboardFlag = 0
                for team in teams:
                    if "homepage" in team.keys():
                        if team["homepage"] == "dashboard":
                            toolDashboardFlag + 1
                        elif team["homepage"] == "duDashboard":
                            duDashboardFlag + 1
                if teams.count() == toolDashboardFlag:
                    home_page = "dashboard"
                elif teams.count() == duDashboardFlag:
                    home_page = "duDashboard"
                else:
                    system_details = self.collection.find_one()
                    home_page = system_details.get("homepage", None)
            else:
                system_details = self.collection.find_one()
                home_page = system_details.get("homepage", None)
        except Exception as e:  # catch *all* exceptions
            print str(e)
            traceback.print_exc()
        return home_page
