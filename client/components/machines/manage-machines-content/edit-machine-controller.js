define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'toolTips',
'userServicesApp', 'machineServicesApp'],function (app) {
  'use strict';

    var editMachineControllerApp = angular.module('editMachineControllerApp', ['ui.router', '720kb.tooltips',
    'userServicesApp', 'machineServicesApp']);

    editMachineControllerApp.controller('EditMachineController', function ($scope,$rootScope, $stateParams, GetAllMachine, GetAllMachineTypes, Machine, $window, $state, UpdateMachine, Users, ViewFavouriteMachine, FavMachineDelete, AddFavouriteMachine, UserProfile, TestMachine, MachineGroup, TagsAll, MachineDelete,UserGroup, GetDeploymentHistory) {
    $scope.hideShowMoreMachine = false;
    $scope.machineNameFilterFlag = true;
    $scope.hostFilterFlag = false;
    $scope.machineTypeFilterFlag = false;
    $scope.tagsFilterFlag = false;
    var machineNameFilter = "";
    var hostFilter ="";
    var machineTypeFilter = [];
    var tagsFilter = [];
    $scope.flexibleAttributes = {};
    $scope.faNameValueMap = {};
    $scope.faDefLoaded = function(faDef){
        $scope.flexibleAttributes = faDef;
    };
    $scope.envVars = [];

    $scope.useredit_errors = {
        password : '',
        confirmpassword : ''
    };
    $scope.selectedData = {
        password : ''
    };

    $scope.revertDeployment = {
            'duDataList' : []
    };

    $scope.permittedUsers =  [];
    $scope.permitted_teams = [];
    $scope.selectedMachineName = '';
    $scope.ToolsOnMachine = [];
    $scope.includedIn = [];
    $scope.wasFavourite = "";
    var machine_id = "";
    $scope.machine = {
        machine_type : ""
    };
    $scope.shell_type = [
        "/bin/bash -c",
        "/bin/ksh -c",
        "/bin/sh -c",
        "/bin/csh -c"
    ];
    $scope.reload_commands = [
        ". ~/.profile",
        ". ~/.bash_profile",
        ". ~/.bashrc"
    ];
    $scope.isFilterApplied = false;
    $scope.openFilter = function()
    {
        if(document.getElementById("open_filter").style.display === "none" || document.getElementById("open_filter").style.display === "")
        {
            $('#open_filter').show();
            $scope.open_filter = true;
        }
        else
        {
            $('#open_filter').hide();
            $scope.open_filter = false;
        }
    };

    $scope.userData = $rootScope.userProfile.userData.user;

    $scope.getUserProfile = UserProfile.get({
        username : $scope.userData
    },
    function(getUserProfileResponse)
    {
        $scope.userId = getUserProfileResponse.data._id.$oid;
        var myFavMachine = [];
        $scope.allMyFavMachine = [];
        ViewFavouriteMachine.get({
            id : $scope.userId
        },
        function(viewFavouriteMachineResponse){
            $scope.favouriteMachines = viewFavouriteMachineResponse.data;
            for(var k in $scope.favouriteMachines) myFavMachine.push(k);
            for(var a=0; a < myFavMachine.length; a++)
            {
                var data = $scope.favouriteMachines[myFavMachine[a]];
                if(data)
                {
                    for(var b=0; b < data.length; b++)
                    {
                        $scope.allMyFavMachine.push(data[b]["machine_id"]);

                    }
                }
            }
        },
        function(viewFavouriteMachineErrorResponse){
            $rootScope.handleResponse(viewFavouriteMachineErrorResponse);
        });
    },
    function(getUserProfileErrorResponse)
    {
        $rootScope.handleResponse(getUserProfileErrorResponse);
    });

    GetAllMachine.getAll({
    },
    function(successResponse){
        $scope.machines = successResponse.data.data;
        $scope.currentPage = successResponse.data.page;
        $scope.totalCount = successResponse.data.total;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.isFavorites = function(id)
    {
        if($scope.allMyFavMachine)
        {
            return $scope.allMyFavMachine.indexOf(id) !== -1;
        }
    }

    $scope.cancleFilter = function()
    {
        $('#open_filter').hide(700);
    };

    $scope.showNameFilter = function()
    {
        if($scope.machineNameFilterFlag === true)
        {
            $scope.machineNameFilterFlag = false;
        }
        else
        {
            $scope.machineNameFilterFlag = true;
        }
    };
    $scope.showHostFilter = function()
    {
        if($scope.hostFilterFlag === true)
        {
            $scope.hostFilterFlag = false;
        }
        else
        {
            $scope.hostFilterFlag = true;
        }
    };
    $scope.setNameFilterCSS = function(flag)
    {
        if(flag === false)
        {
            return '';
        }
        else
        {
            return 'vp-filterelement__filterrowlvlone--expanded';
        }
    };
    $scope.setHostFilterCSS = function(flag)
    {
        if(flag === false)
        {
            return '';
        }
        else
        {
            return 'vp-filterelement__filterrowlvlone--expanded';
        }
    };
    $scope.showMachineTypeFilter = function()
    {
        if($scope.machineTypeFilterFlag === true)
        {
            $scope.machineTypeFilterFlag = false;
        }
        else
        {
            $scope.machineTypeFilterFlag = true;
        }
    };

    $scope.setMachineTypeFilterCSS = function(flag)
    {
        if(flag === false)
        {
            return '';
        }
        else
        {
            return 'vp-filterelement__filterrowlvlone--expanded';
        }
    };

    $scope.showTagsFilter = function()
    {
        if($scope.tagsFilterFlag === true)
        {
            $scope.tagsFilterFlag = false;
        }
        else
        {
            $scope.tagsFilterFlag = true;
        }
    };

    $scope.setTagsFilterCSS = function(flag)
    {
        if(flag === false)
        {
            return '';
        }
        else
        {
            return 'vp-filterelement__filterrowlvlone--expanded';
        }
    };
    $scope.setTagsFilter = function(tag)
    {
        var tagFlag = 0;
        var ind = 0;
        var tagFilterLen = tagsFilter.length;
        if(tagFilterLen>0)
        {
            for(var a=0; a<tagFilterLen; a++)
            {
                if(tagsFilter[a] === tag)
                {
                    ind = a;
                }
                else
                {
                    tagFlag++;
                }
            }

            if(tagFlag === tagFilterLen)
            {
                tagsFilter.push(tag);
            }
            else
            {
                tagsFilter.splice(ind, 1);
            }
        }
        else
        {
            tagsFilter.push(tag);
        }
    };
    $scope.setMachineTypeFilter = function(type)
    {
        var typeFlag = 0;
        var ind = 0;
        var typeFilterLen = machineTypeFilter.length;
        if(typeFilterLen>0)
        {
            for(var a=0; a<typeFilterLen; a++)
            {
                if(machineTypeFilter[a] === type)
                {
                    ind = a;
                }
                else
                {
                    typeFlag++;
                }
            }

            if(typeFlag === typeFilterLen)
            {
                machineTypeFilter.push(type);
            }
            else
            {
                machineTypeFilter.splice(ind, 1);
            }
        }
        else
        {
            machineTypeFilter.push(type);
        }
    };

    $scope.setHostFilter = function(host)
    {
        hostFilter = host;
    };

    $scope.setNameFilter = function(name)
    {
        machineNameFilter = name;
    };

    $scope.applyMachineFilters = function()
    {
        var machine_name = "";
        var machine_type = "";
        var host = "";
        var tags = "";
        var perpage = 0;

        if(machineNameFilter !== null && machineNameFilter!== undefined && machineNameFilter !== '')
        {
            machine_name = machineNameFilter;
        }
        else
        {
           machine_name =null;
        }

        if(hostFilter !== null && hostFilter!== undefined && hostFilter !== '')
        {
            host = hostFilter;
        }
        else
        {
            host = null;
        }

        if(machineTypeFilter.length>0)
        {
            machine_type = machineTypeFilter.toString();
        }
        else
        {
            machine_type = null;
        }

        if(tagsFilter.length>0)
        {
            tags = tagsFilter.toString();
        }
        else
        {
            tags = null;
        }
        if(machine_name === null && host === null && machine_type === null && tags === null)
        {
            perpage = null;
            $scope.hideShowMoreMachine = false;
            $scope.isFilterApplied = false;
        }
        else
        {
            $scope.hideShowMoreMachine = true;
            $scope.isFilterApplied = true;
        }
        var jsonData={
            machine_name : machine_name,
            host : host,
            machine_type : machine_type,
            tags : tags,
            page : 0,
            perpage : perpage
        };
        $('#open_filter').hide(700);
        GetAllMachine.get({
            machine_name : machine_name,
            host : host,
            machine_type : machine_type,
            tags : tags,
            page : 0,
            perpage : perpage
        },
        function(successResponse)
        {
            delete $scope.Machine;
            delete $scope.machines;
            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;
            $scope.machines = successResponse.data.data;
            $scope.$watch(function(scope) {
                return scope.machines;
            },
            function(newValue, oldValue) {
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.closeFilter = function(form)
    {
        machineNameFilter = "";
        hostFilter ="";
        machineTypeFilter = [];
        tagsFilter = [];
        $('#open_filter').hide(700);
        $scope.open_filter = false;
        $scope.hideShowMoreMachine = false;
        $scope.isFilterApplied = false;
        GetAllMachine.getAll({
        },
        function(successResponse)
        {
            delete $scope.Machine;
            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;
            $scope.machines = successResponse.data.data;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };
    $scope.showMoreMachine = function()
    {
        $scope.currentPage = $scope.currentPage+1;
        $scope.tempMachines = [];
        angular.copy($scope.machines, $scope.tempMachines);
        delete $scope.machines;
        GetAllMachine.get({
           page:$scope.currentPage
        },
        function(successResponse)
        {
            $scope.machines = [];
            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;
            for(var a=0; a<successResponse.data.data.length; a++)
            {
                $scope.tempMachines.push(successResponse.data.data[a]);
            }
            for(var b=0; b<$scope.tempMachines.length; b++)
            {
                $scope.machines.push($scope.tempMachines[b]);
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

    };



    $scope.setMachineTypeCSS = function(machine_type, machine_id)
    {
        var styles = "";
        if(machine_id === $scope.selectedMachineId)
        {
            styles = styles + "vp-search__item--selected";
        }
        return styles;
    };

    $scope.showUsers = function()
    {
        if(document.getElementById("add_users").style.display === "none" || document.getElementById("add_users").style.display === "")
        {
            document.getElementById("add_users").style.display = "block";
        }
        else
        {
           document.getElementById("add_users").style.display = "none";
        }
    };

    $scope.showTeamGroups = function()
    {
            if(document.getElementById("add_team_groups").style.display === "none" || document.getElementById("add_team_groups").style.display === "")
            {
                document.getElementById("add_team_groups").style.display = "block";
            }
            else
            {
               document.getElementById("add_team_groups").style.display = "none";
            }
    };

    $scope.closeAddTeam = function()
    {
       document.getElementById("add_team_groups").style.display = "none";
    } ;

    $scope.showMachineGroups = function()
    {
        if(document.getElementById("add_machine_groups").style.display === "none" || document.getElementById("add_machine_groups").style.display === "")
        {
            document.getElementById("add_machine_groups").style.display = "block";
        }
        else
        {
           document.getElementById("add_machine_groups").style.display = "none";
        }
    };

    $scope.addUser = function(user)
    {
        var user_flag = 0;
        var ind = 0;
        if($scope.permittedUsers)
        {
            for(var c=0;  c<$scope.permittedUsers.length; c++)
            {
                if(user._id.$oid===$scope.permittedUsers[c]._id.$oid)
                {
                    user_flag++;
                    ind = c;
                }
            }

            if(user_flag===0)
            {
                $scope.permittedUsers.push(user);
            }
            else
            {
                $scope.permittedUsers.splice(ind, 1);
            }
        }
        else
        {
            $scope.permittedUsers = [];
            $scope.permittedUsers.push(user);
        }
    };

    $scope.removeUser = function(user)
    {
        for(var a=0; a<$scope.permittedUsers.length; a++)
        {
            if($scope.permittedUsers[a]._id.$oid === user._id.$oid)
            {
                $scope.permittedUsers.splice(a, 1);
            }
        }

        for(var b=0; b<$scope.users.length; b++)
        {
            if($scope.users[b]._id.$oid === user._id.$oid)
            {
                $scope.users[b].selected = false;
            }
        }
    };

    $scope.isUserSelected = function(user)
    {
        var flag = 0;
        if(!$scope.permittedUsers)
        {
            $scope.permittedUsers = [];
        }
        for(var j=0; j<$scope.permittedUsers.length; j++)
        {
            if(user === $scope.permittedUsers[j].user)
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

    $scope.addteam = function(team)
    {
            var user_flag = 0;
            var ind = 0;
            if($scope.permitted_teams)
            {
                for(var c=0;  c<$scope.permitted_teams.length; c++)
                {
                    if(team._id.$oid===$scope.permitted_teams[c]._id.$oid)
                    {
                        user_flag++;
                        ind = c;
                    }
                }

                if(user_flag===0)
                {
                    $scope.permitted_teams.push(team);
                }
                else
                {
                    $scope.permitted_teams.splice(ind, 1);
                }
            }
            else
            {
                $scope.permitted_teams = [];
                $scope.permitted_teams.push(team);
            }
    };

    $scope.isTeamSelected = function(team)
    {
        var flag = 0;
        if(!$scope.permitted_teams)
        {
            $scope.permitted_teams = [];
        }
        for(var j=0; j<$scope.permitted_teams.length; j++)
        {
            if(team === $scope.permitted_teams[j])
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

    $scope.removeFromTeamGroup = function(team)
    {
        var tag_flag = 0;
        var ind = 0;
        if($scope.permitted_teams.length>0)
        {
            for(var c=0;  c<$scope.permitted_teams.length; c++)
            {
                if(team===$scope.permitted_teams[c])
                {
                    tag_flag++;
                    ind = c;
                }
            }

            if(tag_flag===0)
            {
                $scope.permitted_teams.push(team);
            }
            else
            {
                $scope.permitted_teams.splice(ind, 1);
            }
        }
        else
        {
            $scope.permitted_teams = [];
            $scope.permitted_teams.push(team);
        }
    };

    $scope.addToMachineGroup = function(group)
    {
        var group_flag = 0;
        var ind = 0;
        if($scope.includedIn)
        {
            for(var c=0;  c<$scope.includedIn.length; c++)
            {
                if(group=== $scope.includedIn[c])
                {
                    group_flag++;
                    ind = c;
                }
            }

            if(group_flag===0)
            {
                $scope.includedIn.push(group);

            }
            else
            {
                $scope.includedIn.splice(ind, 1);
            }
        }
        else
        {
            $scope.includedIn = [];
            $scope.includedIn.push(group);
        }
    };

    $scope.removeFromMachineGroup = function(group)
    {
        for(var a=0; a<$scope.includedIn.length; a++)
        {
            if($scope.includedIn[a].group_id === group.group_id)
            {
                $scope.includedIn.splice(a, 1);
            }
        }

        for(var b=0; b<$scope.MachineGroups.data.length; b++)
        {
            if($scope.MachineGroups.data[b].group_id === group.group_id)
            {
                $scope.MachineGroups.data[b].selected = false;
            }
        }
    };

    $scope.isMachineGroupSelected = function(group)
    {
        var flag = 0;
        if($scope.includedIn.length>0)
        {
            for(var j=0; j<$scope.includedIn.length; j++)
            {
                if(group === $scope.includedIn[j].group_name)
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
        }
    };

    $scope.openDeleteMachineConfirmationPopup = function(machine_id)
    {
        $scope.machineToDelete = machine_id;
        $('#show_delete_machine_confirmation_popup').show(700);
    };

    $scope.removeThisMachine = function()
    {
        var machineCountFlag = 0;
        $scope.machineDeletionStatus = MachineDelete.remove({
            id : $scope.machineToDelete
        },
        function (machineDeleteSuccessResponse)
        {
            $('#show_delete_machine_confirmation_popup').hide(700);
            $rootScope.handleResponse(machineDeleteSuccessResponse);
            var favMachineId = '';
            for(var k=0; k<$scope.favouriteMachines['Production'].length;k++)
            {
                if(id === $scope.favouriteMachines['Production'][k].machine_id)
                {
                    machineCountFlag++;
                    favMachineId = $scope.favouriteMachines['Production'][i]._id.$oid;
                }
            }

            for(var m=0; m<$scope.favouriteMachines['IUT'].length;m++)
            {
                if(id === $scope.favouriteMachines['IUT'][m].machine_id)
                {
                    machineCountFlag++;
                    favMachineId = $scope.favouriteMachines['IUT'][i]._id.$oid;
                }
            }

            for(var i=0; i<$scope.favouriteMachines['UT'].length;i++)
            {
                if(id === $scope.favouriteMachines['UT'][i].machine_id)
                {
                    machineCountFlag++;
                    favMachineId = $scope.favouriteMachines['UT'][i]._id.$oid;
                }
            }

            for(var l=0; l<$scope.favouriteMachines['ST'].length;l++)
            {
                if(id === $scope.favouriteMachines['ST'][l].machine_id)
                {
                    machineCountFlag++;
                    favMachineId = $scope.favouriteMachines['ST'][i]._id.$oid;
                }
            }

            for(var j=0; j<$scope.favouriteMachines['Value Package Master'].length;j++)
            {
                if(id === $scope.favouriteMachines['Value Package Master'][j].machine_id)
                {
                    machineCountFlag++;
                    favMachineId = $scope.favouriteMachines['Value Package Master'][i]._id.$oid;
                }
            }

            for(var n=0; n<$scope.favouriteMachines['Other'].length;n++)
            {
                if(id === $scope.favouriteMachines['Other'][n].machine_id)
                {
                    machineCountFlag++;
                    favMachineId = $scope.favouriteMachines['Other'][i]._id.$oid;
                }
            }

            for(var o=0; o<$scope.favouriteMachines['UAT'].length; o++)
            {
                if(id === $scope.favouriteMachines['UAT'][o].machine_id)
                {
                    machineCountFlag++;
                    favMachineId = $scope.favouriteMachines['UAT'][i]._id.$oid;
                }
            }

            for(var p=0; p<$scope.favouriteMachines['SIT'].length; p++)
            {
                if(id === $scope.favouriteMachines['SIT'][p].machine_id)
                {
                    machineCountFlag++;
                    favMachineId = $scope.favouriteMachines['SIT'][i]._id.$oid;
                }
            }

            for(var q=0; q<$scope.favouriteMachines['PET'].length; q++)
            {
                if(id === $scope.favouriteMachines['PET'][q].machine_id)
                {
                    machineCountFlag++;
                    favMachineId = $scope.favouriteMachines['PET'][i]._id.$oid;
                }
            }


            if(machineCountFlag>0)
            {
                FavMachineDelete.remove({
                    id : favMachineId
                },
                function(favMachineDeleteSuccessResponse)
                {
                    $rootScope.handleResponse(favMachineDeleteSuccessResponse);
                },
                function (favMachineDeleteErrorResponse)
                {
                    $rootScope.handleResponse(favMachineDeleteErrorResponse);
                });
            }

            $state.go('manageMachines');
            $scope.machines = GetAllMachine.get({
            },
            function(successResponse)
            {
                $scope.machines = successResponse.data.data;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
            delete $scope.Machine;
         },
         function (machineDeleteErrorResponse)
         {
            $('#show_delete_machine_confirmation_popup').hide(700);
            $rootScope.handleResponse(machineDeleteErrorResponse);
         });
    };

    $scope.closeDeleteMachineConfirmationPopup = function()
    {
        $('#show_delete_machine_confirmation_popup').hide(700);
    };

    $scope.clearAllData = function()
    {
        $scope.permittedUsers = [];
    };

    $scope.discardMachineChanges = function()
    {
        delete $scope.selectedMachineName;
        delete $scope.Machine;
        $rootScope.currentStatus = "";
        $state.go('manageMachines');
    };

    $scope.closeUser = function()
    {
        document.getElementById("add_users").style.display = "none";
    };

    $scope.closeAddMachineGroup = function()
    {
        document.getElementById("add_machine_groups").style.display = "none";
    };

    $scope.showEditPassword = function()
    {
        if(document.getElementById("update_password").style.display === "none" || document.getElementById("update_password").style.display === '')
        {
            document.getElementById("update_password").style.display = "block";
        }
        else
        {
           document.getElementById("update_password").style.display = "none";
        }
    };

    $scope.closePassword = function()
    {
        document.getElementById("update_password").style.display = "none";
    };

    $scope.checkPassword = function()
     {
        $scope.useredit_errors.password ='';
        $scope.useredit_errors.confirmpassword ='';
        $scope.useredit_errors.password_mismatch ='';
        if($scope.Machine.data.password==='' || $scope.Machine.data.password===undefined )
        {
            $scope.useredit_errors.password ="Please enter password!";
            return false;
        }
        else if($scope.Machine.data.confirmpassword==='' || $scope.Machine.data.confirmpassword===undefined )
        {
            $scope.useredit_errors.confirmpassword ="Please confirm entered password!";
            return false;
        }
        else if($scope.Machine.data.password!=='' &&  $scope.Machine.data.confirmpassword!=='' && $scope.Machine.data.password!==undefined && $scope.Machine.data.confirmpassword!==undefined  && $scope.Machine.data.password!==$scope.Machine.data.confirmpassword)
        {
            $scope.useredit_errors.password_mismatch ="Password and Confirm Password should match!";
            return false;
        }
        else if($scope.Machine.data.password!=='' &&  $scope.Machine.data.confirmpassword!=='' && $scope.Machine.data.password!==undefined && $scope.Machine.data.confirmpassword!==undefined  && $scope.Machine.data.password===$scope.Machine.data.confirmpassword)
        {
            document.getElementById("update_password").style.display = "none";
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
        if($scope.Machine.data.tag.length>0)
        {
            for(var c=0;  c<$scope.Machine.data.tag.length; c++)
            {
                if(tag.name===$scope.Machine.data.tag[c])
                {
                    tag_flag++;
                    ind = c;
                }
            }

            if(tag_flag===0)
            {
                $scope.Machine.data.tag.push(tag.name);
            }
            else
            {
                $scope.Machine.data.tag.splice(ind, 1);
            }

        }
        else
        {
            $scope.Machine.data.tag = [];
            $scope.Machine.data.tag.push(tag.name);
        }
    };

    $scope.removeTag = function(tag)
    {
        var tag_flag = 0;
        var ind = 0;
        if($scope.Machine.data.tag.length>0)
        {
            for(var c=0;  c<$scope.Machine.data.tag.length; c++)
            {
                if(tag===$scope.Machine.data.tag[c])
                {
                    tag_flag++;
                    ind = c;
                }
            }

            if(tag_flag===0)
            {
                $scope.Machine.data.tag.push(tag.name);
            }
            else
            {
                $scope.Machine.data.tag.splice(ind, 1);
            }

        }
        else
        {
            $scope.Machine.data.tag = [];
            $scope.Machine.data.tag.push(tag.name);
        }
    };

    $scope.isTagSelected = function(tag)
    {
        var flag = 0;
        if(!$scope.Machine.data.tag)
        {
            $scope.Machine.data.tag = [];
        }
        for(var j=0; j<$scope.Machine.data.tag.length; j++)
        {
            if(tag === $scope.Machine.data.tag[j])
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

    TagsAll.get({
    },
    function(successResponse)
    {
        $scope.allTags = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.changeMachineFavoriteParam = function(param)
    {
        if(param === 'true' || param === true)
        {
            $scope.Machine.data.fav = false;
        }
        else
        {
            $scope.Machine.data.fav = true;
        }
    };
    $scope.MachineTypes = GetAllMachineTypes.get({
    },
    function( types)
    {
        $scope.types = types.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    var favMachineJsonData = {};
    $scope.selectMachine = function(machine_id)
    {
        $scope.faNameValueMap = {};
        delete $scope.machineConnectionMessage;
        $scope.Machine = Machine.get({
            id: machine_id
        },
        function(response)
        {
            machine_id = response.data._id.$oid;
            if (response.data.flexible_attributes){
                for(var fa in response.data.flexible_attributes){
                    $scope.faNameValueMap[fa] = response.data.flexible_attributes[fa];
                }
            }

            $scope.envVars.splice(0, $scope.envVars.length);
            if (response.data.environment_variables){
                $scope.envVars.push.apply($scope.envVars, response.data.environment_variables);
            }

            var machineCountFlag = 0;
            if ($scope.favouriteMachines)
            {
                for(var k=0; k<$scope.favouriteMachines['Production'].length;k++)
                {
                    if(response.data._id.$oid === $scope.favouriteMachines['Production'][k].machine_id)
                    {
                        machineCountFlag++;
                    }
                }

                for(var m=0; m<$scope.favouriteMachines['IUT'].length;m++)
                {
                    if(response.data._id.$oid === $scope.favouriteMachines['IUT'][m].machine_id)
                    {
                        machineCountFlag++;
                    }
                }
                for(var i=0; i<$scope.favouriteMachines['UT'].length;i++)
                {
                    if(response.data._id.$oid === $scope.favouriteMachines['UT'][i].machine_id)
                    {
                        machineCountFlag++;
                    }
                }
                for(var l=0; l<$scope.favouriteMachines['ST'].length;l++)
                {
                    if(response.data._id.$oid === $scope.favouriteMachines['ST'][l].machine_id)
                    {
                        machineCountFlag++;
                    }
                }
                for(var j=0; j<$scope.favouriteMachines['Value Package Master'].length;j++)
                {
                    if(response.data._id.$oid === $scope.favouriteMachines['Value Package Master'][j].machine_id)
                    {
                        machineCountFlag++;
                    }
                }
                for(var n=0; n<$scope.favouriteMachines['Other'].length;n++)
                {
                    if(response.data._id.$oid === $scope.favouriteMachines['Other'][n].machine_id)
                    {
                        machineCountFlag++;
                    }
                }
                for(var o=0; o<$scope.favouriteMachines['UAT'].length; o++)
                {
                    if(response.data._id.$oid === $scope.favouriteMachines['UAT'][o].machine_id)
                    {
                        machineCountFlag++;
                    }
                }
                for(var p=0; p<$scope.favouriteMachines['SIT'].length; p++)
                {
                    if(response.data._id.$oid === $scope.favouriteMachines['SIT'][p].machine_id)
                    {
                        machineCountFlag++;
                    }
                }
                for(var q=0; q<$scope.favouriteMachines['PET'].length; q++)
                {
                    if(response.data._id.$oid === $scope.favouriteMachines['PET'][q].machine_id)
                    {
                        machineCountFlag++;
                    }
                }

                if($scope.favouriteMachines['Test'])
                {
                    for(var s=0; s<$scope.favouriteMachines['Test'].length; s++)
                    {
                        if(response.data._id.$oid === $scope.favouriteMachines['Test'][s].machine_id)
                        {
                            machineCountFlag++;
                        }
                    }
                }

                if(machineCountFlag > 0)
                {
                    $scope.Machine.data.fav = true;
                }
                else
                {
                    $scope.Machine.data.fav = false;
                }
            }

            $scope.selectedMachineName = response.data.machine_name;
            $scope.selectedMachineId = response.data._id.$oid;
            $scope.machine = response.data;
            $scope.oldMachineData = response.data;
            $scope.Machine.data.port = parseInt(response.data.port, 10);
            if(response.data.Tools)
            {
                $scope.ToolsOnMachine = response.data.Tools;
            }
            if(response.data.deploymentunits)
            {
                $scope.duOnMachine = response.data.deploymentunits;
            }
            if(response.data.steps_to_auth)
            {
                $scope.steps_in_push = response.data.steps_to_auth;
                if($scope.steps_in_push.length > 0)
                {
                    if($scope.Machine.data.tunneling_flag === undefined)
                    {
                        $scope.Machine.data.tunneling_flag = true;
                    }
                    for(var r=0; r<response.data.steps_to_auth.length; r++)
                    {
                        if(response.data.steps_to_auth[r].auth_type === 'SSH')
                        {
                            $scope.Machine.data.steps_to_auth[r].port = parseInt(response.data.steps_to_auth[r].port, 10);
                        }
                    }
                }
            }

            if(response.data.included_in)
            {
                $scope.includedIn = response.data.included_in;
            }

            if((!response.data.auth_type) || response.data.auth_type === null || response.data.auth_type === '' || response.data.auth_type === undefined)
            {
                $scope.Machine.data.auth_type = 'password';
            }

//            if(response.data.history)
//            {
//                $scope.deploymentHistoryTools = response.data.history.tools;
//                $scope.deploymentHistoryDU = response.data.history.dus;
//            }


            $scope.allUsers = Users.get({
                id:"all"
            },
            function(users)
            {
                $scope.users = users.data;
                $scope.permittedUsers = [] ;

                for(var i =0 ; i  < $scope.machine.permitted_users.length ; i++)
                {
                    for( var j=0;  j <$scope.users.length;j++ )
                    {
                        if($scope.machine.permitted_users[i]==='all')
                        {
                            $scope.users[j].selected = true;
                            if($scope.machine.permitted_users[i]==='all')
                            {
                                $scope.permittedUsers.push($scope.users[j]);
                            }
                        }
                        else if($scope.machine.permitted_users[i]._id.$oid === $scope.users[j]._id.$oid)
                        {
                            $scope.users[j].selected = true;
                            $scope.permittedUsers.push($scope.users[j]);
                        }
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            $scope.AllTeam = UserGroup.get({
            },
            function(successResponse)
            {
                $scope.teams = successResponse;
                $scope.permitted_teams = [] ;

                for(var i =0 ; i  < $scope.machine.permitted_teams.length ; i++)
                {
                    for( var j=0;  j <$scope.teams.data.length;j++ )
                    {
                        if($scope.machine.permitted_teams[i] === $scope.teams.data[j]._id.$oid)
                        {
                            $scope.teams.data[j].selected = true;
                            $scope.permitted_teams.push($scope.teams.data[j]);
                        }
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            $scope.MachineGroups = MachineGroup.get({
            },
            function(successResponse)
            {
                $scope.MachineGroups = successResponse.data;
                $scope.includedIn =[];
                for(var i =0 ; i  < $scope.machine.included_in.length ; i++)
                {
                    for( var j=0;  j <$scope.MachineGroups.data.length;j++ )
                    {
                        if($scope.machine.included_in[i] === $scope.MachineGroups.data[j]._id.$oid)
                        {
                            $scope.MachineGroups.data[j].selected = true;
                            $scope.includedIn.push($scope.MachineGroups.data[j]);
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

    if($stateParams.id)
    {
        $scope.selectMachine($stateParams.id);
    }

    $rootScope.$on('GetToolDeploymentHistory', function(event, args){
        GetDeploymentHistory.get({
            id: $scope.selectedMachineId,
            entity: 'tool'
        },
        function(getToolDeploymentHistorySuccessReponse)
        {
            if(getToolDeploymentHistorySuccessReponse.data.history)
            {
                $scope.toolDeployments = getToolDeploymentHistorySuccessReponse.data.history.tools;
            }
        },
        function(getToolDeploymentHistoryErrorReponse)
        {
            $rootScope.handleResponse(getToolDeploymentHistoryErrorReponse);
        });
    });

    $rootScope.$on('GetDUDeploymentHistory', function(event, args){
        GetDeploymentHistory.get({
            id: $scope.selectedMachineId,
            entity: 'du'
        },
        function(getDUDeploymentHistorySuccessReponse)
        {
            if(getDUDeploymentHistorySuccessReponse.data.history)
            {
                $scope.duDeployments = getDUDeploymentHistorySuccessReponse.data.history.dus;
            }
        },
        function(getDUDeploymentHistoryErrorReponse)
        {
            $rootScope.handleResponse(getDUDeploymentHistoryErrorReponse);
        });
    });

    $scope.auth_types_push = [
        "SSH" , "Telnet"
    ];

    $scope.step = {
        type : ""
    };

    var stepLength = 1;
    $scope.steps_in_push = [];
    $scope.steps_in_push.length = 0;

    $scope.addNewStep = function() {
        var newItemNo = $scope.steps_in_push.length+1;
        $scope.steps_in_push.push({ order : newItemNo, port : 22});
    };

    $scope.removeStep = function(index) {
        $scope.steps_in_push.splice(index, 1);
    };

    $scope.setDefaultPort = function(step_type, index)
    {
        if(step_type==='SSH')
        {
            $scope.steps_in_push[index].port = 22;
        }
        else
        {
            delete $scope.steps_in_push[index].port;
        }
    };

    $scope.moveStepUp = function(index) {
        var elementToMoveUp = $scope.steps_in_push[index];
        var elementToMoveDown = $scope.steps_in_push[index-1];
        if(elementToMoveDown!=null)
        {
            $scope.steps_in_push[index-1] = elementToMoveUp;
            $scope.steps_in_push[index] = elementToMoveDown;
        }
    };

    $scope.moveStepDown = function(index) {
        var elementToMoveDown = $scope.steps_in_push[index];
        var elementToMoveUp = $scope.steps_in_push[index+1];

        if(elementToMoveUp!=null)
        {
            $scope.steps_in_push[index] = elementToMoveUp;
            $scope.steps_in_push[index+1] = elementToMoveDown;
        }
    };

    // This function is written to get the clicked version and show the details of that version
    $scope.showVersionDetails = function(ver)
    {
        $scope.ID = ver;
        $scope.isActive = false;
        $scope.isActive = !$scope.isActive;
    };

    $scope.setReloadCommand = function(value)
    {
        $scope.machine.reload_command = value;
    };

    $scope.viewToolDeploymentHistory = function(index)
    {
        $scope.toolDeploymentHistory = $scope.toolDeployments[index].deployments;
        $('#show_tool_deployment_history_popup').show(700);
    };

    $scope.closeToolDeploymentHistoryPopup = function()
    {
        $('#show_tool_deployment_history_popup').hide(700);
    };

    $scope.viewDUDeploymentHistory = function(index)
    {
        $scope.duDeploymentHistory = $scope.duDeployments[index].deployments;
        $('#show_du_deployment_history_popup').show(700);
    };

    $scope.closeDUDeploymentHistoryPopup = function()
    {
        $('#show_du_deployment_history_popup').hide(700);
    };

     $scope.testConnection = function(form)
     {
        $scope.newMachineErrors = {
            ip : ''
        };
        var sendUpdatedMachine = {};
        sendUpdatedMachine._id  = {
            oid: ""
        };

        if($scope.Machine.data.reload_command === 'not required')
        {
            $scope.Machine.data.reload_command = '';
        }

        if($scope.Machine.data.shell_type === ' ' || $scope.Machine.data.shell_type === undefined || $scope.Machine.data.shell_type === null)
        {
            $scope.Machine.data.shell_type = '';
        }
        sendUpdatedMachine._id.oid = $scope.Machine.data._id.$oid;
        sendUpdatedMachine.machine_name = $scope.Machine.data.machine_name;
        sendUpdatedMachine.host = $scope.Machine.data.host;
        sendUpdatedMachine.ip = $scope.Machine.data.ip;
        sendUpdatedMachine.username = $scope.Machine.data.username;
        sendUpdatedMachine.shell_type = $scope.Machine.data.shell_type;
        sendUpdatedMachine.reload_command = $scope.Machine.data.reload_command;
        sendUpdatedMachine.auth_type = $scope.Machine.data.auth_type;
        sendUpdatedMachine.machine_type = $scope.Machine.data.machine_type;
        if (!(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(sendUpdatedMachine.ip)))
        {
            $scope.newMachineErrors.ip = 'Please enter valid IP Address!';
            $rootScope.handleResponse('Please enter valid IP Address!');
            return false;
        }
        if($scope.selectedData.password!== '')
        {
            sendUpdatedMachine.username = $scope.selectedData.password;
        }
        else
        {
            sendUpdatedMachine.password = $scope.Machine.data.password;
        }

        sendUpdatedMachine.port = $scope.Machine.data.port;
        sendUpdatedMachine.account_id = $rootScope.userProfile.userData.account_details._id.$oid;
        sendUpdatedMachine.permitted_users = [];

        if($scope.permittedUsers.length > 0)
        {
            angular.forEach($scope.permittedUsers, function (item) {
                sendUpdatedMachine.permitted_users.push(item._id.$oid);
            });
        }
//        else
//        {
//            sendUpdatedMachine.permitted_users.push("all");
//        }

        if($scope.Machine.data.auth_type === 'ssh' && ($scope.Machine.data.password === null || $scope.Machine.data.password === '' || $scope.Machine.data.password === undefined))
        {
            sendUpdatedMachine.password = '12345';
        }
        if($scope.Machine.data.tunneling_flag === true)
        {
            sendUpdatedMachine.steps_to_auth = $scope.Machine.data.steps_to_auth;
        }
        else
        {
            sendUpdatedMachine.steps_to_auth =[];
        }

        if(((sendUpdatedMachine.host === '' || sendUpdatedMachine.host === null || sendUpdatedMachine.host === undefined) || (sendUpdatedMachine.username === '' || sendUpdatedMachine.username === null || sendUpdatedMachine.username === undefined) || (sendUpdatedMachine.ip === '' || sendUpdatedMachine.ip === null || sendUpdatedMachine.ip === undefined) || (sendUpdatedMachine.auth_type === '' || sendUpdatedMachine.auth_type === null || sendUpdatedMachine.auth_type === undefined)) && ((sendUpdatedMachine.auth_type === 'password') && (sendUpdatedMachine.password === '' || sendUpdatedMachine.password === null || sendUpdatedMachine.password === undefined)))
        {
            $rootScope.handleResponse('Mandatory fields required to test connection are missing');
            return false;
        }

        for(var j=0; j<sendUpdatedMachine.steps_to_auth.length; j++)
        {
            var step = j+1;
            if(sendUpdatedMachine.steps_to_auth[j].type === '' || sendUpdatedMachine.steps_to_auth[j].type === null || sendUpdatedMachine.steps_to_auth[j].type === undefined)
            {
                $rootScope.handleResponse('Please select authentication type for step '+step+' in tunneling');
                return false;
            }
            if(sendUpdatedMachine.steps_to_auth[j].host === '' || sendUpdatedMachine.steps_to_auth[j].host === null || sendUpdatedMachine.steps_to_auth[j].host === undefined)
            {
                $rootScope.handleResponse('Please enter host name for step '+step+' in tunneling');
                return false;
            }
            if(sendUpdatedMachine.steps_to_auth[j].port === '' || sendUpdatedMachine.steps_to_auth[j].port === null || sendUpdatedMachine.steps_to_auth[j].port === undefined)
            {
                $rootScope.handleResponse('Please enter port number for step '+step+' in tunneling');
                return false;
            }
            if(sendUpdatedMachine.steps_to_auth[j].username === '' || sendUpdatedMachine.steps_to_auth[j].username === null || sendUpdatedMachine.steps_to_auth[j].username === undefined)
            {
                $rootScope.handleResponse('Please enter username for step '+step+' in tunneling');
                return false;
            }
            if(sendUpdatedMachine.steps_to_auth[j].password === '' || sendUpdatedMachine.steps_to_auth[j].password === null || sendUpdatedMachine.steps_to_auth[j].password === undefined)
            {
                $rootScope.handleResponse('Please enter password for step '+step+' in tunneling');
                return false;
            }
        }

        //sendUpdatedMachine.steps_to_auth = $scope.steps_in_push;

        TestMachine.save (sendUpdatedMachine, function (testMachineSuccessResponse){
            $rootScope.handleResponse(testMachineSuccessResponse);
            $scope.machineConnectionMessage = testMachineSuccessResponse.message;
        },
        function(testMachineErrorResponse)
        {
            $scope.machineConnectionMessage = testMachineErrorResponse.data;
            $rootScope.handleResponse(testMachineErrorResponse);
        });
    };

    $scope.editMachine = function(form)
    {
        if($scope.Machine.data.machine_name === '' || $scope.Machine.data.machine_name === undefined || $scope.Machine.data.machine_name === null)
        {
            $rootScope.handleResponse('Please fill the Machine Name');
            return false;
        }
        if($scope.Machine.data.reload_command === 'not required')
        {
            $scope.Machine.data.reload_command = '';
        }

        if($scope.Machine.data.shell_type === ' ' || $scope.Machine.data.shell_type === undefined || $scope.Machine.data.shell_type === null)
        {
            $scope.Machine.data.shell_type = '';
        }
        if($scope.Machine.data.machine_name === ' ' || $scope.Machine.data.machine_name === undefined || $scope.Machine.data.machine_name === null)
        {
            $scope.Machine.data.machine_name = '';
        }

        $scope.newMachineErrors = {
            ip : ''
        };
        var sendUpdatedMachine = {};
        sendUpdatedMachine._id  = {
            oid: ""
        };
        sendUpdatedMachine._id.oid = $scope.Machine.data._id.$oid;
        sendUpdatedMachine.machine_name = $scope.Machine.data.machine_name;
        sendUpdatedMachine.host = $scope.Machine.data.host;
        sendUpdatedMachine.ip = $scope.Machine.data.ip;
        sendUpdatedMachine.username = $scope.Machine.data.username;
        sendUpdatedMachine.shell_type = $scope.Machine.data.shell_type;
        sendUpdatedMachine.reload_command = $scope.Machine.data.reload_command;
        sendUpdatedMachine.tag = $scope.Machine.data.tag;
        sendUpdatedMachine.auth_type = $scope.Machine.data.auth_type;
        sendUpdatedMachine.machine_type = $scope.Machine.data.machine_type;
        sendUpdatedMachine.flexible_attributes = $scope.faNameValueMap;
        sendUpdatedMachine.environment_variables = $scope.envVars;
        sendUpdatedMachine.tunneling_flag = $scope.Machine.data.tunneling_flag;

        if (!(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(sendUpdatedMachine.ip)))
        {
            $scope.newMachineErrors.ip = 'Please enter valid IP Address!';
            $rootScope.handleResponse('Please enter valid IP Address!');
            return false;
        }

        if($scope.selectedData.password!== '')
        {
            sendUpdatedMachine.password = $scope.selectedData.password;
        }
        else
        {
            sendUpdatedMachine.password = $scope.Machine.data.password;
        }
        sendUpdatedMachine.port = $scope.Machine.data.port;
        sendUpdatedMachine.account_id = $scope.Machine.data.account_id;
        sendUpdatedMachine.permitted_users = [];
        sendUpdatedMachine.permitted_teams = [];
        sendUpdatedMachine.included_in = [];

        if($scope.permittedUsers.length > 0)
        {
            angular.forEach($scope.permittedUsers, function (item) {
                sendUpdatedMachine.permitted_users.push(item._id.$oid);
            });
            /*if($scope.users.length === sendUpdatedMachine.permitted_users.length)
            {
                delete sendUpdatedMachine.permitted_users;
            }*/
        }
        else
        {
            sendUpdatedMachine.permitted_users = [];
        }

        if($scope.permitted_teams.length > 0)
        {
            angular.forEach($scope.permitted_teams, function (item) {
                sendUpdatedMachine.permitted_teams.push(item._id.$oid);
            });
            /*if($scope.teams.data.length === sendUpdatedMachine.permitted_teams.length)
            {
                delete sendUpdatedMachine.permitted_teams;
            }*/
        }
        else
        {
            sendUpdatedMachine.permitted_teams = [];
        }

        if($scope.Machine.data.auth_type === 'ssh' && ($scope.Machine.data.password === null || $scope.Machine.data.password === '' || $scope.Machine.data.password === undefined))
        {
            sendUpdatedMachine.password = '12345';
        }

        if(((sendUpdatedMachine.host === '' || sendUpdatedMachine.host === null || sendUpdatedMachine.host === undefined) || (sendUpdatedMachine.username === '' || sendUpdatedMachine.username === null || sendUpdatedMachine.username === undefined) || (sendUpdatedMachine.ip === '' || sendUpdatedMachine.ip === null || sendUpdatedMachine.ip === undefined) || (sendUpdatedMachine.auth_type === '' || sendUpdatedMachine.auth_type === null || sendUpdatedMachine.auth_type === undefined)) || ((sendUpdatedMachine.auth_type === 'password') && (sendUpdatedMachine.password === '' || sendUpdatedMachine.password === null || sendUpdatedMachine.password === undefined)))
        {
            $rootScope.handleResponse('Mandatory fields required to update machine are missing');
            return false;
        }

        if($scope.Machine.data.tunneling_flag === true)
        {
            if($scope.Machine.data.steps_to_auth)
            {
                for(var j=0; j<$scope.Machine.data.steps_to_auth.length; j++)
                {
                    var step = j+1;
                    if($scope.Machine.data.steps_to_auth[j].type === '' || $scope.Machine.data.steps_to_auth[j].type === null || $scope.Machine.data.steps_to_auth[j].type === undefined)
                    {
                        $rootScope.handleResponse('Please select authentication type for step '+step+' in tunneling');
                        return false;
                    }
                    if($scope.Machine.data.steps_to_auth[j].host === '' || $scope.Machine.data.steps_to_auth[j].host === null || $scope.Machine.data.steps_to_auth[j].host === undefined)
                    {
                        $rootScope.handleResponse('Please enter host name for step '+step+' in tunneling');
                        return false;
                    }
                    if($scope.Machine.data.steps_to_auth[j].port === '' || $scope.Machine.data.steps_to_auth[j].port === null || $scope.Machine.data.steps_to_auth[j].port === undefined)
                    {
                        $rootScope.handleResponse('Please enter port number for step '+step+' in tunneling');
                        return false;
                    }
                    if($scope.Machine.data.steps_to_auth[j].username === '' || $scope.Machine.data.steps_to_auth[j].username === null || $scope.Machine.data.steps_to_auth[j].username === undefined)
                    {
                        $rootScope.handleResponse('Please enter username for step '+step+' in tunneling');
                        return false;
                    }
                    if($scope.Machine.data.steps_to_auth[j].password === '' || $scope.Machine.data.steps_to_auth[j].password === null || $scope.Machine.data.steps_to_auth[j].password === undefined)
                    {
                        $rootScope.handleResponse('Please enter password for step '+step+' in tunneling');
                        return false;
                    }
                }
            }
            else
            {
                $scope.Machine.data.steps_to_auth = [];
            }
        }
        else
        {
            $scope.Machine.data.steps_to_auth = [];
        }

        sendUpdatedMachine.steps_to_auth = $scope.Machine.data.steps_to_auth;
        sendUpdatedMachine.included_in = [];
        for(var b=0; b<$scope.includedIn.length; b++)
        {
            sendUpdatedMachine.included_in.push($scope.includedIn[b]._id.$oid);
        }

        UpdateMachine.update(sendUpdatedMachine,function (updateSuccessMachineResponse){
            $scope.isMachineUpdated = updateSuccessMachineResponse.result;
            var machineCountFlag = 0;
            var myFavMachineToUpdate =[];
            var favMachineId = '';

            if ($scope.favouriteMachines)
            {
                for(var k in $scope.favouriteMachines) myFavMachineToUpdate.push(k);
                for(var a=0; a < myFavMachineToUpdate.length; a++)
                {
                    var data = $scope.favouriteMachines[myFavMachineToUpdate[a]];
                    for(var b=0; b < data.length; b++)
                    {
                        if(sendUpdatedMachine._id.oid === data[b]["machine_id"])
                        {
                            machineCountFlag++;
                            favMachineId = data[b]._id.$oid;
                        }

                    }
                }
                /*for(var k=0; k<$scope.favouriteMachines['Production'].length;k++)
                {
                    if(sendUpdatedMachine._id.oid === $scope.favouriteMachines['Production'][k].machine_id)
                    {
                        machineCountFlag++;
                        favMachineId = $scope.favouriteMachines['Production'][k]._id.$oid;
                    }
                }

                for(var m=0; m<$scope.favouriteMachines['IUT'].length;m++)
                {
                    if(sendUpdatedMachine._id.oid === $scope.favouriteMachines['IUT'][m].machine_id)
                    {
                        machineCountFlag++;
                        favMachineId = $scope.favouriteMachines['IUT'][m]._id.$oid;
                    }
                }

                for(var i=0; i<$scope.favouriteMachines['UT'].length;i++)
                {
                    if(sendUpdatedMachine._id.oid === $scope.favouriteMachines['UT'][i].machine_id)
                    {
                        machineCountFlag++;
                        favMachineId = $scope.favouriteMachines['UT'][i]._id.$oid;
                    }
                }

                for(var l=0; l<$scope.favouriteMachines['ST'].length;l++)
                {
                    if(sendUpdatedMachine._id.oid === $scope.favouriteMachines['ST'][l].machine_id)
                    {
                        machineCountFlag++;
                        favMachineId = $scope.favouriteMachines['ST'][l]._id.$oid;
                    }
                }

                for(var j=0; j<$scope.favouriteMachines['Value Package Master'].length;j++)
                {
                    if(sendUpdatedMachine._id.oid === $scope.favouriteMachines['Value Package Master'][j].machine_id)
                    {
                        machineCountFlag++;
                        favMachineId = $scope.favouriteMachines['Value Package Master'][j]._id.$oid;
                    }
                }

                for(var n=0; n<$scope.favouriteMachines['Other'].length;n++)
                {
                    if(sendUpdatedMachine._id.oid === $scope.favouriteMachines['Other'][n].machine_id)
                    {
                        machineCountFlag++;
                        favMachineId = $scope.favouriteMachines['Other'][n]._id.$oid;
                    }
                }

                for(var o=0; o<$scope.favouriteMachines['UAT'].length; o++)
                {
                    if(sendUpdatedMachine._id.oid === $scope.favouriteMachines['UAT'][o].machine_id)
                    {
                        machineCountFlag++;
                        favMachineId = $scope.favouriteMachines['UAT'][o]._id.$oid;
                    }
                }

                for(var p=0; p<$scope.favouriteMachines['SIT'].length; p++)
                {
                    if(sendUpdatedMachine._id.oid === $scope.favouriteMachines['SIT'][p].machine_id)
                    {
                        machineCountFlag++;
                        favMachineId = $scope.favouriteMachines['SIT'][p]._id.$oid;
                    }
                }

                for(var q=0; q<$scope.favouriteMachines['PET'].length; q++)
                {
                    if(sendUpdatedMachine._id.oid === $scope.favouriteMachines['PET'][q].machine_id)
                    {
                        machineCountFlag++;
                        favMachineId = $scope.favouriteMachines['PET'][q]._id.$oid;
                    }
                }*/
            }

            if($scope.Machine.data.fav === true || $scope.Machine.data.fav==="true")
            {
                if(machineCountFlag===0)
                {
                    favMachineJsonData.user_id = $scope.userId;
                    favMachineJsonData.machine_id = sendUpdatedMachine._id.oid;
                    favMachineJsonData.status = 1;

                    $scope.addFavMachine=AddFavouriteMachine.save(favMachineJsonData,function(addFavMachineResponse){
                        $rootScope.handleResponse(addFavMachineResponse);
                    },
                    function(addFavMachineErrorResponse){
                        $rootScope.handleResponse(addFavMachineErrorResponse);
                    });
                }
            }
            else
            {
                if(machineCountFlag>0)
                {
                    FavMachineDelete.remove({
                        id : favMachineId
                    },
                    function(favMachineDeleteSuccessResponse)
                    {
                        $rootScope.handleResponse(favMachineDeleteSuccessResponse);
                    },
                    function (favMachineDeleteErrorResponse)
                    {
                        $rootScope.handleResponse(favMachineDeleteErrorResponse);
                    });
                }
            }

            delete $scope.selectedMachineId;
            delete $scope.selectedMachineName;
            delete $scope.machines;
            delete $scope.Machine;
            delete $scope.favouriteMachines;

            GetAllMachine.get({
            },
            function(successResponse){
                $scope.machines = successResponse.data.data;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            $scope.userData = $rootScope.userProfile.userData.user;

            $scope.getUserProfile = UserProfile.get({
                username : $scope.userData
            },
            function(getUserProfileResponse)
            {
                $scope.userId = getUserProfileResponse.data._id.$oid;
                var myFavMachine = [];
                $scope.allMyFavMachine = [];

                ViewFavouriteMachine.get({
                    id : $scope.userId
                },
                function(viewFavouriteMachineResponse){
                    $scope.favouriteMachines = viewFavouriteMachineResponse.data;
                    for(var k in $scope.favouriteMachines) myFavMachine.push(k);
                    for(var a=0; a < myFavMachine.length; a++)
                    {
                        var data = $scope.favouriteMachines[myFavMachine[a]];
                        if(data)
                        {
                            for(var b=0; b < data.length; b++)
                            {
                                $scope.allMyFavMachine.push(data[b]["machine_id"]);

                            }
                        }
                    }
                },
                function(viewFavouriteMachineErrorResponse){
                    $rootScope.handleResponse(viewFavouriteMachineErrorResponse);
                });
            },
            function(getUserProfileErrorResponse)
            {
                $rootScope.handleResponse(getUserProfileErrorResponse);
            });
            $state.go('manageMachines');
            $rootScope.handleResponse(updateSuccessMachineResponse);
        },
        function(updateMachineErrorResponse){
            $rootScope.handleResponse(updateMachineErrorResponse);
        });
    };

    $scope.checkSumForPopup = null;
    $scope.viewChecksumPopup = function(checksum)
    {
        $scope.checkSumForPopup = checksum;
        $('#checkSumPopup').show(700);
    };

    $scope.closeChecksumPopup = function()
    {
        $('#checkSumPopup').hide(700);
    };

    $scope.redeployTool = function(version_id, build_number, build_id, machine_id)
    {
        $state.go('reDeployTool',{version_id : version_id, build_number : build_number, build_id : build_id, machine_id:machine_id});
    };

    $scope.redeployDU = function(du_id, build_number, build_id, machine_id)
    {
        $state.go('reDeployDU',{du_id : du_id,build_number : build_number, build_id : build_id, machine_id:machine_id});
    };

    $scope.undeployTool = function(version_id, build_number, build_id, machine_id)
    {
        $state.go('unDeployTool',{version_id : version_id, build_number : build_number, build_id : build_id, machine_id : machine_id});
    };

    $scope.undeployDU = function(du_id, build_number, build_id, machine_id)
    {
        $state.go('unDeployDU',{du_id : du_id, build_number : build_number, build_id : build_id, machine_id : machine_id});
    };
    $scope.DeploymentGroupDetails = function(machineGroupId)
    {
        $state.go('deploymentrequestsbyid', {id : machineGroupId});
    };

    $scope.version = {
        selected : ""
    };

    $scope.getCurrentVersion = function(version)
    {
        $scope.oldVersion = version._id.$oid;
    };

    $scope.sendUpgradeRequestTool = function(form)
    {
        if ($scope.version.selected === "")
        {
            $rootScope.handleResponse('Please select version to upgrade tool!');
            return false;
        }
        $state.go('upgradeTool',{old_version_id : $scope.oldVersion, new_version_id : $scope.version.selected.version_id, machine_id : $stateParams.id});
    };

    $scope.showDUBuilds = function(du)
    {
        $scope.title = 'Select Build';
        if(document.getElementById("select_build_popup").style.display === "none" || document.getElementById("select_build_popup").style.display === "")
        {
            $scope.duDetails = du;
            $('#select_build_popup').show(700);
        }
        else
        {
            $('#select_build_popup').hide(700);
        }
    };

    $scope.closeSelectBuild = function()
    {
        $('#select_build_popup').hide(700);
    };

    $scope.setDUBuild = function(build)
    {
        $scope.selectedBuild = JSON.parse(build);
    };

    $scope.buildToDeploy = '';

    $scope.revertDeployedDU = function()
    {
        $('#select_build_popup').hide(700);
        $scope.revertDeployment.duDataList = [];
        var machineList = [];
        machineList.push($scope.duDetails.machine_id);
        $scope.revertDeployment.duDataList.push({"du_id" : $scope.duDetails._id.$oid,
        "previous_build_id" : $scope.duDetails.build_id,
        "previous_build_number" : $scope.duDetails.build_no,
        "machine_id" :  machineList,
        "new_build_id" :   $scope.selectedBuild._id.$oid,
        "new_build_number" : $scope.selectedBuild.build_number});

        $state.go('revertDU',{id:JSON.stringify($scope.revertDeployment)});
    };

    $scope.selectMachineGroupToView = function(MachineGroup_id)
    {
          $state.go('editMachineGroup',{id:MachineGroup_id});
    };

});
});