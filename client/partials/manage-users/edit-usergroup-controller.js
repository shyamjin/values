define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

var editUserGroupControllerApp = angular.module('editUserGroupControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
editUserGroupControllerApp.controller('EditUserGroupController', function ($scope, $stateParams, Users, $state, $timeout, $rootScope, UserGroupView, TagsAll, GetAllTools, DeploymentUnitAll, AllToolSet, DUSetAll, MachineGroup, UserGroupEdit, GetAllMachine, Machine){
    $scope.userGroupData = {
        team_name : '',
        description : '',
        distribution_list : '',
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

    function remaining_up()
    {
        var allElements = document.getElementsByClassName('tag_popup');
        for(var i = 0; i < allElements.length; i++)
        {
            $(allElements[i]).slideUp();
        }
    }

    $scope.discardTeamChanges = function()
    {
        $state.go('users');
    };

    $scope.UserGroup = UserGroupView.get({
        id: $state.params.id
    },
    function(userGroupSuccessResponse)
    {
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

    $scope.showAddUser = function()
    {
        if(document.getElementById("add_user").style.display === "none" || document.getElementById("add_user").style.display === "")
        {
             remaining_up();
             $('#add_user').slideDown();
        }
        else
        {
           $('#add_user').slideUp();
        }
    };

    $scope.closeAddUsers = function()
    {
        $('#add_user').slideUp();
    };

    $scope.addUser = function(user)
    {
        var user_flag = 0;
        var ind = 0;
        if($scope.userGroupData.users_id_list.length>0)
        {
            for(var c=0;  c<$scope.userGroupData.users_id_list.length; c++)
            {
                if(user.user === $scope.userGroupData.users_id_list[c].user)
                {
                    user_flag++;
                    ind = c;
                }
            }

            if(user_flag===0)
            {
                $scope.userGroupData.users_id_list.push(user);
            }
            else
            {
                $scope.userGroupData.users_id_list.splice(ind, 1);
            }

        }
        else
        {
            $scope.userGroupData.users_id_list = [];
            $scope.userGroupData.users_id_list.push(user);
        }
    };

    $scope.removeUser = function(user)
    {
        var user_flag = 0;
        var ind = 0;
        if($scope.userGroupData.users_id_list.length>0)
        {
            for(var c=0;  c<$scope.userGroupData.users_id_list.length; c++)
            {
                if(user.user === $scope.userGroupData.users_id_list[c].user)
                {
                    user_flag++;
                    ind = c;
                }
            }
            if(user_flag===0)
            {
                $scope.userGroupData.users_id_list.push(user);
            }
            else
            {
                $scope.userGroupData.users_id_list.splice(ind, 1);
            }
         }
        else
        {
            $scope.userGroupData.users_id_list = [];
            $scope.userGroupData.users_id_list.push(user);
        }
    };

    $scope.isUserSelected = function(user)
    {
        var flag = 0;
        if(!$scope.userGroupData.users_id_list)
        {
            $scope.userGroupData.users_id_list = [];
        }
        for(var j=0; j<$scope.userGroupData.users_id_list.length; j++)
        {
            if(user === $scope.userGroupData.users_id_list[j].user)
            {
                flag++;
            }
        }
        if(flag>0)
        {
            return true;
        }
        else
        {
            return false;
        }
    };

    $scope.showAddTag = function()
    {
        if(document.getElementById("add_tag").style.display === "none" || document.getElementById("add_tag").style.display === "")
        {
            document.getElementById("add_tag").style.display = "block";
        }
        else
        {
           document.getElementById("add_tag").style.display = "none";
        }
    };

    $scope.closeAddTag = function()
    {
        document.getElementById("add_tag").style.display = "none";
    };

    $scope.selectTag = function(tag)
    {
        var tag_flag = 0;
        var ind = 0;
        if($scope.userGroupData.tag.length>0)
        {
            for(var c=0;  c<$scope.userGroupData.tag.length; c++)
            {
                if(tag.name===$scope.userGroupData.tag[c].name)
                {
                    tag_flag++;
                    ind = c;
                }
            }

            if(tag_flag===0)
            {
                $scope.userGroupData.tag.push(tag);
            }
            else
            {
                $scope.userGroupData.tag.splice(ind, 1);
            }
        }
        else
        {
            $scope.userGroupData.tag = [];
            $scope.userGroupData.tag.push(tag);
        }
    };

        $scope.isTagSelected = function(tag)
        {
            var flag = 0;
            if(!$scope.userGroupData.tag)
            {
                $scope.userGroupData.tag = [];
            }
            for(var j=0; j<$scope.userGroupData.tag.length; j++)
            {
                if(tag === $scope.userGroupData.tag[j].name)
                {
                    flag++;
                }
            }
            if(flag>0)
            {
                return true;
            }
            else
            {
                return false;
            }
        };

        $scope.showAddParentEntityTag = function()
        {
            if(document.getElementById("add_parent_entity_tag").style.display === "none" || document.getElementById("add_parent_entity_tag").style.display === "")
            {
                document.getElementById("add_parent_entity_tag").style.display = "block";
            }
            else
            {
               document.getElementById("add_parent_entity_tag").style.display = "none";
            }
        };

        $scope.closeAddParentEntityTag = function()
        {
            document.getElementById("add_parent_entity_tag").style.display = "none";
        };


        $scope.addParentEntityTag = function(tag)
        {
            var tag_flag = 0;
            var ind = 0;
            if($scope.userGroupData.parent_entity_tag_list.length>0)
            {
                for(var c=0;  c<$scope.userGroupData.parent_entity_tag_list.length; c++)
                {
                    if(tag.name===$scope.userGroupData.parent_entity_tag_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.userGroupData.parent_entity_tag_list.push(tag);
                }
                else
                {
                    $scope.userGroupData.parent_entity_tag_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.userGroupData.parent_entity_tag_list = [];
                $scope.userGroupData.parent_entity_tag_list.push(tag);
            }
        };

        $scope.isParentEntityTagSelected = function(tag)
        {
            var flag = 0;
            if(!$scope.userGroupData.parent_entity_tag_list)
            {
                $scope.userGroupData.parent_entity_tag_list = [];
            }
            for(var j=0; j<$scope.userGroupData.parent_entity_tag_list.length; j++)
            {
                if(tag === $scope.userGroupData.parent_entity_tag_list[j].name)
                {
                    flag++;
                }
            }
            if(flag>0)
            {
                return true;
            }
            else
            {
                return false;
            }
        };

        $scope.showAddParentEntitySetTag = function()
        {
            if(document.getElementById("add_parent_entity_set_tag").style.display === "none" || document.getElementById("add_parent_entity_set_tag").style.display === "")
            {
                document.getElementById("add_parent_entity_set_tag").style.display = "block";
            }
            else
            {
               document.getElementById("add_parent_entity_set_tag").style.display = "none";
            }
        };

        $scope.closeAddParentEntitySetTag = function()
        {
            document.getElementById("add_parent_entity_set_tag").style.display = "none";
        };


        $scope.addParentEntitySetTag = function(tag)
        {
            var tag_flag = 0;
            var ind = 0;
            if($scope.userGroupData.parent_entity_set_tag_list.length>0)
            {
                for(var c=0;  c<$scope.userGroupData.parent_entity_set_tag_list.length; c++)
                {
                    if(tag.name===$scope.userGroupData.parent_entity_set_tag_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    if(tag.name === 'all')
                    {
                        $scope.userGroupData.parent_entity_set_tag_list = [];
                        $scope.userGroupData.parent_entity_set_tag_list.push(tag);
                        if($scope.allTags.length>0)
                        {
                            for(var d=1; d<$scope.allTags.length; d++)
                            {
                                $scope.userGroupData.parent_entity_set_tag_list.push($scope.allTags[d]);
                            }
                        }
                    }
                    else
                    {
                        $scope.userGroupData.parent_entity_set_tag_list.push(tag);
                    }
                }
                else
                {
                    if(tag.name === 'all')
                    {
                        $scope.userGroupData.parent_entity_set_tag_list = [];
                    }
                    else
                    {
                        $scope.userGroupData.parent_entity_set_tag_list.splice(ind, 1);
                    }
                }

            }
            else
            {
                $scope.userGroupData.parent_entity_set_tag_list = [];
                $scope.userGroupData.parent_entity_set_tag_list.push(tag);
            }
        };

        $scope.isParentEntitySetTagSelected = function(tag)
        {
            var flag = 0;
            if(!$scope.userGroupData.parent_entity_set_tag_list)
            {
                $scope.userGroupData.parent_entity_set_tag_list = [];
            }
            for(var j=0; j<$scope.userGroupData.parent_entity_set_tag_list.length; j++)
            {
                if(tag === $scope.userGroupData.parent_entity_set_tag_list[j].name)
                {
                    flag++;
                }
            }
            if(flag>0)
            {
                return true;
            }
            else
            {
                return false;
            }
        };

        $scope.showAddParentEntityIdTool = function()
        {
            if(document.getElementById("add_parent_entity_tool").style.display === "none" || document.getElementById("add_parent_entity_tool").style.display === "")
            {
                document.getElementById("add_parent_entity_tool").style.display = "block";
            }
            else
            {
               document.getElementById("add_parent_entity_tool").style.display = "none";
            }
        };

        $scope.closeAddParentEntityIdTool = function()
        {
            document.getElementById("add_parent_entity_tool").style.display = "none";
        };


        $scope.addParentEntityIdTool = function(tool)
        {
            var tag_flag = 0;
            var ind = 0;
            if($scope.userGroupData.parent_entity_id_tool_list.length>0)
            {
                for(var c=0;  c<$scope.userGroupData.parent_entity_id_tool_list.length; c++)
                {
                    if(tool.name===$scope.userGroupData.parent_entity_id_tool_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.userGroupData.parent_entity_id_tool_list.push(tool);
                }
                else
                {
                    $scope.userGroupData.parent_entity_id_tool_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.userGroupData.parent_entity_id_tool_list = [];
                $scope.userGroupData.parent_entity_id_tool_list.push(tool);
            }
        };

        $scope.isParentEntityIdToolSelected = function(tool)
        {
            var flag = 0;
            if(!$scope.userGroupData.parent_entity_id_tool_list)
            {
                $scope.userGroupData.parent_entity_id_tool_list = [];
            }
            for(var j=0; j<$scope.userGroupData.parent_entity_id_tool_list.length; j++)
            {
                if(tool === $scope.userGroupData.parent_entity_id_tool_list[j].name)
                {
                    flag++;
                }
            }
            if(flag>0)
            {
                return true;
            }
            else
            {
                return false;
            }
        };

        $scope.showAddParentEntityIdDU = function()
        {
            if(document.getElementById("add_parent_entity_du").style.display === "none" || document.getElementById("add_parent_entity_du").style.display === "")
            {
                document.getElementById("add_parent_entity_du").style.display = "block";
            }
            else
            {
               document.getElementById("add_parent_entity_du").style.display = "none";
            }
        };

        $scope.closeAddParentEntityIdDU = function()
        {
            document.getElementById("add_parent_entity_du").style.display = "none";
        };


        $scope.addParentEntityIdDU = function(du)
        {
            var tag_flag = 0;
            var ind = 0;
            if($scope.userGroupData.parent_entity_id_du_list.length>0)
            {
                for(var c=0;  c<$scope.userGroupData.parent_entity_id_du_list.length; c++)
                {
                    if(du.name===$scope.userGroupData.parent_entity_id_du_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.userGroupData.parent_entity_id_du_list.push(du);
                }
                else
                {
                    $scope.userGroupData.parent_entity_id_du_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.userGroupData.parent_entity_id_du_list = [];
                $scope.userGroupData.parent_entity_id_du_list.push(du);
            }
        };

        $scope.isParentEntityIdDUSelected = function(du)
        {
            var flag = 0;
            if(!$scope.userGroupData.parent_entity_id_du_list)
            {
                $scope.userGroupData.parent_entity_id_du_list = [];
            }
            for(var j=0; j<$scope.userGroupData.parent_entity_id_du_list.length; j++)
            {
                if(du === $scope.userGroupData.parent_entity_id_du_list[j].name)
                {
                    flag++;
                }
            }
            if(flag>0)
            {
                return true;
            }
            else
            {
                return false;
            }
        };

        $scope.showAddParentEntityIdToolSet = function()
        {
            if(document.getElementById("add_parent_entity_set_tool").style.display === "none" || document.getElementById("add_parent_entity_set_tool").style.display === "")
            {
                document.getElementById("add_parent_entity_set_tool").style.display = "block";
            }
            else
            {
               document.getElementById("add_parent_entity_set_tool").style.display = "none";
            }
        };

        $scope.closeAddParentEntityIdToolSet = function()
        {
            document.getElementById("add_parent_entity_set_tool").style.display = "none";
        };


        $scope.addParentEntityIdToolSet = function(toolset)
        {
            var tag_flag = 0;
            var ind = 0;
            if($scope.userGroupData.parent_entity_set_id_tool_list.length>0)
            {
                for(var c=0;  c<$scope.userGroupData.parent_entity_set_id_tool_list.length; c++)
                {
                    if(toolset.name===$scope.userGroupData.parent_entity_set_id_tool_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.userGroupData.parent_entity_set_id_tool_list.push(toolset);
                }
                else
                {
                    $scope.userGroupData.parent_entity_set_id_tool_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.userGroupData.parent_entity_set_id_tool_list = [];
                $scope.userGroupData.parent_entity_set_id_tool_list.push(toolset);
            }
        };

        $scope.isParentEntityIdToolSetSelected = function(toolset)
        {
            var flag = 0;
            if(!$scope.userGroupData.parent_entity_set_id_tool_list)
            {
                $scope.userGroupData.parent_entity_set_id_tool_list = [];
            }
            for(var j=0; j<$scope.userGroupData.parent_entity_set_id_tool_list.length; j++)
            {
                if(toolset === $scope.userGroupData.parent_entity_set_id_tool_list[j].name)
                {
                    flag++;
                }
            }
            if(flag>0)
            {
                return true;
            }
            else
            {
                return false;
            }
        };

        $scope.showAddParentEntityIdDUSet = function()
        {
            if(document.getElementById("add_parent_entity_set_du").style.display === "none" || document.getElementById("add_parent_entity_set_du").style.display === "")
            {
                document.getElementById("add_parent_entity_set_du").style.display = "block";
            }
            else
            {
               document.getElementById("add_parent_entity_set_du").style.display = "none";
            }
        };

        $scope.closeAddParentEntityIdDUSet = function()
        {
            document.getElementById("add_parent_entity_set_du").style.display = "none";
        };


        $scope.addParentEntityIdDUSet = function(duset)
        {
            var tag_flag = 0;
            var ind = 0;
            if($scope.userGroupData.parent_entity_set_id_du_list.length>0)
            {
                for(var c=0;  c<$scope.userGroupData.parent_entity_set_id_du_list.length; c++)
                {
                    if(duset.name===$scope.userGroupData.parent_entity_set_id_du_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.userGroupData.parent_entity_set_id_du_list.push(duset);
                }
                else
                {
                    $scope.userGroupData.parent_entity_set_id_du_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.userGroupData.parent_entity_set_id_du_list = [];
                $scope.userGroupData.parent_entity_set_id_du_list.push(duset);
            }
        };

        $scope.isParentEntityIdDUSetSelected = function(duset)
        {
            var flag = 0;
            if(!$scope.userGroupData.parent_entity_set_id_du_list)
            {
                $scope.userGroupData.parent_entity_set_id_du_list = [];
            }
            for(var j=0; j<$scope.userGroupData.parent_entity_set_id_du_list.length; j++)
            {
                if(duset === $scope.userGroupData.parent_entity_set_id_du_list[j].name)
                {
                    flag++;
                }
            }
            if(flag>0)
            {
                return true;
            }
            else
            {
                return false;
            }
        };

        $scope.showAddMachine = function()
        {
            if(document.getElementById("add_machine").style.display === "none" || document.getElementById("add_machine").style.display === "")
            {
                document.getElementById("add_machine").style.display = "block";
            }
            else
            {
               document.getElementById("add_machine").style.display = "none";
            }
        };

        $scope.closeAddMachine = function()
        {
            document.getElementById("add_machine").style.display = "none";
        };


        $scope.addMachine = function(machine)
        {
            var tag_flag = 0;
            var ind = 0;
            if($scope.userGroupData.machine_id_list.length>0)
            {
                for(var c=0;  c<$scope.userGroupData.machine_id_list.length; c++)
                {
                    if(machine.machine_name===$scope.userGroupData.machine_id_list[c].machine_name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.userGroupData.machine_id_list.push(machine);
                }
                else
                {
                    $scope.userGroupData.machine_id_list.splice(ind, 1);
                }
            }
            else
            {
                $scope.userGroupData.machine_id_list = [];
                $scope.userGroupData.machine_id_list.push(machine);
            }
        };

        $scope.isMachineSelected = function(machine)
        {
            var flag = 0;
            if(!$scope.userGroupData.machine_id_list)
            {
                $scope.userGroupData.machine_id_list = [];
            }
            for(var j=0; j<$scope.userGroupData.machine_id_list.length; j++)
            {
                if(machine === $scope.userGroupData.machine_id_list[j].machine_name)
                {
                    flag++;
                }
            }
            if(flag>0)
            {
                return true;
            }
            else
            {
                return false;
            }
        };

        $scope.showAddMachineGroup = function()
        {
            if(document.getElementById("add_machine_group").style.display === "none" || document.getElementById("add_machine_group").style.display === "")
            {
                document.getElementById("add_machine_group").style.display = "block";
            }
            else
            {
               document.getElementById("add_machine_group").style.display = "none";
            }
        };

        $scope.closeAddMachineGroup = function()
        {
            document.getElementById("add_machine_group").style.display = "none";
        };


        $scope.addMachineGroup = function(group)
        {
            var tag_flag = 0;
            var ind = 0;
            if($scope.userGroupData.machine_group_id_list.length>0)
            {
                for(var c=0;  c<$scope.userGroupData.machine_group_id_list.length; c++)
                {
                    if(group.group_name===$scope.userGroupData.machine_group_id_list[c].group_name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.userGroupData.machine_group_id_list.push(group);
                }
                else
                {
                    $scope.userGroupData.machine_group_id_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.userGroupData.machine_group_id_list = [];
                $scope.userGroupData.machine_group_id_list.push(group);
            }
        };

        $scope.isMachineGroupSelected = function(group)
        {
            var flag = 0;
            if(!$scope.userGroupData.machine_group_id_list)
            {
                $scope.userGroupData.machine_group_id_list = [];
            }
            for(var j=0; j<$scope.userGroupData.machine_group_id_list.length; j++)
            {
                if(group === $scope.userGroupData.machine_group_id_list[j].group_name)
                {
                    flag++;
                }
            }
            if(flag>0)
            {
                return true;
            }
            else
            {
                return false;
            }
        };

        $scope.updateUserGroup = function(form)
        {
            var jsonData = {
                _id : {
                    oid : $scope.userGroupData.id
                },
                team_name : '',
                description : '',
                distribution_list : '',
                homepage : '',
                users_id_list : [],
                tag_id_list : [],
                parent_entity_tag_list : [],
                parent_entity_set_tag_list : [],
                parent_entity_id_tool_list : [],
                parent_entity_id_du_list : [],
                parent_entity_tool_set_id_list : [],
                parent_entity_du_set_id_list : [],
                machine_id_list : [],
                machine_group_id_list : []
            };

            $scope.usergroupadd_errors=[];
            jsonData.team_name = $scope.userGroupData.team_name;
            jsonData.description = $scope.userGroupData.description;
            jsonData.distribution_list = $scope.userGroupData.distribution_list;
            if($scope.userGroupData.homepage === 'Tool Dashboard' || $scope.userGroupData.homepage === '' || $scope.userGroupData.homepage === null)
            {
                jsonData.homepage = 'dashboard';
            }
            else
            {
                jsonData.homepage = 'duDashboard';
            }

            $scope.usergroupadd_errors.team_name ='';
            if($scope.userGroupData.team_name==='' || $scope.userGroupData.team_name===undefined )
            {
                $scope.usergroupadd_errors.team_name ="Please enter team name!";
                return false;
            }
            else
            {
                $scope.usergroupadd_errors.team_name ='';
            }

            if($scope.userGroupData.distribution_list === '' || $scope.userGroupData.distribution_list === undefined || $scope.userGroupData.distribution_list === null)
            {
                $scope.usergroupadd_errors.distribution_list ="Please enter distribution list!";
                return false;
            }
            else
            {
                var support = $scope.userGroupData.distribution_list;
                var atpos = support.indexOf("@");
                var dotpos = support.lastIndexOf(".");
                if (atpos<1 || dotpos<atpos+2 || dotpos+2>=support.length) {
                    $scope.usergroupadd_errors.distribution_list = 'Please enter valid email address in distribution list!';
                    return false;
                }
                else
                {
                    $scope.usergroupadd_errors.distribution_list ='';
                }
            }

            $scope.usergroupadd_errors.description ='';

            if($scope.userGroupData.users_id_list.length>0)
            {
                for(var i=0; i<$scope.userGroupData.users_id_list.length; i++)
                {
                    jsonData.users_id_list.push($scope.userGroupData.users_id_list[i]._id.$oid);
                }
            }

            if($scope.userGroupData.tag.length>0)
            {
                for(var j=0; j<$scope.userGroupData.tag.length; j++)
                {
                    if($scope.userGroupData.tag[j].name === 'all')
                    {
                        jsonData.tag_id_list.push('all');
                    }
                    else
                    {
                        jsonData.tag_id_list.push($scope.userGroupData.tag[j]._id.$oid);
                    }
                }
            }

            if($scope.userGroupData.parent_entity_tag_list.length>0)
            {
                for(var k=0; k<$scope.userGroupData.parent_entity_tag_list.length; k++)
                {
                    if($scope.userGroupData.parent_entity_tag_list[k].name === 'all')
                    {
                        jsonData.parent_entity_tag_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_tag_list.push($scope.userGroupData.parent_entity_tag_list[k]._id.$oid);
                    }
                }
            }

            if($scope.userGroupData.parent_entity_set_tag_list.length>0)
            {
                for(var l=0; l<$scope.userGroupData.parent_entity_set_tag_list.length; l++)
                {
                    if($scope.userGroupData.parent_entity_set_tag_list[l].name === 'all')
                    {
                        jsonData.parent_entity_set_tag_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_set_tag_list.push($scope.userGroupData.parent_entity_set_tag_list[l]._id.$oid);
                    }
                }
            }

            if($scope.userGroupData.parent_entity_id_tool_list.length>0)
            {
                for(var m=0; m<$scope.userGroupData.parent_entity_id_tool_list.length; m++)
                {
                    if($scope.userGroupData.parent_entity_id_tool_list[m].name === 'all')
                    {
                        jsonData.parent_entity_id_tool_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_id_tool_list.push($scope.userGroupData.parent_entity_id_tool_list[m]._id.$oid);
                    }
                }
            }

            if($scope.userGroupData.parent_entity_id_du_list.length>0)
            {
                for(var n=0; n<$scope.userGroupData.parent_entity_id_du_list.length; n++)
                {
                    if($scope.userGroupData.parent_entity_id_du_list[n].name === 'all')
                    {
                        jsonData.parent_entity_id_du_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_id_du_list.push($scope.userGroupData.parent_entity_id_du_list[n]._id.$oid);
                    }
                }
            }

            if($scope.userGroupData.parent_entity_set_id_tool_list.length>0)
            {
                for(var o=0; o<$scope.userGroupData.parent_entity_set_id_tool_list.length; o++)
                {
                    if($scope.userGroupData.parent_entity_set_id_tool_list[o].name === 'all')
                    {
                        jsonData.parent_entity_tool_set_id_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_tool_set_id_list.push($scope.userGroupData.parent_entity_set_id_tool_list[o]._id.$oid);
                    }
                }
            }

            if($scope.userGroupData.parent_entity_set_id_du_list.length>0)
            {
                for(var p=0; p<$scope.userGroupData.parent_entity_set_id_du_list.length; p++)
                {
                    if($scope.userGroupData.parent_entity_set_id_du_list[p].name === 'all')
                    {
                        jsonData.parent_entity_du_set_id_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_du_set_id_list.push($scope.userGroupData.parent_entity_set_id_du_list[p]._id.$oid);
                    }
                }
            }

            if($scope.userGroupData.machine_id_list.length>0)
            {
                for(var q=0; q<$scope.userGroupData.machine_id_list.length; q++)
                {
                    if($scope.userGroupData.machine_id_list[q].machine_name === 'all')
                    {
                        jsonData.machine_id_list.push('all');
                    }
                    else
                    {
                        jsonData.machine_id_list.push($scope.userGroupData.machine_id_list[q]._id.$oid);
                    }
                }
            }

            if($scope.userGroupData.machine_group_id_list.length>0)
            {
                for(var s=0; s<$scope.userGroupData.machine_group_id_list.length; s++)
                {
                    if($scope.userGroupData.machine_group_id_list[s].group_name === 'all')
                    {
                        jsonData.machine_group_id_list.push('all');
                    }
                    else
                    {
                        jsonData.machine_group_id_list.push($scope.userGroupData.machine_group_id_list[s]._id.$oid);
                    }
                }
            }

            $scope.UserGroupStatus = UserGroupEdit.update(jsonData, function(userGroupUpdateSuccessResponse){
                $state.go('manageUserGroups');
                $rootScope.handleResponse(userGroupUpdateSuccessResponse);
            },
            function(userGroupUpdateErrorResponse){
                $rootScope.handleResponse(userGroupUpdateErrorResponse);
            });
        };

 });
});
