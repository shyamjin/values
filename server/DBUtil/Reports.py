import re

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
from settings import mongodb


class Reports(DBUtil):

    def __init__(self):
        db = mongodb
        DBUtil.__init__(self, db)
        self.collection = db.Reports

        # indexes
        self.collection.create_index([('name', ASCENDING)], unique=True)

    def GetReports(self):
        return self.collection.find()

    def GetReport(self, object_id):
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def GetReportByName(self, name):
        return (self.collection.find_one({"name": re.compile('^' + re.escape(name) + '$', re.IGNORECASE)}))
