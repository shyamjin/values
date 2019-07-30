from datetime import datetime
import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class DistributionSync(DBUtil):
    '''
        General description:

       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for PermissionGroup.
    '''

    def __init__(self, db):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.DistributionSync
        # indexes
        # self.collection.create_index([('_id', ASCENDING)], unique=True,)

    def GetDistributeRequestAll(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities of all the existing DistributionSync.
        Example :
             GetDistributeRequestAll(id)
        '''
        return self.collection.find()

    def GetDistributeRequest(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            DistributionSync. stored in the database.
        Returns:
                Returns Database entity by the id of the DistributionSync..
        Example :
             GetDistributeRequest(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def getDistributionByImpOperation(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities ByImpOperation like operation,status,compared of the existing DistributionSync.
        Example :
             getDistributionByImpOperation(id)
        '''
        return (list(self.collection.find({"operation": "insert", "status": "compared"}, {'_id': 1, 'tool_data': 1, 'master_clone_request_id': 1})))

    def getDistributionByUpdOperation(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities ByUpdOperation like operation,status,compared of the existing DistributionSync.
        Example :
             getDistributionByImpOperation(id)
        '''
        return (list(self.collection.find({"operation": "update", "status": "compared"}, {'_id': 1, 'tool_data': 1, 'master_clone_request_id': 1})))

    def getDistributionIdByOperation(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            DistributionSync. stored in the database.
        Returns:
                Returns Database entity by Operation like insert, update of the DistributionSync..
        Example :
             getDistributionIdByOperation(id)
        '''
        return (self.collection.find_one({"operation": {"$in": ["insert", "update"]}, "status": "compared", "_id": ObjectId(object_id)}))

    def AddDistribution(self, per):
        '''
        General description:
        Args:
            param1 (per) : This is the parameter which has the details of the\
            Distribution to be added in the database.
        Returns:
                Returns the id of the newly created Distribution from the database.
        Example :
             AddDistribution( per)
        '''
        if per.get("status") is None:
            per["status"] = "new"
        per["updated_time"] = datetime.now()
        per["created_time"] = datetime.now()
        result = self.collection.insert_one(per)
        return(result.inserted_id)

    def GetNewDistribution(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns New Database entities of Distribution.
        Example :
             GetNewDistribution(id)
        '''
        return self.collection.find({"status": re.compile("new", re.IGNORECASE)}).sort([("process_order", ASCENDING)])


#     def GetHandledDistribution(self):
#         return self.collection.find({ "status" :{ "$in": [re.compile("cancelled", re.IGNORECASE)]}});
#

    def GetComparedDistribution(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Compared Database entities of Distribution.
        Example :
             GetComparedDistribution(id)
        '''
        return self.collection.find({"status": re.compile("compared", re.IGNORECASE)}).sort([("created_time", ASCENDING), ("_id", ASCENDING)])

    def GetComparedAndSuccessDistribution(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Compared And Success Database entities of Distribution.
        Example :
             GetComparedAndSuccessDistribution(id)
        '''
        return self.collection.find({"status": {"$in": [re.compile("compared", re.IGNORECASE), re.compile("success", re.IGNORECASE), re.compile("failed", re.IGNORECASE)]}}).sort([("created_time", ASCENDING), ("_id", ASCENDING)])

    def CancelAllDistributions(self):
        '''
        General description:
        Args:
           No arguments.
        Returns:
                Returns the count of the records deleted successfully\
                for the given id of the Distributions
        Example :
             CancelAllDistributions(id)
        '''
        result = self.collection.update(
            {}, {"$set": {"status": "cancelled"}}, multi=True)

    def UpdateDistribution(self, configData):
        '''
        General description:
        Args:
            param1 (configData) : This is the parameter which has the details of the\
            Distribution to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the Distribution
        Example :
             updateDistribution(configData)
        '''
        jsonnewEntry = {}
        for key in configData.keys():
            if key != "_id":
                jsonnewEntry[key] = configData[key]
        result = self.collection.update_one({"_id": ObjectId(configData["_id"]["oid"])}, {
                                            "$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def UpdateDistributionStatus(self, object_id, status, message):
        '''
        General description:
        Args:
         param1 (object_id) : This is the unique id of the\
            DistributionSync stored in the database.
            param2 :  status(string) :This is the parameter which determines \
             status of Distribution.
            This has two values - True /False .
            param3 :  message(string) :This is the parameter which give the status message.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the Distribution.
        Example :
             UpdateDistributionStatus(object_id, status, message)
        '''
        jsonEntry = {}
        jsonEntry["status"] = status
        jsonEntry["status_message"] = message
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": jsonEntry}, upsert=False)
        return result

    def DeleteDistribution(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            Distribution stored in the database.
        Returns:
                Returns the count of the records deleted successfully\
                for the given id of the Distribution.
        Example :
             DeleteDistribution(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def get_distribution_by_filter(self, filter):
        '''
        General description:
        Args:
            param1; filter (object) : This is the filter that we want to search with
        Returns:
                Returns the database entity based on the filter
        Example :
            get_distribution_by_filter(filter)
        '''
        return self.collection.find(filter)
