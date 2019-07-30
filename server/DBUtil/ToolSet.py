'''
Created on Nov 2, 2016

@author: SJAJULA
'''
import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
import Tags
import Tool
import Versions


class ToolSet(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for ToolSet.
    '''

    def __init__(self, db):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.ToolSet
        self.toolDB = Tool.Tool(db)
        self.versionsDB = Versions.Versions(db)
        self.tagDB = Tags.Tags()
        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def get_all_tool_set(self, filter_required=None, skip=0, limit=0):
        '''
        General description:

        Args:
            param 1 : filter_required (JSON) : This is the JSON object which has conditions \
            that determines which tools to be considered from the Tools stored in the database.

            param 2 : skip (integer) : This is the count of the\
            Tools to be skipped.

            param 3 : limit (integer) : This is the count of the\
            Tools to be limited from the database .
        Returns:
                Returns the database entities existing for ToolSet based on status filter \
                skip count ,limit count and filer_required .
        Example :
            get_all_tool_set(filter_required,skip,limit)
        '''
        # default value of limit and skip is set in respective APIs
        # in DAO skip=0 , limit =0 means it will send all documents
        if filter_required:
            count = self.collection.find(filter_required).skip(
                skip).limit(limit).count()
            if count < 1:
                skip = 0
            tool_set_list = self.collection.find(
                filter_required).skip(skip).limit(limit)
        else:
            count = self.collection.find().skip(skip).limit(limit).count()
            if count < 1:
                skip = 0
            tool_set_list = self.collection.find().skip(skip).limit(limit)
        final_list = []
        if tool_set_list.count() > 0:
            for tool_set in tool_set_list:
                if tool_set.get("tag"):
                    tool_set["tag"] = self.tagDB.get_tag_names_from_given_ids_list(
                        tool_set["tag"])
                final_list.append(tool_set)
        return final_list

    def GetAllToolSetIds(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns list of all tool set ids.
        Example :
            get_tag_ids()
        '''
        toolsets = self.collection.find()
        toolset_ids_list = []
        for toolset in toolsets:
            toolset_ids_list.append(str(toolset["_id"]))
        return toolset_ids_list

    def get_tool_set(self, object_id):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            ToolSet stored in the database.
        Returns:
                Returns the database entity based on the ToolSet id.
        Example :
            get_tool_set(object_id)
        '''
        tool_set = self.collection.find_one({"_id": ObjectId(object_id)})
        if tool_set and tool_set.get("tag"):
            tool_set["tag"] = self.tagDB.get_tag_names_from_given_ids_list(
                tool_set["tag"])
        return tool_set

    def get_tool_set_by_condition(self, condition, condition_value):
        '''
        General description:

        Args:
            param1 : condition(string) : This is the unique id of the\
            ToolSet stored in the database. This determines the condition on which the\
            toolsets will be fetched from database.

            param 2:  condition_value(list) : This is the unique value of the\
            ToolSet stored in the database. This full fills the condition on which the\
            toolsets will be fetched from database. Its a kind of list.
        Returns:
                Returns the database entity based on the condition.
        Example :
            get_tool_set_by_condition(condition,condition_value)
        '''
        return self.collection.find({condition: {"$in": [str(condition_value)]}})

    def get_tool_set_by_group_name(self, text):
        '''
        General description:

        Args:
            param 1: text(string) :This is the parameter which \
            has the unique name of the existing ToolSet in the database.
        Returns:
                Returns the existing database entity based on the ToolSet name \
                from the ToolSet database.
        Example :
            get_tool_set_by_group_name(text)
        '''
        tool_set = self.collection.find_one(
            {"name": re.compile('^' + re.escape(text) + '$', re.IGNORECASE)})
        if tool_set and tool_set.get("tag"):
            tool_set["tag"] = self.tagDB.get_tag_names_from_given_ids_list(
                tool_set["tag"])
        return tool_set

    def add_new_tool_set(self, new_tool):
        '''
        General description:

        Args:
            param1 : new_tool(JSON) : This is the parameter which has details \
            for new ToolSet .
        Returns:
              Returns the id of the newly created ToolSet in the database.
        Example :
             add_new_tool_set(new_tool)
        '''
        result = self.collection.insert_one(new_tool)
        return str(result.inserted_id)

    def update_tool_set(self, tool):
        '''
        General description:

        Args:
            param1 : tool (JSON) : This is the parameter which has details of ToolSet.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_tool_set(tool)
        '''
        json_new_entry = {}
        for key in tool.keys():
            if key != "_id":
                json_new_entry[key] = tool[key]
        result = self.collection.update_one({"_id": ObjectId(tool["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_tool_set(self, object_id):
        '''
        General description:

        Args:
           param1 : object_id(object) : This is the unique id of the\
            tool stored in the database.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_tool_set(id)
        '''
        return self.collection.delete_one({"_id": ObjectId(object_id)}).deleted_count

    def add_tool_set_logo(self, short_path, thumbnail_path, object_id):
        '''
        General description:

        Args:
            param 1 : object_id(object) : This is the unique id of the\
            Tool stored in the database.

            param 2 : short_path(string) : This is the parameter which has details \
            for path where the logo file is present for a tool .

            param 3 : thumbnail_path(string) : This is the parameter which has details \
            for path where the thumbnail logo file is present for a tool
        Returns:
              Returns the count of the successful records updated.
        Example :
             add_tool_logo(id ,short_path,thumbnail_path )
        '''
        result = self.collection.update_one({"_id": ObjectId(object_id)},
                                            {"$set": {"logo": short_path,
                                                      "thumbnail_logo": thumbnail_path}})
        return result.modified_count
