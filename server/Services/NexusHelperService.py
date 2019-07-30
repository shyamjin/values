'''
Created on Mar 28, 2018

@author: PDINDA
'''

import os,re,shutil
from os.path import join
import requests

def validate_file_exists(file_to_upload):
    if not os.path.isfile(file_to_upload):
        raise Exception("Invalid File : " + file_to_upload)
    
def validate_mandatory_fields(data_details={},file_to_upload=None):
    validate_file_exists(file_to_upload)
    if not data_details.get("repo") or not data_details.get("extension")\
     or not data_details.get("groupId") or not data_details.get("artifactId") \
     or not data_details.get("version") or not data_details.get("package") or not data_details.get("classifier"):
        raise ValueError("Required data to upload to nexus is missing: additional_info.repo_id" +
                         data_details.get("repo") + " package_type: " + data_details.get("extension")\
                          + " additional_info.package: " +
                         data_details.get("groupId") + " additional_info.artifact: "
                         + data_details.get("artifactId") + " additional_info.version: " +
                         data_details.get("version") + " package_type: " + data_details.get("package") +
                         " build_number: " + data_details.get("classifier"))
    
    
def validate_build_data_structure(build_details):
    keys_to_validate=["file_path","package_type","file_size",\
                          "type","additional_info","package_name"]
    keys_to_validate_in_additional_info=["repo_id","package","file_name","artifact",\
                                         "relative_path","version"]
    validate_keys_exists(build_details, "build", keys_to_validate)
    validate_keys_exists(build_details.get("additional_info"), "build additional_info", keys_to_validate_in_additional_info)
    if build_details.get("additional_artifacts"):
        validate_additional_artifacts(build_details.get("additional_artifacts"))
    validate_data(build_details)
    
def validate_keys_exists(obj, obj_name, keys):
    for key in keys:
        if not obj.get(key):
            raise Exception("mandatory key: " + key + " is missing in " + obj_name)

def get_additional_artifacts_keys(repo_provider):
    if repo_provider.lower() == "yum":
        return ["repo_id", "file_name", "package", "artifact", "version", "relative_path", "type"]
    elif repo_provider.lower() == "docker":
        return ["file_name"] 
    else:
        return []

def validate_additional_artifacts(additional_artifacts):
    validate_keys_exists(additional_artifacts, "additional_artifacts", ["repo_provider", "artifacts"])
    for artifact in additional_artifacts.get("artifacts"):
        validate_keys_exists(artifact, "additional_artifacts -> artifact", get_additional_artifacts_keys(additional_artifacts.get("repo_provider")))

def validate_data(build):
    repo=build.get("additional_info").get("repo_id")
    groupId=build.get("additional_info").get("package").replace(".","/")
    #artifactId= build.get("additional_info").get("artifact").replace(".","/")
    artifactId= build.get("additional_info").get("artifact")
    version=build.get("additional_info").get("version")
    package=build.get("package_type")
    file_path=build.get("file_path")
    relative_path=build.get("additional_info").get("relative_path")
    file_name=build.get("additional_info").get("file_name")
    package_name=build.get("package_name")
   
    if not relative_path.startswith(repo):
        raise Exception ("value of additional_info.relative_path should start with value of additional_info.repo_id")                    
    if not relative_path.startswith(repo+"/"+groupId):
        raise Exception ("value of additional_info.relative_path should start with value of additional_info-->repo_id+package")
    if not relative_path.startswith(repo+"/"+groupId+"/"+artifactId):
        raise Exception ("value of additional_info.relative_path should start with value of additional_info-->repo_id+package+artifact")
    if not relative_path in (repo+"/"+groupId+"/"+artifactId+"/"+version):
        raise Exception ("value of additional_info.relative_path should start with value of additional_info-->repo_id+package+artifact+version")
    if relative_path not in file_path:
        raise Exception ("value of additional_info.relative_path should be path of file_path")
    if relative_path+"/"+file_name not in file_path:
        raise Exception ("value of additional_info-->relative_path+file_name should be path of file_path")    
    if not package_name.endswith(package):
        raise Exception ("value of package_name should end with value of package_type")

def download_build(build,directory_to_export_to,create_inside_relative_path = True):
    fileName = build.get("additional_info").get("file_name")
    if create_inside_relative_path == True: # In Deployment we dont want the relative_path dir structure created . It will send False
        relative_path = build.get("additional_info").get("relative_path")
        full_file_path = join(directory_to_export_to, relative_path)
        full_file_path_with_name = join(full_file_path, fileName)
    else:
        full_file_path = join(directory_to_export_to)
        full_file_path_with_name = join(directory_to_export_to, fileName)
    if build.get("file_path"):
        print "download_build: Trying to download :" + build["file_path"]
        try:
            r = requests.get(build["file_path"], verify=False, stream=True)
            if r.status_code != 200:
                raise ValueError(
                    "Unable to download file from URL: " + build["file_path"] + ".Invalid URL ??")
            else:
                print build["file_path"] + " is a valid url !! "
            if not os.path.exists(full_file_path):
                os.makedirs(full_file_path)
            with open(full_file_path_with_name, 'wb') as f:
                total_length = int(r.headers.get('content-length'))
                if total_length is None: # no content length header
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                else:
                    dl = 0
                    printed = 0
                    total_length = int(total_length)
                    for data in r.iter_content(chunk_size=4096*2):
                        dl += len(data)
                        f.write(data)
                        done = int(50 * dl / total_length)
                        if  printed <> done:
                            printed = done
                            print fileName+" "+str(done*2)+"%" +" |%s%s|" % ("=" * done, ' ' * (50-done))+" "+str(dl)+"/"+str(total_length)      
            print "download_build:Completed downloading :" + build["file_path"]
        except Exception as e:
            raise Exception(
                "Build URL is valid.But failed to download or save file !!!: " + build["file_path"]+" with error: "+str(e.message))
    else:        
        raise Exception("Build does not have a file_path")
