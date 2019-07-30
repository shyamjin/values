/*
Author - nlate
Description -
    1. Controller that handles with list of tools and filters
Methods -
    1.
Uses -
    1. Create Tool Set - components/tools/create-tool-set/tools-search-column/toolssearchcolumn.component.html
*/

define(['angular'],function (app) {
  'use strict';

var createToolSetToolSearchComponentControllerApp = angular.module('createToolSetToolSearchComponentControllerApp', []);

createToolSetToolSearchComponentControllerApp.controller("SearchToolsController",function($scope, $stateParams, $rootScope) {
    $scope.selectedTools = [];
    //scope.selectedTools = $rootScope.toolSetDetailsFactory.getToolList();
    $scope.addTool = function(tool)
    {
        var toolset_flag = 0;
        var tools_length = $scope.selectedTools.length;
        var ind = 0;
        if(tools_length>0)
        {
            for(var c=0;  c<$scope.selectedTools.length; c++)
            {
                if((tool.tool_id===$scope.selectedTools[c].tool_id))
                {
                    toolset_flag++;
                    ind = c;
                }
            }

            if(toolset_flag===0)
            {
                $scope.selectedTools.push(tool);
            }

        }
        else
        {
             $scope.selectedTools = [];
             $scope.selectedTools.push(tool);
        }
        $rootScope.$emit('setSelectedToolList', {selectedTools : $scope.selectedTools});
    };
});

});