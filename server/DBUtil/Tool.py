from datetime import datetime
import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
import Tags
import Versions


# Tool statuses Mapping
# status           value
# active           1
# in development   2
# deprecated       3
# deleted          0
class Tool(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for Tool.
    '''

    def __init__(self, db):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.Tool
        self.versionsDB = Versions.Versions(db)
        self.tagDB = Tags.Tags()
        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)
        self.collection.create_index([('tag', ASCENDING)], unique=False)

    def get_tools_all(self, stat_filter=None, filter_required=None, skip=0, limit=0):
        '''
        General description:

        Args:
            param 1 : stat_filter (string) : This is the status of the\
            Tools stored in the database.It can be (active / indevelopment / deprecated
            deleted )

            param 2 : filter_required (JSON) : This is the JSON object which has conditions \
            that determines which tools to be considered from the Tools stored in the database.

            param 3 : skip (integer) : This is the count of the\
            Tools to be skipped.

            param 4 : limit (integer) : This is the count of the\
            Tools to be limited from the database .
        Returns:
                Returns the database entities existing for Tool based on status filter \
                skip count ,limit count and filer_required .
        Example :
            get_tools_all(stat_filter ,filter_required,skip,limit)
        '''
        # default value of limit and skip is set in respective APIs
        # in DAO skip=0 , limit =0 means it will send all documents
        condition_to_filter = {}
        if stat_filter:
            mapping = [('active', '1'), ('indevelopment', '2'),
                       ('deprecated', '3'), ('deleted', '0')]
            for k, v in mapping:
                stat_filter = [w.replace(k, v) for w in stat_filter]
            condition_to_filter = {"status": {"$in": stat_filter}}
        if filter_required:
            condition_to_filter.update(filter_required)
        if len(condition_to_filter.keys()) > 0:
            count = self.collection.find(condition_to_filter).skip(
                skip).limit(limit).count()
            if count < 1:
                skip = 0
            return self.collection.find(condition_to_filter).skip(skip).limit(limit)
        else:
            count = self.collection.find().skip(skip).limit(limit).count()
            if count < 1:
                skip = 0
            return self.collection.find().skip(skip).limit(limit)

    def is_file_present(self, file_name):
        '''
        General description:

        Args:
            param 1 : file_name (string) : This is the unique name of the logo file\
            for the Tool stored in the database.
        Returns:
                Returns true or false depending on if the logo file exists for the tool\
                in the tools database.
        Example :
            is_file_present(file_name)
        '''
        if self.collection.find_one({"$or": [{"logo": re.compile(file_name, re.IGNORECASE)},
                                             {"thumbnail_logo": re.compile(file_name, re.IGNORECASE)}]}):
            return True
        else:
            return False

    def get_tool_by_id(self, object_id, is_all_details):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            Tool stored in the database.

            param2 : get_all_details(string) :This is the parameter which determines \
            whether all Tool details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the Tool id and\
                is_all_details parameter.
        Example :
            get_tool_by_id(id ,True)
        '''
        tool = self.collection.find_one({"_id": ObjectId(str(object_id))})
        if is_all_details == True and tool is not None:
            tool = self.get_tool_details(tool, None, True)

        if tool and tool.get("tag"):
            tool["tag"] = self.tagDB.get_tag_names_from_given_ids_list(
                tool["tag"])
        return tool

    def GetAllToolIds(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns list of all tool ids.
        Example :
            get_tag_ids()
        '''
        tools = self.collection.find()
        tool_ids_list = []
        for tool in tools:
            tool_ids_list.append(str(tool["_id"]))
        return tool_ids_list

    def get_tool_by_name(self, text, is_all_details=False):
        '''
        General description:

        Args:
            param 1: text(string) :This is the parameter which \
            has the unique name of the existing Tool in the database.

            param2 : get_all_details(string) :This is the parameter which determines \
            whether all Tool details should be visible to user or not.\
            This has two values - True /False .
            Returns:
                Returns the existing database entity based on the Tool name \
                from the Tool database.
        Example :
            get_tool_by_name(text,True)
        '''
        tool = self.collection.find_one(
            {"name": re.compile('^' + re.escape(text) + '$', re.IGNORECASE)})
        if is_all_details == True and tool is not None:
            tool = self.get_tool_details(tool, None, True)
        if tool and tool.get("tag"):
            tool["tag"] = self.tagDB.get_tag_names_from_given_ids_list(
                tool["tag"])
        return tool

    def get_tool_by_tag(self, tag):
        '''
        General description:

        Args:
            param 1: tag(string) :This is the parameter which \
            has the unique tag names for the existing Tool in the database.
            Returns:
                Returns the existing database entity based on the Tool Tags \
                from the Tool database.
        Example :
            get_tool_by_tag(tag)
        '''
        tag_name = self.tagDB.get_tag_by_name(tag)
        tools=[]
        if tag_name:
            tools = self.collection.find({"tag": re.compile(
                '^' + re.escape(str(tag_name["_id"])) + '$', re.IGNORECASE)})
        return tools

    def get_tool_by_version(self, version_id, is_all_details):
        '''
        General description:

        Args:
            param1 : version_id(object) : This is the unique id of the\
            Tool version stored in the versions database.

            param2 : get_all_details(string) :This is the parameter which determines \
            whether all Tool details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the Tool version id and\
                is_all_details parameter.
        Example :
            get_tool_by_version(version_id ,True)
        '''
        version = self.versionsDB.get_version(version_id, False)
        if version:
            return self.get_tool_by_id(version["tool_id"], is_all_details)
        return None

    def add_tool(self, new_tool):
        '''
        General description:

        Args:
            param1 : new_tool(JSON) : This is the parameter which has details \
            for new Tool .
        Returns:
              Returns the id of the newly created Tool in the database.
        Example :
             add_tool(new_tool)
        '''
        result = self.collection.insert_one(new_tool)

        return str(result.inserted_id)

    def update_tool(self, tool):
        '''
        General description:

        Args:
            param1 : tool (JSON) : This is the parameter which has details of Tool.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_tool(tool)
        '''
        json_new_entry = {}
        for key in tool.keys():
            if key != "_id":
                json_new_entry[key] = tool[key]
        result = self.collection.update_one({"_id": ObjectId(tool["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_tool(self, object_id):
        '''
        General description:

        Args:
           param1 : object_id(object) : This is the unique id of the\
            tool stored in the database.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_tool(id)
        '''
        return self.collection.delete_one({"_id": ObjectId(object_id)}).deleted_count

    def delete_tool_logo_url(self, data):
        '''
        General description:

        Args:
           param1 : data (JSON) : This is the parameter which has details of\
           Tool in JSON object.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_tool_logo_url(data)
        '''
        self.collection.update({}, {"$unset": {data: 1}})

    def add_tool_logo(self, short_path, thumbnail_path, object_id):
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

    def get_tool_details(self, tool, version_id, is_last_version):
        '''
        General description:

        Args:
            param 1 : tool(JSON) : This is the parameter which has details \
            for Tool .

            param 2 : version_id(object) : This is the unique id of the\
            Tool version stored in the versions database.

            param 3 : is_last_version(string) :This is the parameter which determines \
            whether the version of the Tool is the last version or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the tool details ,Tool version id and\
                is_last_version parameters.
        Example :
            get_tool_details(tool ,version_id ,True)
        '''
        if tool == None or tool == '':
            return tool
        tool_id = str(tool["_id"])
        version = ''
        if is_last_version == True:
            version = self.versionsDB.get_last_active_version_by_tool_id(
                tool_id, True)
        else:
            version = self.versionsDB.get_version(version_id, True)
        if version == '' or version == None:
            raise ValueError("No version is found for the tool")
        tool["version"] = version
        return tool

    def get_tool_details_to_sync(self):
        '''
        General description:

        Args:
            param 1 : requested_by(string) :This is the parameter which determines \
            who has requested for sync services.
        Returns:
                Returns the database entity based on the sync request details for the Tool\
                from requested_by parameters.
        Example :
            get_tool_details_to_sync(requested_by)
        '''
        tool_versions = []
        tool_version_with_no_active_version = []
        tools = self.get_tools_all(['active'])
        if tools is None:
            return None
        for rec in tools:
            if rec.get("tag"):
                rec["tag"] = self.tagDB.get_tag_names_from_given_ids_list(
                    rec["tag"])
            record = {}
            tool_id = str(rec["_id"])
            versions = self.versionsDB.get_sync_versions_by_tool_id(
                str(tool_id), True)
            if versions is None or not versions:
                tool_version_with_no_active_version.append(
                    str(rec.get("name")))
                continue
            versions_arr = []
            for ver in versions:
                ver["source_version_id"] = str(ver.get("_id"))
                ver.pop("_id")
                ver.pop("tool_id")
                if datetime.strptime((str(str(ver['version_date']).split()[0])), "%Y-%m-%d"):
                    ver["version_date"] = str(ver["version_date"])
                if ver.get("document") is not None:
                    ver["document"] = self.trim_data_for_sync(
                        ver.get("document"))
                if ver.get("build") is not None:
                    builds = []
                    for build in ver.get("build"):
                        build = self.trim_data_for_sync(build)
                        if build.get("build_date"):
                            build["build_date"] = str(build["build_date"])
                        builds.append(build)
                    ver["build"] = builds
                if ver.get("deployment_field") is not None:
                    ver["deployment_field"] = self.trim_data_for_sync(
                        ver.get("deployment_field"))
                if ver.get("media_file") is not None:
                    ver["media_file"] = self.trim_data_for_sync(
                        ver.get("media_file"))
                versions_arr.append(ver)
            rec["versions"] = versions_arr
            record["source_tool_id"] = str(rec.get("_id"))
            rec.pop("_id")
            record["tool_data"] = rec
            tool_versions.append(record)
        return tool_versions, tool_version_with_no_active_version

    def trim_data_for_sync(self, data):
        '''
        General description:

        Args:
           param1 : data (JSON) : This is the parameter which has details of\
           Tool in JSON object.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             trim_data_for_sync(data)
        '''
        if data:
            if "_id" in data.keys():
                data.pop("_id")
            if "version_id" in data.keys():  # TODO REMOVE LATER.Not required from 2.0.3
                data.pop("version_id")
            if "parent_entity_id" in data.keys():
                data.pop("parent_entity_id")
        return data
