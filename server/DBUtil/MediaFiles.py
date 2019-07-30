import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class MediaFiles(DBUtil):
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
        self.collection = db.MediaFiles
        # indexes
        self.collection.create_index(
            [('parent_entity_id', ASCENDING)], unique=True)

    def get_all_media_files(self):
        '''
        General description:
        Args:
            No arguments.
        Returns:
                Returns Database entities of all the existing MediaFiles.
        Example :
             get_all_media_files(id)
        '''
        return self.collection.find()

    def get_media_file_by_id(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            MediaFiles stored in the database.
        Returns:
                Returns Database entity by the id of the MediaFiles.
        Example :
             get_media_file_by_id(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def get_media_files(self, parent_entity_id):
        '''
        General description:
        Args:
            param1 (parent_entity_id) : This is the unique id of the \
            tool version or deployment unit stored in the database.
        Returns:
                Returns Database entity by the parent_entity_id of the MediaFiles.
        Example :
             get_media_files(parent_entity_id)
        '''
        return self.collection.find_one({"parent_entity_id": parent_entity_id})

    def add_media_files(self, media_files):
        '''
        General description:
        Args:
            param1 (media_files) : This is the parameter which has the details of the\
            MediaFiles to be added in the database.
        Returns:
                Returns the id of the newly created MediaFile from the database.
        Example :
             add_media_files(media_files)
        '''
        result = self.collection.insert_one(media_files)
        return str(result.inserted_id)

    def delete_media_file(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            MediaFiles stored in the database.
        Returns:
                Returns the count of the records deleted successfully\
                for the given id of the MediaFile.
        Example :
             delete_media_file(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def update_media_files(self, media_files):
        '''
        General description:
        Args:
            param1 (media_files) : This is the parameter which has the details of the\
            MediaFiles to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the MediaFile.
        Example :
             update_media_files(media_files)
        '''
        json_new_entry = {}
        for key in media_files.keys():
            if key != "_id":
                json_new_entry[key] = media_files[key]
        result = self.collection.update_one({"_id": ObjectId(media_files["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def is_file_present(self, file_name):
        '''
        General description:
        Args:
            param1 (file_name) : This is the unique filename of the \
            existing MediaFiles stored in the database.
        Returns:
                Returns true or false depending whether the file exists or not.
        Example :
             is_file_present(file_name)
        '''
        if self.collection.find_one({"$or": [{"media_files.url": re.compile(file_name, re.IGNORECASE)},
                                             {"media_files.thumbnail_url": re.compile(file_name, re.IGNORECASE)}]}):
            return True
        else:
            return False
