from datetime import datetime
import re

from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING

import Build
from DBUtil import DBUtil
import DeploymentFields
import Documents
import MediaFiles


class Versions(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       
    '''

    def __init__(self, db):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.Versions
        self.deploymentFieldsDB = DeploymentFields.DeploymentFields(db)
        self.buildDB = Build.Build()
        self.documentsDB = Documents.Documents(db)
        self.mediaFilesDB = MediaFiles.MediaFiles(db)

        # indexes
        self.collection.create_index(
            [('tool_id', ASCENDING), ('version_name', ASCENDING), ('version_number', ASCENDING)], unique=True)

    def get_all_tool_versions(self, tool_id, is_active=False,filer_required=None):
        '''
        General description:

        Args:
            param1 : tool_id(object) : This is the unique id of the\
            ToolVersions stored in the database.

            param2 : is_active(string) :This is the parameter which determines \
            whether all active ToolVersions details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the parent_entity_id.
        Example :
            get_all_tool_versions(tool_id , True)
        '''
        filters={}
        if is_active:
            filters ={"tool_id": tool_id, "status": "1"}
        else:
            filters = {"tool_id": tool_id}
        if filer_required:
            if not tool_id:
                filters={}
            filters.update(filer_required)
        
        return self.collection.find(filters).sort([("version_date", DESCENDING),("version_number", DESCENDING)])


    def get_all_version(self):
        '''
        General description:

        Args:
           None
        Returns:
                Returns the database entity .
        Example :
            get_all_version()
        '''
        return self.collection.find()

    def get_version_by_tool_id_name_and_number(self, tool_id, version_name, version_number):
        '''
        General description:

        Args:
            param 1 : tool_id (object) : This is the unique id of the\
            tool stored in the database.

            param 2 : version_name(string) : This is the unique name of the\
            version stored in the database.

            param 3 : version_number(integer) : This is the unique number of the\
            version stored in the database.
        Returns:
                Returns the database entity based on the toolid, version_name and version_number.
        Example :
            get_version_by_tool_id_name_and_number(toolid , version_name ,version_number)
        '''
        return self.collection.find_one({"tool_id": tool_id,
                                         "version_name": re.compile('^' + re.escape(version_name) + '$', re.IGNORECASE),
                                         "version_number": version_number})

    def get_version(self, object_id, is_all_details=False):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            ToolVersions stored in the database.

            param2 : is_all_details(string) :This is the parameter which determines \
            whether ToolVersions details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the is_all_details and objectid of Versions .
        Example :
            get_version(object_id , True)
        '''
        version = self.collection.find_one({"_id": ObjectId(object_id)})
        if is_all_details == True and version is not None:
            version = self.get_version_details(version)
        return version

    def get_last_active_version_by_tool_id(self, tool_id, is_all_details):
        '''
        General description:

        Args:
            param1 : tool_id(object) : This is the unique id of the\
            ToolVersions stored in the database.

            param2 : is_all_details(string) :This is the parameter which determines \
            whether ToolVersions details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the is_all_details and toolid of Versions .
        Example :
            get_last_active_version_by_tool_id(tool_id , True)
        '''
        version_cur = self.collection.find({"tool_id": tool_id, "status": "1"}).sort([("version_date", DESCENDING),
                                                                                      ("version_number", DESCENDING)]).limit(1)
        version = None
        if version_cur.count() > 0:
            version = version_cur[0]
        else:
            return version
        if is_all_details == True:
            version = self.get_version_details(version_cur[0])
        return version

    def get_version_detail_and_status(self, tool_id, vnumber, vname, is_all_details):
        '''
        General description:

        Args:
            param 1 : tool_id (object) : This is the unique id of the\
            tool stored in the database.

            param 2 : vname (string) : This is the unique name of the\
            version stored in the database.

            param 3 : vnumber (integer) : This is the unique number of the\
            version stored in the database.

            param 4 : is_all_details(string) :This is the parameter which determines \
            whether ToolVersions details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the toolid, version_name and version_number.
        Example :
            get_version_detail_and_status(toolid , vname ,vnumber ,True)
        '''
        versionlist = []
        version = self.collection.find_one({"tool_id": tool_id,
                                            "version_number": vnumber,
                                            "version_name": re.compile('^' + re.escape(vname) + '$', re.IGNORECASE)})
        if is_all_details == True and version is not None:
            version = self.get_version_details(version)
        versionlist.append(version)
        if version is not None:
            if version["status"] == "1":
                versionlist.append(True)
            else:
                versionlist.append(False)
        else:
            versionlist.append(False)
        return versionlist

    def get_sync_versions_by_tool_id(self, tool_id, is_all_details):
        '''
        General description:

        Args:
            param 1 : tool_id (object) : This is the unique id of the\
            tool stored in the database.

            param 2 : is_all_details(string) :This is the parameter which determines \
            whether ToolVersions details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the toolid.
        Example :
            get_sync_versions_by_tool_id(toolid , True)
        '''
        version_cur = self.collection.find({"tool_id": tool_id, "status": "1"}).sort(
            [("version_date", DESCENDING),
             ("version_number", DESCENDING)])
        versions = []
        for ver in version_cur:
            if is_all_details: ver = self.get_version_details(ver)
            versions.append(ver)
        return versions

    def add_version(self, new_version):
        '''
        General description:

        Args:
            param1 : new_version(JSON) : This is the parameter which has details \
            for new Version .
        Returns:
              Returns the id of the newly created Version in the database.
        Example :
             add_version(new_version)
        '''
        new_version["status"] = "1"
        if new_version.get("version_date") is None:
            new_version["version_date"] = datetime.strptime(
                (str(str(datetime.now()).split()[0])), "%Y-%m-%d")
        result = self.collection.insert_one(new_version)
        return str(result.inserted_id)

    def update_version(self, version):
        '''
        General description:

        Args:
            param1 : version (JSON) : This is the parameter which has details of version.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_version(version)
        '''
        json_new_entry = {}
        for key in version.keys():
            if key != "_id":
                json_new_entry[key] = version[key]
        result = self.collection.update_one({"_id": ObjectId(version["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def update_version_screen_short(self, data, object_id):
        '''
        General description:

        Args:
            param 1 : object_id (object) : This is the unique id of the\
            version stored in the database.

            param 2 : data (JSON) : This is the parameter which has details of version.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_version_screen_short(id,data)
        '''
        result = self.collection.update_one({"_id": ObjectId(object_id)},
                                            {"$push": {"media_file": data}}, upsert=False)
        return result.modified_count

    def delete_version(self, object_id):
        '''
        General description:

        Args:
           param1 : object_id(object) : This is the unique id of the\
            Version stored in the database.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_version(id)
        '''
        result = self.collection.delete_one(
            {"_id": ObjectId(object_id)}).deleted_count
        return result

    def get_version_details(self, version):
        '''
        General description:

        Args:
            param1 : version(object) : This is the parameter which has details of version.
        Returns:
                Returns the version details in a JSON object.
        Example :
            get_version_details(version)
        '''
        if version == None or version == '':
            return version
        if version.get("pre_requiests") and len(version.get("pre_requiests")) > 0:
            if not len(version.get("pre_requiests")[0]) > 0:
                version["pre_requiests"] = None
        parent_entity_id = str(version["_id"])
        build = self.buildDB.get_active_build(parent_entity_id)
        if build is not None and build.count() > 0:
            version["build"] = build
        else:
            version["build"] = None
        document = self.documentsDB.GetDocuments(parent_entity_id)
        if document is not None:
            if document.get("documents") and len(document.get("documents")) > 0:
                if len(document.get("documents")[0]) > 0:
                    version["document"] = document
                else:
                    version["document"] = None
            else:
                version["document"] = None
        else:
            version["document"] = None
        deployment_field = self.deploymentFieldsDB.GetDeploymentFields(
            parent_entity_id)
        if deployment_field is not None:
            if deployment_field.get("fields") and len(deployment_field.get("fields")) > 0:
                if len(deployment_field.get("fields")[0]) > 0:
                    version["deployment_field"] = deployment_field
                else:
                    version["deployment_field"] = None
            else:
                version["deployment_field"] = None
        else:
            version["deployment_field"] = None
        media_file = self.mediaFilesDB.get_media_files(parent_entity_id)
        if media_file is not None:
            if media_file.get("media_files") and len(media_file.get("media_files")) > 0:
                if len(media_file.get("media_files")[0]) > 0:
                    version["media_file"] = media_file
                else:
                    version["media_file"] = None
            else:
                version["media_file"] = None
        else:
            version["media_file"] = None
        return version

    def get_tool_with_all_version_name_and_number(self, tool_id, is_all_details, only_name_and_number):
        '''
        General description:

        Args:
            param 1 : tool_id (object) : This is the unique id of the\
            tool stored in the database.

            param 2 : only_name_and_number (string) : This is the unique name and  number of the\
            version stored in the database.

            param 3 : is_all_details(string) :This is the parameter which determines \
            whether ToolVersions details should be visible to user or not.\
            This has two values - True /False .
        Returns:
                Returns the database entity based on the toolid, version_name and version_number.
        Example :
            get_tool_with_all_version_name_and_number(toolid , only_name_and_number ,True)
        '''
        version = self.collection.find({"tool_id": tool_id}).sort([("version_date", DESCENDING),
                                                                   ("version_number", DESCENDING)])
        versions_list = []
        if is_all_details == True and version is not None:
            for ver in version:
                result = self.get_version_details(ver)
                ver = {}
                ver["version_name"] = result.get("version_name")
                ver["version_number"] = result.get("version_number")
                ver["version_id"] = str(result.get("_id"))
                if only_name_and_number:
                    versions_list.append(ver)
                else:
                    versions_list.append(result)
        return versions_list
