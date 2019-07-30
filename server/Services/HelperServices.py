'''
Created on Jul 20, 2016

@author: pdinda
'''
import shutil,re,string,random
from DBUtil import Versions, Tool, DeploymentFields, Sync, \
     Documents, MediaFiles,DeploymentUnit,Config,ExitPointPlugins,State
from settings import mongodb


configdb = Config.Config(mongodb)
versionsDB = Versions.Versions(mongodb)
toolDB = Tool.Tool(mongodb)
deploymentFieldsDB = DeploymentFields.DeploymentFields(mongodb)
syncDb = Sync.Sync(mongodb)
documentsDB = Documents.Documents(mongodb)
mediaFilesDB = MediaFiles.MediaFiles(mongodb)
deploymentunitdb = DeploymentUnit.DeploymentUnit()
exitPointPlugins=ExitPointPlugins.ExitPointPlugins()
statedb=State.State(mongodb)



def add_update_deployment_fields(deploymentFieldData, parent_entity_id):
    """Add Update a DeploymentField"""
    Deploymentinsert = {}
    Deploymentinsert['parent_entity_id'] = parent_entity_id
    Deploymentinsert['fields'] = deploymentFieldData
    for data in deploymentFieldData:
        keys_to_check = ["input_name", "input_type"]
        keys_whose_value_cannot_empty = ["input_name", "input_type"]
        for key in keys_to_check:
            if key not in data.keys():
                raise ValueError(
                    "Deployment field key: " + key + " was not found for:" + data.get("input_name"))
            if key in keys_whose_value_cannot_empty and not data.get(key):
                raise ValueError("Deployment field key: " + key +
                                 " cannot have empty value")    
    DeploymentField = deploymentFieldsDB.GetDeploymentFields(parent_entity_id)
    if DeploymentField:
        Deploymentinsert["_id"] = {}
        Deploymentinsert["_id"]["oid"] = str(DeploymentField.get("_id"))
        DeploymentFieldsresult = deploymentFieldsDB.UpdateDeploymentFields(
            Deploymentinsert)
    else:
        DeploymentFieldsresult = deploymentFieldsDB.AddDeploymentFields(
            Deploymentinsert)
    if DeploymentFieldsresult is None:
        raise Exception(
            "Unable to update DeploymentField for parent_entity_id " + str(parent_entity_id))
    return str(DeploymentFieldsresult)


def add_update_media_files(MediaFiles, version_id, directory_to_import_from=None, full_media_files_path=None, media_files_path=None):
    """Add Update a MediaFile"""
    MediaFilesinsert = {}
    MediaFilesinsert['parent_entity_id'] = version_id
    MediaFilesinsert['media_files'] = MediaFiles
    media_files = []
    for media in MediaFilesinsert['media_files']:
        if media.get("url"):
            file_name = media.get("url").split('/')[-1]
            media["url"] = media_files_path + "/" + file_name
        if media.get("thumbnail_url"):
            file_name = media.get("thumbnail_url").split('/')[-1]
            media["thumbnail_url"] = media_files_path + "/" + file_name
        else:
            media["thumbnail_url"] = media["url"]
        media_files.append(media)
    MediaFilesinsert['media_files'] = media_files
    MediaFile = mediaFilesDB.get_media_files(version_id)
    if MediaFile:
        MediaFilesinsert["_id"] = {}
        MediaFilesinsert["_id"]["oid"] = str(MediaFile.get("_id"))
        MediaFilesresult = mediaFilesDB.update_media_files(MediaFilesinsert)
    else:
        MediaFilesresult = mediaFilesDB.add_media_files(MediaFilesinsert)
    if MediaFilesresult is None:
        raise Exception(
            "Unable to update MediaFiles for version " + str(version_id))
    elif directory_to_import_from:
        for media in MediaFilesinsert['media_files']:
            if media.get("url"):
                file_name = media.get("url").split('/')[-1]
                print "Copying file :" + file_name
                shutil.copy(directory_to_import_from + '/mediaFiles/' +
                            file_name, full_media_files_path)
                print "Copying file completed for :" + file_name
            if media.get("thumbnail_url"):
                file_name = media.get("thumbnail_url").split('/')[-1]
                print "Copying file :" + file_name
                shutil.copy(directory_to_import_from + '/mediaFiles/' +
                            file_name, full_media_files_path)
                print "Copying file completed for :" + file_name
    return str(MediaFilesresult)


def add_update_documents(Documents, parent_entity_id):
    """Add Update a Document"""
    DocumentFieldsupdate = {}
    DocumentFieldsupdate['documents'] = Documents
    DocumentFieldsupdate['parent_entity_id'] = parent_entity_id
    doc = documentsDB.GetDocuments(parent_entity_id)
    if doc:
        DocumentFieldsupdate["_id"] = {}
        DocumentFieldsupdate["_id"]["oid"] = str(doc.get("_id"))
        DocumentFieldsresult = documentsDB.UpdateDocuments(
            DocumentFieldsupdate)
    else:
        DocumentFieldsresult = documentsDB.AddDocuments(DocumentFieldsupdate)
    if DocumentFieldsresult is None:
        raise Exception(
            "Unable to update Document for parent_entity_id " + parent_entity_id)
    return str(DocumentFieldsresult)


def add_update_logo(data, logo_path, full_logo_path, directory_to_import_from):
    # CHECK LOGO
    logo_default_letter = (data["name"][:1]).lower()
    if data.get("logo") in [None, "", "None"]:
        image_path = logo_path + '/default_' + logo_default_letter + '.png'
        data["logo"] = image_path
    else:
        if "default" not in data.get("logo"):
            file_name = data.get("logo").split('/')[-1]
            data["logo"] = logo_path + "/" + file_name
            if directory_to_import_from:
                print "Copying file :" + file_name
                shutil.copy(directory_to_import_from + '/logos/' +
                            file_name, full_logo_path)
                print "Copying file completed for :" + file_name
        else:
            image_path = logo_path + '/default_' + logo_default_letter + '.png'
            data["logo"] = image_path
    if data.get("thumbnail_logo") in [None, "", "None"] and data.get("logo") not in [None, "", "None"]:
        data["thumbnail_logo"] = data["logo"]
    else:
        if "default" not in data.get("thumbnail_logo"):
            file_name = data.get("thumbnail_logo").split('/')[-1]
            data["thumbnail_logo"] = logo_path + "/" + file_name
            if directory_to_import_from:
                print "Copying file :" + file_name
                shutil.copy(directory_to_import_from + '/logos/' +
                            file_name, full_logo_path)
                print "Copying file completed for :" + file_name
        else:
            image_path = logo_path + '/default_' + logo_default_letter + '.png'
            data["thumbnail_logo"] = image_path
    return data


def filter_handler(entity,filters,set_value,filter_type):
        if filters and len(filters) > 0:
                if entity.get(filter_type) and "any" not in filters:
                    if filter_type == "tag":
                        if filters and len(filters) > 0:
                            status = False
                            for tag in filters:
                                if tag not in set_value : status = True
                            return status
                    else:
                        if filters and len(filters) > 0 and len(list(set(filters) & set(set_value))) < 1:
                            return True
                            
                else:
                    if filters and len(filters) > 0 and "any" not in filters:
                        return True
        return False
    

def get_details_of_parent_entity_id(parent_entity_id):
    ver = versionsDB.get_version(parent_entity_id)
    if ver and toolDB.get_tool_by_id(ver.get("tool_id"),False): return ver
    du = deploymentunitdb.GetDeploymentUnitById(parent_entity_id)
    if (du is not None): return du
    state = statedb.get_state_by_id(parent_entity_id, False)
    if (state is not None): return state
    raise Exception ("No entity exist for provided parent_entity_id: "+str(parent_entity_id))


def validate_name(text,entity_name="name"):
    if not text or not re.match("^[a-zA-Z0-9]", text[0]):
        raise ValueError ("The "+entity_name+" cannot start with a special character")
    

def replace_hostname_with_actual(item,host,actual_host):
    if type(item) == str or type(item) == unicode:
        return str(item).replace(host,actual_host)
    elif type(item) == dict:
        for i in item.keys():
            item[i]=replace_hostname_with_actual(item[i],host,actual_host)
    elif type(item) == list:
        for counter, value in enumerate(item):
            item.pop(counter)
            item.append=(replace_hostname_with_actual(value,host,actual_host))
    return item


def delete_plugin_repo_validation(item,key_to_validate,entity):
    dus = deploymentunitdb.GetAllDeploymentUnits(None, None, False, {key_to_validate: {"$in": [item]}})
    present_in_du=[]
    for du in dus:
        if du.get("name") not in present_in_du:
            present_in_du.append(du.get("name")) 
    
    versions = versionsDB.get_all_tool_versions(None, None, {key_to_validate: {"$in": [item]}})
    present_in_ver=[]
    for ver in versions:
        tool_name=""
        if toolDB.get_tool_by_id(ver.get("tool_id"),False) :
            tool_name=toolDB.get_tool_by_id(ver.get("tool_id"),False).get("name")
        ToolVer= tool_name+"_"+ver.get("version_name")+"_"+ver.get("version_number")
        if ToolVer not in present_in_ver:
            present_in_ver.append(ToolVer)        
    err=""
    if len(present_in_du)>0: 
        err="The "+entity+" cannot be deleted as it is present in Du: " + (','.join(map(str, present_in_du)))
    if len(present_in_ver)>0:
        if len(err)>0: 
            err=err + " and present in Tools with Versions: " + (','.join(map(str, present_in_ver)))
        else:
            err="The "+entity+" cannot be deleted as it is present in Tools with Versions: " + (','.join(map(str, present_in_ver)))
    if len(err)>0:
        raise ValueError (err)

def genrate_random_key(key_length = 15):
    symbols='!@#$%&*'
    return ''.join(random.choice(string.letters + string.digits + symbols) for _ in range(15)) 
            