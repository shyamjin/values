from pymongo import MongoClient


# PROVIDE SERVERS LIST
server_list= ['localhost']
db_port=27018
db_user="test"
db_pass="test"


# PROVIDE COLLECTION LIST
collections_to_clean=[                     
                     "DeploymentRequest",
                     "ToolsOnMachine",
                     "ToolInstallation",
                     "DeploymentRequestGroup"
                     ]


'''
BELOW IS HANDLER TO REMOVE ABOVE GIVEN
'''
for server in server_list:
    print '**************************************************************************************************************************'
    print "Checking "+server
    print '**************************************************************************************************************************'
    serverclient = MongoClient(server, db_port)
    serverclient.admin.authenticate(db_user,db_pass)
    serverDb = serverclient.DeploymentManager
    
    for coll_to_clean in collections_to_clean:
        if coll_to_clean in serverDb.collection_names():
            count=serverDb[coll_to_clean].count()
            if count > 0:
                print "Removing "+str(count)+" documents from collection "+coll_to_clean
                serverDb[coll_to_clean].delete_many({})
                   

print "Done!!"    