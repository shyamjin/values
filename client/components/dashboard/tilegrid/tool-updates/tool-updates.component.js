require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['requestTabComponent', 'settingsServicesApp']
});

define(['angular'],function (app) {
  'use strict';

var updatedToolsComponentControllerApp = angular.module('updatedToolsComponentControllerApp', ['requestTabComponent', 'settingsServicesApp']);

updatedToolsComponentControllerApp.controller('UpdatedToolListController', function ($scope, $state, $rootScope, UpdatedTools, ImportUpdate) {
    $scope.selectedTools = [];
    $scope.selectedToolsList = [];
    $scope.selectTool = function(tool)
    {
        var flag = 0;
        var ind = 0;
        var length = $scope.selectedTools.length;
        if(length>0)
        {
            for(var id=0; id<length; id++)
            {
                if($scope.selectedTools[id] === tool._id.$oid)
                {
                    flag++;
                    ind = id;
                }
            }
            if(flag===0)
            {
                $scope.selectedTools.push(tool._id.$oid);
                $scope.selectedToolsList.push(tool.name);
                for(var a=0; a<$scope.applications.length; a++)
                {
                    if($scope.applications[a].name === tool.name)
                    {
                        $scope.applications[a].isSelected = true;
                    }
                }
            }
            else
            {
                for(var b=0; b<$scope.applications.length; b++)
                {
                    if($scope.applications[b].name === $scope.selectedToolsList[ind])
                    {
                        $scope.applications[b].isSelected = false;
                    }
                }
                $scope.selectedTools.splice(ind, 1);
                $scope.selectedToolsList.splice(ind, 1);
            }
        }
        else
        {
            for(var c=0; c<$scope.applications.length; c++)
            {
                if($scope.applications[c].name === tool.name)
                {
                    $scope.applications[c].isSelected = true;
                }
            }
            $scope.selectedTools.push(tool._id.$oid);
            $scope.selectedToolsList.push(tool.name);
        }
    };

    $scope.isToolSelected = function(tool)
    {
        var flag = 0;
        for(var j=0; j<$scope.selectedToolsList.length; j++)
        {
            if(tool.name === $scope.selectedToolsList[j])
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

    $scope.removeTool = function(tool)
    {
        var flag = 0;
        var ind = 0;
        var length = $scope.selectedTools.length;
        if(length>0)
        {
            for(var id=0; id<length; id++)
            {
                if($scope.selectedToolsList[id] === tool)
                {
                    flag++;
                    ind = id;
                }
            }
            if(flag===0)
            {
                $scope.selectedTools.push(tool._id.$oid);
                $scope.selectedToolsList.push(tool.name);
                for(var a=0; a<$scope.applications.length; a++)
                {
                    if($scope.applications[a].name === tool.name)
                    {
                        $scope.applications[a].isSelected = true;
                    }
                }
            }
            else
            {
                for(var b=0; b<$scope.applications.length; b++)
                {
                    if($scope.applications[b].name === $scope.selectedToolsList[ind])
                    {
                        $scope.applications[b].isSelected = false;
                    }
                }
                $scope.selectedTools.splice(ind, 1);
                $scope.selectedToolsList.splice(ind, 1);
            }
        }
        else
        {
            for(var c=0; c<$scope.applications.length; c++)
            {
                if($scope.applications[c].name === tool.name)
                {
                    $scope.applications[c].isSelected = true;
                }
            }
            $scope.selectedTools.push(tool._id.$oid);
            $scope.selectedToolsList.push(tool.name);
        }
    };

    $scope.selectMultipleToolsForUpdate = function(selectedTools)
    {
        if(selectedTools.length>0)
        {
            var jsonData = {};
            jsonData.ids = [];
            for(var i=0; i<selectedTools.length; i++)
            {
                jsonData.ids.push(selectedTools[i]);
            }
            jsonData.type = 'updatetool';

            ImportUpdate.save(jsonData, function(importSuccessResponse){
                $scope.responseMessage = importSuccessResponse;
                $state.go('toolImportUpdateStatus', {'request_id' : jsonData.ids});
                $rootScope.handleResponse(importSuccessResponse);
            },
            function(importErrorResponse)
            {
                $rootScope.handleResponse(importErrorResponse);
            });
        }
    };

    $scope.updateImportTool = function(id)
    {
        var jsonData = {};
        jsonData.ids = [];
        jsonData.ids.push(id);
        jsonData.type = 'updatetool';

        ImportUpdate.save(jsonData, function(importSuccessResponse){
            $scope.responseMessage = importSuccessResponse;
            $state.go('toolImportUpdateStatus', {'request_id' : jsonData.ids});
            $rootScope.handleResponse(importSuccessResponse);
            delete $scope.applications;
            $scope.applications = UpdatedTools.query({
            },
            function(application)
            {
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        },
        function(importErrorResponse)
        {
            $rootScope.handleResponse(importErrorResponse);
        });
    };

    $scope.applications = UpdatedTools.query({
    },
    function(successResponse)
    {
        if(successResponse.data)
        {
            $rootScope.updatedToolsCount = successResponse.data.UpdateTool.length;
            $rootScope.newToolsCount = successResponse.data.ImportTool.length;
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

});

});