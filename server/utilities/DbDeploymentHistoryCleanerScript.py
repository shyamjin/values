from pymongo import MongoClient


# PROVIDE SERVERS LIST
server_list= ['ilutdto374.corp.amdocs.com']
db_port=22275
db_user="vpadmin"
db_pass="vpadmin"


# PROVIDE COLLECTION LIST
collections_to_clean=[                     
                     "DistributionSync",
                     "ProposedTools",
                     "DeploymentRequest",
                     "ToolsOnMachine",
                     "Emails",
                     "ToolInstallation",
                     "Auditing",
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