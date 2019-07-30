define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

  var manageRolesControllerApp = angular.module('manageRolesControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
  manageRolesControllerApp.controller('ManageRolesController', function($scope, $stateParams, $state, PermissionGroup, RoleAdd, Role, RolePermissionEdit, $rootScope){
    $scope.getRole = function(role, href)
    {
        var ref = document.getElementById(href); //or grab it by tagname etc
        if($rootScope.userProfile.userData.rolename==='SuperAdmin' || role===$rootScope.userProfile.userData.rolename)
        {
          return '';
        }
        else if($rootScope.userProfile.userData.rolename==='Admin' && role==='SuperAdmin')
        {
          document.getElementById(href).removeAttribute("href");
          return 'disabled';
        }
        else if(($rootScope.userProfile.userData.rolename==='Admin' && role==='Operator') || ($rootScope.userProfile.userData.rolename==='Admin' && role==='Guest'))
        {
          return '';
        }
        else
        {
          document.getElementById(href).removeAttribute("href");
          return 'disabled';
        }
      };

      $scope.finalData =[
      {
       role_id:'',
       permissiongroup:[]
     }];

     var rolesSucessData=[];
     $scope.roles = Role.get({
      id:"all"
    },
    function(SucessResponse)
    {
      if(SucessResponse.data)
      {
        rolesSucessData= SucessResponse.data;
        for(var k=0;k<rolesSucessData.length;k++)
        {
          $scope.finalData[k] = {
            role_id:'',
            permissiongroup:[]
          };
          $scope.finalData[k].role_id=rolesSucessData[k]._id.$oid;
          $scope.finalData[k].permissiongroup=rolesSucessData[k].permissiongroup;
        }
      }
    },
    function(errorResponse)
    {
      $rootScope.handleResponse(errorResponse);
    });

     $scope.permissiongroup = PermissionGroup.get({
      id:"all"
    },
    function(errorResponse)
    {
      $rootScope.handleResponse(errorResponse);
    });

     $scope.discardRolePermissionChanges=function()
     {
      $state.go("users");
    };

    $scope.exist=function(permissiongroup,role)
    {
      var flag=false;
      for(var i=0;i<role.permissiongroup.length;i++)
      {
        if(permissiongroup._id.$oid=== role.permissiongroup[i])
        {
          flag=true;
          return flag;
        }
        else
        {
          continue;
        }
      }
      return flag;
    };

    $scope.toggleSelection=function(permissionGroupSelected,role)
    {
      var group_length = $scope.finalData.length;
      if(group_length>0)
      {
        for(var a=0; a<group_length; a++)
        {
          if($scope.finalData[a].role_id === role._id.$oid)
          {
            var permissionLength=$scope.finalData[a].permissiongroup.length;
            if(permissionLength >0)
            {
              var pushpermissiongroup=[];
              var pushFlag=true;
              for(var b=0;b<permissionLength;b++)
              {
                if($scope.finalData[a].permissiongroup[b]===permissionGroupSelected._id.$oid)
                {
                  $scope.finalData[a].permissiongroup.splice(b, 1);
                  pushFlag=false;
                  b=b-1;
                  for(var j=0;j<pushpermissiongroup.length;j++)
                  {
                    if(pushpermissiongroup[j]===permissionGroupSelected._id.$oid)
                    {
                      pushpermissiongroup.splice(j,1);
                      j=j-1;
                      break;
                    }
                  }
                }
              }
              if(pushFlag===true)
              {
                pushpermissiongroup.push(permissionGroupSelected._id.$oid);
              }
              if(pushpermissiongroup.length>0)
              {
                $scope.finalData[a].permissiongroup.push(pushpermissiongroup[0]);
                pushpermissiongroup=[];
              }
            }
            else
            {
              $scope.finalData[a].permissiongroup.push(permissionGroupSelected._id.$oid);
            }
          }
        }
      }
      else
      {
        $scope.finalData.push({'role_id' : role._id.$oid, 'permissiongroup' : permissionGroupSelected._id.$oid});
      }
    };

    $scope.updateRolesPermissions = function(form)
    {
      $scope.roleStatus = "Role Updated";
      $scope.roleStatus = RolePermissionEdit.update({"roles":$scope.finalData}, function(response){
        if(response.result=="success")
        {
          $rootScope.handleResponse(response);
          $state.transitionTo($state.current, $stateParams, {
            reload: true, inherit: false, notify: true
          });
        }
      },
      function(errorResponse)
      {
        $rootScope.handleResponse(errorResponse);
      });
    };
  });
});
