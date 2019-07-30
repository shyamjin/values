import os
import re

from bson.objectid import ObjectId
from pymongo import DESCENDING

from DBUtil import DBUtil
from settings import mongodb


# TODO
# SAVED EXPORTS
no_of_saved_exports = 5


class SavedExports(DBUtil):
    def __init__(self):
        db = mongodb
        DBUtil.__init__(self, db)
        self.collection = db.SavedExports

    def get_exports(self):
        return self.collection.find().sort([['_id', DESCENDING]])

    def get_export_by_Id(self, object_id):
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def add_exports(self, NEW_EXPORT):
        result = self.collection.insert_one(NEW_EXPORT)
        return str(result.inserted_id)

    def delete_extra_exports(self, saved_export_full_path):
        records = self.collection.find().sort(
            [['_id', DESCENDING]]).skip(no_of_saved_exports)
        if records:
            try:
                for record in records:
                    if os.path.isfile(saved_export_full_path + "/" + record.get("file_name")):
                        os.remove(saved_export_full_path +
                                  "/" + record.get("file_name"))
                    self.collection.delete_one(
                        {"_id": ObjectId(record.get('_id'))})
            except:
                print "exception in deleting saved exports"
                return 1
        return 1
