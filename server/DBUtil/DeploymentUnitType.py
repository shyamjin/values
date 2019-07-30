import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
from settings import mongodb


class DeploymentUnitType(DBUtil):
    '''
        General description:

       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for PermissionGroup.
    '''

    def __init__(self):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        db = mongodb
        DBUtil.__init__(self, db)
        self.collection = db.DeploymentUnitType

        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def GetDeploymentUnitType(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities of DeploymentUnitType
        Example :
             GetDeploymentUnitType(id)
        '''
        return self.collection.find()

    def GetDeploymentUnitTypeById(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            DeploymentUnitType stored in the database.
        Returns:
                Returns Database entities by id of DeploymentUnitType
        Example :
             GetDeploymentUnitType(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def GetDeploymentUnitTypeByName(self, name):
        '''
        General description:
        Args:
            param1 (name) : This is the unique name of the\
            DeploymentUnitType stored in the database.
        Returns:
                Returns Database entities of DeploymentUnitType by name
        Example :
             GetDeploymentUnitTypeByname(name)
        '''
        return (self.collection.find_one({"name": re.compile('^' + re.escape(name) + '$', re.IGNORECASE)}))

    def AddDeploymentUnitType(self, newDeploymentUnitType):
        '''
        General description:
        Args:
            param1 (newDeploymentUnitType) : This is the parameter which has the details of the\
           DeploymentUnitType to be added in the database.
        Returns:
                Returns the id of the newly created DeploymentUnitType from the database.
        Example :
             AddDeploymentUnitType(newDeploymentUnitType)
        '''
        # newDeploymentUnitType["status"]="1"
        result = self.collection.insert_one(newDeploymentUnitType)
        return str(result.inserted_id)

    def UpdateDeploymentUnitType(self, DUtype):
        '''
        General description:
        Args:
            param1 (DUtype) : This is the parameter which has the details of the\
            DeploymentUnitType to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the DeploymentUnitType.
        Example :
             UpdateDeploymentUnitType(DUtype)
        '''
        result = self.collection.update_one({"_id": ObjectId(DUtype["_id"]["oid"])}, {
                                            "$set": {"name": DUtype["name"]}})
        return result.modified_count

    def DeleteDeploymentUnitType(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            DeploymentUnitType stored in the database.
        Returns:
                Returns the count of the records deleted successfully\
                for the given id of the DeploymentUnitType
        Example :
             DeleteDeploymentUnitType(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count
