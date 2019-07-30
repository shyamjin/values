'''
Created on April 13, 2017
@author: ILANPI
this module  is managing all the connection,activation,triggering,installation of plugins
all the connection to the plugin should be done from this plugin

'''

import logging
import os

from autologging import logged
from yapsy.PluginManager import PluginManager

from DBUtil import Plugins
from Plugins.IPostDeploymentPlugin import IPostDeploymentPlugin
from Plugins.IPreDeploymentPlugin import IPreDeploymentPlugin
from settings import mongodb


@logged(logging.getLogger("PluginsManagerService"))
class PluginsManagerService(object):
    """
    Description: main class in order to manage all the plugin operations like loading and triggering
    """

    def __init__(self):
        self.plugin_manager = PluginManager()
        self.loaded_plugin_list = []
        self.loaded_plugin_objects = None
        self.plugin_db = Plugins.Plugins(mongodb)
        self.plugin_location = os.path.abspath(
            os.path.join(os.getcwd(), 'Plugins'))
        self.deleted_plugin_location = os.path.abspath(
            os.path.join(os.getcwd(), 'Plugins_deleted'))
        self.load_plugin()

    def load_plugin(self):
        """loads all  plugins from folder and activates the plugins

        Returns:
           :dict: active_plugins_dict_from_db

        Raises:
            no_value
            no_active_plugins

        """

        # Build the manager
        # Tell it the default place(s) where to find plugins
        print "###################"
        print "STARTED PLUGIN LOAD "
        print "###################"

        if os.path.isdir(self.plugin_location) is True:

            try:
                # set plugins from folder
                self.plugin_manager.setPluginPlaces([self.plugin_location])

                # define interfaces to load you have defined
                self.plugin_manager.setCategoriesFilter({
                    "PreDeploymentPlugin": IPreDeploymentPlugin,
                    "PostDeploymentPlugin": IPostDeploymentPlugin
                })

                # Load all plugins from plugin folder
                self.plugin_manager.collectPlugins()
                loaded_plugin_from_folder = [
                    x.name for x in self.plugin_manager.getAllPlugins()]

               # validate plugin if not valid deactivate
                for plugin in loaded_plugin_from_folder:
                    if not self.is_valid_plugin(plugin):

                        self.deactivate(plugin)

                        print(
                            "the following plugin is deactivate cause is not valid: " + plugin)

               # update DB with new plugins
                self.detect_new_plugins()

               # load all activated plugins from DB
                active_plugins_dict_from_db = self.plugin_db.get_all_plugin(
                    status='active')
                active_plugins_in_db = [
                    x['name'] for x in self.plugin_db.get_all_plugin(status='active')]
               # final active_plugins list
                if active_plugins_in_db is None:
                    print "no plugins installed"
                elif loaded_plugin_from_folder is None:
                    print "no plugins in the plugins folder"

                else:
                    active_plugins = [
                        x for x in loaded_plugin_from_folder if x in active_plugins_in_db]

                    for plugin in active_plugins:
                        # validate plugin if not valid deactivate
                        if not self.is_valid_plugin(plugin):
                            print "plugin is not valid: " + plugin + " deactivate"
                            self.deactivate(plugin)
                        else:
                            # activate
                            self.plugin_manager.activatePluginByName(plugin)
                            print "loaded plugin name: " + plugin
                            ValueError("loaded plugin name: " + plugin)

                    print "###################"
                    print "COMPLETED PLUGIN LOAD "
                    print "###################"

                    return active_plugins_dict_from_db

            except (Exception, ValueError) as error:
                print error
                raise ValueError("Unable to load plugins :", error)

        elif os.path.isdir(self.plugin_location) is False:
            raise ValueError("plugin folder is set to " +
                             self.plugin_location + " missing or not configured well")

        else:
            raise ValueError("unknown err during plugin loading")

    def detect_new_plugins(self):
        """
        updates new plugins in db

        :param loaded_plugin_from_folder:
        :return:
        """

        # load all from db

        loaded_plugin_from_folder = self.plugin_manager.getAllPlugins()

        plugins_in_db = [x.get('name')
                         for x in self.plugin_db.get_all_plugin()]

        if not plugins_in_db:
            new_plugins = loaded_plugin_from_folder
        else:
            new_plugins = [
                x for x in loaded_plugin_from_folder if x.name not in plugins_in_db]

        for plugin_object in new_plugins:

            # get plugin type
            parent_class = type(plugin_object.plugin_object).__bases__
            parent_class_name = parent_class[0].__name__

            plugin_dict = {'name': plugin_object.name,
                           'category': parent_class_name[1:],
                           'author': plugin_object.author,
                           'version': str(plugin_object.version),
                           'description': plugin_object.description,
                           'status': 'inactive'}

            try:
                self.plugin_db.add_plugin(plugin_dict)
            except Exception as error:
                print error
                raise RuntimeError("unable to insert the plugin to DB")

    def install_plugin(self, plugin_name):
        '''
        activates the plugin and triggers the install method of the plugin

        :param plugin_name: string
        :return:
        :raises
         RuntimeError "unable to insert the plugin to DB"
        '''

        # set plugins from folder
        # self.plugin_location = os.path.abspath(os.path.join(os.getcwd(), 'Plugins'))
        # self.load_plugin()
        plugin_details = self.plugin_db.get_plugin_by_name(plugin_name)
        plugin_object = self.plugin_manager.getPluginByName(
            plugin_name, plugin_details.get('category'))

        if plugin_object:
            try:
                self.activate(plugin_name)
                return plugin_object.plugin_object.install()
            except Exception as error:
                print error
                raise RuntimeError(
                    "unable to insert the plugin to DB: ", error)
        else:
            raise ValueError("no active plugin with this name")

    def is_valid_plugin(self, plugin):
        '''
        validate that plugin has all the required methods and attributes

        :param plugin:
        :return:
            True or False
        '''

        # mandatory element lists
        plugin_mandatory_attributes = [
            'author', 'name', 'version', 'description']
        plugin_mandatory_methods = ['preform',
                                    'activate', 'deactivate', 'is_activated']

        # get plugin
        plugin = self.plugin_manager.getPluginByName(
            plugin, 'PreDeploymentPlugin')

        # check plugin manifest
        try:
            for attribute in plugin_mandatory_attributes:
                if str(getattr(plugin, attribute, None)) == "":
                    raise ValueError("plugin is missing value in " + attribute)
        except (ValueError, AttributeError) as error:
            print error
            return False

        # check plugin methods
        try:
            methods = [x for x in plugin_mandatory_methods if x not in dir(
                plugin.plugin_object)]
            if len(methods) > 0:
                raise ValueError(
                    "folowwing methods are missing " + str(methods))

        except(ValueError, AttributeError) as error:
            print error
            return False

        return True

    def uninstall_plugin(self, plugin):
        '''
        triggers the uninstall method of the  plugin by name
        remove the db details
        rename the plugin folder

        :param plugin_name:
        '''

        try:
            # get category form DB
            plugin_details = self.plugin_db.get_plugin_by_name(plugin)
            if plugin_details:
                plugin_object = self.plugin_manager.getPluginByName(
                    plugin, plugin_details.get('category'))

                # uninstal
                plugin_object.plugin_object.uninstall()

                # delete from db
                self.plugin_db.delete_plugin_by_name(plugin)

                # check if deleted folder exists
                if os.path.isdir(self.deleted_plugin_location) is not True:
                    os.mkdir(self.deleted_plugin_location)

                # delete folder
                os.rename(self.plugin_location + "/" + plugin,
                          self.deleted_plugin_location + "/" + plugin + ".deleted")
            else:
                raise ValueError('couldnt find plugin')

        except (ValueError, Exception) as error:
            print error
            raise RuntimeError(
                " could not uninstall plugin " + plugin + " " + error)

    def activate(self, plugin_name):
        '''
        activates plugin by name

        :param plugin_name:
        :raise
                 RuntimeError "could not activate plugin"
        '''

        try:
            # get category form DB
            plugin_details = self.plugin_db.get_plugin_by_name(plugin_name)

            # activate
            self.plugin_manager.activatePluginByName(
                plugin_name, plugin_details.get('category'))

            # updateDB
            self.plugin_db.update_plugin_status(plugin_name, 'active')
        except Exception as error:
            print error
            raise RuntimeError(" could not activate plugin " + plugin_name)

    def deactivate(self, plugin_name):
        '''
              deactivates plugin by name

              :param plugin_name: string
              :raise
                 RuntimeError "could not deactivate plugin"
        '''

        try:
            # get category form DB
            plugin_details = self.plugin_db.get_plugin_by_name(plugin_name)

            # deactivate
            self.plugin_manager.deactivatePluginByName(
                plugin_name, plugin_details.get('category'))
            # updateDB
            self.plugin_db.update_plugin_status(plugin_name, 'inactive')

        except Exception as error:
            print error
            raise RuntimeError(" could not deactivate plugin " + plugin_name)

    def preform(self, category, plugin_name):
        """
        execute the preform method of plugin in category

        :param plugin_name: string
        :param category: string
        :raises
            RuntimeError unable to trigger operation of plugin:
        """
        try:
            plugin = self.plugin_manager.getPluginByName(plugin_name, category)
            plugin.plugin_object.preform()

        except Exception as error:
            print error
            raise RuntimeError(
                " unable to trigger operation of plugin:" + plugin_name)

    def preform_all_in_category(self, category, **keyargs):
        '''
        triggers all preform methods of plugin in the provided category

        :param category:
        :return:
        :raises
             RuntimeError "unable to execute the plugin logic"
        '''

        for (key, value) in keyargs.iteritems():
            print (key, value)

        try:
            for plugin in self.plugin_manager.getPluginsOfCategory(category):
                print("preforming action of plugin " + plugin.name)
                plugin.plugin_object.preform()
        except (ValueError, Exception) as error:
            print error
            raise RuntimeError("unable to execute the plugin logic: " + error)

    # ## test
    def test(self):
        # just for test
        for p in self.plugin_manager.getPluginsOfCategory('PreDeploymentPlugin'):
            self.install_plugin('TestPlugin')
