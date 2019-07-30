require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent','toolTips']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent','toolTips'],function (app) {
  'use strict';

var manageStatesControllerApp = angular.module('manageStatesControllerApp', ['ui.router','statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent','720kb.tooltips']);

manageStatesControllerApp.controller('ManageStatesController', function($timeout, $scope, $rootScope, $state, $location, $stateParams, $http,GetAllDuState, DUStateViewById, ApprovalStatusAll,DeploymentUnitAll,ViewDU, editDuState, StateDelete){
    $scope.showAll = true;
    $scope.showLess = false;
    $scope.duStateisDeleted = false;
    $scope.selectedBuild = '';
    $scope.isFilterApplied = false;
    $scope.approvalStatusFlag = false;
    $scope.hideShowMoreDuState = false;
    $scope.DunameFlag =false;
    var approvalStatusFilter = [];
    var dunameFilter =[];

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
    $scope.searchDUState = function(event,searchStateKeyword)
    {
        if (searchStateKeyword.length ==0)
        {
            delete $scope.AllDuState ;
                GetAllDuState.get({
                page:0,
                type:'dustate'
            },
            function(successResponse)
            {
                $scope.AllDuState = successResponse.data;
                $scope.currentPage = successResponse.page;
                $scope.totalCount = successResponse.total;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        }

    };

    $scope.searchStateWithName = function(keyword)
    {
        $rootScope.searchProgress = true;
        $scope.hideShowMoreDuState = true;
        delete $scope.AllDuState ;
        GetAllDuState.get({
           approval_status: null,
           parent_entity_id: null,
           type:'dustate',
           name:keyword,
           page: 0,
           perpage:0
        },
        function(successResponse)
        {
            delete $scope.AllDuState ;
            delete $rootScope.searchProgress;
            $('#open_filter').hide(500);
            $scope.AllDuState  = successResponse.data;
            $scope.currentPage = successResponse.page;
            $scope.totalCount = successResponse.total;

            $scope.$watch(function(scope) {
                return scope.AllDuState ;
            },
            function(newValue, oldValue) {
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.applyDuStateFilters = function()
    {
        var ApprovalStatus = '';
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

        if(dunameFilter.length>0)
        {
            duname = dunameFilter.toString();
        }
        else
        {
            duname = null;
        }
        if(ApprovalStatus === null && duname === null)
        {
            perpage = null;
            $scope.hideShowMoreDuState = false;
            $scope.isFilterApplied = false;
        }
        else
        {
            $scope.hideShowMoreDuState = true;
            $scope.isFilterApplied = true;
            $scope.duStateisDeleted = true;
        }
        delete $scope.AllDuState ;
        GetAllDuState.get({
           approval_status: ApprovalStatus,
           parent_entity_id: duname,
           type:'dustate',
           page: 0,
           perpage:perpage
        },
        function(successResponse)
        {
            delete $scope.AllDuState ;
            $('#open_filter').hide(500);
            $scope.AllDuState  = successResponse.data;
            $scope.currentPage = successResponse.page;
            $scope.totalCount = successResponse.total;

            $scope.$watch(function(scope) {
                return scope.AllDuState ;
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
        dunameFilter = [];
        $('#open_filter').hide(500);
        $scope.open_filter = false;
        $scope.hideShowMoreDuState = false;
        $scope.isFilterApplied = false;
        $scope.duStateisDeleted = true;
        GetAllDuState.get({
            page:0,
            type:'dustate'
        },
        function(successResponse)
        {
            delete $scope.application;
            $scope.AllDuState = successResponse.data;
            $scope.currentPage = successResponse.page;
            $scope.totalCount = successResponse.total;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.showMoreDuState = function()
    {
        var ApprovalStatus = '';
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
        angular.copy($scope.AllDuState, $scope.tempDuSets);
        delete $scope.AllDuState;
        GetAllDuState.get({
           approval_status: ApprovalStatus,
           parent_entity_id: duname,
           type:'dustate',
           page:$scope.currentPage
        },
        function(successResponse)
        {
            $scope.AllDuState = [];
            $scope.currentPage = successResponse.page;
            $scope.totalCount = successResponse.total;
           for(var a=0; a<successResponse.data.length; a++)
            {
                $scope.tempDuSets.push(successResponse.data[a]);
            }
            for(var b=0; b<$scope.tempDuSets.length; b++)
            {
                $scope.AllDuState.push($scope.tempDuSets[b]);
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

    };

    GetAllDuState.get({
        page:0,
        type:'dustate'
    },
    function(successResponse)
    {
        $scope.AllDuState = successResponse.data;
        $scope.currentPage = successResponse.page;
        $scope.totalCount = successResponse.total;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.selectDuState = function(stateId)
    {
        $scope.application = {};
        $scope.deployment = {};
        $scope.buildDetails = {};
        DUStateViewById.get({
            id:stateId
        },
        function(viewDUStateSuccessResponse)
        {
            $scope.duStateisDeleted = false;
            $scope.application = viewDUStateSuccessResponse;
           // $scope.application.data.build_number = $scope.application.data.build.build_number.toString();
            $scope.buildDetails = $scope.application.data.build;
            var approval_status = $scope.application.data.approval_status;
            //var build_id= $scope.application.data.build._id.$oid;
            $scope.oldStatus = '';
            //$scope.oldBuild ='';
            if(viewDUStateSuccessResponse.data.deployment_field)
            {
                for(var d=0; d<viewDUStateSuccessResponse.data.deployment_field.fields.length; d++)
                {
                    if(viewDUStateSuccessResponse.data.deployment_field.fields[d].input_type === 'date')
                    {
                        var date = new Date(viewDUStateSuccessResponse.data.deployment_field.fields[d].default_value);
                        delete viewDUStateSuccessResponse.data.deployment_field.fields[d].default_value;
                        viewDUStateSuccessResponse.data.deployment_field.fields[d].default_value = date;
                    }
                }
                }

            /*ViewDU.get({
                id : $scope.application.data.parent_entity_id
            },
            function(viewDUSuccessResponse)
            {
                $scope.deployment = viewDUSuccessResponse;
                if($scope.deployment.data.build)
                {
                    for(var d=0; d<$scope.deployment.data.build.length; d++)
                    {
                        $scope.deployment.data.build[d].build_number = $scope.deployment.data.build[d].build_number.toString();
                        if($scope.deployment.data.build[d].build_number === $scope.application.data.build_number)
                        {
                            $scope.buildDetails = $scope.deployment.data.build[d];
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
    /*$scope.showBuildDetails = function(value)
    {
        if($scope.deployment.data.build)
        {
            for(var d=0; d<$scope.deployment.data.build.length; d++)
            {
                if($scope.deployment.data.build[d].build_number === value)
                {
                    $scope.buildDetails = $scope.deployment.data.build[d];
                }
            }
        }
        $scope.application.data.build_id= $scope.buildDetails._id.$oid;
        $scope.application.data.build_number= $scope.buildDetails.build_number;
    };*/
    $scope.addApproval = function(value)
    {
        var approval_status = value;
        $scope.application.data.approval_status ='';
        $scope.application.data.approval_status= approval_status;
    };
    $scope.showMoreContent = function()
    {
        $scope.showAll = false;
        $scope.showLess = true;
        $('#release_notes_build').removeClass('text--ellipsis');
    };

    $scope.showLessContent = function()
    {
        $scope.showAll = true;
        $scope.showLess = false;
        $('#release_notes_build').addClass('text--ellipsis');
    };
    $scope.isFieldSelected = function(fieldName, fieldValue)
    {
        var duIndex = 0;
        for(var d=0;  d<$scope.application.data.deployment_field.fields.length; d++)
        {
            if($scope.application.data.deployment_field.fields[d].input_name === fieldName)
            {
                duIndex = d;
            }
        }

        if($scope.application.data.deployment_field.fields[duIndex].default_value)
        {
            var result = $.inArray(fieldValue, $scope.application.data.deployment_field.fields[duIndex].default_value);
            if(result < 0)
            {
                return false;
            }
            else
            {
                return true;
            }
        }
    };
    $scope.addDefaultValueToCheckbox = function(fieldName, fieldValue)
    {
        var fieldIndex = 0;
        for(var validFieldIndex = 0; validFieldIndex<$scope.application.data.deployment_field.fields.length; validFieldIndex++)
        {
            if($scope.application.data.deployment_field.fields[validFieldIndex].input_name === fieldName)
            {
                fieldIndex = validFieldIndex;
            }
        }

        if($scope.application.data.deployment_field.fields[fieldIndex].default_value)
        {
            var result = $.inArray(fieldValue, $scope.application.data.deployment_field.fields[fieldIndex].default_value);
            if(result < 0)
            {
                $scope.application.data.deployment_field.fields[fieldIndex].default_value.push(fieldValue);
            }
            else
            {
                var index = $scope.application.data.deployment_field.fields[fieldIndex].default_value.indexOf(fieldValue);
                $scope.application.data.deployment_field.fields[fieldIndex].default_value.splice(index, 1);
            }
        }
        else
        {
            $scope.application.data.deployment_field.fields[fieldIndex].default_value = [];
            $scope.application.data.deployment_field.fields[fieldIndex].default_value.push(fieldValue);
        }
    };
    $scope.editDUState = function(form)
    {
        var duData = {
        _id : {
                oid : ''
        }};

        if($scope.application.data.build._id.$oid === "" || $scope.application.data.build._id.$oid===undefined || $scope.application.data.build._id.$oid===null)
        {
            $rootScope.handleResponse('Please select the Build');
            return false;
        }
         if($scope.application.data.approval_status === "" || $scope.application.data.approval_status===undefined || $scope.application.data.approval_status===null)
        {
            $rootScope.handleResponse('Please select the Status');
            return false;
        }
        for(var d=0; d< $scope.application.data.deployment_field.fields.length; d++)
        {
            if($scope.application.data.deployment_field.fields[d].input_type === 'checkbox')
            {
               delete $scope.application.data.deployment_field.fields[d].selected_values;
            }
        }
        duData._id.oid = $scope.application.data._id.$oid;
        duData.name = $scope.application.data.name;
        duData.parent_entity_id = $scope.application.data.parent_entity_id;
        duData.build_id = $scope.application.data.build._id.$oid;
        duData.approval_status = $scope.application.data.approval_status;
        duData.deployment_field = $scope.application.data.deployment_field;

        $scope.createState = editDuState.update(duData,function(stateUpdateSuccessResponse)
        {
            $state.go('manageStates');
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
            $state.go('manageStates');

            GetAllDuState.get({
            page:0,
            type:'dustate'
            },
            function(successResponse){
            $scope.AllDuState = successResponse.data;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
            delete $scope.AllDuState;
         },
         function (stateDeleteErrorResponse){
            $rootScope.handleResponse(stateDeleteErrorResponse);
        });

    };

    $scope.discardDUStateChanges = function()
    {
        $scope.duStateisDeleted = true;
        delete $scope.application;
        $state.go('manageStates');

    };


});
});