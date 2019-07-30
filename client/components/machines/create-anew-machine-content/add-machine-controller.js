define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'toolTips',
'userServicesApp', 'machineServicesApp'],function (app) {
  'use strict';

    var addNewMachineControllerApp = angular.module('addNewMachineControllerApp', ['ui.router', '720kb.tooltips',
    'userServicesApp', 'machineServicesApp']);

    addNewMachineControllerApp.controller('AddMachineController', function ($scope, $rootScope, $stateParams, Machine, $window, $state, GetAllMachineTypes, MachineAdd, Users, AddFavouriteMachine, UserProfile, TestMachine, MachineGroup, TagsAll,UserGroup) {
        $scope.envVars = [];

        $scope.newMachineData = {
            permitted_users : [],
            included_in : [],
            permitted_teams:[],
            port : 22,
            shell_type : 'not required',
            reload_command : 'not required',
            tunneling_flag:false,
            tag : [],
            fav : false,
            auth_type : ''
        };

        $scope.machinetype = {
            selected : ''
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

       $scope.permitted_users = [];
       if($scope.permitted_users.includes($rootScope.userProfile.userData)=== false)
       {
           $scope.permitted_users.push($rootScope.userProfile.userData);
       }
       $scope.included_in = [];
       $scope.permitted_teams = [];

        $scope.authtypespush = {
            selected : ""
        };

        $scope.machine = {
            permitted_users : ''
        };

        $scope.auth_types_push = [
            "SSH" , "Telnet"
        ];
        $scope.step = {
            type : ""
        };
        var stepLength = 1;
        $scope.steps_in_push = [];

        $scope.steps_in_push.length = 0;

        $scope.setReloadCommand = function(value)
        {
            $scope.reload_command = value;
        };

        $scope.discardMachineChanges = function()
        {
            $state.go('manageMachines');
        };

        $scope.flexibleAttributes = {};
        $scope.faNameValueMap = {};
        $scope.faDefLoaded = function(faDef){
            $scope.flexibleAttributes = faDef;
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

        $scope.changeMachineFavoriteParam = function(param)
        {
            if(param === 'true' || param === true)
            {
                $scope.newMachineData.fav = false;
            }
            else
            {
                $scope.newMachineData.fav = true;
            }
        };

        $scope.addUser = function(user)
        {
            var user_flag = 0;
            var ind = 0;
            if($scope.permitted_users)
            {
                for(var c=0;  c<$scope.permitted_users.length; c++)
                {
                    if(user._id.$oid===$scope.permitted_users[c]._id.$oid)
                    {
                        user_flag++;
                        ind = c;
                    }
                }

                if(user_flag===0)
                {
                    $scope.permitted_users.push(user);
                }
                else
                {
                    $scope.permitted_users.splice(ind, 1);
                }
            }
            else
            {
                $scope.permitted_users = [];
                $scope.permitted_users.push(user);
            }
        };

        $scope.removeUser = function(user)
        {
            for(var a=0; a<$scope.permitted_users.length; a++)
            {
                if($scope.permitted_users[a]._id.$oid === user._id.$oid)
                {
                    $scope.permitted_users.splice(a, 1);
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
            if(!$scope.permitted_users)
            {
                $scope.permitted_users = [];
            }
            for(var j=0; j<$scope.permitted_users.length; j++)
            {
                if(user === $scope.permitted_users[j].user)
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

        $scope.addToMachineGroup = function(group)
        {
            var group_flag = 0;
            var ind = 0;
            if($scope.included_in.length>0)
            {
                for(var c=0;  c<$scope.included_in.length; c++)
                {
                    if(group._id.$oid === $scope.included_in[c].group_id)
                    {
                        group_flag++;
                        ind = c;
                    }
                }

                if(group_flag===0)
                {
                    $scope.included_in.push({'group_name' : group.group_name, 'group_id' : group._id.$oid});
                    for(var d=0; d<$scope.included_in.length; d++)
                    {
                        if($scope.included_in[d].group_id === group._id.$oid)
                        {
                            $scope.included_in[d].selected = true;
                        }
                    }
                }
                else
                {
                    $scope.included_in.splice(ind, 1);
                }
            }
            else
            {
                $scope.included_in.push({'group_name' : group.group_name, 'group_id' : group._id.$oid});
            }
        };

        $scope.removeFromMachineGroup = function(group)
        {
            for(var a=0; a<$scope.newMachineData.included_in.length; a++)
            {
                if($scope.included_in[a].group_id === group.group_id)
                {
                    $scope.included_in.splice(a, 1);
                }
            }

            for(var b=0; b<$scope.MachineGroups.data.length; b++)
            {
                if($scope.MachineGroups.data[b]._id.$oid === group.group_id)
                {
                    $scope.MachineGroups.data[b].selected = false;
                }
            }
        };

        $scope.closeUser = function()
        {
            document.getElementById("add_users").style.display = "none";
        };

        $scope.closeAddMachineGroup = function()
        {
            document.getElementById("add_machine_groups").style.display = "none";
        };


        $scope.addNewStep = function() {
            var newItemNo = $scope.steps_in_push.length+1;
            $scope.steps_in_push.push({ order : newItemNo, port : 22});
        };

        $scope.removeStep = function(index) {
            $scope.steps_in_push.splice(index, 1);
        };

        $scope.selectMachineType = function(type)
        {
            $scope.machine_type = type;
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

        $scope.closeAddTag = function()
        {
            document.getElementById("add_tag").style.display = "none";
        };
        $scope.closeAddUsers = function()
        {
         document.getElementById("add_users").style.display = "none";
        };

        $scope.selectTag = function(tag)
        {
            var tag_flag = 0;
            var ind = 0;
            if($scope.newMachineData.tag.length>0)
            {
                for(var c=0;  c<$scope.newMachineData.tag.length; c++)
                {
                    if(tag.name===$scope.newMachineData.tag[c])
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.newMachineData.tag.push(tag.name);
                }
                else
                {
                    $scope.newMachineData.tag.splice(ind, 1);
                }

            }
            else
            {
                $scope.newMachineData.tag = [];
                $scope.newMachineData.tag.push(tag.name);
            }
        };

        $scope.removeTag = function(tag)
        {
            var tag_flag = 0;
            var ind = 0;
            if($scope.newMachineData.tag.length>0)
            {
                for(var c=0;  c<$scope.newMachineData.tag.length; c++)
                {
                    if(tag===$scope.newMachineData.tag[c])
                    {
                        tag_flag++;
                        ind = c;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.newMachineData.tag.push(tag.name);
                }
                else
                {
                    $scope.newMachineData.tag.splice(ind, 1);
                }

            }
            else
            {
                $scope.newMachineData.tag = [];
                $scope.newMachineData.tag.push(tag.name);
            }
        };

        $scope.isTagSelected = function(tag)
        {
            var flag = 0;
            for(var j=0; j<$scope.newMachineData.tag.length; j++)
            {
                if(tag === $scope.newMachineData.tag[j])
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
        $scope.teams = UserGroup.get({

        },
        function(successResponse){
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
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
        $scope.isTeamSelected = function(team)
        {
            var flag = 0;
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

      var favMachineJsonData={};

      GetAllMachineTypes.get({
      },
      function(successResponse){
        $scope.types = successResponse.data;
      },
      function(errorResponse)
      {
        $rootScope.handleResponse(errorResponse);
      });

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

    MachineGroup.get({
    },
    function(successResponse){
        $scope.MachineGroups = successResponse.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.testConnection = function(form)
    {
        $scope.newMachineErrors = {
            ip : ''
        };
        var sendUpdatedMachine = {};
        sendUpdatedMachine = $scope.newMachineData;
        sendUpdatedMachine.account_id = $rootScope.userProfile.userData.account_details._id.$oid;
        sendUpdatedMachine.machine_type = $scope.machine_type;
        sendUpdatedMachine.shell_type = $scope.newMachineData.shell_type;
        if (!(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(sendUpdatedMachine.ip)))
        {
            $scope.newMachineErrors.ip = 'Please enter valid IP Address!';
            $rootScope.handleResponse('Please enter valid IP Address!');
            return false;
        }
        if(sendUpdatedMachine.shell_type === ' ' || sendUpdatedMachine.shell_type === undefined || sendUpdatedMachine.shell_type === null)
        {
            sendUpdatedMachine.shell_type = '';
        }
        if($scope.newMachineData.reload_command === 'not required')
        {
            sendUpdatedMachine.reload_command = '';
        }
        else
        {
            sendUpdatedMachine.reload_command = $scope.newMachineData.reload_command;
        }

        if($scope.newMachineData.auth_type === 'ssh' && ($scope.newMachineData.password === null || $scope.newMachineData.password === '' || $scope.newMachineData.password === undefined))
        {
            sendUpdatedMachine.password = '12345';
        }

        if(((sendUpdatedMachine.host === '' || sendUpdatedMachine.host === null || sendUpdatedMachine.host === undefined) || (sendUpdatedMachine.username === '' || sendUpdatedMachine.username === null || sendUpdatedMachine.username === undefined) || (sendUpdatedMachine.ip === '' || sendUpdatedMachine.ip === null || sendUpdatedMachine.ip === undefined) || (sendUpdatedMachine.machine_type === '' || sendUpdatedMachine.machine_type === null || sendUpdatedMachine.machine_type === undefined) || (sendUpdatedMachine.reload_command === null || sendUpdatedMachine.reload_command === undefined) || (sendUpdatedMachine.auth_type === '' || sendUpdatedMachine.auth_type === null || sendUpdatedMachine.auth_type === undefined)) || ($scope.newMachineData.auth_type === 'password' && (sendUpdatedMachine.password === '' || sendUpdatedMachine.password === null || sendUpdatedMachine.password === undefined)))
        {
            $rootScope.handleResponse('Mandatory fields required to test connection are missing');
            return false;
        }
        if($scope.newMachineData.tunneling_flag === true)
        {
            sendUpdatedMachine.steps_to_auth = $scope.steps_in_push;
        }
        else
        {
            sendUpdatedMachine.steps_to_auth =[];
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

        TestMachine.save (sendUpdatedMachine, function (testMachineSuccessResponse){
            $rootScope.handleResponse(testMachineSuccessResponse);
            $scope.machineConnectionMessage = testMachineSuccessResponse.message;
        },
        function(testMachineErrorResponse){
            $scope.machineConnectionMessage = testMachineErrorResponse.data;
            $rootScope.handleResponse(testMachineErrorResponse);
        });
    };

    $scope.createNewMachine = function(form)
    {
        $scope.newMachineErrors = {
            ip : ''
        };
        $scope.newMachineData.permitted_users = [];
        if (!(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test($scope.newMachineData.ip)))
        {
            $scope.newMachineErrors.ip = 'Please enter valid IP Address!';
            $rootScope.handleResponse('Please enter valid IP Address!');
            return false;

        }

        $scope.requestForm=true;
        var jsonData = {};

        jsonData = $scope.newMachineData;
        var port = angular.copy(jsonData.port);
        jsonData.port = port;
        jsonData.machine_type = $scope.machine_type;
        jsonData.account_id=$rootScope.userProfile.userData.account_details._id.$oid;
        jsonData.tunneling_flag= $scope.newMachineData.tunneling_flag;
        jsonData.flexible_attributes = $scope.faNameValueMap;
        jsonData.environment_variables = $scope.envVars;
        for(var i=0; i<$scope.permitted_users.length; i++)
        {
            $scope.newMachineData.permitted_users.push($scope.permitted_users[i]._id.$oid);
        }
        for(var j=0; j<$scope.included_in.length; j++)
        {
            $scope.newMachineData.included_in.push($scope.included_in[j].group_id);
        }
//        if( jsonData.permitted_users.length === 0)
//        {
//            jsonData.permitted_users.push("all");
//        }
        for(var k=0; k<$scope.permitted_teams.length; k++)
        {
            $scope.newMachineData.permitted_teams.push($scope.permitted_teams[k]._id.$oid);
        }
        jsonData.status = "1";

        if(jsonData.shell_type === 'not required')
        {
            jsonData.shell_type = '';
        }

        if(jsonData.reload_command === 'not required')
        {
            jsonData.reload_command = '';
        }
        else
        {
            jsonData.reload_command = jsonData.reload_command;
        }

        if(jsonData.auth_type === 'ssh' && (jsonData.password === null || jsonData.password === '' || jsonData.password === undefined))
        {
            jsonData.password = '12345';
        }

        if(((jsonData.host === '' || jsonData.host === null || jsonData.host === undefined) || (jsonData.username === '' || jsonData.username === null || jsonData.username === undefined) || (jsonData.ip === '' || jsonData.ip === null || jsonData.ip === undefined) || (jsonData.machine_type === '' || jsonData.machine_type === null || jsonData.machine_type === undefined) || (jsonData.reload_command === null || jsonData.reload_command === undefined)) || ( (jsonData.password === '' || jsonData.password === null || jsonData.password === undefined) && jsonData.auth_type === 'password'))
        {
            $rootScope.handleResponse('Mandatory fields required to create new machine are missing');
            return false;
        }

        for(var l=0; l<$scope.steps_in_push.length; l++)
        {
            var step = l+1;
            if($scope.steps_in_push[l].type === '' || $scope.steps_in_push[l].type === null || $scope.steps_in_push[l].type === undefined)
            {
                $rootScope.handleResponse('Please select authentication type for step '+step+' in tunneling');
                return false;
            }
            if($scope.steps_in_push[l].host === '' || $scope.steps_in_push[l].host === null || $scope.steps_in_push[l].host === undefined)
            {
                $rootScope.handleResponse('Please enter host name for step '+step+' in tunneling');
                return false;
            }
            if($scope.steps_in_push[l].port === '' || $scope.steps_in_push[l].port === null || $scope.steps_in_push[l].port === undefined)
            {
                $rootScope.handleResponse('Please enter port number for step '+step+' in tunneling');
                return false;
            }
            if($scope.steps_in_push[l].username === '' || $scope.steps_in_push[l].username === null || $scope.steps_in_push[l].username === undefined)
            {
                $rootScope.handleResponse('Please enter username for step '+step+' in tunneling');
                return false;
            }
            if($scope.steps_in_push[l].password === '' || $scope.steps_in_push[l].password === null || $scope.steps_in_push[l].password === undefined)
            {
                $rootScope.handleResponse('Please enter password for step '+step+' in tunneling');
                return false;
            }
        }
        jsonData.steps_to_auth = $scope.steps_in_push;
        $scope.getUserProfile = UserProfile.get({
            username : $rootScope.userProfile.userData.user
        },
        function(response)
        {
            $scope.userId = response.data._id.$oid;
            $scope.account_id = response.data.account_details._id.$oid;
            jsonData.account_id = $scope.account_id;
            MachineAdd.save (jsonData, function (addMachineSuccessResponse){
                $rootScope.handleResponse(addMachineSuccessResponse);
                $scope.machineId = response.data.id;
                if($scope.newMachineData.fav === true || $scope.newMachineData.fav === 'true')
                {
                    favMachineJsonData.user_id = $scope.userId;
                    favMachineJsonData.machine_id = addMachineSuccessResponse.data.id;
                    favMachineJsonData.status = 1;
                    AddFavouriteMachine.save(favMachineJsonData,function(addFavMachineResponse){
                        $rootScope.handleResponse(addFavMachineResponse);
                    },
                    function(addFavMachineErrorResponse){
                        $rootScope.handleResponse(addFavMachineErrorResponse);
                    });
                }
                $scope.displayTab = 0;
                $state.go('manageMachines');
            },
            function(addMachineErrorResponse){
                $rootScope.handleResponse(addMachineErrorResponse);
            });
        },
        function(errorResponse)
        {
            $scope.errorAdd="true";
            error = errorResponse.data;
            $rootScope.handleResponse(error);
        });
    };

});
});