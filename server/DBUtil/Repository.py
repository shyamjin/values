from bson.objectid import ObjectId
from pymongo import ASCENDING
import re
from Services import PasswordHelper
from DBUtil import DBUtil
from settings import mongodb,key



class Repository(DBUtil):
    '''
    General description :
    This class has definition for functions that provides add /update/ delete \
     search by entities in database for Repository.
    '''

    def __init__(self):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        db = mongodb
        DBUtil.__init__(self, db)
        self.collection = db.Repository
        self.passHelper = PasswordHelper.PasswordHelper(key)
        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def encrypt(self, repository):
        '''
        General description:
        Args:
            param1 repository(JSON) : This is the JSON object which has details like \
            password  .
        Returns:
                Returns Database entity by the Repository \
                of the Repository.

        '''
        if repository:
            for key in repository.keys():
                if "pass" in str(key).lower():
                    repository[key] = self.passHelper.encrypt(repository.get(key))
        return repository

    def decrypt(self, repository):
        '''
        General description:
        Args:
            param1 : repository(JSON) : This is the parameter which has details like \
            password /key .
        Returns:
                Returns Database entity by the repository \
                of the repository.
        '''
        if repository:
            for key in repository.keys():
                if "pass" in str(key).lower():
                    repository[key] = self.passHelper.decrypt(repository.get(key))
        return repository

    def get_all(self,filter={}):
        '''
          General description:
          Args:
             no Args
          Returns:
                  Returns Database entities existing in the Repository collection.
          Example :
          get_all()
        '''
        repository = self.collection.find(filter).sort([['name', ASCENDING]])
        repository_list = []
        for rec in repository:
            repository_list.append(self.decrypt(rec))
        return repository_list

    def add(self, repository): 
        '''
          General description:
          Args:
              param1 repository(String) : This is the parameter which has the details for \
              the data to be added in database.
          Returns:
                  Returns Database entity id of the data created
          Example :
               add()
        '''
        result = self.collection.insert_one(self.encrypt(repository))
        return(result.inserted_id)
    
    
    def delete(self, object_id):
        '''
        General description:

        Args:
           param1 : object_id(object) : This is the unique id of the\
            state stored in the database.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete(id)
        '''
        return self.collection.delete_one({"_id": ObjectId(str(object_id))}).deleted_count
        
    def replace(self, repository):
        '''
          General description:
          Args:
              param1 repository(String) : This is the parameter which has the details for \
              the data to be added in database.              
          Returns:
                  Returns update count
          Example :
               replace(repository)
        '''
        object_id=repository.get("_id").get("oid")
        repository.pop("_id")
        repository = self.encrypt(repository)
        result = self.collection.replace_one(
            {"_id": ObjectId(str(object_id))}, repository, upsert=True)
        return str(result.modified_count)
    
    def get_repository_by_id(self, object_id,isAllDetails=False):
        repository = self.collection.find_one({"_id": ObjectId(str(object_id))})
        repository = self.decrypt(repository)
        return repository 
    
    def get_repository_by_name(self, name, isAllDetails=False):
        '''
        General description:

        Args:
             param1 (name) : This is the name of the\
            Repository stored in the database.

            param2: is_all_details(string) :This is the parameter which determines \
            whether all Repository should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the Repository and\
                is_all_details parameter.
        Example :
            get_repository_by_name(name,True)
        '''
        repository = (self.collection.find_one(
            {"name": re.compile('^' + re.escape(name) + '$', re.IGNORECASE)}))
        repository = self.decrypt(repository)
        return repository
    
