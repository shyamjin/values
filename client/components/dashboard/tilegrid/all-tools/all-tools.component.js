require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['requestTabComponent', 'toolServicesApp', 'toolSetServicesApp','toolTips']
});

define(['angular'],function (app) {
  'use strict';

var allToolsComponentControllerApp = angular.module('allToolsComponentControllerApp', ['requestTabComponent', 'toolServicesApp', 'toolSetServicesApp','720kb.tooltips']);

allToolsComponentControllerApp.controller('ToolListController', function ($scope, $state, $rootScope, GetAllTools, AllToolSet, TagsAll) {
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
    $scope.lines = 0;
    $scope.addNewTool =  function()
    {
        $state.go("createNewTool");
    };
    $rootScope.$on("searchToolEvent", function (event, args) {
        var keyword = args.keyword;
        $scope.searchToolWithName(keyword);
    });

    $scope.deployTool = function(version_id, build_number)
    {
        if(build_number === '' || build_number === null || build_number === undefined)
        {
            $rootScope.handleResponse("Unable to deploy as latest version of this tool does not have a valid build");
            return false;
        }
        else
        {
            $state.go('deployTool', {id:version_id, build_number: build_number});
        }
    };

    $scope.getReleaseNotesLineCount = function()
    {
        var paraHeight = document.getElementById('release_notes_content').offsetHeight;
        var lineHeight = parseInt(document.getElementById('release_notes_content').style.lineHeight, 10);
        $scope.lines = (divHeight / lineHeight);
        return '';
    };

    $scope.selectedTools = [];
    $scope.selectedToolsList = [];

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
            $('#show_dashboard_filter').hide(700);
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
        $('#show_dashboard_filter').hide(700);
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

    $scope.selectTool = function(tool)
    {
        var flag = 0;
        var ind = 0;
        var elementId = '';
        var length = $scope.selectedTools.length;
        if(length>0)
        {
            for(var id=0; id<length; id++)
            {
                if($scope.selectedTools[id].version_id === tool.versions[0].version_id)
                {
                    flag++;
                    ind = id;
                }
            }
            if(flag===0)
            {
                if(tool.versions[0].latest_build_number)
                {
                    $scope.selectedTools.push({"version_id": tool.versions[0].version_id, "build_number": tool.versions[0].latest_build_number, "build_id": tool.versions[0].latest_build_id});
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
                    $rootScope.handleResponse("Unable to deploy as latest version of the tool "+tool.name+" does not have a valid build");
                    elementId = document.getElementById("select_check_"+tool.name);
                    elementId.checked = false;
                    return false;
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
            if(tool.versions[0].latest_build_number)
            {
                for(var c=0; c<$scope.applications.length; c++)
                {
                    if($scope.applications[c].name === tool.name)
                    {
                        $scope.applications[c].isSelected = true;
                    }
                }
                $scope.selectedTools.push({"version_id": tool.versions[0].version_id, "build_number": tool.versions[0].latest_build_number, "build_id": tool.versions[0].latest_build_id});
                $scope.selectedToolsList.push(tool.name);
            }
            else
            {
                $rootScope.handleResponse("Unable to select tool "+tool.name+" as its latest version does not have a valid build");
                elementId = document.getElementById("select_check_"+tool.name);
                elementId.checked = false;
                return false;
            }
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
                $scope.selectedTools.push(tool.versions[0].version_id);
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
            $scope.selectedTools.push(tool.versions[0].version_id);
            $scope.selectedToolsList.push(tool.name);
        }
    };

    $scope.selectMultipleToolsForDeployment = function(selectedTools)
    {
        if(selectedTools.length>0)
        {
            $state.go('deployMultipleTools', {tools: JSON.stringify(selectedTools)});
        }
    };

    /*$scope.isPageAvailable = function()
    {
        if($scope.applications)
        {
            if($scope.totalCount === $scope.applications.length)
            {
                return false;
            }
            else
            {
                return true;
            }
        }
    };*/

    $scope.showMoreTools = function()
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
        $scope.currentPage = $scope.currentPage+1;
        $scope.tempTools = [];
        angular.copy($scope.applications, $scope.tempTools);
        delete $scope.application;
        GetAllTools.get({
            id: "all",
            status: status,
            tags: tag,
            toolset: toolset,
            page: $scope.currentPage
        },
        function(successResponse)
        {
            $scope.applications = [];
            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;
            for(var a=0; a<successResponse.data.data.length; a++)
            {
                successResponse.data.data[a].isSelected = false;
                $scope.tempTools.push(successResponse.data.data[a]);
            }
            for(var b=0; b<$scope.tempTools.length; b++)
            {
                $scope.tempTools[b].isSelected = false;
                $scope.applications.push($scope.tempTools[b]);
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.searchToolWithName = function(keyword)
    {
        var perpage = 0;
        if(keyword === '')
        {
            perpage = null;
            $scope.hideShowMoreTools = false;
        }
        else
        {
            $scope.hideShowMoreTools = true;
        }
        $rootScope.searchProgress = true;
        delete $scope.application;
        GetAllTools.get({
            id: "all",
            status: "active,indevelopment,deprecated",
            tags: null,
            toolset: null,
            toolname: keyword,
            page: 0,
            perpage: perpage
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
            $scope.$watch(function(scope) {
                return scope.applications;
            },
            function(newValue, oldValue) {
            });
            delete $rootScope.searchProgress;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
            delete $rootScope.searchProgress;
        });
    };
});

});