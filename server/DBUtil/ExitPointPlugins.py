import re

from bson.objectid import ObjectId
from pymongo import ASCENDING
from werkzeug import secure_filename
from settings import mongodb,key
from Services import PasswordHelper

class ExitPointPlugins():
    '''
    General description :
    This class has definition for functions that provides add /update/ delete \
     search by entities in database for ExitPointPlugins.
    '''

    def __init__(self):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        db = mongodb
        self.collection = db.ExitPointPlugins
        self.passHelper = PasswordHelper.PasswordHelper(key)

        # indexes
        self.collection.create_index([('plugin_name', ASCENDING)], unique=True)
        # repo_provider is also unique,but is implemented on code level as deployment does not have repo_provider

    def encrypt_or_decrypt_keys(self,data,decrypt_ind=True):
        if data:
            keys_to_match = ["user","password"]
            for key in  data.keys():
                for match in keys_to_match:
                    if match in key:
                        if not decrypt_ind:
                            data[key]=self.passHelper.encrypt(data[key])
                        else:
                            data[key]=self.passHelper.decrypt(data[key])
                        break    
        return  data          
            

    def get_all(self,filters_to_apply={}):
        '''
          General description:
          Args:
             no Args
          Returns:
                  Returns Database entities existing in the ExitPointPlugins collection.
          Example :
          get_all()
        '''
        if filters_to_apply:
            return self.collection.find(filters_to_apply)
        return self.collection.find()


    def get_by_id(self, object_id):
        '''
          General description:
          Args:
              param1 (object_id) : This is the ExitPointPlugins Id which is stored in database
          Returns:
                  Returns Database entity of ExitPointPlugins for the given ExitPointPlugins Id
          Example :
              get_by_id(id)
        '''
        return self.encrypt_or_decrypt_keys(self.collection.find_one({"_id": ObjectId(object_id)}))

    def get_by_repo_provider(self, repo_provider):
        '''
         General description:
         Args:
             param1 repo_provider(String) : This is the repo_provider which is part of a ExitPointPlugins.
         Returns:
                 Returns Database entity of account for the given repo_provider.
         Example :
              get_by_repo_provider("Test")
        '''

        return self.encrypt_or_decrypt_keys(self.collection.find_one({"repo_provider": re.compile('^' + re.escape(repo_provider) + '$', re.IGNORECASE)}))
    
    def get_by_plugin_name(self, plugin_name):
        '''
         General description:
         Args:
             param1 plugin_name(String) : This is the repo_provider which is part of a ExitPointPlugins.
         Returns:
                 Returns Database entity of account for the given repo_provider.
         Example :
              get_by_plugin_name("Test")
        '''

        return self.encrypt_or_decrypt_keys(self.collection.find_one({"plugin_name": re.compile('^' + re.escape(plugin_name) + '$', re.IGNORECASE)}))

    def add(self, data):
        '''
          General description:
          Args:
              param1 add(String) : This is the parameter which has the details for \
              the add to be added in database.
          Returns:
                  Returns Database entity id of the newAccount created
          Example :
               add(data)
        '''
        self.perform_validation(data, True)
        self.encrypt_or_decrypt_keys(data,False)
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def perform_validation(self,data,is_new_record=True):
        if data.get("plugin_name"): 
            data["plugin_name"] = secure_filename(data.get("plugin_name"))
            if data.get("type"):
                data["type"]=data["type"].lower()
                if data.get("type") == "sync" and "SyncPlugin" not in data.get("plugin_name"):
                    raise Exception("Invalid file name.File should have name including SyncPlugin in it")
                elif data.get("type") == "deployment" and "DeploymentPlugin" not in data.get("plugin_name"):
                    raise Exception("Invalid file name.File should have name including DeploymentPlugin in it")
                elif data.get("type") == "repository" and "RepositoryPlugin" not in data.get("plugin_name"):
                    raise Exception("Invalid file name.File should have name including RepositoryPlugin in it")                        
        if  is_new_record:
            if self.get_by_repo_provider(data.get("repo_provider","")):
                raise Exception ("A record for the same provider already exists: "+data.get("repo_provider",""))
            if self.get_by_plugin_name(data.get("plugin_name","")):
                raise Exception ("A record for the same plugin_name already exists: "+data.get("plugin_name","") )
        else:
            existing_data=self.get_by_repo_provider(data.get("repo_provider",""))
            if existing_data:
                if str(existing_data.get("_id")) <> data["_id"]["oid"]:
                    raise Exception ("A record for the same provider already exists: "+data.get("repo_provider",""))
            existing_data=self.get_by_plugin_name(data.get("plugin_name",""))
            if existing_data:
                if str(existing_data.get("_id")) <> data["_id"]["oid"]:
                    raise Exception ("A record for the same plugin_name already exists: "+data.get("plugin_name",""))    
                
             
    def replace(self, data):
        '''
          General description:
          Args:
              param1 ( data) : This is the parameter which has the details for \
              the existing plugin to be updated in database.Its a JSON object.
          Returns:
                  Returns the count of records successfully updated .
          Example :
               replace( data):
        '''
        self.perform_validation(data, False)
        self.encrypt_or_decrypt_keys(data,False)
        jsonnewEntry = {}
        for key in data.keys():
            if key != "_id":
                jsonnewEntry[key] = data[key]
        result = self.collection.replace_one({"_id": ObjectId(data["_id"]["oid"])},jsonnewEntry)
        return result.modified_count

    def delete(self, object_id):
        '''
         General description:
         Args:
             param1 (object_id) : This is the unique id of \
             the existing plugin to be deleted from database.
         Returns:
                 Returns the count of records successfully deleted.
         Example :
              delete(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def delete_all(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Deletes the existing database entities of the PreRequisite.
        Example :
             delete_all(id)
        '''
        self.collection.delete_many({})
