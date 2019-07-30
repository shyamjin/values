require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : []
});

define(['angular'],function (app) {
  'use strict';

var toolDashboardFilterComponentControllerApp = angular.module('toolDashboardFilterComponentControllerApp', []);

toolDashboardFilterComponentControllerApp.controller("ToolDashboardFilterComponentController",function($scope, $rootScope, $timeout){
    $scope.applications = [];
    $scope.filterType = 'All';
    $scope.statusFlag = true;
    $scope.tagsFlag = false;
    $scope.toolsetsFlag = false;
    $scope.hideShowMoreTools = false;
    var statusFilter = [];
    var tagFilter = [];
    var toolsetFilter = [];
    $scope.isFilterApplied = false;

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

    $scope.tagsAll = TagsAll.get({
    },
    function(tags)
    {
        $scope.tagsAll = tags;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.toolsetsAll = AllToolSet.get({
    },
    function(toolsetSuccessResponse)
    {
        $scope.toolsetsAll = toolsetSuccessResponse.data.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
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
        var perpage = 0;

        if(statusFilter.length>0)
        {
            status = statusFilter.toString();
        }
        else
        {
            status = "active,indevelopment";
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

        if(status === 'active,indevelopment' && tag === null && toolset === null)
        {
            perpage = null;
            $scope.hideShowMoreTools = false;
        }
        else
        {
            $scope.hideShowMoreTools = true;
        }

        GetAllTools.get({
           id: "all",
           status: status,
           tags: tag,
           toolset: toolset,
           page: 0,
           perpage: perpage
        },
        function(successResponse)
        {
            delete $scope.applications;
            $scope.isFilterApplied = true;
            $scope.applications = [];
            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;
            for(var a=0; a<successResponse.data.data.length; a++)
            {
                successResponse.data.data[a].isSelected = false;
                $scope.applications.push(successResponse.data.data[a]);
            }
            $scope.$watch(function(scope) {
                return scope.applications;
            },
            function(newValue, oldValue) {
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

    };
    $scope.clearToolFilter = function()
    {
        statusFilter = [];
        tagFilter = [];
        toolsetFilter = [];
        $('#open_filter').hide();
        $scope.open_filter = false;
        $scope.isFilterApplied = false;
        $scope.hideShowMoreTools = false;
        GetAllTools.get({
        id: "all",
        status: "active,indevelopment"
        },
        function(successResponse)
        {
            $scope.applications = [];
            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;
            for(var a=0; a<successResponse.data.data.length; a++)
            {
                successResponse.data.data[a].isSelected = false;
                $scope.applications.push(successResponse.data.data[a]);
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.showFilter = function(tab)
    {
        if(document.getElementById("show_dashboard_filter").style.display === "none" || document.getElementById("show_dashboard_filter").style.display === "")
        {
                $('#show_dashboard_filter').show(700);
        }
        else
        {
            $('#show_dashboard_filter').hide(700);
        }
    };

    $scope.cancleFilter = function()
    {
        $('#show_dashboard_filter').hide(700);
    };
});

});