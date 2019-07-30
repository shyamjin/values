"""
DB interface with plugin
"""
from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class Plugins(DBUtil):
    '''
        General description :
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
        self.collection = db.Plugins
        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def get_plugin_by_name(self, plugin_name):
        '''
        General description::
        Retrieves from DB  the plugin based on name
        Args:
            param1 (plugin_name) : This is the unique name of the\
            Plugins stored in the database.
        Returns:
                Returns Database entity by the name \
                of the Plugins.
        Example :
             get_plugin_by_name(plugin_name)
        '''
        return self.collection.find_one({"name": plugin_name})

    def get_plugin_by_id(self, plugin_id):
        '''
        General description::
        Retrieves from DB  the plugin based on id
        Args:
            param1 (plugin_oid) : This is the unique name of the\
            Plugins stored in the database.
        Returns:
                Returns Database entity by the name \
                of the Plugins.
        Example :
             get_plugin_by_name(plugin_name)
        '''
        return self.collection.find_one({"_id": ObjectId(plugin_id)})

    def get_all_plugin(self, status=None):
        '''
        General description::
        Retrieves from DB all the plugins based on status
        Args:
            param1 (status) : This is the parameter which determines \
            whether all PermissionGroup should be searched.\
            This has two values - active /inactive
        Returns:
                Returns Database entity by the status flag \
                of the Plugins.
        Example :
             get_all_plugin(status)
        '''
        status_filter = [status]
        if not status:
            return self.collection.find()
        else:
            return self.collection.find({"status": {"$in": status_filter}})

    def add_plugin(self, plugin):
        '''
        General description:
        Args:
            param1 (plugin) : This is the parameter which has the details of the\
            Plugins to be added in the database.Its a JSON object.
        Returns:
                Returns the id of the newly created Plugins from the database.
        Example :
             add_plugin(plugin)
        '''
        result = self.collection.insert_one(plugin)
        return str(result.inserted_id)

    def update_plugin_status(self, name, status):
        '''
        General description:
        Args:
            param1 (name) : This is the unique name of the\
            Plugins stored in the database.
            param2 (status) : This is the parameter which determines \
            whether all PermissionGroup should be searched.\
            This has two values - active /inactive
        Returns:
               Returns the count of the records updated successfully \
               for the given name and status flags of the Plugins.
        Example :
             update_plugin_status(name,status)
        '''
        result = self.collection.update_one({"name": name},
                                            {"$set": {"status": status}})
        return result.modified_count

    def delete_plugin(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the\
            Plugins stored in the database.
        Returns:
                Returns the count of the records deleted successfully \
                for the given id of the Plugins.
        Example :
             delete_plugin(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def delete_plugin_by_name(self, name):
        '''
        General description:
        Args:
            param1 (name) : This is the unique name of the\
            Plugins stored in the database.
        Returns:
                Returns the count of the records deleted successfully \
                for the given name of the Plugins.
        Example :
             delete_plugin_by_name(name)
        '''
        result = self.collection.delete_one({"name": name})
        return result.deleted_count
