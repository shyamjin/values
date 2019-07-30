define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

  var editRoleControllerApp = angular.module('editRoleControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
  editRoleControllerApp.controller('EditRoleController', function($scope, $stateParams, $rootScope, $state, PermissionGroup, RoleEdit, Role, $timeout){
    $scope.availablePermissionGroup = {
      selected : ""
    };
    $scope.removedPermissionGroup = {
      selected : ""
    };
    var editRoleWithNewPermissionGroup = {};

    editRoleWithNewPermissionGroup._id = {
      oid : ""
    };
    editRoleWithNewPermissionGroup.permissiongroup = [];
    var permission_groups = [{}];
    $scope.roleData = Role.get({
      id:"view"+"/"+$stateParams.id
    },
    function(successResponse)
    {
      $rootScope.handleResponse(successResponse);
    },
    function(errorResponse)
    {
      $rootScope.handleResponse(errorResponse);
    });

    $scope.permissiongroup = PermissionGroup.get({
      id:"all"
    },
    function(response)
    {
      $timeout(function()
      {
        $scope.lengthOfAllPermissionGroups = response.data.length;
        $scope.lengthOfAssignedGroups = $scope.roleData.data.permissiongroup.length;
        $scope.availablePermissionGroup = [];
        var count = 1;
        var flag=0;
        for(var i=0;i<$scope.lengthOfAllPermissionGroups;i++)
        {
          flag=0;
          for(var j=0;j<$scope.lengthOfAssignedGroups;j++)
          {
            if(response.data[i]._id.$oid===$scope.roleData.data.permissiongroup[j])
            {


             flag=flag+1;
           }
           else
           {
            console.log("Data already available in role permission group ");
            console.log(response.data[i]);
            count = count+1;
            console.log(count);
          }
        }
        if(flag>0)
        {
         console.log("machine is present");
       }
       else if(flag===0)
       {
         $scope.availablePermissionGroup[i] = response.data[i];
       }
     }

     var all_permissions = [];
     all_permissions.push($scope.roleData.data.permissiongroup_details);
     $scope.mixed_permissions = all_permissions;

     $scope.getNewData = function()
     {
      for(var k=0;k<$scope.availablePermissionGroup.selected.length;k++)
      {
        var item = $scope.availablePermissionGroup.selected[k];
        var ind = $scope.availablePermissionGroup.indexOf(item);
        if(all_permissions[0].indexOf(item) <= -1)
        {
          all_permissions[0].push(item);
          $scope.availablePermissionGroup.splice(ind,1);
        }
      }
      $scope.availablePermissionGroup.selected = '';
    };

    $scope.removeOldData = function(id)
    {
      var len = all_permissions[0].length;
      for(var l=0;l<len;l++)
      {
        if((all_permissions[0][l]._id.$oid)===id)
        {
          $scope.availablePermissionGroup.push(all_permissions[0][l]);
          all_permissions[0].splice(l,1);
        }
      }
    };

    $scope.editRole = function(form)
    {
      var counter=0;
      var jsonData = {};
      var a = $("form").serializeArray();
      $.each(a, function () {
        if (jsonData[this.name]) {
          if (!jsonData[this.name].push) {
            jsonData[this.name] = [jsonData[this.name]];
          }
          jsonData[this.name].push(this.value || '');
        }
        else {
          jsonData[this.name] = this.value || '';
        }
      });

      editRoleWithNewPermissionGroup._id.oid = jsonData.role_id;
      for(var m=0;m<all_permissions[0].length;m++)
      {
        editRoleWithNewPermissionGroup.permissiongroup[m] = all_permissions[0][m]._id.$oid;
      }

      editRoleWithNewPermissionGroup.name = jsonData.role_name;

      $scope.roleStatus = "Role Updated";
      RoleEdit.update(editRoleWithNewPermissionGroup, function(response){
        if(response.result=="success")
        {
          $state.go('manageRoles');
          $rootScope.handleResponse(response);
        }
      },
      function(errorResponse)
      {
        $rootScope.handleResponse(errorResponse);
      });
    };
  },500);
    },
    function(errorResponse)
    {
      $rootScope.handleResponse(errorResponse);
    });
  });
});
