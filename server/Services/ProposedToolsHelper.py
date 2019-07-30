from datetime import datetime
import os,json,shutil,subprocess,traceback
from DBUtil import ProposedTools,Tool,Config,SystemDetails,Versions,Repository
from settings import mongodb, proposed_tool_git_full_path,\
    proposed_tool_jenkins_full_path,logo_path, logo_full_path, current_path
from Services import Mailer,HelperServices
from modules import ToolAPI


#DB
proposedToolsDB=ProposedTools.ProposedTools()
toolDB=Tool.Tool(mongodb)
configdb = Config.Config(mongodb)
sysdetailsDB = SystemDetails.SystemDetails(mongodb)
system_details = sysdetailsDB.get_system_details_single()
tooldb = Tool.Tool(mongodb)
versionsDB = Versions.Versions(mongodb)
RepositoryDB= Repository.Repository()
#SERVICES
mailer = Mailer.Mailer()

def email_tool_proposed(pt_details):
    mailer.send_html_notification(pt_details.get("support_details"),None,None, 17,
                                   {"name": pt_details.get("name"), "machine_host": system_details.get("hostname")})

def email_approval_req(pt_details):
    proposed_tool_support_email=configdb.getConfigByName("ProposedToolService").get("support_details")
    mailer.send_html_notification(proposed_tool_support_email,None,pt_details.get("support_details"), 15,
                                   {"name": pt_details.get("name"), "machine_host": system_details.get("hostname")})
    
def email_approved(pt_details,git_dir_name):
    proposed_tool_support_email=configdb.getConfigByName("ProposedToolService").get("support_details")
    mailer.send_html_notification(pt_details.get("support_details"),None,proposed_tool_support_email, 16,
                                   {"name": pt_details.get("name"), "machine_host": system_details.get("hostname"),
                                    "username":pt_details.get("support_details").split("@")[0],"git_dir":git_dir_name})
        
def email_rejeted(pt_details):
    proposed_tool_support_email=configdb.getConfigByName("ProposedToolService").get("support_details")
    mailer.send_html_notification(pt_details.get("support_details"),None,proposed_tool_support_email, 18,
                                   {"name": pt_details.get("name"), "machine_host": system_details.get("hostname")})

def create_request(pt_details):
    
    all_default_repos = list(RepositoryDB.get_all({"is_default_repo_ind":"true"}))
    if not all_default_repos: raise Exception("Default Repository could not be found")
    final_data={
    "name": pt_details.get("name"),
    "tag": [],
    "support_details": pt_details.get("support_details"),
    "request_reason": pt_details.get("request_reason"),
    "description": pt_details.get("description"),
    "version": {
        "version_name": pt_details.get("version").get("version_name"),
        "version_date": str(datetime.now()),
        "version_number": pt_details.get("version").get("version_number"),
        "pre_requiests": [],
        "branch_tag": "Branch",
        "gitlab_repo": "",
        "gitlab_branch": "master",
        "jenkins_job": "",
#         "document": {"documents": []},
        "backward_compatible": "no",
        "release_notes": "",
        "mps_certified": [],
#         "deployment_field": {"fields": []},
        "deployer_to_use": "DefaultDeploymentPlugin",
        "dependent_tools": [],
        "repository_to_use":all_default_repos[0].get("name")
    },
    "artifacts_only" : "false", 
    "is_tool_cloneable" : "true"   ,
    "allow_build_download" : "false"             
    }
    HelperServices.validate_name(final_data.get("name"),"tool name")
    final_data = HelperServices.add_update_logo(final_data, logo_path, logo_full_path, None)
    validate_mandatory_details(final_data)
    validate_existing_tool(final_data)
    validate_pk_tool(final_data)
    validate_mandatory_details(final_data)
    return final_data

def validate_pk_tool(pt_details):
    if proposedToolsDB.get_by_name( pt_details.get("name")):
        raise Exception("A Tool was already proposed with this name.Please try a different Name")

def validate_existing_tool(pt_details):
    if toolDB.get_tool_by_name( pt_details.get("name"), False):
        raise Exception("A Tool already exists with this name.Please try a different Name")
    
def validate_mandatory_details(pt_details):
    keys_to_validate=["name","support_details","description"]
    keys_to_validate_in_version=["version_name","version_number"]
    for key in keys_to_validate:
        if not pt_details.get(key):
            raise Exception("Mandatory key: "+key+" was not found in request")
    for key in keys_to_validate_in_version:
        if not pt_details.get("version",{}).get(key):
            raise Exception("Mandatory key: "+key+" was not found in request")    
        
def create_git_dir_for_proposed_tool(git_dir_path,tool_name):  
    try:
        os.makedirs(git_dir_path)      
        src_files = os.listdir(proposed_tool_git_full_path)
        for file_name in src_files:
            full_file_name = os.path.join(proposed_tool_git_full_path, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name,git_dir_path)
        modify_git_install_for_proposed_tool(git_dir_path,tool_name)        
        subprocess.check_output('git init && git add .',\
                            cwd=git_dir_path, shell=True)
        subprocess.check_output('git -c user.name="vpadmin" -c user.email="vpadmin@amdocs.com" commit -m "Init"',\
                        cwd=git_dir_path, shell=True)   
        subprocess.check_output('git checkout -b dummy',\
                        cwd=git_dir_path, shell=True)                     
    except Exception as e:  # catch *all* exceptions
        shutil.rmtree(git_dir_path, True)
        raise e        
    return True
    
def create_jenkins_dir_for_proposed_tool(jenkins_dir_path):   
    try:     
        os.makedirs(jenkins_dir_path)      
        src_files = os.listdir(proposed_tool_jenkins_full_path)
        for file_name in src_files:
            full_file_name = os.path.join(proposed_tool_jenkins_full_path, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name,jenkins_dir_path)
    except Exception as e:  # catch *all* exceptions
        shutil.rmtree(jenkins_dir_path, True)
        raise e                
    return True        
            
def modify_jenkins_config_for_proposed_tool(artifact,version_name,response,proposed_tool_config,jenkins_dir_path,git_dir_name):        
    with open(os.path.join(jenkins_dir_path,"config.xml"), "r+") as f:
        data = f.read()
        if "VERNAME" in data: data = data.replace("VERNAME",version_name)
        if "MONGOID" in data: data = data.replace("MONGOID",\
                        json.loads(response[0].data).get("data").get("version_id"))
        if "PACNAME" in data: data = data.replace("PACNAME",proposed_tool_config.get("package"))
        if "ARTINAME" in data: data = data.replace("ARTINAME",artifact)
        if "REPONAME" in data: data = data.replace("REPONAME",proposed_tool_config.get("reponame"))
        if "GIT_DIR_NAME" in data: data = data.replace("GIT_DIR_NAME",git_dir_name)
        f.seek(0)
        f.write(data)
        f.truncate()

def modify_git_install_for_proposed_tool(git_dir_path,tool_name):        
    with open(os.path.join(git_dir_path,"install.sh"), "r+") as f:
        data = f.read()
        if "TOOLNAME" in data: data = data.replace("TOOLNAME",tool_name)
        f.seek(0)
        f.write(data)
        f.truncate()
        
def parse_add_tool_response(request):        
    response=ToolAPI.add_tool()  
    if response[1] <> 200:
        raise Exception(json.loads(response[0].data).get("message"))
    tool_id=json.loads(response[0].data).get("data").get("_id")
    version_id=json.loads(response[0].data).get("data").get("version_id")
    return  response,tool_id,version_id        
  
def validate_git_details(proposed_tool_config,request):  
    git_path=proposed_tool_config.get('gitpath')
    git_dir_name=str(request.json.get("name").replace(" ","_")).lower()
    git_dir_path=os.path.normpath(os.path.join(git_path,git_dir_name))
    if os.path.exists(git_dir_path):
        raise Exception("Git project with name: "+git_dir_name+" already exists")
    return git_dir_name,git_dir_path

def validate_jenkins_details(git_dir_name,version_name,version_number,proposed_tool_config,request):  
    jenkins_dir_name=str(git_dir_name+"_"+version_name+"_"+str(version_number)).lower().replace(" ", "_").replace(".", "_")
    jenkins_path=proposed_tool_config.get('jenkinspath')
    jenkins_dir_path=os.path.normpath(os.path.join(jenkins_path,"jobs",jenkins_dir_name))        
    if os.path.exists(jenkins_dir_path):
        raise Exception("Jenkins project with name: "+jenkins_dir_name+" already exists")
    return jenkins_dir_name,jenkins_dir_path
    
def add_request_for_user_add_and_jenkins_restart(user,git_project_name):
    user_list_file=os.path.join(current_path,"utilities/ProposedTools/scheduler/UsersListForAutoCreation.txt")
    if os.path.exists(user_list_file):
        with open(user_list_file, "a") as myfile:
            myfile.write(user+":"+git_project_name+"\n")
            print "Entry: "+"\n"+user+":"+git_project_name+" was added to file:"+user_list_file
    else:
        print "File: "+user_list_file+" does not exists.Entry will not be made"         
        
def approve_tool(request):
    git_dir_path=""
    git_dir_created=False
    jenkins_dir_path=""
    jenkins_dir_created=False
    tool_id=""
    version_id=""
    try:
        # CLEAN UNWANTED DATA        
        for key in ["request_reason"]:
            if key in request.json.keys():
                request.json.pop(key)
        
        #Load Config
        proposed_tool_config=configdb.getConfigByName("ProposedToolService")        
        #BUILD AND VALIDATE GIT      
        git_dir_name,git_dir_path=validate_git_details(proposed_tool_config, request)        
        #BUILD AND VALIDATE JENKINS
        version_name=str(request.json["version"]["version_name"]).lower()
        version_number=str(request.json["version"]["version_number"]).lower() 
        artifact=str(request.json.get("name").replace(" ","_")).lower()       
        jenkins_dir_name,jenkins_dir_path=validate_jenkins_details(git_dir_name, version_name,version_number,\
                                                                    proposed_tool_config, request)
        #PREPARE DATA
        request.json["version"]["gitlab_repo"]=git_dir_name
        request.json["version"]["jenkins_job"]=jenkins_dir_name   
        request.json["status"]="2"    
        
        # ADD NEW TOOL IN DB
        response,tool_id,version_id=parse_add_tool_response(request)
        #CREATE GIT
        git_dir_created=create_git_dir_for_proposed_tool(git_dir_path,str(request.json.get("name").replace(" ","_")).lower())
        #CREATE JENKINS
        jenkins_dir_created=create_jenkins_dir_for_proposed_tool(jenkins_dir_path)
        #MODIFY JENKINS CONFIG
        modify_jenkins_config_for_proposed_tool(artifact,str(version_name+"_"+str(version_number)).lower().replace(" ", "_").replace(".", "_"), response,\
                         proposed_tool_config, jenkins_dir_path, git_dir_name)        
        
        #SET UsersListForAutoCreation.txt for auto restart
        add_request_for_user_add_and_jenkins_restart(request.json.get("support_details").split("@")[0],git_dir_name)
        
        # DELETE REQUEST FROM DB
        proposedToolsDB.delete(str(request.json.get("_id")))
        
        # EMAIL USER
        email_approved(request.json,git_dir_name)
        return json.loads(response[0].data), 200
    except Exception as e:  # catch *all* exceptions
        print "Error :" + str(e)
        traceback.print_exc()
        #CLEAR DATA
        if git_dir_created and os.path.exists(git_dir_path): shutil.rmtree(git_dir_path)
        if jenkins_dir_created and os.path.exists(jenkins_dir_path): shutil.rmtree(jenkins_dir_path)
        if tool_id:
            tooldb.delete_tool(tool_id)
        if version_id:
            versionsDB.delete_version(version_id)
        raise e   