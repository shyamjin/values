/*
Author - nlate
Description -
    1. Controller that handles with the add tool in the tool set
Methods -
    1.
Uses -
    1. Create Tool Set - components/tools/create-tool-set/popups/addtool-popup.component.html
*/

define(['angular'],function (app) {
  'use strict';

var createToolSetAddToolComponentControllerApp = angular.module('createToolSetAddToolComponentControllerApp', []);

createToolSetAddToolComponentControllerApp.controller("AddToolController",function($scope, $rootScope, GetAllTools, AllToolSet) {
    $scope.filterType = 'All';
    $scope.statusFlag = true;
    $scope.tagsFlag = false;
    $scope.toolsetsFlag = false;
    var jsonData = {};
    var statusFilter = [];
    var tagFilter = [];
    var toolsetFilter = [];
    $scope.selectedTools = [];
    $scope.allTools = [];

    $scope.openFilter = function()
    {
        if(document.getElementById("open_filter").style.display === "none" || document.getElementById("open_filter").style.display === "")
        {
            $('#open_filter').show(700);
            $scope.open_filter = true;
        }
        else
        {
            $('#open_filter').hide(700);
            $scope.open_filter = false;
        }
    };

    GetAllTools.get({
       id: "all",
       status: "active,indevelopment,deprecated",
       page: 0,
       perpage: 0
    },
    function(application)
    {
        $scope.applicationsAll = application.data.data;
        for(var t1=0; t1<application.data.data.length; t1++)
        {
            for(var t2=0; t2<application.data.data[t1].versions.length; t2++)
            {
                $scope.allTools.push({'tool_id' : application.data.data[t1]._id.$oid, 'status' : application.data.data[t1].status, 'tool_name' : application.data.data[t1].name, 'tool_version' : application.data.data[t1].name+' '+application.data.data[t1].versions[t2].version_number, 'version_id' : application.data.data[t1].versions[t2].version_id, 'version_name' : application.data.data[t1].versions[t2].version_name, 'version_number' : application.data.data[t1].versions[t2].version_number});
            }
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.showStatus = function()
    {
        if($scope.statusFlag === true)
        {
            $scope.statusFlag = false;
        }
        else
        {
            $scope.statusFlag = true;
        }
    };

    $scope.setStatusCSS = function(flag)
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

    $scope.showTags = function()
    {
        if($scope.tagsFlag === true)
        {
            $scope.tagsFlag = false;
        }
        else
        {
            $scope.tagsFlag = true;
        }
    };

    $scope.setTagsCSS = function(flag)
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

    $scope.showToolsets = function()
    {
        if($scope.toolsetsFlag === true)
        {
            $scope.toolsetsFlag = false;
        }
        else
        {
            $scope.toolsetsFlag = true;
        }
    };

    $scope.setToolsetsCSS = function(flag)
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

    $scope.toolsetsAll = AllToolSet.get({

    },
    function(toolsetSuccessResponse)
    {
        $scope.toolsetsAll = toolsetSuccessResponse.data.data;
    },
    function(errorResponse)
    {
        if(errorResponse.message==="Unexpected token < in JSON at position 0")
        {
            $rootScope.isNavbarVisible = false;
            $rootScope.userProfile.permitted_routes = "";
            $rootScope.handleResponse("Please login again!");
            $state.go('login');
        }
        if(errorResponse.message!=="Unexpected token < in JSON at position 0")
        {
            $rootScope.handleResponse(errorResponse.message);
        }
    });

    $scope.setStatusFilter = function(status)
    {
        var statusFlag = 0;
        var ind = 0;
        var statusFilterLen = statusFilter.length;
        if(statusFilterLen>0)
        {
            for(var a=0; a<statusFilterLen; a++)
            {
                if(statusFilter[a] === status)
                {
                    ind = a;
                }
                else
                {
                    statusFlag++;
                }
            }

            if(statusFlag === statusFilterLen)
            {
                statusFilter.push(status);
            }
            else
            {
                statusFilter.splice(ind, 1);
            }
        }
        else
        {
            statusFilter.push(status);
        }
    };

    $scope.setTagFilter = function(tag)
    {
        var tagFlag = 0;
        var ind = 0;
        var tagFilterLen = tagFilter.length;
        if(tagFilterLen>0)
        {
            for(var a=0; a<tagFilterLen; a++)
            {
                if(tagFilter[a] === tag)
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
                tagFilter.push(tag);
            }
            else
            {
                tagFilter.splice(ind, 1);
            }
        }
        else
        {
            tagFilter.push(tag);
        }
    };

    $scope.setToolsetFilter = function(toolset)
    {
        var toolsetFlag = 0;
        var ind = 0;
        var toolsetFilterLen = toolsetFilter.length;
        if(toolsetFilterLen>0)
        {
            for(var a=0; a<toolsetFilterLen; a++)
            {
                if(toolsetFilter[a] === toolset)
                {
                    ind = a;
                }
                else
                {
                    toolsetFlag++;
                }
            }

            if(toolsetFlag === toolsetFilterLen)
            {
                toolsetFilter.push(toolset);
            }
            else
            {
                toolsetFilter.splice(ind, 1);
            }
        }
        else
        {
            toolsetFilter.push(toolset);
        }
    };

    $scope.applyToolFilters = function()
    {
        var status = '';
        var tag = '';
        var toolset = '';

        if(statusFilter.length>0)
        {
            status = statusFilter.toString();
        }
        else
        {
            status = null;
        }

        if(tagFilter.length>0)
        {
            tag = tagFilter.toString();
        }
        else
        {
            tag = null;
        }

        if(toolsetFilter.length>0)
        {
            toolset = toolsetFilter.toString();
        }
        else
        {
            toolset = null;
        }

        GetAllTools.get({
           id: "all",
           status: status,
           tags: tag,
           toolset: toolset,
           page: 0,
           perpage: 0
        },
        function(application)
        {
            $scope.applicationsAll = application.data.data;
            $scope.allTools = [];
            for(var t1=0; t1<application.data.data.length; t1++)
            {
                for(var t2=0; t2<application.data.data[t1].versions.length; t2++)
                {
                    $scope.allTools.push({
                        'tool_id' : application.data.data[t1]._id.$oid,
                        'status' : application.data.data[t1].status,
                        'tool_name' : application.data.data[t1].name,
                        'version_id' : application.data.data[t1].versions[t2].version_id,
                        'version_name' : application.data.data[t1].versions[t2].version_name,
                        'version_number' : application.data.data[t1].versions[t2].version_number});
                }
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.removeToolFromSelectedTools = function(index)
    {
        $rootScope.toolSetDetailsFactory.removeTool($scope.selectedTools,index);
        $scope.selectedTools = $rootScope.toolSetDetailsFactory.getToolList();
    };

    $scope.updateToolsetList = function()
    {
        $('#show_tools').hide(700);
        $rootScope.$emit('updateToolList', {selectedTools : $scope.selectedTools});
    };

    $scope.deleteToolsetList = function()
    {
        $('#show_tools').hide(700);
        $scope.selectedTools = [];
        $rootScope.toolSetDetailsFactory.removeAllTools();
    };

    $rootScope.$on('setSelectedToolList', function(event, args){
        $scope.selectedTools = args.selectedTools;
    });
});

});