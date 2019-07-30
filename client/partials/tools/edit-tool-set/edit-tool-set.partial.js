/*
Author - nlate
Description -
    1. Controller that handles with the common operations required in create tool set
Methods -
    1.
Uses -
    1. Edit Tool Set - partials/tools/edit-tool-set/edit-tool-set.partial.html
*/

define(['angular', 'toolSetServicesApp', 'editToolSetInfoComponentControllerApp', 'editToolSetBarComponentControllerApp', 'editToolSetAddToolComponentControllerApp', 'editToolSetToolSearchComponentControllerApp'],function (app) {
  'use strict';

var editToolSetPartialControllerApp = angular.module('editToolSetPartialControllerApp', ['toolSetServicesApp', 'editToolSetInfoComponentControllerApp', 'editToolSetBarComponentControllerApp', 'editToolSetAddToolComponentControllerApp', 'editToolSetToolSearchComponentControllerApp']);

editToolSetPartialControllerApp.controller("EditToolSetPartialController",function($scope, $stateParams, ToolSetByID, GetAllTools, $rootScope) {
    var toolList = [];
    ToolSetByID.get({
       id: $stateParams.id
    },
    function(toolsetViewSuccessResponse)
    {
        $scope.toolSetData = toolsetViewSuccessResponse;
        if(toolsetViewSuccessResponse.data.logo)
        {
            var logoFileName = toolsetViewSuccessResponse.data.logo;
            var lenLogo = logoFileName.length;
            $scope.logoFilename = logoFileName.substring(20, lenLogo);
            $scope.logoFileSelected = $scope.logoFilename;
        }

        $scope.applicationsAll = GetAllTools.get({
           id: "all",
           status: "active,indevelopment,deprecated",
           page: 0,
           perpage: 0
        },
        function(application)
        {
            for(var t1=0; t1<application.data.data.length; t1++)
            {
                for(var t2=0; t2<application.data.data[t1].versions.length; t2++)
                {
                    for(var t3=0; t3<toolsetViewSuccessResponse.data.tool_set.length; t3++)
                    {
                        if(toolsetViewSuccessResponse.data.tool_set[t3].version_id === application.data.data[t1].versions[t2].version_id)
                        {
                            toolList.push({'tool_id' : application.data.data[t1]._id.$oid, 'status' : application.data.data[t1].status, 'tool_name' : application.data.data[t1].name, 'version_name' : application.data.data[t1].versions[t2].version_name, 'version_id' : application.data.data[t1].versions[t2].version_id, 'version_number' : application.data.data[t1].versions[t2].version_number, 'tool_version' : application.data.data[t1].name+' '+application.data.data[t1].versions[t2].version_number});
                        }
                    }
                }
            }

            $rootScope.toolSetDetailsFactory.setToolSetData(toolsetViewSuccessResponse.data);
            $rootScope.toolSetDetailsFactory.setToolList(toolList);
            $rootScope.$emit('updateToolList', {selectedTools : toolList});
            $rootScope.$emit('setSelectedToolList', {selectedTools : toolList});
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    },
    function(toolsetViewErrorResponse)
    {
       $rootScope.handleResponse(toolsetViewErrorResponse);
    });
});

});