import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
from settings import mongodb


class DeploymentUnitApprovalStatus(DBUtil):
    '''
        General description:

       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for DeploymentUnit.
    '''

    def __init__(self):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        db = mongodb
        DBUtil.__init__(self, db)
        self.collection = db.DeploymentUnitApprovalStatus

        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def GetAllDeploymentUnitApprovalStatus(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities of all the existing DeploymentUnitApprovalStatus.
        Example :
             GetAllDeploymentUnitApprovalStatus(id)
        '''
        return self.collection.find()

    def GetDeploymentUnitApprovalStatusById(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            DeploymentUnitApprovalStatus stored in the database.
        Returns:
                Returns Database entity by the id of the DeploymentUnitApprovalStatus
        Example :
             GetDeploymentUnitApprovalStatusById(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def GetDeploymentUnitApprovalStatusByName(self, name):
        '''
        General description:
        Args:
            param1 (name) : This is the name of the\
            DeploymentUnitApprovalStatus stored in the database.
        Returns:
                Returns Database entity by the id of the DeploymentUnitApprovalStatus
        Example :
             GetDeploymentUnitApprovalStatusByname(name)
        '''

        return (self.collection.find_one({"name": re.compile('^' + re.escape(name) + '$', re.IGNORECASE)}))

    def AddDeploymentUnitApprovalStatus(self, newDeploymentUnitApprovalStatus):
        '''
        General description:
        Args:
            param1 (DeploymentUnitApprovalStatus) : This is the parameter which has the details of the\
            DeploymentUnitApprovalStatus to be added in the database.
        Returns:
                Returns the id of the newly created DeploymentUnitApprovalStatus from the database.
        Example :
             AddDeploymentUnitApprovalStatus(AddDeploymentUnitApprovalStatus)
        '''
        result = self.collection.insert_one(newDeploymentUnitApprovalStatus)
        return result.inserted_id

    def UpdateDeploymentUnitApprovalStatus(self, DUApprovalStatus):
        '''
        General description:
        Args:
            param1 (ApprovalStatus) : This is the parameter which has the details of the\
            ApprovalStatus to be added in the database.

        Returns:
                Returns the id of the newly created ApprovalStatus from the database.
        Example :
             add_media_files(ApprovalStatus)
        '''

        result = self.collection.update_one({"_id": ObjectId(DUApprovalStatus["_id"]["oid"])}, {
                                            "$set": {"name": DUApprovalStatus["name"]}})
        return result.modified_count

    def DeleteDeploymentUnitApprovalStatus(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            DeploymentUnitApprovalStatus stored in the database.
        Returns:
                Returns the count of the records deleted successfully\
                for the given id of the DeploymentUnitApprovalStatus.
        Example :
             DeleteDeploymentUnitApprovalStatus(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count
    
    def delete_all(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Deletes the existing database entities of the Collection.
        Example :
             delete_all(id)
        '''
        self.collection.delete_many({})
