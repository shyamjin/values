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

var editToolSetToolSearchComponentControllerApp = angular.module('editToolSetToolSearchComponentControllerApp', []);

editToolSetToolSearchComponentControllerApp.controller("EditToolSearchToolsController",function($scope, $stateParams, $rootScope) {
    $scope.selectValueToolSet = [];

    $scope.selectValueToolSet = $rootScope.toolSetDetailsFactory.getToolList();
    $rootScope.$on('setSelectedToolList', function(event, args){
        $scope.selectedTools = args.selectedTools;
    });
    $scope.addTool = function(tool)
    {
        if( $scope.selectedTools.length ==0)
        {
            $scope.selectValueToolSet= [];
        }
        var toolset_flag = 0;
        var tools_length = $scope.selectValueToolSet.length;
        var ind = 0;
        if(tools_length>0)
        {
            for(var c=0;  c<$scope.selectValueToolSet.length; c++)
            {
                if((tool.tool_id===$scope.selectValueToolSet[c].tool_id))
                {
                    toolset_flag++;
                    ind = c;
                }
            }

            if(toolset_flag===0)
            {
                $scope.selectValueToolSet.push(tool);
            }

        }
        else
        {
             $scope.selectValueToolSet = [];
             $scope.selectValueToolSet.push(tool);
        }
        $rootScope.$emit('setSelectedToolList', {selectedTools : $scope.selectValueToolSet});
    };
});

});