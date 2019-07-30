from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class ToolInstallation(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for ToolInstallation.
    '''

    def __init__(self, db):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.Collection = db.ToolInstallation
        # indexes
        self.Collection.create_index(
            [('version_id', ASCENDING), ('machine_id', ASCENDING)], unique=True)

    def get_all_machines_version(self):
        '''
        General description:

        Args:
            No Arguments.
        Returns:
                Returns the database entities existing for ToolInstallation.
        Example :
            get_all_machines_version()
        '''
        return self.Collection.find()

    def get_machines_by_version(self, version_id):
        '''
        General description:

        Args:
            param1 : version_id(object) : This is the unique id of the\
            ToolInstallation stored in the database.
        Returns:
                Returns the database entity based on the ToolInstallation.
        Example :
            get_machines_by_version(version_id)
        '''
        return self.Collection.find({"version_id": version_id})

    def get_versions_by_machine(self, machine_id):
        '''
        General description:

        Args:
            param1 : machine_id(object) : This is the unique id of the\
            ToolInstallation stored in the database.
        Returns:
                Returns the database entity based on the ToolInstallation.
        Example :
            get_versions_by_machine(machine_id)
        '''
        return self.Collection.find({"machine_id": machine_id})

    def add_tool_installation(self, new_installation):
        '''
        General description:

        Args:
            param1 : new_installation(JSON) : This is the parameter which has details \
            for new ToolInstallation .
        Returns:
              Returns the id of the newly created ToolInstallation in the database.
        Example :
             add_tool_installation(new_installation)
        '''
        result = self.Collection.insert_one(new_installation)
        return str(result.inserted_id)

    def update_tool_installation(self, installation):
        '''
        General description:

        Args:
            param1 : installation (JSON) : This is the parameter which has details of Tool.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_tool_installation(installation)
        '''
        json_new_entry = {}
        for key in installation.keys():
            if key != "_id":
                json_new_entry[key] = installation[key]
        result = self.Collection.update_one({"_id": ObjectId(installation["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_tool_installation(self, install_id):
        '''
        General description:

        Args:
           param1 : install_id(object) : This is the unique id of the\
            tool installation stored in the database.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_tool_installation(install_id)
        '''
        result = self.Collection.delete_one({"_id": ObjectId(install_id)})
        return str(result.modified_count())
