'''
#########################################################################################
TEAM PERMISSIONS SERVER AND GUI
#########################################################################################

{
    "_id" : ObjectId("58f7662dc6d2912590d3c29d"),
    "tag_id_list" : [
        "58a1650bf37d66833f91c0bf",
        "58a1650bf37d66833f91c0c2"
    ],
    "parent_entity_tag_list" : [
        "58a1650bf37d66833f91c0c5",
        "58ecab30c6d2918bc45e3f63",
        "58ecab30c6d2918bc45e3f64",
        "58cbb9106287da000b5e442d"
    ],
    "description" : "sa",
    "distribution_list" : "stuti.jaiswal@amdocs.com",
    "users_id_list" : [
        "58f4b77bc6d2912b30f806ad",
        "58e4c867c6d29130985e4483"
    ],
    "parent_entity_id_list" : [
        "58ecab30c6d2918bc45e3f65",
        "574befa3f37d66422c960644",
        "58ecab30c6d2918bc45e3f65",
        "58ecadf9c6d2919440398e08"
    ],
    "team_name" : "oiiioi",
    "machine_id_list" : [
        "57df8fbbf37d669444355347",
        "58cbe853e17192000b925256"
    ],
    "machine_group_id_list" : [
        "58f758a679e9335e0a7e9eca"
    ],
    "parent_entity_set_tag_list" : [
        "58ce6ea4d183550010859f89",
        "58cbb9106287da000b5e442d",
        "58ce6ea4d183550010859f89"
    ],
    "parent_entity_set_id_list" : [
        "58d2717f5b6f6b000ed31d8b",
        "58ce6ea4d183550010859f8a",
        "58cbdf7ee171920012f7b613",
        "58fdf1f979e9335e0a7e9ecb"
    ]
}

'''

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DBUtil import DBUtil
from settings import key


class Teams(DBUtil):
    '''
       General description :
       This class has definition for functions that provides add /update/ delete \
       / search by entities in database for Teams.
    '''

    def __init__(self, db):
        '''
        General description:
        This function initializes the database variables and \
        index to refer in functions.
        '''
        DBUtil.__init__(self, db)
        self.collection = db.Teams
        # indexes
        self.collection.create_index([('team_name', ASCENDING)], unique=True)

    def get_all_teams(self):
        '''
        General description:

        Args:
            No Argument.
        Returns:
                Returns the database entities existing for Teams.
        Example :
            get_all_teams()
        '''
        return self.collection.find()

    def get_team(self, object_id):
        '''
        General description:

        Args:
            param1 : object_id(object) : This is the unique id of the\
            Teams stored in the database.
        Returns:
                Returns the database entity based on the Teams id.
        Example :
            get_team(id)
        '''
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def get_team_by_name(self, name):
        '''
        General description:

        Args:
            param1 : name(string) : This is the unique name of the\
            Teams stored in the database.
        Returns:
                Returns the database entity based on the unique Team name.
        Example :
            get_team_by_name(name)
        '''
        return self.collection.find_one({"team_name": name})

    def get_team_by_user(self, user_id):
        '''
        General description:

        Args:
            param1 : user_id(object) : This is the unique id of the\
            users associated with a team stored in the database.
        Returns:
                Returns the database entity based on the user id.
        Example :
            get_team_by_user(user_id)
        '''
        return self.collection.find({"users_id_list": user_id})

    def add_team(self, team):
        '''
        General description:

        Args:
            param1 : team(JSON) : This is the parameter which has details \
            for new team .
        Returns:
              Returns the id of the newly created team in the database.
        Example :
             add_team(team)
        '''
        result = self.collection.insert_one(team)
        return str(result.inserted_id)

    def add_machine_to_team(self, team_id, machine_id):
        '''
        General description: This function adds machines to team

        Args:
            param1 : team_id : This is the team object id .
        Example :
             add_machines_to_team(team)
        '''
        result = self.collection.update_one(
            {"_id": ObjectId(team_id)}, {"$push": {"machine_id_list": machine_id}})
        return result.modified_count

    def add_user_to_team(self, object_id, id_user):
        '''
        General description:

        Args:
           param1 : object_id(object) : This is the unique id of the\
            team stored in the database.
           param1 : id_user(object) : This is the unique id of the\
            users associated with a team stored in the database.
        Returns:
              Returns the count of the successful records updated.
        Example :
             add_user_to_team(id , id_user)
        '''
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$push": {"users_id_list": id_user}})
        return result.modified_count

    def remove_user_from_team(self, object_id, id_user):
        '''
        General description:

        Args:
           param1 : object_id(object) : This is the unique id of the\
            team stored in the database.
           param1 : id_user(object) : This is the unique id of the\
           users associated with a team stored in the database.           
        Returns:
              Returns the count of the successful records deleted.
        Example :
             remove_user_from_team(id , id_user)
        '''
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$pull": {"users_id_list": id_user}})
        return result.modified_count

    def update_team(self, team):
        '''
        General description:

        Args:
            param1 : team(JSON) : This is the parameter which has details of team.
        Returns:
              Returns the count of the successful records updated.
        Example :
             update_team(team)
        '''
        json_new_entry = {}
        for key in team.keys():
            if key != "_id":
                json_new_entry[key] = team[key]
        result = self.collection.update_one({"_id": ObjectId(team["_id"]["oid"])},
                                            {"$set": json_new_entry}, upsert=False)
        return result.modified_count

    def delete_team(self, object_id):
        '''
        General description:

        Args:
           param1 : object_id(object) : This is the unique id of the\
            team stored in the database.
        Returns:
              Returns the count of the successful records deleted.
        Example :
             delete_team(id)
        '''
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def get_user_groups_for_view(self, object_id):
        '''
        General description:

        Args:
           param1 : object_id(object) : This is the unique id of the\
            team stored in the database.
        Returns:
              Returns the database entity based on the team id.
        Example :
             get_user_groups_for_view(id)
        '''
        group_temp = self.collection.find_one(
            {"_id": ObjectId(object_id)}, {"team_name": 1})  # ,"_id" :0
        group_temp["_id"] = str(object_id)
        group_temp["team_id"] = group_temp["_id"]
        del group_temp["_id"]
        return group_temp

    def remove_machine_from_all_teams(self, id_machine):
        '''
        General description:
        Args:       
            param1 (id_machine) : This is the machine ID which we want to remove .
        Returns:
                Returns the count of records that has been updated /removed\
                successfully for a given MachineGroup .
        Example :
             remove_machine_from_all_teams(id, id_machine)
        '''
        result = self.collection.update_many(
            {"machine_id_list": id_machine}, {"$pull": {"machine_id_list": id_machine}})
        return result

    def get_teams_by_machine(self, machine_id):
        '''
        General description:
        Args:
            param1 (machine_id) : This is the machine_id which is part of a team.
        Returns:
                Returns Database entity of team for the given machine_id
        Example :
             get_teams_by_machine(id)
        '''
        return self.collection.find({"machine_id_list": machine_id})
    
    def get_teams_by_filter(self, id):
        '''
        General description:
        Args:
            param1 (id) : The id of the parent in team.
        Returns:
                Returns Database list of team for the given tool_set_id_list
        Example :
             get_teams_by_filter(id)
        '''
        return self.collection.find({"$or":[{"tag_id_list" : {"$in" : [id]}},
                                            {"parent_entity_tag_list" : {"$in" : [id]}},
                                            {"parent_entity_set_tag_list" : {"$in" : [id]}},
                                            {"parent_entity_id_list" : {"$in" : [id]}},
                                            {"machine_id_list" : {"$in" : [id]}},
                                            {"machine_group_id_list" : {"$in" : [id]}},
                                            {"parent_entity_id_du_list" : {"$in" : [id]}},
                                            {"parent_entity_set_id_list" : {"$in" : [id]}},
                                            {"parent_entity_id_tool_list" : {"$in" : [id]}},
                                            {"parent_entity_du_set_id_list" : {"$in" : [id]}},
                                            {"parent_entity_tool_set_id_list" : {"$in" : [id]}},
                                            {"users_id_list" : {"$in" : [id]}}
                                            ]})
