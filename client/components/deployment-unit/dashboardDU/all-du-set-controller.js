define(['angular', 'ngResource', 'uiRouter', 'ngCookies','toolTips', 'jquery', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp'], function (app) {
  'use strict';

var allDUSetControllerApp = angular.module('allDUSetControllerApp', ['ui.router','720kb.tooltips', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp']);

allDUSetControllerApp.controller('AllDUSetController', function ($scope, $rootScope, $state, $stateParams,  $location, $interval, DUSetAll, DeploymentUnitAll, TagsAll, ApprovalStatusAll,ViewDUSet, GetAllDUBuildData) {
    $scope.filterType = 'All';
    $scope.approvalStatusFlag = true;
    $scope.tagsFlag = false;
    $scope.DunameFlag =false;
    $scope.hideShowMoreDuSet = false;
    $scope.isFilterApplied = false;
    var approvalStatusFilter = [];
    var tagFilter = [];
    var dunameFilter =[];
    $scope.tags = new TagsAll();

    $scope.createNewDuPackage = function()
    {
        $state.go("createDUSet");
    };

    $rootScope.$on("searchDUSetEvent", function (event, args) {
        var keyword = args.keyword;
        $scope.searchDUSetWithName(keyword);
    });

    DUSetAll.get({
    },
    function(successResponse)
    {
        $scope.DUSets = successResponse.data.data;
        $scope.currentPage = successResponse.data.page;
        $scope.totalCount = successResponse.data.total;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.showApprovalStatus = function()
    {
        if($scope.approvalStatusFlag === true)
        {
            $scope.approvalStatusFlag = false;
        }
        else
        {
            $scope.approvalStatusFlag = true;
        }
    };

    $scope.setApprovalStatusCSS = function(flag)
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

    $scope.showDuname = function()
    {
        if($scope.DunameFlag === true)
        {
            $scope.DunameFlag = false;
        }
        else
        {
            $scope.DunameFlag = true;
        }
    };

    $scope.setDunameCSS = function(flag)
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
    $scope.dunamesAll = DeploymentUnitAll.get({
        page: 0,
        perpage: 0
    },
    function(successResponse)
    {
        $scope.dunamesAll = [];
        for(var a=0; a<successResponse.data.length; a++)
        {
            for(var b=0; b<successResponse.data[a].data.length; b++)
            {
                $scope.dunamesAll.push(successResponse.data[a].data[b]);
            }
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

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


    $scope.approvalStatus = ApprovalStatusAll.get({
    },
    function(successResponse)
    {
        $scope.approvalStatus = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.setApprovalStatusFilter = function(ApprovalStatus)
    {
        var approvalStatusFlag = 0;
        var ind = 0;
        var approvalStatusFilterLen = approvalStatusFilter.length;
        if(approvalStatusFilterLen>0)
        {
            for(var a=0; a<approvalStatusFilterLen; a++)
            {
                if(approvalStatusFilter[a] === ApprovalStatus)
                {
                    ind = a;
                }
                else
                {
                    approvalStatusFlag++;
                }
            }

            if(approvalStatusFlag === approvalStatusFilterLen)
            {
                approvalStatusFilter.push(ApprovalStatus);
            }
            else
            {
                approvalStatusFilter.splice(ind, 1);
            }
        }
        else
        {
            approvalStatusFilter.push(ApprovalStatus);
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

    $scope.setDunameFilter = function(duname)
    {
        var DunameFlag = 0;
        var ind = 0;
        var dunameFilterLen = dunameFilter.length;
        if(dunameFilterLen>0)
        {
            for(var a=0; a<dunameFilterLen; a++)
            {
                if(dunameFilter[a] === duname)
                {
                    ind = a;
                }
                else
                {
                    DunameFlag++;
                }
            }

            if(DunameFlag === dunameFilterLen)
            {
                dunameFilter.push(duname);
            }
            else
            {
                dunameFilter.splice(ind, 1);
            }
        }
        else
        {
            dunameFilter.push(duname);
        }
    };
    $scope.applyDuSetFilters = function()
    {
        var ApprovalStatus = '';
        var tag = '';
        var duname = '';
        var perpage = 0;

        $scope.tempDU = [];
        if(approvalStatusFilter.length>0)
        {
            ApprovalStatus = approvalStatusFilter.toString();
        }
        else
        {
            ApprovalStatus = null;
        }

        if(tagFilter.length>0)
        {
            tag = tagFilter.toString();
        }
        else
        {
            tag = null;
        }

        if(dunameFilter.length>0)
        {
            duname = dunameFilter.toString();
        }
        else
        {
            duname = null;
        }
        if(ApprovalStatus === null && tag === null && duname === null)
        {
            perpage = null;
            $scope.hideShowMoreDuSet = false;
            $scope.isFilterApplied = false;
        }
        else
        {
            $scope.hideShowMoreDuSet = true;
            $scope.isFilterApplied = true;
        }
        delete $scope.DUSets ;
        DUSetAll.get({
           approval_status: ApprovalStatus,
           tags: tag,
           duname: duname,
           page: 0,
           perpage:perpage
        },
        function(successResponse)
        {
            delete $scope.DUSets ;
            $('#show_dashboard_filter_duset').hide(700);
            $scope.DUSets  = [];
            $scope.currentPage = successResponse.data.page;
                $scope.totalCount = successResponse.data.total;
            
            for(var d=0; d<successResponse.data.data.length; d++)
            {
                $scope.DUSets .push(successResponse.data.data[d]);
            }
            $scope.$watch(function(scope) {
                return scope.DUSets ;
            },
            function(newValue, oldValue) {
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.searchDUSetWithName = function(keyword)
    {
        delete $scope.DUSets;
        $rootScope.searchProgress = true;
        $scope.hideShowMoreDuSet = true;

        DUSetAll.get({
           approval_status: null,
           tags: null,
           name: keyword,
           page: 0,
           perpage: 0
        },
        function(successResponse)
        {
            delete $scope.DUSets ;
            delete $rootScope.searchProgress;
            $('#show_dashboard_filter_duset').hide(700);
            $scope.DUSets  = [];
            $scope.currentPage = successResponse.data.page;
                $scope.totalCount = successResponse.data.total;
            
            for(var d=0; d<successResponse.data.data.length; d++)
            {
                $scope.DUSets .push(successResponse.data.data[d]);
            }
            $scope.$watch(function(scope) {
                return scope.DUSets ;
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

    $rootScope.showDuSetFilter = function(tab)
    {
        if(document.getElementById("show_dashboard_filter_duset").style.display === "none" || document.getElementById("show_dashboard_filter_duset").style.display === "")
        {
                $('#show_dashboard_filter_duset').show(700);
        }
        else
        {
            $('#show_dashboard_filter_duset').hide(700);
        }
    };

    $scope.closeDuSetFilter = function()
    {
        approvalStatusFilter = [];
        tagFilter = [];
        dunameFilter = [];
        $('#show_dashboard_filter_duset').hide(700);
        $scope.hideShowMoreDuSet = false;
        $scope.isFilterApplied = false;
        DUSetAll.get({
        },
        function(successResponse)
        {
            $scope.DUSets = successResponse.data.data;
            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };
    $scope.cancleDuSetFilter = function()
    {
        $('#show_dashboard_filter_duset').hide(700);
    };

    $scope.showMoreDUSet = function()
    {
        var ApprovalStatus = '';
        var tag = '';
        var duname = '';

        $scope.tempDU = [];
        if(approvalStatusFilter.length>0)
        {
            ApprovalStatus = approvalStatusFilter.toString();
        }
        else
        {
            ApprovalStatus = null;
        }

        if(tagFilter.length>0)
        {
            tag = tagFilter.toString();
        }
        else
        {
            tag = null;
        }

        if(dunameFilter.length>0)
        {
            duname = dunameFilter.toString();
        }
        else
        {
            duname = null;
        }
        $scope.currentPage = $scope.currentPage+1;
        $scope.tempDuSets = [];
        angular.copy($scope.DUSets, $scope.tempDuSets);
        delete $scope.DUSets;
        DUSetAll.get({
            approval_status: ApprovalStatus,
            tags: tag,
            duname: duname,
            page: $scope.currentPage
        },
        function(successResponse)
        {
            $scope.DUSets = [];
            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;


            for(var a=0; a<successResponse.data.data.length; a++)
            {
                $scope.tempDuSets.push(successResponse.data.data[a]);
            }
            for(var b=0; b<$scope.tempDuSets.length; b++)
            {
                $scope.DUSets.push($scope.tempDuSets[b]);
            }

        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };
    $scope.duSetDeploy = function (duset_id)
    {
        GetAllDUBuildData.get({
            id : duset_id
        },
        function(viewDUSetSuccessResponse)
        {
            $scope.deployDUSetData = {
                'duset_id' : viewDUSetSuccessResponse.data._id.$oid,
                'duDataList' : []
            };
            for(var i=0; i<viewDUSetSuccessResponse.data.du_set_details.length; i++)
            {
                if(viewDUSetSuccessResponse.data.du_set_details[i].build)
                {
                    if(viewDUSetSuccessResponse.data.du_set_details[i].build[0]._id.$oid === null || viewDUSetSuccessResponse.data.du_set_details[i].build[0]._id.$oid === undefined || viewDUSetSuccessResponse.data.du_set_details[i].build[0]._id.$oid === '')
                    {
                        $rootScope.handleResponse("Unable to deploy as "+viewDUSetSuccessResponse.data.du_set_details[i].name+" does not have a valid build");
                        return false;
                    }
                    else
                    {
                        var defaultDUValueToPush= {
                            "name" : viewDUSetSuccessResponse.data.du_set_details[i].name,
                            "type" : viewDUSetSuccessResponse.data.du_set_details[i].type,
                            "dependent" : viewDUSetSuccessResponse.data.du_set_details[i].dependent,
                            "order" : viewDUSetSuccessResponse.data.du_set_details[i].order,
                            "flexible_attributes": viewDUSetSuccessResponse.data.du_set_details[i].flexible_attributes,
                            'du_id' : viewDUSetSuccessResponse.data.du_set_details[i]._id.$oid,
                            "state_id" : undefined,
                            'build_id' : viewDUSetSuccessResponse.data.du_set_details[i].build[0]._id.$oid,
                            "build_number":viewDUSetSuccessResponse.data.du_set_details[i].build[0].build_number,
                            "deployment_field":viewDUSetSuccessResponse.data.du_set_details[i].deployment_field,
                            "package_state_id":undefined
                          };
                        $scope.deployDUSetData.duDataList.push(defaultDUValueToPush);
                    }

                }
                else
                {
                    $rootScope.handleResponse("Unable to deploy as "+viewDUSetSuccessResponse.data.du_set_details[i].name+" does not have a valid build");
                    return false;
                }

            }
            if($scope.deployDUSetData.duDataList.length>0)
            {
                $state.go('deployDUSet', {id:JSON.stringify($scope.deployDUSetData)});
            }
        },
        function(viewDUErrorResponse)
        {
            $rootScope.handleResponse(viewDUErrorResponse);
        });
    };

});
});