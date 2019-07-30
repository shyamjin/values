define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

  var addUsersControllerApp = angular.module('addUsersControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
  addUsersControllerApp.controller('AddNewUserController', function($scope, $stateParams, $http, $state, $rootScope, Users, Role, UserAdd,GetAccount,UserGroup, TagsAll){
    var jsonData = {};
    $scope.includedIn = [];
    $scope.useradd_errors=[];
    $scope.newUsersData=[];
    var jsonIncludedIn=[];
    $scope.role = {
        selected : ""
    };
    $scope.account={
        selected: ""
    };
    $scope.roles = Role.get({
        id:"all"
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.accounts = GetAccount.get({
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.exist=function(item)
    {
        var flag=false;
        for(var i=0;i<$scope.includedIn.length;i++)
        {
            if($scope.includedIn[i].team_id === item.team_id)
            {
                flag=true;
                return flag;
            }
            else
            {
                flag=false;
                continue;}
            }
            return flag;
        };

        $scope.showAddTeam = function()
        {
            if(document.getElementById("add_user_to_team").style.display === "none" || document.getElementById("add_user_to_team").style.display === "")
            {
                document.getElementById("add_user_to_team").style.display = "block";
            }
            else
            {
               document.getElementById("add_user_to_team").style.display = "none";
           }
       };

       $scope.closeAddTeam = function()
       {
        document.getElementById("add_user_to_team").style.display = "none";
    };

    $scope.isTeamSelected = function(team)
    {
        var flag = 0;
        if(!$scope.includedIn)
        {
            $scope.includedIn = [];
        }
        for(var a=0; a<$scope.includedIn.length; a++)
        {
            if($scope.includedIn[a].team_id === team)
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

    $scope.toggleSelection=function(item)
    {
        var count=0;
        var group_length = $scope.includedIn.length;

        if(group_length>0)
        {
            for(var a=0; a<group_length; a++)
            {
                if($scope.includedIn[a].team_id === item.team_id)
                {
                    $scope.includedIn.splice(a, 1);
                }
                else
                {
                    count++;
                }
            }
            if(count===group_length)
            {
                $scope.includedIn.push({'team_id' : item.team_id, 'team_name' : item.team_name});
            }
        }
        else
        {
            $scope.includedIn.push({'team_id' : item.team_id, 'team_name' : item.team_name});
        }
    };

    $scope.userGroupList = [];
    $scope.userGroups=UserGroup.get({
    },
    function(userGroupSuccessResponse)
    {
        for(var a=0; a<userGroupSuccessResponse.data.length; a++)
        {
            $scope.userGroupList.push({'team_id' : userGroupSuccessResponse.data[a]._id.$oid,'team_name' : userGroupSuccessResponse.data[a].team_name});
        }
        $rootScope.handleResponse(userGroupSuccessResponse);
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.addNewUser = function(addNewUserForm)
    {
        $scope.useradd_errors.userName ='';
        if($scope.newUsersData.userName==='' || $scope.newUsersData.userName===undefined )
        {
            $scope.useradd_errors.userName ="Please enter user name!";
            return false;
        }

        $scope.useradd_errors.employeeId ='';
        if($scope.newUsersData.employeeId==='' || $scope.newUsersData.employeeId===undefined || $scope.newUsersData.employeeId==='0')
        {
            $scope.useradd_errors.employeeId ="Please enter employee id!";
            return false;
        }
        var user_email = $scope.newUsersData.email;
        $scope.useradd_errors.email='';
        if($scope.newUsersData.email==='')
        {
            $scope.useradd_errors.email="Please enter email address!";
            return false;
        }
        else if($scope.newUsersData.email===undefined || $scope.newUsersData.email!=='' )
        {
            $scope.useradd_errors.email='';
            if($scope.newUsersData.email===undefined)
            {
                $scope.useradd_errors.email ="Please enter valid email address!";
                return false;
            }
            var atpos = $scope.newUsersData.email.indexOf("@");
            var dotpos = $scope.newUsersData.email.lastIndexOf(".");
            if (atpos<1 || dotpos<atpos+2 || dotpos+2>=$scope.newUsersData.email.length)
            {
                $scope.useradd_errors.email ="Please enter valid email address!";
                return false;
            }
        }
        $scope.useradd_errors.role ='';
        if($scope.newUsersData.role==='' || $scope.newUsersData.role===undefined )
        {
            $scope.useradd_errors.role ="Please select role!";
            return false;
        }
        $scope.useradd_errors.account ='';
        if($scope.account.selected==='' || $scope.account.selected===undefined)
        {
            $scope.useradd_errors.account ="Please select Account!";
            return false;
        }
        jsonData.employeeid = $scope.newUsersData.employeeId;
        jsonData.user = $scope.newUsersData.userName;
        jsonData.included_in = [];
        jsonData.roleid = $scope.newUsersData.role;
        jsonData.email = $scope.newUsersData.email;
        jsonData.accountid = $scope.account.selected;

        if($scope.newUsersData.homepage === 'Tool Dashboard' || $scope.newUsersData.homepage === '' || $scope.newUsersData.homepage === null || $scope.newUsersData.homepage === undefined)
        {
            jsonData.homepage = 'dashboard';
        }
        else
        {
            jsonData.homepage = 'duDashboard';
        }

        for(var i=0;i<$scope.includedIn.length;i++)
        {
            jsonData.included_in.push($scope.includedIn[i].team_id);
        }

        $scope.user_id = UserAdd.save(jsonData,function(response){
            $scope.newUsersData=[];
            $state.go('users');
            delete $scope.users;
            $rootScope.handleResponse(response);
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };
});
});