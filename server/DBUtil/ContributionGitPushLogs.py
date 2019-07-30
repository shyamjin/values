from datetime import datetime

from bson.objectid import ObjectId

from DBUtil import DBUtil


class ContributionGitPushLogs(DBUtil):
    '''                                                                                
    General description :                                                           
    This class has definition for functions that provides add /update/ delete \     
    / search by entities in database for ContributionGitPushLogs.                   
    '''

    def __init__(self, db):
        '''                                                            
          General description:                                           
          This function initializes the database variables and           
          index to refer in functions.                                   
        '''
        DBUtil.__init__(self, db)
        self.collection = db.ContributionGitPushLogs
        # indexes
        # self.collection.create_index([('catalog_name', ASCENDING)])

    def ContributionGitPushLogsAll(self):
        '''                                                  
         General description:                                 
         Args:                                                
            No Arguments.                                     
         Returns:                                             
                 Returns all existing Database entities \     
                 of the ContributionGitPushLogs.              
         Example :                                            
              ContributionGitPushLogsAll()                    
        '''
        return self.collection.find()

    def GetContributionGitPushLogs(self, object_id):
        '''                                                                                                           
         General description:                                                                                          
         Args:                                                                                                         
             param1 (object_id) : This is the unique id of the ContributionGitPushLogs store in the database.          
         Returns:                                                                                                      
                 Returns Database entity by the id of the ContributionGitPushLogs                                      
         Example :                                                                                                     
              GetContributionGitPushLogs(id)                                                                           
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def AddContributionGitPushLogs(self, per):
        '''                                                                                                  
         General description:                                                                                 
         Args:                                                                                                
             param1 (per) : This is the parameter which has the details for \                                 
             the new ContributionGitPushLogs to be added in database.                                         
         Returns:                                                                                             
                 Returns Database entity id of the new ContributionGitPushLogs created                        
         Example :                                                                                            
              AddContributionGitPushLogs(per)                                                                 
        '''
        per["created_time"] = datetime.now()
        result = self.collection.insert_one(per)
        return(result.inserted_id)

    def UpdateContributionGitPushLogs(self, configData):
        '''                                                                                                   
         General description:                                                                                  
         Args:                                                                                                 
             param1 (configData) : This is the parameter which has the details for \                           
             the existing ContributionGitPushLogs to be updated in database.Its a JSON object.                 
         Returns:                                                                                              
                 Returns the count of records successfully updated .                                           
         Example :                                                                                             
              UpdateContributionGitPushLogs(configData)                                                        
        '''
        jsonnewEntry = {}
        for key in configData.keys():
            if key != "_id":
                jsonnewEntry[key] = configData[key]
        result = self.collection.update_one({"_id": ObjectId(configData["_id"]["oid"])}, {
                                            "$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def DeleteContributionGitPushLogs(self, object_id):
        '''                                                                                          
         General description:                                                                         
         Args:                                                                                        
             param1 (object_id) : This is the unique id of \                                          
             the existing machine type to be deleted from database.                                   
         Returns:                                                                                     
                 Returns the count of records successfully deleted.                                   
         Example :                                                                                    
             DeleteContributionGitPushLogs(id)                                                        
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count
