'''
Created on Mar 21, 2016

@author: PDINDA
'''

from datetime import datetime

from bson.objectid import ObjectId

from DBUtil import DBUtil
from Services import PasswordHelper
from settings import key
from pymongo import ASCENDING


class Config(DBUtil):
    '''
    General description:

       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for Config.
    '''

    def __init__(self, db):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.Config
        self.passHelper = PasswordHelper.PasswordHelper(key)

        # indexes
        # self.collection.create_index([('_id', ASCENDING)], unique=True,)


# 525 Change
    def get_config_by_id(self, id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Config stored in the database.
        Returns:
                Returns Database entity by the id of the Config.
        Example :
             get_config_by_id(id)
        '''
        result = (self.collection.find_one({"_id": ObjectId(id)}))
        if not result:
            return result
        else:
            return self.decrypt(result)

# 525 Change
    def getConfigByConfigId(self, id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Config stored in the database.
        Returns:
                Returns Database entity by the id of the Config.
        Example :
             getConfigByConfigId(id)
        '''

        result = self.collection.find_one({"configid": int(id)})
        if not result:
            return result
        else:
            return self.decrypt(result)
# 525 Change

    def getConfigByName(self, name):
        '''
        General description:
        Args:
            param1 (name) : This is the name of the\
            Config stored in the database.
        Returns:
                Returns Database entity by the name of the Config.
        Example :
             getConfigByConfigname(name)
        '''
        result = self.collection.find_one({"name": name})
        if not result:
            return result
        return self.decrypt(result)


# 525 Change

    def GetAllConfig(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities of all the existing Config.
        Example :
             GetAllConfig(id)
        '''
        result = self.collection.find().sort([("name", ASCENDING)])
        if not result:
            return result
        else:
            list = []
            for rec in result:
                list.append(self.decrypt(rec))
            return list

# 525 Change
    def AddConfig(self, per):
        '''
        General description:
        Args:
            param1 (per) : This is the parameter which has the details of the\
            Config to be added in the database.
        Returns:
                Returns the id of the newly created Config from the database.
        Example :
             AddConfig(per)
        '''
        per = self.encrypt(per)
        result = self.collection.insert_one(per)
        return(result.inserted_id)
    # 525 Start

    def encrypt(self, configData):
        '''
        General description:
        Args:
            param1 config_details(JSON) : This is the JSON object which has details like \
            password  .
        Returns:
                Returns Database entity by the configData \
                of the config.

        '''
        for key in configData.keys():
            if "pass" in str(key).lower():
                configData[key] = self.passHelper.encrypt(configData.get(key))
        return configData

    def decrypt(self, configData):
        '''
        General description:
        Args:
            param1 : config_details(JSON) : This is the parameter which has details like \
            password /key .
        Returns:
                Returns Database entity by the configData \
                of the config.
        '''
        for key in configData.keys():
            if "pass" in str(key).lower():
                configData[key] = self.passHelper.decrypt(configData.get(key))
        return configData

    # 525 End
    def UpdateConfig(self, configData):
        '''
        General description:
        Args:
            param1 (configData) : This is the parameter which has the details of the\
            configData to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the config.
        Example :
             UpdateConfig(configData)
        '''
        jsonnewEntry = {}
        for key in configData.keys():
            if key != "_id":
                jsonnewEntry[key] = configData[key]
        # 525
        jsonnewEntry = self.encrypt(jsonnewEntry)
        result = self.collection.update_one({"_id": ObjectId(configData["_id"]["oid"])}, {
                                            "$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def UpdateStartTime(self, config_id, status, run_message=""):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            Config stored in the database.
            param2 (status) : This is the parameter which has the details of the\
            run_status to be updated in the database.
            param3(run_message):This is the parameter which has the details of the\
            run_message to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the config.
        Example :
             UpdateStartTime(config_id, status, run_message="")
        '''
        jsonnewEntry = {}
        jsonnewEntry["start_time"] = datetime.now()
        jsonnewEntry["end_time"] = ""
        jsonnewEntry["run_status"] = status
        jsonnewEntry["run_message"] = run_message
        result = self.getConfigByConfigId(config_id)
        jsonnewEntry["_id"] = {"oid": str(result["_id"])}
        return self.UpdateConfig(jsonnewEntry)

    def UpdateEndTime(self, config_id, status, run_message=""):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            Config stored in the database.
            param2 (status) : This is the parameter which has the details of the\
            run_status to be updated in the database.
            param3(run_message):This is the parameter which has the details of the\
            run_message to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the config.
        Example :
             UpdateEndTime(config_id, status, run_message="")
        '''
        jsonnewEntry = {}
        jsonnewEntry["end_time"] = datetime.now()
        jsonnewEntry["run_status"] = status
        jsonnewEntry["run_message"] = run_message
        result = self.getConfigByConfigId(config_id)
        jsonnewEntry["_id"] = {"oid": str(result["_id"])}
        return self.UpdateConfig(jsonnewEntry)

    def DeleteConfig(self, id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            Config stored in the database.
        Returns:
                Returns the count of the records deleted successfully\
                for the given id of the Config.
        Example :
             DeleteConfig(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count
