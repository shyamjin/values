'''
Created on Mar 16, 2016

@author: PDINDA
'''

import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil


class EmailTemplate(DBUtil):
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
        self.collection = db.EmailTemplate

        # indexes
        self.collection.create_index([('templateid', ASCENDING)], unique=True,)

    def AddTemplate(self, template):
        '''
        General description:
        Args:
            param1 (template) : This is the parameter which has the details of the\
            template to be added in the database.
        Returns:
                Returns the id of the newly created template from the database.
        Example :
             AddTemplate(template)
        '''
        result = self.collection.find_one(sort=[("templateid", -1)])
        template.update({"templateid": result['templateid'] + 1})
        result = self.collection.insert_one(template)
        return(result.inserted_id)

    def UpdateTemplate(self, object_id, template):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
           Template stored in the database.
            param1 (template) : This is the parameter which has the details of the\
            template to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the Template
        Example :
             UpdateTemplate(object_id, template)
        '''
        result = self.collection.update_one({'_id': object_id}, template)
        return(result.inserted_id)

    def RemoveTemplate(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            Template stored in the database.
        Returns:
                Returns the count of the records Removed successfully\
                for the given id of the Template.
        Example :
             RemoveTemplate(id)
        '''
        return (self.collection.delete_one({"_id": object_id}))

    def GetTemplateById(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            Template stored in the database.
        Returns:
               Returns Database entity by the id of the of the Template.
        Example :
             GetTemplateById(id)
        '''
        return (self.collection.find_one({"_id": ObjectId(object_id)}))

    def GetTemplateByTemplateId(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique id of the existing \
            Template stored in the database.
        Returns:
               Returns Database entity by the id of the of the Template.
        Example :
             GetTemplateByTemplateId(id)
        '''
        return (self.collection.find_one({"templateid": object_id}))

    def GetTemplateByName(self, name):
        '''
        General description:
        Args:
            param1 (name) : This is the unique name of the existing \
            Template stored in the database.
        Returns:
               Returns Database entity by the name of the of the Template.
        Example :
             GetTemplateByname(name)
        '''
        return (self.collection.find_one({"name": re.compile('^' + re.escape(name) + '$', re.IGNORECASE)}))
