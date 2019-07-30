define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

var createUserGroupControllerApp = angular.module('createUserGroupControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
createUserGroupControllerApp.controller('CreateUserGroupController', function ($scope, $stateParams, GetAllMachine, Machine, $state, $rootScope, $timeout, Users,createUserGroup, TagsAll, GetAllTools, DeploymentUnitAll, AllToolSet, DUSetAll, MachineGroup) {
    $scope.newUserGroupData = {
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

    $scope.handleSelection=function(userItem)
    {
        var idx=$scope.userData.indexOf(userItem);
        if(idx>-1)
        {
            $scope.userData.splice(idx,1);
        }
        else
        {
            $scope.userData.push(userItem);
        }
    };

        Users.get({
            id:"all"
        },
        function(successResponse){
            $scope.users = successResponse.data;
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
            $scope.currentPage = successResponse.page;
            $scope.totalCount = successResponse.total;
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
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

        DUSetAll.get({
        },
        function(successResponse)
        {
            $scope.allDUSets = successResponse.data.data;
            $scope.allDUSets.splice(0, 0, allEntityObj);
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

        $scope.machines = GetAllMachine.get({
        },
        function(successResponse)
        {
            $scope.allMachines = successResponse.data.data;
            $scope.allMachines.splice(0, 0, allMachineEntityObj);
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
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

        TagsAll.get({
        },
        function(successResponse)
        {
            $scope.allTags = successResponse;
            $scope.allTags.splice(0, 0, allEntityObj);
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
            if($scope.newUserGroupData.users_id_list.length>0)
            {
                for(var c=0;  c<$scope.newUserGroupData.users_id_list.length; c++)
                {
                    if(user.user === $scope.newUserGroupData.users_id_list[c].user)
                    {
                        user_flag++;
                        ind = c;
                    }
                }

                if(user_flag===0)
                {
                    $scope.newUserGroupData.users_id_list.push(user);
                }
                else
                {
                    $scope.newUserGroupData.users_id_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.newUserGroupData.users_id_list = [];
                $scope.newUserGroupData.users_id_list.push(user);
            }
        };

        $scope.removeUser = function(user)
        {
            var user_flag = 0;
            var ind = 0;
            if($scope.newUserGroupData.users_id_list.length>0)
            {
                for(var c=0;  c<$scope.newUserGroupData.users_id_list.length; c++)
                {
                    if(user.user === $scope.newUserGroupData.users_id_list[c].user)
                    {
                        user_flag++;
                        ind = c;
                    }
                }

                if(user_flag===0)
                {
                    $scope.newUserGroupData.users_id_list.push(user);
                }
                else
                {
                    $scope.newUserGroupData.users_id_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.newUserGroupData.users_id_list = [];
                $scope.newUserGroupData.users_id_list.push(user);
            }
        };

        $scope.isUserSelected = function(user)
        {
            var flag = 0;
            if(!$scope.newUserGroupData.users_id_list)
            {
                $scope.newUserGroupData.users_id_list = [];
            }
            for(var j=0; j<$scope.newUserGroupData.users_id_list.length; j++)
            {
                if(user === $scope.newUserGroupData.users_id_list[j].user)
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
            if($scope.newUserGroupData.tag.length>0)
            {
                for(var c=0;  c<$scope.newUserGroupData.tag.length; c++)
                {
                    if(tag.name===$scope.newUserGroupData.tag[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.newUserGroupData.tag.push(tag);
                }
                else
                {
                    $scope.newUserGroupData.tag.splice(ind, 1);
                }

            }
            else
            {
                $scope.newUserGroupData.tag = [];
                $scope.newUserGroupData.tag.push(tag);
            }
        };

        $scope.isTagSelected = function(tag)
        {
            var flag = 0;
            if(!$scope.newUserGroupData.tag)
            {
                $scope.newUserGroupData.tag = [];
            }
            for(var j=0; j<$scope.newUserGroupData.tag.length; j++)
            {
                if(tag === $scope.newUserGroupData.tag[j].name)
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
            if($scope.newUserGroupData.parent_entity_tag_list.length>0)
            {
                for(var c=0;  c<$scope.newUserGroupData.parent_entity_tag_list.length; c++)
                {
                    if(tag.name===$scope.newUserGroupData.parent_entity_tag_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.newUserGroupData.parent_entity_tag_list.push(tag);
                }
                else
                {
                    $scope.newUserGroupData.parent_entity_tag_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.newUserGroupData.parent_entity_tag_list = [];
                $scope.newUserGroupData.parent_entity_tag_list.push(tag);
            }
        };

        $scope.isParentEntityTagSelected = function(tag)
        {
            var flag = 0;
            if(!$scope.newUserGroupData.parent_entity_tag_list)
            {
                $scope.newUserGroupData.parent_entity_tag_list = [];
            }
            for(var j=0; j<$scope.newUserGroupData.parent_entity_tag_list.length; j++)
            {
                if(tag === $scope.newUserGroupData.parent_entity_tag_list[j].name)
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
            if($scope.newUserGroupData.parent_entity_set_tag_list.length>0)
            {
                for(var c=0;  c<$scope.newUserGroupData.parent_entity_set_tag_list.length; c++)
                {
                    if(tag.name===$scope.newUserGroupData.parent_entity_set_tag_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.newUserGroupData.parent_entity_set_tag_list.push(tag);
                }
                else
                {
                    $scope.newUserGroupData.parent_entity_set_tag_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.newUserGroupData.parent_entity_set_tag_list = [];
                $scope.newUserGroupData.parent_entity_set_tag_list.push(tag);
            }
        };

        $scope.isParentEntitySetTagSelected = function(tag)
        {
            var flag = 0;
            if(!$scope.newUserGroupData.parent_entity_set_tag_list)
            {
                $scope.newUserGroupData.parent_entity_set_tag_list = [];
            }
            for(var j=0; j<$scope.newUserGroupData.parent_entity_set_tag_list.length; j++)
            {
                if(tag === $scope.newUserGroupData.parent_entity_set_tag_list[j].name)
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
            if($scope.newUserGroupData.parent_entity_id_tool_list.length>0)
            {
                for(var c=0;  c<$scope.newUserGroupData.parent_entity_id_tool_list.length; c++)
                {
                    if(tool.name===$scope.newUserGroupData.parent_entity_id_tool_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.newUserGroupData.parent_entity_id_tool_list.push(tool);
                }
                else
                {
                    $scope.newUserGroupData.parent_entity_id_tool_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.newUserGroupData.parent_entity_id_tool_list = [];
                $scope.newUserGroupData.parent_entity_id_tool_list.push(tool);
            }
        };

        $scope.isParentEntityIdToolSelected = function(tool)
        {
            var flag = 0;
            if(!$scope.newUserGroupData.parent_entity_id_tool_list)
            {
                $scope.newUserGroupData.parent_entity_id_tool_list = [];
            }
            for(var j=0; j<$scope.newUserGroupData.parent_entity_id_tool_list.length; j++)
            {
                if(tool === $scope.newUserGroupData.parent_entity_id_tool_list[j].name)
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
            if($scope.newUserGroupData.parent_entity_id_du_list.length>0)
            {
                for(var c=0;  c<$scope.newUserGroupData.parent_entity_id_du_list.length; c++)
                {
                    if(du.name===$scope.newUserGroupData.parent_entity_id_du_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.newUserGroupData.parent_entity_id_du_list.push(du);
                }
                else
                {
                    $scope.newUserGroupData.parent_entity_id_du_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.newUserGroupData.parent_entity_id_du_list = [];
                $scope.newUserGroupData.parent_entity_id_du_list.push(du);
            }
        };

        $scope.isParentEntityIdDUSelected = function(du)
        {
            var flag = 0;
            if(!$scope.newUserGroupData.parent_entity_id_du_list)
            {
                $scope.newUserGroupData.parent_entity_id_du_list = [];
            }
            for(var j=0; j<$scope.newUserGroupData.parent_entity_id_du_list.length; j++)
            {
                if(du === $scope.newUserGroupData.parent_entity_id_du_list[j].name)
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
            if($scope.newUserGroupData.parent_entity_set_id_tool_list.length>0)
            {
                for(var c=0;  c<$scope.newUserGroupData.parent_entity_set_id_tool_list.length; c++)
                {
                    if(toolset.name===$scope.newUserGroupData.parent_entity_set_id_tool_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.newUserGroupData.parent_entity_set_id_tool_list.push(toolset);
                }
                else
                {
                    $scope.newUserGroupData.parent_entity_set_id_tool_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.newUserGroupData.parent_entity_set_id_tool_list = [];
                $scope.newUserGroupData.parent_entity_set_id_tool_list.push(toolset);
            }
        };

        $scope.isParentEntityIdToolSetSelected = function(toolset)
        {
            var flag = 0;
            if(!$scope.newUserGroupData.parent_entity_set_id_tool_list)
            {
                $scope.newUserGroupData.parent_entity_set_id_tool_list = [];
            }
            for(var j=0; j<$scope.newUserGroupData.parent_entity_set_id_tool_list.length; j++)
            {
                if(toolset === $scope.newUserGroupData.parent_entity_set_id_tool_list[j].name)
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
            if($scope.newUserGroupData.parent_entity_set_id_du_list.length>0)
            {
                for(var c=0;  c<$scope.newUserGroupData.parent_entity_set_id_du_list.length; c++)
                {
                    if(duset.name===$scope.newUserGroupData.parent_entity_set_id_du_list[c].name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.newUserGroupData.parent_entity_set_id_du_list.push(duset);
                }
                else
                {
                    $scope.newUserGroupData.parent_entity_set_id_du_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.newUserGroupData.parent_entity_set_id_du_list = [];
                $scope.newUserGroupData.parent_entity_set_id_du_list.push(duset);
            }
        };

        $scope.isParentEntityIdDUSetSelected = function(duset)
        {
            var flag = 0;
            if(!$scope.newUserGroupData.parent_entity_set_id_du_list)
            {
                $scope.newUserGroupData.parent_entity_set_id_du_list = [];
            }
            for(var j=0; j<$scope.newUserGroupData.parent_entity_set_id_du_list.length; j++)
            {
                if(duset === $scope.newUserGroupData.parent_entity_set_id_du_list[j].name)
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
            if($scope.newUserGroupData.machine_id_list.length>0)
            {
                for(var c=0;  c<$scope.newUserGroupData.machine_id_list.length; c++)
                {
                    if(machine.machine_name===$scope.newUserGroupData.machine_id_list[c].machine_name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.newUserGroupData.machine_id_list.push(machine);
                }
                else
                {
                    $scope.newUserGroupData.machine_id_list.splice(ind, 1);
                }
            }
            else
            {
                $scope.newUserGroupData.machine_id_list = [];
                $scope.newUserGroupData.machine_id_list.push(machine);
            }
        };

        $scope.isMachineSelected = function(machine)
        {
            var flag = 0;
            if(!$scope.newUserGroupData.machine_id_list)
            {
                $scope.newUserGroupData.machine_id_list = [];
            }
            for(var j=0; j<$scope.newUserGroupData.machine_id_list.length; j++)
            {
                if(machine === $scope.newUserGroupData.machine_id_list[j].machine_name)
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
            if($scope.newUserGroupData.machine_group_id_list.length>0)
            {
                for(var c=0;  c<$scope.newUserGroupData.machine_group_id_list.length; c++)
                {
                    if(group.group_name===$scope.newUserGroupData.machine_group_id_list[c].group_name)
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.newUserGroupData.machine_group_id_list.push(group);
                }
                else
                {
                    $scope.newUserGroupData.machine_group_id_list.splice(ind, 1);
                }

            }
            else
            {
                $scope.newUserGroupData.machine_group_id_list = [];
                $scope.newUserGroupData.machine_group_id_list.push(group);
            }
        };

        $scope.isMachineGroupSelected = function(group)
        {
            var flag = 0;
            if(!$scope.newUserGroupData.machine_group_id_list)
            {
                $scope.newUserGroupData.machine_group_id_list = [];
            }
            for(var j=0; j<$scope.newUserGroupData.machine_group_id_list.length; j++)
            {
                if(group === $scope.newUserGroupData.machine_group_id_list[j].group_name)
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

        $scope.addUserGroup = function(form)
        {
            var jsonData = {
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
            jsonData.team_name = $scope.newUserGroupData.teamName;
            jsonData.description = $scope.newUserGroupData.description;
            jsonData.distribution_list = $scope.newUserGroupData.distribution_list;
            if($scope.newUserGroupData.homepage === 'Tool Dashboard' || $scope.newUserGroupData.homepage === '' || $scope.newUserGroupData.homepage === null)
            {
                jsonData.homepage = 'dashboard';
            }
            else
            {
                jsonData.homepage = 'duDashboard';
            }

            $scope.usergroupadd_errors.team_name ='';
            if($scope.newUserGroupData.teamName==='' || $scope.newUserGroupData.teamName===undefined )
            {
                $scope.usergroupadd_errors.team_name ="Please enter team name!";
                return false;
            }
            else
            {
                $scope.usergroupadd_errors.team_name ='';
            }

            if($scope.newUserGroupData.distribution_list==='' || $scope.newUserGroupData.distribution_list===undefined )
            {
                $scope.usergroupadd_errors.distribution_list ="Please enter distribution list!";
                return false;
            }
            else
            {
                var support = $scope.newUserGroupData.distribution_list;
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

            if($scope.newUserGroupData.users_id_list.length>0)
            {
                for(var i=0; i<$scope.newUserGroupData.users_id_list.length; i++)
                {
                    jsonData.users_id_list.push($scope.newUserGroupData.users_id_list[i]._id.$oid);
                }
            }

            if($scope.newUserGroupData.tag.length>0)
            {
                for(var j=0; j<$scope.newUserGroupData.tag.length; j++)
                {
                    if($scope.newUserGroupData.tag[j].name === 'all')
                    {
                        jsonData.tag_id_list.push('all');
                    }
                    else
                    {
                        jsonData.tag_id_list.push($scope.newUserGroupData.tag[j]._id.$oid);
                    }
                }
            }

            if($scope.newUserGroupData.parent_entity_tag_list.length>0)
            {
                for(var k=0; k<$scope.newUserGroupData.parent_entity_tag_list.length; k++)
                {
                    if($scope.newUserGroupData.parent_entity_tag_list[k].name === 'all')
                    {
                        jsonData.parent_entity_tag_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_tag_list.push($scope.newUserGroupData.parent_entity_tag_list[k]._id.$oid);
                    }
                }
            }

            if($scope.newUserGroupData.parent_entity_set_tag_list.length>0)
            {
                for(var l=0; l<$scope.newUserGroupData.parent_entity_set_tag_list.length; l++)
                {
                    if($scope.newUserGroupData.parent_entity_set_tag_list[l].name === 'all')
                    {
                        jsonData.parent_entity_set_tag_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_set_tag_list.push($scope.newUserGroupData.parent_entity_set_tag_list[l]._id.$oid);
                    }
                }
            }

            if($scope.newUserGroupData.parent_entity_id_tool_list.length>0)
            {
                for(var m=0; m<$scope.newUserGroupData.parent_entity_id_tool_list.length; m++)
                {
                    if($scope.newUserGroupData.parent_entity_id_tool_list[m].name === 'all')
                    {
                        jsonData.parent_entity_id_tool_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_id_tool_list.push($scope.newUserGroupData.parent_entity_id_tool_list[m]._id.$oid);
                    }
                }
            }

            if($scope.newUserGroupData.parent_entity_id_du_list.length>0)
            {
                for(var n=0; n<$scope.newUserGroupData.parent_entity_id_du_list.length; n++)
                {
                    if($scope.newUserGroupData.parent_entity_id_du_list[n].name === 'all')
                    {
                        jsonData.parent_entity_id_du_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_id_du_list.push($scope.newUserGroupData.parent_entity_id_du_list[n]._id.$oid);
                    }
                }
            }

            if($scope.newUserGroupData.parent_entity_set_id_tool_list.length>0)
            {
                for(var o=0; o<$scope.newUserGroupData.parent_entity_set_id_tool_list.length; o++)
                {
                    if($scope.newUserGroupData.parent_entity_set_id_tool_list[o].name === 'all')
                    {
                        jsonData.parent_entity_tool_set_id_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_tool_set_id_list.push($scope.newUserGroupData.parent_entity_set_id_tool_list[o]._id.$oid);
                    }
                }
            }

            if($scope.newUserGroupData.parent_entity_set_id_du_list.length>0)
            {
                for(var p=0; p<$scope.newUserGroupData.parent_entity_set_id_du_list.length; p++)
                {
                    if($scope.newUserGroupData.parent_entity_set_id_du_list[p].name === 'all')
                    {
                        jsonData.parent_entity_du_set_id_list.push('all');
                    }
                    else
                    {
                        jsonData.parent_entity_du_set_id_list.push($scope.newUserGroupData.parent_entity_set_id_du_list[p]._id.$oid);
                    }
                }
            }

            if($scope.newUserGroupData.machine_id_list.length>0)
            {
                for(var q=0; q<$scope.newUserGroupData.machine_id_list.length; q++)
                {
                    if($scope.newUserGroupData.machine_id_list[q].machine_name === 'all')
                    {
                        jsonData.machine_id_list.push('all');
                    }
                    else
                    {
                        jsonData.machine_id_list.push($scope.newUserGroupData.machine_id_list[q]._id.$oid);
                    }
                }
            }

            if($scope.newUserGroupData.machine_group_id_list.length>0)
            {
                for(var s=0; s<$scope.newUserGroupData.machine_group_id_list.length; s++)
                {
                    if($scope.newUserGroupData.machine_group_id_list[s].group_name === 'all')
                    {
                        jsonData.machine_group_id_list.push('all');
                    }
                    else
                    {
                        jsonData.machine_group_id_list.push($scope.newUserGroupData.machine_group_id_list[s]._id.$oid);
                    }
                }
            }

            $scope.userGroupStatus = createUserGroup.save(jsonData, function(userGroupSuccessAddResponse){
                $state.go('manageUserGroups');
                $rootScope.handleResponse(userGroupSuccessAddResponse);
            },
            function(userGroupErrorAddResponse){
                $rootScope.handleResponse(userGroupErrorAddResponse);
            });
        };
});
});
