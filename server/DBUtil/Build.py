'''
WHEN CALLED FROM JENKINS

echo "------------------------Uploading build to deployment manager------------------------"

BUILD_FILE_NAME="${JOB_NAME}_${BUILD_NUMBER}.zip"
SIZE=$(du -Ph ${BUILD_FILE_NAME} | awk '{print $1}')

echo ${PACKAGE}
STATUS=1
PACKAGE_NAME=${BUILD_FILE_NAME}
VERSION_ID="${MONGO_VERSION_ID}"
NEW_PACKAGE=`echo ${PACKAGE} | sed s/\\\./\\\//g`
RELATIVE_PATH="${REPO_ID}/${NEW_PACKAGE}/${ARTIFACT}/${VERSION}"
ADDITIONAL_INFO="{\"version\" : \"${VERSION}\",\"package\" : \"${PACKAGE}\",\"artifact\" : \"${ARTIFACT}\",\"repo_id\" : \"${REPO_ID}\",\"relative_path\" : \"${RELATIVE_PATH}\",\"file_name\" : \"${ARTIFACT}-${VERSION}-${BUILD_NUMBER}.zip\"}"
FILE_PATH="${NEXUS_URL}/${REPO_ID}/${NEW_PACKAGE}/${ARTIFACT}/${VERSION}/${ARTIFACT}-${VERSION}-${BUILD_NUMBER}.zip"
ADD_BUILD_URL=${DP_MANAGER_URL}/versions/build/add
JSON="{\"status\" : \"${STATUS}\", \"build_number\" : \"${BUILD_NUMBER}\", \"package_name\" : \"${PACKAGE_NAME}\",\"package_type\":\"zip\",\"version_id\" : \"${VERSION_ID}\",\"type\" : \"url\",\"file_path\" : \"${FILE_PATH}\",\"file_size\" : \"${SIZE}\",\"additional_info\" :${ADDITIONAL_INFO}}"
echo ${NEW_PACKAGE}


RESULT=$(echo ${JSON} | curl -k --silent  --output /dev/stderr  --write-out "%{http_code}"  -H  "Content-Type: application/json" --request POST --data @- ${ADD_BUILD_URL})

if [ $RESULT -eq 200 ]
then
    echo "curl -k command passed, removing the ${BUILD_FILE_NAME}"
    rm -f ${BUILD_FILE_NAME}
else
    echo "curl -k command failed,removing the ${BUILD_FILE_NAME}"
    rm -f ${BUILD_FILE_NAME}
    exit 1
fi
'''

from datetime import datetime

from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING

from DBUtil import DBUtil
from settings import mongodb


class Build(DBUtil):
    '''
        General description:

       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for Build.
    '''

    def __init__(self):
        '''
           General description:
           This function initializes the database variables and \
           index to refer in functions.
        '''
        db = mongodb
        DBUtil.__init__(self, db)
        self.collection = db.Build
        # indexes
        self.collection.create_index(
            [('parent_entity_id', ASCENDING), ('build_number', DESCENDING)], unique=True)
        self.collection.create_index([('parent_entity_id', ASCENDING), (
            'parent_entity_type', ASCENDING), ('build_number', DESCENDING)], unique=True)

    def get_build(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique Id which is stored in database
        Returns:
                Returns Database entity of GetBuild for the given Machine Group Id
        Example :
            get_build(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def get_all_build(self):
        '''
        General description:
        Arg:
            No Arg
        Returns:
                Returns Database entity of Build for the given filters
        Example :
             get_all_build() 
        '''
        return self.collection.find().sort([['build_number', DESCENDING]])

    def get_active_build(self, parent_entity_id,only_build_number=False):
        '''
         General description:
        Args:
        param 1 : parent_entity_id (object) : This is the unique id of the\
            Build stored in the database.
        Returns:
                Returns the database entity based on the parent_entity_id.
        Example :
            get_active_build(parent_entity_id)
        '''
        if only_build_number:
            return self.collection.find({"parent_entity_id": parent_entity_id, "status": "1"},{"_id":1,"build_number":1}).sort([['build_number', DESCENDING]])
        return self.collection.find({"parent_entity_id": parent_entity_id, "status": "1"}).sort([['build_number', DESCENDING]])
    
    def get_active_build_lesser_than_build_number(self, parent_entity_id,build_number):
        '''
         General description:
        Args:
        param 1 : parent_entity_id (object) : This is the unique id of the\
            Build stored in the database.
        param 2 : build_number (integer) : Provided build number    
        Returns:
                Returns the database entity based on the parent_entity_id and builds lesser than the given build no
        Example :
            get_active_build(parent_entity_id)
        '''
        return self.collection.find({"parent_entity_id": parent_entity_id, "status": "1",\
                                     "build_number": {"$lt": build_number}}).sort([['build_number', DESCENDING]])
    
    def get_active_build_for_unittest(self, parent_entity_id):
        '''
         General description:
        Args:
        param 1 : parent_entity_id (object) : This is the unique id of the\
            Build stored in the database.
        Returns:
                Returns the database entity based on the parent_entity_id.
        Example :
            get_active_build(parent_entity_id)
        '''
        data= self.collection.find({"parent_entity_id": parent_entity_id, "status": "1"}).sort([['build_number', DESCENDING]])
        
        for rec in data:
            return str(rec.get("_id"))
    
    def get_last_active_build(self, parent_entity_id):
        '''
        General description:
         Args:
            param1 : parent_entity_id(object) : This is the unique id of the
            Build stored in the database.
        Returns:
                Returns the database entity based on parent_entity_id.
        Example :
            get_last_active_build(parent_entity_id)
        '''
        data = self.collection.find({"parent_entity_id": parent_entity_id, "status": "1"}).sort(
            [['build_number', DESCENDING]]).limit(1)
        rec = None
        if data.count() > 0:
            return data[0]
        else:
            return rec

    def get_build_by_id(self,object_id, is_active,only_build_number=False):
        '''
        General description:
        Args:
            param1 (object_id) : This is the unique Id which is stored in database
            param2 is_active(String):This is the parameter which determines \
            whether Build  should be Active or not.\
        Returns:
                Returns the database entity based on object_id.
        Example :
            get_build_by_id(object_id, is_active)
        '''
        if only_build_number:
            if is_active:
                return self.collection.find_one({"_id": ObjectId(str(object_id)), "status": "1"},{"_id":1,"build_number":1})
            else:
                return self.collection.find_one({"_id": ObjectId(str(object_id))},{"_id":1,"build_number":1})
        else:
            if is_active:
                return self.collection.find_one({"_id": ObjectId(str(object_id)), "status": "1"})
            else:
                return self.collection.find_one({"_id": ObjectId(str(object_id))})
    
        
    def get_build_by_number(self, parent_entity_id, build_number, is_active):
        '''
        General description:
        Args:
            param1 :parent_entity_id(object) : This is the parameter which has details of Build.
            param2 build_number(integer) : This is the unique Id which is stored in database
            param3 is_active(integer):This is the parameter which determines \
            whether Build  should be Active or not.\
        Returns:
                Returns the database entity based on parent_entity_id,build_number.
        Example :
            get_build_by_number(parent_entity_id, build_number,1)
        '''
        if is_active:
            return self.collection.find_one({"build_number": build_number, "parent_entity_id": parent_entity_id, "status": "1"})
        else:
            return self.collection.find_one({"build_number": build_number, "parent_entity_id": parent_entity_id})

    def get_handled_build(self):
        '''
        General description:
        Args:
           no args
        Returns:
                Returns the database entity 
        Example :
            get_handled_build()
        '''
        return self.collection.find({"status": "0"}).sort([['build_number', DESCENDING]])

    def delete_build(self, object_id):
        '''
        General description:
        Args:
            param1 (object_id) : This is the ID of the existing \
           Build which we have to delete.
        Returns:
                Returns the count of records that has been deleted \
                successfully for a given Build .
        Example :
             delete_build(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def delete_build_by_parent_entitity_id(self, peid):
        '''
        General description:
        Args:

             param1 :parent_entity_id(object) : This is the parameter which has details of Build.
        Returns:
                Returns the count of records that has been deleted \
                successfully for a given Build .
        Example :
             delete_build_by_parent_entitity_id(peid)
        '''

        result = self.collection.delete_many({"parent_entity_id": peid})
        return result.deleted_count

    def get_all_builds(self, parent_entity_id):
        '''
        General description:
        Args:param1 :parent_entity_id(object) : This is the parameter which has details of Build.

        Returns:
                Returns Database entity based on  parent_entity_id.
        Example :
             get_all_builds(parent_entity_id) 
        '''
        return self.collection.find({"parent_entity_id": parent_entity_id}).sort([['build_number', DESCENDING]])

    def add_build(self, newBuild):
        '''
        General description:

        Args:
            param1 (newBuild) : This is the parameter which has the details of the\
           Build to be added in the database.Its a JSON object.
        Returns:
                Returns the id of the newly created Build from the database.
        Example :
             add_build(newBuild)
        '''
        if newBuild.get("build_number"):
            newBuild["build_number"] = int(newBuild['build_number'])
        if not newBuild.get("build_date"):
            newBuild["build_date"] = datetime.strptime(
                (str(datetime.now()).split(".")[0]), "%Y-%m-%d %H:%M:%S")
        else:
            newBuild["build_date"] = datetime.strptime(
                (str(newBuild["build_date"]).split(".")[0]), "%Y-%m-%d %H:%M:%S")
        result = self.collection.insert_one(newBuild)
        return str(result.inserted_id)

    def update_build(self, build):
        '''
        General description:
        Args:
            param1 (build) : This is the parameter which has the details of the\
            build to be updated in the database.
        Returns:
                 Returns the count of the records updated successfully \
                 for the given id of the build.
        Example :
             update_build( build)
        '''
        json_new_entry = {}
        for key in build.keys():
            if key != "_id":
                json_new_entry[key] = build[key]
        if json_new_entry.get("build_number"):
            json_new_entry["build_number"] = int(
                json_new_entry['build_number'])
        if json_new_entry.get("build_date"):
            json_new_entry["build_date"] = datetime.strptime(
                (str(json_new_entry["build_date"]).split(".")[0]), "%Y-%m-%d %H:%M:%S")
        result = self.collection.update_one({"_id": ObjectId(build["_id"]["oid"])}, {
                                            "$set": json_new_entry}, upsert=False)
        return result.modified_count

    def set_build_active(self, parent_entity_id, object_id):
        '''
        General description:
        Args:
        param1 (object_id) : This is the ID of the existing \
           Build which we have to set active.
           parent_entity_id(object) : This is the parameter which has details of Build.
        Returns:
                 Returns the count of the records set active successfully \
                 for the given id of the build.
        Example :
             set_build_active( parent_entity_id, object_id)
        '''
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": {"status": "1"}}, upsert=False)
        return result.modified_count
