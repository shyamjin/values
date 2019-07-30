from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class DeploymentFields(DBUtil):
    '''                                                                                   
     General description:                                                              

    This class has definition for functions that provides add /update/ delete \        
    / search by entities in database for MachineType.                                  
    '''

    def __init__(self, db):
        '''                                                                
         General description :                                           
         This function initializes the database variables and \          
         index to refer in functions.                                    
        '''
        DBUtil.__init__(self, db)
        self.collection = db.DeploymentFields
        # indexes
        self.collection.create_index(
            [('parent_entity_id', ASCENDING)], unique=True)

    def GetAllDeploymentFields(self):
        '''                                                                                 
         General description:                                                                
            Args:                                                                               
         no args                                                                             
             Returns:                                                                         
                 Returns the all database entities existing for DeploymentFields             

         Example :                                                                           
         GetAllDeploymentFields()                                                        
        '''

        return self.collection.find()

    def GetDeploymentFields(self, parent_entity_id):
        '''                                                                                                      
         General description:                                                                                     
         Args:                                                                                                    
             param1 (parent_entity_id) : This is the unique id of the DeploymentFields store in the database.          
         Returns:                                                                                                 
                 Returns Database entity by the id of the DeploymentFields                                        
         Example :                                                                                                
              GetDeploymentFields(id)                                                                             
        '''
        return self.collection.find_one({"parent_entity_id": parent_entity_id})

    def AddDeploymentFields(self, fields):
        '''                                                                                             
         General description:                                                                            
         Args:                                                                                           
             param1 (fields) : This is the parameter which has the details of the\                       
            fields to be added in the database.Its a JSON object.                                        
         Returns:                                                                                        
                 Returns the id of the newly created fields from the database.                           
         Example :                                                                                       
              AddDeploymentFields(fields)                                                                
        '''
        result = self.collection.insert_one(fields)
        return str(result.inserted_id)

    def UpdateDeploymentFields(self, fields):
        '''                                                                                  
         General description:                                                                 
         Args:                                                                                
             param1 (fields) : This is the parameter which has the details of the\            
             fields to be added in the database.Its a JSON object.                            
         Returns:                                                                             
                Returns the count of the records updated successfully \                       
                for the given fields of the DeploymentFields.                                 
         Example :                                                                            
              UpdateDeploymentFields(fields)                                                  
        '''
        jsonnewEntry = {}
        for key in fields.keys():
            if key != "_id":
                jsonnewEntry[key] = fields[key]
        result = self.collection.update_one({"_id": ObjectId(fields["_id"]["oid"])}, {
                                            "$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def DeleteDeploymentFields(self, object_id):
        '''                                                                        
          General description:                                                       
          Args:                                                                      
              param1 (object_id) : This is the unique id of the\                     
             DeploymentFields stored in the database.                                
          Returns:                                                                   
                  Returns the count of the records deleted successfully \            
                  for the given id of the DeploymentFields.                          
          Example :                                                                  
               DeleteDeploymentFields(id)                                            
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def delete_dep_field_by_parent_entity_id(self, peid):
        '''                                                                          
         General description:                                                         
         Args:                                                                        
             param1 (peid) : This is the ParentEntity id of the\                      
            DeploymentFields stored in the database.                                  
         Returns:                                                                     
                 Returns the count of the records deleted successfully \              
                 for the given id of the DeploymentFields.                            
         Example :                                                                    
              delete_dep_field_by_parent_entity_id(peid)                            
        '''
        result = self.collection.delete_many({"parent_entity_id": peid})
        return result.deleted_count
