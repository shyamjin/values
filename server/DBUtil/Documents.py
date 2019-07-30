from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class Documents(DBUtil):
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
        self.collection = db.Documents
        # indexes
        self.collection.create_index(
            [('parent_entity_id', ASCENDING)], unique=True)

    def GetDocuments(self, parent_entity_id):
        '''
        General description:
        Args:
            param1 (parent_entity_id) : This is the unique id of the\
            Documents stored in the database.
        Returns:
                Returns Database entity by the parent_entity_id of the Documents
        Example :
             GetDocuments(parent_entity_id)
        '''
        return self.collection.find_one({"parent_entity_id": parent_entity_id})

    def GetAllDocuments(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities of all the existing Documents.
        Example :
             GetAllDocuments(id)
        '''
        return self.collection.find()

    def AddDocuments(self, documents):
        '''
        General description:
        Args:
            param1 (documents) : This is the parameter which has the details of the\
            documents to be added in the database.
        Returns:
                Returns the id of the newly created documents from the database.
        Example :
             AddDocuments(documents)
        '''
        result = self.collection.insert_one(documents)
        return str(result.inserted_id)

    def UpdateDocuments(self, documents):
        '''
        General description:
        Args:
            param1 (documents) : This is the parameter which has the details of the\
            documents to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the documents.
        Example :
             UpdateDocuments(documents)
        '''
        jsonnewEntry = {}
        for key in documents.keys():
            if key != "_id":
                jsonnewEntry[key] = documents[key]
        result = self.collection.update_one({"_id": ObjectId(documents["_id"]["oid"])}, {
                                            "$set": jsonnewEntry}, upsert=False)
        return result.modified_count

    def DeleteDocuments(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            Documents stored in the database.
        Returns:
                Returns the count of the records deleted successfully\
                for the given id of the Documents.
        Example :
             DeleteDocuments(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count
