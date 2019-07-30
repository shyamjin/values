from DBUtil import DBUtil
from Services import PasswordHelper
from settings import key


class Counter(DBUtil):
    '''                                                                                           
    General description :                                                                      
    This class has definition for functions that provides add /update/ delete \                
    / search by entities in database for Counter.                                              
    '''

    def __init__(self, db):
        '''                                                                 
         General description:                                                
         This function initializes the database variables and \              
         index to refer in functions.                                        
        '''

        DBUtil.__init__(self, db)
        self.collection = db.Counter
        self.passHelper = PasswordHelper.PasswordHelper(key)
        # indexes
        # self.collection.create_index([('count_no', ASCENDING)], unique=True,)

    def UpdateCounter(self, counterData):
        '''                                                                                       
         General description:                                                                      
         Args:                                                                                     
             param1 (counterData) : This is the parameter which has the details of the\            
             Counter to be updated in the database.                                                
         Returns:                                                                                  
                  Returns the count of the records updated successfully \                          
                  for the given id of the Counter.                                                 
         Example :                                                                                 
          UpdateCounter(counterData)                                                           
        '''
        result = self.collection.update_one({'_id': counterData["_id"]}, {
                                            "$set": {"count_no": counterData["count_no"]}})
        return result

    def AddCounter(self, record):
        '''                                                                               
         General description:                                                              
         Args:                                                                             
             param1 (record) : This is the parameter which has the details of the\         
             record to be added in the database.                                           
         Returns:                                                                          
                 Returns the id of the newly created Counter from the database.            
         Example :                                                                         
              AddCounter(record)                                                           
        '''
        result = self.collection.insert_one(record)
        return(result.inserted_id)

    def get_counter(self):
        '''                                                             
         General description:                                            
         Args:                                                           
             No arguments.                                               
         Returns:                                                        
                 Returns Database entities of  the existing counter.     
         Example :                                                       
              get_counter(id)                                    
        '''
        result = self.collection.find_one()
        if result is None:
            self.AddCounter({"count_no": "1"})
            return str(1)
        result["count_no"] = str(int(result["count_no"]) + 1)
        self.UpdateCounter(result)
        return str(result["count_no"])
