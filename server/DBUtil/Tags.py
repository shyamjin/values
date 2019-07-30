import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
from settings import mongodb
from wrapt.decorators import synchronized


class Tags(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for Tags.
    '''

    def __init__(self):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        db = mongodb
        DBUtil.__init__(self, db)
        self.collection = db.Tags

        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def get_tags(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns the database entities existing for Tags.
        Example :
            get_tags()
        '''
        return self.collection.find().sort([("name",ASCENDING)])

    def get_tag_by_id(self, object_id):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            Tags stored in the database.
        Returns:
                Returns the database entity based on the Tags id.
        Example :
            get_tag_by_id(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def get_tag_by_name(self, name):
        '''
        General description:

        Args:
            param1 : name(string) : This is the unique name of the\
            Tags stored in the database.
        Returns:
                Returns the database entity based on the Tags name.
        Example :
            get_tag_by_name(name)
        '''
        return (self.collection.find_one({"name": re.compile('^' + re.escape(name) + '$', re.IGNORECASE)}))

    def get_tag_names_from_given_ids_list(self, tags_list):
        '''
        General description:

        Args:
            param1 : tags_list(list) : This is the list of tags \
            stored in the database.
        Returns:
                Returns the database entity as tags lists based on the Tags Id.
        Example :
            get_tag_names_from_given_ids_list(tags_list)
        '''
        if type(tags_list) is not list:
            raise ValueError("Tag is expected to be of type list but got type as:"
                + str(type(tags_list)))
        tag_name_list = []
        result = {}
        for tag in tags_list:
            if str(tag).lower() == "all":
                result["name"] = "all"
            else:
                result = self.get_tag_by_id(str(tag))
            if result:
                if str(result["name"]) not in tag_name_list:
                    tag_name_list.append(str(result["name"]))
        return tag_name_list

    def get_tag_ids_from_given_ids_list(self, tags_list):
        '''
        General description:

        Args:
            param1 : tags_list(list) : This is the list of tags \
            stored in the database.
        Returns:
                Returns the database entity as tags lists based on the Tags name.
        Example :
            get_tag_ids_from_given_ids_list(tags_list)
        '''
        tag_ids_list = []
        if type(tags_list) is list:
            for tag in tags_list:
                result = self.get_tag_by_name(tag)
                if result:
                    if str(result["_id"]) not in tag_ids_list:
                        tag_ids_list.append(str(result["_id"]))
                else:
                    new_tag = str(self.auto_add_new_tag(tag))
                    if new_tag not in tag_ids_list:
                        tag_ids_list.append(new_tag)
            return tag_ids_list
        else:
            raise ValueError(
                "Tag is expected to be of type list but got type as:"
                + str(type(tags_list)))
    
    @synchronized
    def auto_add_new_tag(self,tag):
        result = self.get_tag_by_name(tag)
        if result:
            return str(result["_id"])
        else:
            data = {}
            data["name"] = tag
            new_tag = str(self.add_tag(data))
            return str(new_tag)

    def GetAllTagIds(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns list of all tag ids.
        Example :
            get_tag_ids()
        '''
        tags = self.collection.find().sort([("name",ASCENDING)])
        tag_ids_list = []
        for tag in tags:
            tag_ids_list.append(str(tag["_id"]))
        return tag_ids_list

    def add_tag(self, new_tag):
        '''
        General description:

        Args:
            param1 : new_tag(JSON) : This is the parameter which has details \
            for new Tag .
        Returns:
              Returns the id of the newly created tag the database.
        Example :
             add_tag(new_tag)
        '''
        result = self.collection.insert_one(new_tag)
        return str(result.inserted_id)

    def update_tag(self, tag):
        '''
        General description:

        Args:
            param1 : tag(JSON) : This is the parameter which has details of tag.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_tag(tag)
        '''
        result = self.collection.update_one({"_id": ObjectId(tag["_id"]["oid"])},
                                            {"$set": {"name": tag["name"]}})
        return result.modified_count

    def delete_tag(self, object_id):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            Tag stored in the database.
        Returns:
                Returns the count of the records deleted successfully \
                for the given Tag id .
        Example :
             delete_tag(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count
