require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent','toolTips']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent','toolTips'],function (app) {
  'use strict';

var editDUSetStateControllerApp = angular.module('editDUSetStateControllerApp', ['ui.router','statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent','720kb.tooltips']);

editDUSetStateControllerApp.controller('editDUSetStateController', function($timeout, $scope, $rootScope, $state, $location, $stateParams, $http, GetAllDuState, DUStateViewById, ApprovalStatusAll, ViewDUSet, editDuState, StateDelete , DUSetAll, DeploymentUnitAll) {
    $scope.duStateisDeleted = false;
    $scope.isFilterApplied = false;
    $scope.approvalStatusFlag = false;
    $scope.hideShowMoreDuPackageState = false;
    $scope.DuSetnameFlag = false;
    $scope.duNameFlag = false;
    var approvalStatusFilter = [];
    var duSetnameFilter = [];
    var duFilter = [];
    GetAllDuState.get({
        page:0,
        type:'dusetstate'
    },
    function(successResponse)
    {
        $scope.AllDuSetState = successResponse.data;
        $scope.currentPage = successResponse.page;
        $scope.totalStateCount = successResponse.total;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });
    $scope.openFilter = function()
    {
        if(document.getElementById("open_filter").style.display === "none" || document.getElementById("open_filter").style.display === "")
            {
                $('#open_filter').show(500);
                $scope.open_filter = true;
            }
        else
            {
                $('#open_filter').hide(500);
                $scope.open_filter = false;
            }
    };
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

    $scope.showDuSetname = function()
    {
                if($scope.DuSetnameFlag === true)
                {
                    $scope.DuSetnameFlag = false;
                }
                else
                {
                    $scope.DuSetnameFlag = true;
                }
    };

    $scope.showDuName = function()
    {
                if($scope.duNameFlag === true)
                {
                    $scope.duNameFlag = false;
                }
                else
                {
                    $scope.duNameFlag = true;
                }
    };

    $scope.setDuSetnameCSS = function(flag)
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

    $scope.setDuNameCSS = function(flag)
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

    $scope.dusetsAll = DUSetAll.get({
        page: 0,
        perpage: 0
    },
    function(dusetSuccessResponse)
    {
        $scope.dusetsAll = dusetSuccessResponse.data.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    DeploymentUnitAll.get({
        page: 0,
        perpage: 0
    },
    function(successResponse)
    {
        $scope.applications = successResponse.data;
        $scope.deploymentUnitsAll = [];
        for(var i=0; i<$scope.applications.length; i++)
        {
            for(var j=0; j<$scope.applications[i].data.length; j++)
            {
                $scope.deploymentUnitsAll.push($scope.applications[i].data[j]);
            }
        }
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

    $scope.setDuSetnameFilter = function(duname)
    {
        var DuSetnameFlag = 0;
        var ind = 0;
        var duSetnameFilterLen = duSetnameFilter.length;
        if(duSetnameFilterLen>0)
        {
            for(var a=0; a<duSetnameFilterLen; a++)
            {
                if(duSetnameFilter[a] === duname)
                {
                    ind = a;
                }
                else
                {
                    DuSetnameFlag++;
                }
            }

            if(DuSetnameFlag === duSetnameFilterLen)
            {
                duSetnameFilter.push(duname);
            }
            else
            {
                duSetnameFilter.splice(ind, 1);
            }
        }
        else
        {
            duSetnameFilter.push(duname);
        }
    };

    $scope.setDuNameFilter = function(du)
    {
        var duFlag = 0;
        var ind = 0;
        var duFilterLen = duFilter.length;
        if(duFilter>0)
        {
            for(var a=0; a<duFilter; a++)
            {
                if(duFilter[a] === du)
                {
                    ind = a;
                }
                else
                {
                    duFlag++;
                }
            }

            if(duFlag === duFilterLen)
            {
                duFilterLen.push(du);
            }
            else
            {
                duFilter.splice(ind, 1);
            }
        }
        else
        {
            duFilter.push(du);
        }
    };
    $scope.searchDUStateSet = function(event,searchStateSetKeyword)
    {
        if (searchStateSetKeyword.length ==0)
        {
            delete $scope.AllDuSetState ;
            GetAllDuState.get({
                page:0,
                type:'dusetstate'
            },
            function(successResponse)
            {
                $scope.AllDuSetState = successResponse.data;
                $scope.currentPage = successResponse.page;
                $scope.totalStateCount = successResponse.total;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        }

    };

    $scope.searchStateSetWithName = function(keyword)
    {
        $rootScope.searchProgress = true;
        $scope.hideShowMoreDuPackageState = true;
        delete $scope.AllDuSetState ;
        GetAllDuState.get({
           approval_status: null,
           parent_entity_id: null,
           type: 'dusetstate',
           name:keyword,
           page: 0,
           perpage: 0,
           du_id : null
        },
        function(successResponse)
        {
            delete $scope.AllDuSetState ;
            delete $rootScope.searchProgress;
            $('#open_filter').hide(500);
            $scope.AllDuSetState  = successResponse.data;
            $scope.currentPage = successResponse.page;
            $scope.totalStateCount = successResponse.total;

            $scope.$watch(function(scope) {
                return scope.AllDuSetState ;
            },
            function(newValue, oldValue) {
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.applyDuSetStateFilters = function()
    {
        var ApprovalStatus = '';
        var duSetname = '';
        var du = '';
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

        if(duSetnameFilter.length>0)
        {
            duSetname = duSetnameFilter.toString();
        }
        else
        {
            duSetname = null;
        }

        if(duFilter.length>0)
        {
            du= duFilter.toString();
        }
        else
        {
            du = null;
        }

        if(ApprovalStatus === null && duSetname === null)
        {
            perpage = null;
            $scope.hideShowMoreDuPackageState = false;
            $scope.isFilterApplied = false;
        }
        else
        {
            $scope.hideShowMoreDuPackageState = true;
            $scope.isFilterApplied = true;
            $scope.duStateisDeleted = true;
        }
        delete $scope.AllDuSetState ;
        GetAllDuState.get({
           approval_status: ApprovalStatus,
           parent_entity_id: duSetname,
           type: 'dusetstate',
           page: 0,
           perpage: perpage,
           du_id : du
        },
        function(successResponse)
        {
            delete $scope.AllDuSetState ;
            $('#open_filter').hide(500);
            $scope.AllDuSetState  = successResponse.data;
            $scope.currentPage = successResponse.page;
            $scope.totalStateCount = successResponse.total;

            $scope.$watch(function(scope) {
                return scope.AllDuSetState ;
            },
            function(newValue, oldValue) {
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

    };

    $scope.cancleFilter = function()
    {
        $('#open_filter').hide(500);
    };

    $scope.closeFilter = function(form)
    {
        approvalStatusFilter = [];
        duSetnameFilter = [];
        duFilter = [];
        $('#open_filter').hide(500);
        $scope.open_filter = false;
        $scope.hideShowMoreDuPackageState = false;
        $scope.isFilterApplied = false;
        $scope.duStateisDeleted = true;
        GetAllDuState.get({
            page:0,
            type:'dusetstate'
        },
        function(successResponse)
        {
            delete $scope.application;
            $scope.AllDuSetState = successResponse.data;
            $scope.currentPage = successResponse.page;
            $scope.totalStateCount = successResponse.total;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.showMoreDuSetState = function()
    {
        var ApprovalStatus = '';
        var duSetname = '';

        $scope.tempDU = [];
        if(approvalStatusFilter.length>0)
        {
            ApprovalStatus = approvalStatusFilter.toString();
        }
        else
        {
            ApprovalStatus = null;
        }

        if(duSetnameFilter.length>0)
        {
            duSetname = duSetnameFilter.toString();
        }
        else
        {
            duSetname = null;
        }
        $scope.currentPage = $scope.currentPage+1;
        $scope.tempDuStateSets = [];
        angular.copy($scope.AllDuSetState, $scope.tempDuStateSets);
        delete $scope.AllDuSetState;
        GetAllDuState.get({
           approval_status: ApprovalStatus,
           parent_entity_id: duSetname,
           type:'dusetstate',
           page:$scope.currentPage
        },
        function(successResponse)
        {
            $scope.AllDuSetState = [];
            $scope.currentPage = successResponse.page;
            $scope.totalStateCount = successResponse.total;
            for(var a=0; a<successResponse.data.length; a++)
            {
                $scope.tempDuStateSets.push(successResponse.data[a]);
            }
            for(var b=0; b<$scope.tempDuStateSets.length; b++)
            {
                $scope.AllDuSetState.push($scope.tempDuStateSets[b]);
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };


    $scope.selectDuSetState = function(stateId)
    {
        $scope.application = {};
        $scope.AlLDuDetails = {};
        DUStateViewById.get({
            id:stateId
        },
        function(viewDUStateSuccessResponse)
        {
            $scope.duStateisDeleted = false;
            $scope.application = viewDUStateSuccessResponse;
            var approval_status = $scope.application.data.approval_status;
            $scope.oldStatus = '';
           /* ViewDUSet.get({
                id : $scope.application.data.parent_entity_id
                },
                function(viewDUSetSuccessResponse)
                {
                    $scope.AlLDuDetails = viewDUSetSuccessResponse;
                    for(var i=0; i<$scope.application.data.states.length; i++ )
                    {
                        for(var j=0; j<$scope.AlLDuDetails.data.du_set_details.length; j++)
                        {
                            if($scope.application.data.states[j].parent_entity_id === $scope.AlLDuDetails.data.du_set_details[i]._id.$oid)
                            {
                                $scope.AlLDuDetails.data.du_set_details[i].selectedState=$scope.application.data.states[j]._id.$oid;
                            }
                        }
                    }
                },
                function(viewDUErrorResponse)
                {
                    $rootScope.handleResponse(errorResponse);
            });*/
            ApprovalStatusAll.get({
            },
            function(successResponse)
            {
                $scope.approvalStatusAll = successResponse;
                for(var i=0; i<$scope.approvalStatusAll.length; i++)
                {
                    if($scope.approvalStatusAll[i]._id.$oid === approval_status)
                    {
                        $scope.application.data.approval_status = $scope.approvalStatusAll[i].name;
                        $scope.oldStatus = $scope.approvalStatusAll[i].name;
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

        },
        function(viewDUStateErrorResponse)
        {
            $rootScope.handleResponse(viewDUStateErrorResponse);
        });
    };
    /*$scope.selectDUState = function(duId, value)
    {
        var validDUFlag = 0;
        var validDUIndex = 0;
        var validDUBuildFlag = 0;
        var validDUBuildIndex = 0;
        for(var i=0; i<$scope.application.data.states.length; i++ )
        {
            if($scope.application.data.states[i].parent_entity_id === duId)
            {
                if($scope.application.data.states[i]._id.$oid === value)
                {
                    validDUBuildFlag++;
                    validDUBuildIndex = i;
                }
            }
            else
            {
                validDUFlag++;
            }

        }
        if(validDUFlag === $scope.application.data.states.length)
        {
             $scope.application.data.states.push({'du_id' : duId,'state' : value});
        }
        else
        {
            $scope.application.data.states[validDUBuildIndex].state = value;
        }
    };*/

    $scope.editDUSetState = function(form)
    {
        var validFieldFlag = 0;
        var validFieldIndex = 0;
        var duName = [];
        var state =[];
        var duData = {
        _id : {
                oid : ''
        }};

        if($scope.application.data.approval_status === '' || $scope.application.data.approval_status===undefined || $scope.application.data.approval_status===null)
        {
            $rootScope.handleResponse('Please select the Status');
            return false;
        }
        /*if ($scope.application.data.states.length === 0)
        {
            $rootScope.handleResponse('Please select states for all du');
            return false;
        }
        else
        {
            for(var j=0; j<$scope.AlLDuDetails.data.du_set_details.length; j++)
            {
                for(var i=0; i<$scope.application.data.states.length; i++ )
                {
                    if ($scope.AlLDuDetails.data.du_set_details[j]._id.$oid !== $scope.application.data.states[i].parent_entity_id)
                    {
                        validFieldFlag++;
                        validFieldIndex = j;
                    }
                }
                if (validFieldFlag >= $scope.application.data.states.length)
                {
                    duName.push($scope.AlLDuDetails.data.du_set_details[validFieldIndex].name);
                    validFieldFlag = 0;
                }
                else
                {
                    validFieldFlag = 0;
                }
            }
            if (duName.length > 0)
            {
                $rootScope.handleResponse('Please select the state for du'+duName.toString());
                return false;
            }
        }*/

        for (var k=0; k<$scope.application.data.states.length; k++)
        {
            state.push($scope.application.data.states[k]._id.$oid);
           /* if($scope.application.data.states[k].state)
            {
                state.push($scope.application.data.states[k].state);
            }
            else
            {
                state.push($scope.application.data.states[k]._id.$oid);
            }*/
        }

        duData._id.oid = $scope.application.data._id.$oid;
        duData.name = $scope.application.data.name;
        duData.parent_entity_id = $scope.application.data.parent_entity_id;
        duData.approval_status = $scope.application.data.approval_status;
        duData.states = state;

        $scope.createState = editDuState.update(duData,function(stateUpdateSuccessResponse)
        {
            $state.go('viwDUSetState');
            $scope.duStateisDeleted = true;
            $rootScope.handleResponse(stateUpdateSuccessResponse);
        },
        function(stateUpdateErrorResponse)
        {
            $rootScope.handleResponse(stateUpdateErrorResponse);
        });

    };

    $scope.removeThisState = function(id)
    {
        StateDelete.remove({
            id : id
        },
        function (stateDeleteSuccessResponse)
        {
            $rootScope.handleResponse(stateDeleteSuccessResponse);
            $scope.duStateisDeleted = true;
            $state.go('viwDUSetState');
            GetAllDuState.get({
                page:0,
                type:'dusetstate'
            },
            function(successResponse)
            {
                $scope.AllDuSetState = successResponse.data;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
            delete $scope.AllDuSetState;
         },
         function (stateDeleteErrorResponse){
            $rootScope.handleResponse(stateDeleteErrorResponse);
        });

    };

    $scope.discardDUSetStateChanges = function()
    {
        $scope.duStateisDeleted = true;
        delete $scope.application;
        $state.go('viwDUSetState');
    };

});
});