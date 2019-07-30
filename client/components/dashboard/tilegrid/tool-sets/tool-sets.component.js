require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['requestTabComponent', 'toolServicesApp', 'toolSetServicesApp']
});

define(['angular','toolTips'],function (app) {
  'use strict';

var toolSetListComponentControllerApp = angular.module('toolSetListComponentControllerApp', ['requestTabComponent', 'toolServicesApp', 'toolSetServicesApp','720kb.tooltips']);

toolSetListComponentControllerApp.controller('ToolSetListController', function ($scope, $stateParams, $window, AllToolSet, $state, $timeout, $rootScope, ToolSetByID, TagsAll, GetAllTools) {
    $rootScope.$on("searchToolSetEvent", function (event, args) {
        var keyword = args.keyword;
        $scope.searchToolSetWithName(keyword);
    });

    $scope.AddToolSet = function()
    {
        $state.go("newToolSet");
    };
    $scope.filterType = 'All';
    $scope.tagsFlag = false;
    $scope.toolsFlag = false;
    $scope.hideShowMoreToolset = false;
    $scope.isFilterApplied = false;
    var tagFilter = [];
    var toolsFilter = [];
    $scope.selectedTools = [];

    AllToolSet.get({
    },
    function(alltoolsets)
    {
        $scope.ToolSets = alltoolsets.data.data;
        $scope.currentPage = alltoolsets.data.page;
        $scope.totalCount = alltoolsets.data.total;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

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

    $scope.showTools = function()
    {
        if($scope.toolsFlag === true)
        {
            $scope.toolsFlag = false;
        }
        else
        {
            $scope.toolsFlag = true;
        }
    };

    $scope.setToolsCSS = function(flag)
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

    GetAllTools.get({
        id: "all",
        status: "active,indevelopment,deprecated",
        page: 0,
        perpage: 0
    },
    function(toolsSuccessResponse)
    {
        $scope.toolsAll = toolsSuccessResponse.data.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

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

    $scope.setToolsFilter = function(tool)
    {
        var toolsFlag = 0;
        var ind = 0;
        var toolsFilterLen = toolsFilter.length;
        if(toolsFilterLen>0)
            {
                for(var a=0; a<toolsFilterLen; a++)
                {
                    if(toolsFilter[a] === tool)
                    {
                        ind = a;
                    }
                    else
                    {
                        toolsFlag++;
                    }
                }

                if(toolsFlag === toolsFilterLen)
                {
                    toolsFilter.push(tool);
                }
                else
                {
                    toolsFilter.splice(ind, 1);
                }
            }
            else
            {
                toolsFilter.push(tool);
            }
        };

    $scope.applyToolSetFilters = function()
    {
        var tag = '';
        var toolname = '';
        var perpage = 0;

        if(tagFilter.length>0)
        {
            tag = tagFilter.toString();
        }
        else
        {
            tag = null;
        }

        if(toolsFilter.length>0)
        {
            toolname = toolsFilter.toString();
        }
        else
        {
            toolname = null;
        }
        if(tag === null && toolname === null)
        {
            perpage = null;
            $scope.hideShowMoreToolset = false;
            $scope.isFilterApplied = false;
        }
        else
        {
            $scope.hideShowMoreToolset = true;
            $scope.isFilterApplied = true;
        }

        delete $scope.ToolSets;
        AllToolSet.get({
            tags: tag,
            toolname: toolname,
            page:0,
            perpage:perpage
        },
        function(alltoolsets)
        {
            delete $scope.ToolSets;
            $('#show_dashboard_toolset_filter').hide(700);
            $scope.ToolSets = [];
            $scope.currentPage = alltoolsets.data.page;
            $scope.totalCount = alltoolsets.data.total;

            for(var b=0; b<alltoolsets.data.data.length; b++)
            {
                $scope.ToolSets.push(alltoolsets.data.data[b]);
            }
            $scope.$watch(function(scope) {
                return scope.ToolSets;
            },
            function(newValue, oldValue) {
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.showToolSetFilter = function(tab)
    {
        if(document.getElementById("show_dashboard_toolset_filter").style.display === "none" || document.getElementById("show_dashboard_toolset_filter").style.display === "")
        {
                $('#show_dashboard_toolset_filter').show(700);
        }
        else
        {
            $('#show_dashboard_toolset_filter').hide(700);
        }
    };

    $scope.closeToolSetFilter = function()
    {
        tagFilter = [];
        toolsFilter = [];
        $('#show_dashboard_toolset_filter').hide(700);
        $scope.hideShowMoreToolset = false;
        $scope.isFilterApplied = false;
        AllToolSet.get({
        },
        function(alltoolsets)
        {
            $scope.ToolSets = alltoolsets.data.data;
            $scope.currentPage = alltoolsets.data.page;
            $scope.totalCount = alltoolsets.data.total;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };
    $scope.cancleToolSetFilter = function()
    {
        $('#show_dashboard_toolset_filter').hide(700);
    };

    $scope.showMoreToolSets = function()
    {
        var tag = '';
        var toolname = '';

        if(tagFilter.length>0)
        {
            tag = tagFilter.toString();
        }
        else
        {
            tag = null;
        }

        if(toolsFilter.length>0)
        {
            toolname = toolsFilter.toString();
        }
        else
        {
            toolname = null;
        }
        $scope.currentPage = $scope.currentPage+1;
        $scope.tempToolSets = [];
        angular.copy($scope.ToolSets, $scope.tempToolSets);
        delete $scope.ToolSets;
        AllToolSet.get({
            tags: tag,
            toolname: toolname,
            page: $scope.currentPage
        },
        function(alltoolsets)
        {
            delete $scope.ToolSets;
            $scope.ToolSets = [];
            $scope.currentPage = alltoolsets.data.data.page;
            $scope.totalCount = alltoolsets.data.data.total;

            for(var a=0; a<alltoolsets.data.data.length; a++)
            {
                $scope.ToolSets.push(alltoolsets.data.data[a]);
            }
            for(var b=0; b<$scope.tempToolSets.length; b++)
            {
                $scope.ToolSets.push($scope.tempToolSets[b]);
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.selectToolSet = function(toolset_id)
    {
        $scope.toolSetDetails = ToolSetByID.get({
            id : toolset_id
        },
        function(toolsetSuccessResponse)
        {
            for(var t1=0; t1<toolsetSuccessResponse.data.tool_set.length; t1++)
            {
                if(toolsetSuccessResponse.data.tool_set[t1].build_number === undefined || toolsetSuccessResponse.data.tool_set[t1].build_number === null || toolsetSuccessResponse.data.tool_set[t1].build_number === '')
                {
                    $rootScope.handleResponse("Unable to deploy as latest version of the tool "+toolsetSuccessResponse.data.tool_set[t1].tool_name+" does not have a valid build");
                    return false;
                }
                else
                {
                    $scope.selectedTools.push({"version_id": toolsetSuccessResponse.data.tool_set[t1].version_id, "build_number": toolsetSuccessResponse.data.tool_set[t1].build_number, "build_id": toolsetSuccessResponse.data.tool_set[t1].build_id});
                }
            }
            if($scope.selectedTools.length>0)
            {
                $state.go('deployMultipleTools', {tools: JSON.stringify($scope.selectedTools)});
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.searchToolSetWithName = function(keyword)
    {
        if(keyword === '')
        {
            $scope.hideShowMoreToolset = false;
        }
        else
        {
            $scope.hideShowMoreToolset = true;
        }
        delete $scope.ToolSets;
        $rootScope.searchProgress = true;
        AllToolSet.get({
            name: keyword,
            page: 0,
            perpage: 0
        },
        function(alltoolsets)
        {
            delete $scope.ToolSets;
            delete $rootScope.searchProgress;
            $scope.ToolSets = [];
            $scope.currentPage = alltoolsets.data.page;
            $scope.totalCount = alltoolsets.data.total;

            for(var b=0; b<alltoolsets.data.data.length; b++)
            {
                $scope.ToolSets.push(alltoolsets.data.data[b]);
            }
            $scope.$watch(function(scope) {
                return scope.ToolSets;
            },
            function(newValue, oldValue) {
            });
        },
        function(errorResponse)
        {
            delete $rootScope.searchProgress;
            $rootScope.handleResponse(errorResponse);
        });
    };

});

});