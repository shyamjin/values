define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

  var manageUserGroupControllerApp = angular.module('manageUserGroupControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
  manageUserGroupControllerApp.controller('ManageUserGroupsController', function ($scope, $stateParams, $location, $state, $timeout, $rootScope, UserGroup, Users, UserGroupView, UserGroupDelete, TagsAll, GetAllTools, AllToolSet, DeploymentUnitAll, DUSetAll, GetAllMachine, MachineGroup) {

    var allEntityObj = {
        "name" : "all"
    };

    $scope.allDUEntityObj = {
        "name" : "all"
    };

    var allMachineEntityObj = {
        "machine_name" : "all"
    };

    var allMachineGroupEntityObj = {
        "group_name" : "all"
    };

    $scope.gotoAddTeams = function()
    {
        $state.go('createUserGroup');
    };

    $scope.gotoEditTeams = function(teamItem)
    {
        $state.go('editUserGroup', { id:teamItem._id.$oid });
    };

    $scope.deleteUserGroup=function(userGroupItem)
    {
        $scope.deletedUserStatus = UserGroupDelete.remove({
            id:userGroupItem._id.$oid
        },
        function(groupDeleteRequest)
        {
            $state.go('manageUserGroups');
            $rootScope.handleResponse(groupDeleteRequest);
            $scope.UserGroups = UserGroup.get({
            },
            function(successResponse){
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        },
        function(groupDeleteResponseError)
        {
            $rootScope.handleResponse(groupDeleteResponseError);
        });
    };

    $scope.UserGroups = UserGroup.get({
    },
    function(successResponse)
    {
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.discardUserGroupData=function()
    {
        $scope.UserGroups = UserGroup.get({

        },
        function(successResponse)
        {
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.closeTeamDetailsModal = function()
    {
        $('#view_team_details').hide(700);
    };

    $scope.viewTeamDetails = function(group_id)
    {
        $scope.userGroupData = {
            id: '',
            team_name : '',
            description : '',
            distribution_list : '',
            homepage : '',
            users_id_list : [],
            tag : [],
            parent_entity_tag_list : [],
            parent_entity_set_tag_list : [],
            machine_id_list : [],
            machine_group_id_list : [],
            parent_entity_id_tool_list : [],
            parent_entity_id_du_list : [],
            parent_entity_set_id_tool_list : [],
            parent_entity_set_id_du_list : []
        };
        $scope.UserGroup = UserGroupView.get({
            id: group_id
        },
        function(userGroupSuccessResponse)
        {
            $('#view_team_details').show(700);
            $scope.userGroupData.id = userGroupSuccessResponse.data._id.$oid;
            $scope.userGroupData.team_name = userGroupSuccessResponse.data.team_name;
            $scope.userGroupData.description = userGroupSuccessResponse.data.description;
            $scope.userGroupData.distribution_list = userGroupSuccessResponse.data.distribution_list;
            if(userGroupSuccessResponse.data.homepage === 'dashboard')
            {
                $scope.userGroupData.homepage = 'Tool Dashboard';
            }
            else if((!userGroupSuccessResponse.data.homepage) || userGroupSuccessResponse.data.homepagee === '' || userGroupSuccessResponse.data.homepage === null)
            {
                $scope.userGroupData.homepage = '';
            }
            else
            {
                $scope.userGroupData.homepage = 'DU Dashboard';
            }

            TagsAll.get({
            },
            function(successResponse)
            {
                $scope.allTags = successResponse;
                $scope.allTags.splice(0, 0, allEntityObj);
                for(var t1=0; t1<$scope.allTags.length; t1++)
                {
                    for(var t2=0; t2<userGroupSuccessResponse.data.tag_id_list.length; t2++)
                    {
                        if(userGroupSuccessResponse.data.tag_id_list[t2] === $scope.allTags[t1].name)
                        {
                            $scope.userGroupData.tag.push($scope.allTags[t1]);
                        }
                    }

                    for(var t3=0; t3<userGroupSuccessResponse.data.parent_entity_tag_list.length; t3++)
                    {
                        if(userGroupSuccessResponse.data.parent_entity_tag_list[t3] === $scope.allTags[t1].name)
                        {
                            $scope.userGroupData.parent_entity_tag_list.push($scope.allTags[t1]);
                        }
                    }
                    for(var t4=0; t4<userGroupSuccessResponse.data.parent_entity_set_tag_list.length; t4++)
                    {
                        if(userGroupSuccessResponse.data.parent_entity_set_tag_list[t4] === $scope.allTags[t1].name)
                        {
                            $scope.userGroupData.parent_entity_set_tag_list.push($scope.allTags[t1]);
                        }
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            GetAllTools.get({
                id: "all",
                status: "active,indevelopment,deprecated",
                page: 0,
                perpage: 0
            },
            function(successResponse)
            {
                $scope.allTools = successResponse.data.data;
                $scope.allTools.splice(0, 0, allEntityObj);
                for(var t5=0; t5<$scope.allTools.length; t5++)
                {
                    for(var t6=0; t6<userGroupSuccessResponse.data.tool_list.length; t6++)
                    {
                        if(userGroupSuccessResponse.data.tool_list[t6] === $scope.allTools[t5].name)
                        {
                            $scope.userGroupData.parent_entity_id_tool_list.push($scope.allTools[t5]);
                        }
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            DeploymentUnitAll.get({
                page: 0,
                perpage: 0
            },
            function(successResponse)
            {
                $scope.allDU = successResponse.data;
                $scope.allDU.splice(0, 0, allEntityObj);
                for(var d1=0; d1<userGroupSuccessResponse.data.du_list.length; d1++)
                {
                    if(userGroupSuccessResponse.data.du_list[d1] === 'all')
                    {
                        $scope.userGroupData.parent_entity_id_du_list.push($scope.allDU[0]);
                    }
                    else
                    {
                        for(var d2=1; d2<$scope.allDU.length; d2++)
                        {
                            for(var d3=0; d3<$scope.allDU[d2].data.length; d3++)
                            {
                                if(userGroupSuccessResponse.data.du_list[d1] === $scope.allDU[d2].data[d3].name)
                                {
                                    $scope.userGroupData.parent_entity_id_du_list.push($scope.allDU[d2].data[d3]);
                                }
                            }
                        }
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            AllToolSet.get({
                page: 0,
                perpage: 0
            },
            function(alltoolsets)
            {
                $scope.allToolSets = alltoolsets.data.data;
                $scope.allToolSets.splice(0, 0, allEntityObj);
                for(var t7=0; t7<$scope.allToolSets.length; t7++)
                {
                    for(var t8=0; t8<userGroupSuccessResponse.data.toolset_list.length; t8++)
                    {
                        if(userGroupSuccessResponse.data.toolset_list[t8] === $scope.allToolSets[t7].name)
                        {
                            $scope.userGroupData.parent_entity_set_id_tool_list.push($scope.allToolSets[t7]);
                        }
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            DUSetAll.get({
                page: 0,
                perpage: 0
            },
            function(successResponse)
            {
                $scope.allDUSets = successResponse.data.data;
                $scope.allDUSets.splice(0, 0, allEntityObj);
                $scope.currentPage = successResponse.data.page;
                $scope.totalCount = successResponse.data.total;
                for(var d3=0; d3<$scope.allDUSets.length; d3++)
                {
                    for(var d4=0; d4<userGroupSuccessResponse.data.duset_list.length; d4++)
                    {
                        if(userGroupSuccessResponse.data.duset_list[d4] === $scope.allDUSets[d3].name)
                        {
                            $scope.userGroupData.parent_entity_set_id_du_list.push($scope.allDUSets[d3]);
                        }
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            $scope.machines = GetAllMachine.get({
            },
            function(successResponse){
                $scope.allMachines = successResponse.data.data;
                $scope.allMachines.splice(0, 0, allMachineEntityObj);
                for(var m1=0; m1<$scope.allMachines.length; m1++)
                {
                    for(var m2=0; m2<userGroupSuccessResponse.data.machine_id_list.length; m2++)
                    {
                        if(userGroupSuccessResponse.data.machine_id_list[m2] === $scope.allMachines[m1].machine_name)
                        {
                            $scope.userGroupData.machine_id_list.push($scope.allMachines[m1]);
                        }
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            MachineGroup.get({
            },
            function(successResponse)
            {
                $scope.allMachineGroups = successResponse.data.data;
                $scope.allMachineGroups.splice(0, 0, allMachineGroupEntityObj);
                for(var m3=0; m3<$scope.allMachineGroups.length; m3++)
                {
                    for(var m4=0; m4<userGroupSuccessResponse.data.machine_group_id_list.length; m4++)
                    {
                        if(userGroupSuccessResponse.data.machine_group_id_list[m4] === $scope.allMachineGroups[m3].group_name)
                        {
                            $scope.userGroupData.machine_group_id_list.push($scope.allMachineGroups[m3]);
                        }
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            Users.get({
                id:"all"
            },
            function(successResponse)
            {
                $scope.users = successResponse.data;
                for(var u1=0; u1<$scope.users.length; u1++)
                {
                    for(var u2=0; u2<userGroupSuccessResponse.data.users_id_list.length; u2++)
                    {
                        if(userGroupSuccessResponse.data.users_id_list[u2] === $scope.users[u1].user)
                        {
                            $scope.userGroupData.users_id_list.push($scope.users[u1]);
                        }
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
};
});
});
