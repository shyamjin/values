require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent'],function (app) {
  'use strict';

var addNewDUSetStateControllerApp = angular.module('addNewDUSetStateControllerApp', ['ui.router','statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent']);

addNewDUSetStateControllerApp.controller('CreateNewDUSetStateController', function($timeout, $scope, $rootScope, $state, $location, $stateParams, $http, DUSetAll, ApprovalStatusAll,ViewDUSet, createState,GetAllDUBuildData,GetDUStateData,GetDUSetStateByID)
{
    $scope.BuildFlag =false;
    $scope.StateFlag = false;
    $scope.deploymentTypeToSelect ={
        type :"Build"
    };
    $scope.application = {
        data : {
            statename : '',
            duset : '',
            approval_status:'',
            data:{
                du_set_details:[],
                du_set_details1:{}
            }

        }
    };
    $scope.du_errors = {
         deployment_field_errors : {
            input_name : '',
            input_type : '',
            default_value : '',
            valid_values : '',
            tooltip : ''
        }
    };

    $scope.getDUBuildDetails = function()
	    {
	        $scope.preLoader = true;
	        GetAllDUBuildData.get({
	            id : $scope.AlLDuDetails.data._id.$oid
	        },
	        function(viewDUBuildSuccessResponse)
	        {
	            $scope.AlLDuDetails = viewDUSetSuccessResponse;
	            $scope.application.data.data.du_set_details =[];
	        },
	        function(viewDUBuildErrorResponse)
	        {
	            $rootScope.handleResponse(viewDUBuildErrorResponse);
	        });

	    };

	    $scope.getDUStateDetails = function()
	    {
	        $scope.preLoader = true;
	        GetDUSetStateByID.get({
	            parent_entity_id : $scope.AlLDuDetails.data._id.$oid
	        },
	        function(viewDUStateSuccessResponse)
	        {
	            $scope.AlLDuDetails = viewDUStateSuccessResponse;
	            $scope.application.data.data.du_set_details =[];
	        },
	        function(viewDUBuildErrorResponse)
	        {
	            $rootScope.handleResponse(viewDUBuildErrorResponse);
	        });
	    };

    $scope.setDUDeployType = function(value)
    {
        $scope.deploymentTypeToSelect.type = value;
        $scope.application.data.data.du_set_details1 = {};
        if($scope.deploymentTypeToSelect.type === "Build")
        {
            $scope.BuildFlag =true;
            $scope.StateFlag = false;
            $scope.getDUBuildDetails();
        }
        if($scope.deploymentTypeToSelect.type === "State")
        {
            $scope.BuildFlag =false;
            $scope.StateFlag = true;
            $scope.getDUStateDetails();
        }


    };

    $scope.dusetsAll = DUSetAll.get({
        page: 0,
        perpage: 0
    },
    function(dusetSuccessResponse)
    {
        $scope.dusetsAll = dusetSuccessResponse.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.approvalStatus = ApprovalStatusAll.get({
    },
    function(successResponse)
    {
        $scope.ApprovalsStatus = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });
    $scope.getDUSetById = function(id)
    {
        GetAllDUBuildData.get({
        id : id
        },
        function(viewDUSetSuccessResponse)
        {
            $scope.BuildFlag =true;
            $scope.StateFlag = false;
            $scope.deploymentTypeToSelect.type ="Build";
            $scope.AlLDuDetails = viewDUSetSuccessResponse;
            $scope.application.data.data.du_set_details =[];
        },
        function(viewDUErrorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

    };
    $scope.selectDU = function(duId, value,name)
    {

        if ($scope.application.data.data.du_set_details1[duId] === undefined)
        {
            $scope.application.data.data.du_set_details1[duId]={};
        }

        if($scope.deploymentTypeToSelect.type === "Build")
        {
            if (value !== undefined)
            {
                $scope.application.data.data.du_set_details1[duId]["build_id"]=value;
            }
            if (name !== undefined)
            {
                $scope.application.data.data.du_set_details1[duId]["name"]=name;
            }
        }
        if($scope.deploymentTypeToSelect.type === "State")
        {
            var duValue = JSON.parse(value);
            if (duValue !== undefined)
            {
                $scope.application.data.data.du_set_details1[duId]["state_id"]=duValue._id.$oid;
                for(var du=0; du<$scope.AlLDuDetails.data.du_set_details.length; du++)
                {
                    if($scope.AlLDuDetails.data.du_set_details[du]._id.$oid === duId)
                    {
                        $scope.AlLDuDetails.data.du_set_details[du].state_approval_status = duValue.approval_status;
                    }
                }


                $scope.application.data.data.du_set_details1[duId]["approval_status"] = duValue.approval_status
            }
        }
    };

    $scope.createNewDusetState = function(form)
    {
        var duData = {};
        var validFieldFlag = 0;
        var validFieldIndex = 0;
        var duName = [];
        var state =[];
        var errMessage =[];
        $scope.application.data.data.du_set_details=[];

         for(var j=0; j<$scope.AlLDuDetails.data.du_set_details.length; j++)
         {
             var data=$scope.application.data.data.du_set_details1[$scope.AlLDuDetails.data.du_set_details[j]._id.$oid];
             if (( data === undefined) || (data["name"] !== undefined && data["build_id"] === undefined))
             {
                errMessage.push($scope.AlLDuDetails.data.du_set_details[j].name.toString());
             }
         }

        if (errMessage.length > 0)
        {
            $rootScope.handleResponse('Please enter details for : '+ errMessage.join(','));
            return false;
        }

        for(var m in $scope.application.data.data.du_set_details1)
        {
            var key = m;
            var val = $scope.application.data.data.du_set_details1[m];
            if (val["build_id"] !== undefined)
            {
                $scope.application.data.data.du_set_details.push(val);
            }
            else if (val["state_id"] !== undefined)
            {
                $scope.application.data.data.du_set_details.push(val["state_id"]);
            }

        }
        if($scope.application.data.statename === '')
        {
            $rootScope.handleResponse('Please enter the DU State name');
            return false;
        }

        if($scope.application.data.duset === '')
        {
            $rootScope.handleResponse('Please enter the DU Package Name');
            return false;
        }
        if($scope.application.data.approval_status === '' || $scope.application.data.approval_status===undefined || $scope.application.data.approval_status===null)
        {
            $rootScope.handleResponse('Please select the Status');
            return false;
        }

        for (var k=0; k<$scope.application.data.data.du_set_details.length; k++)
        {
            state.push($scope.application.data.data.du_set_details[k]);
        }

        duData.name = $scope.application.data.statename;
        duData.parent_entity_id = $scope.application.data.duset;
        duData.approval_status = $scope.application.data.approval_status;
        duData.states = state;

        $scope.createState = createState.save(duData,function(stateCreateSuccessResponse)
        {
            $state.go('manageStates');
            $rootScope.handleResponse(stateCreateSuccessResponse);
        },
        function(stateCreateErrorResponse)
        {
            $rootScope.handleResponse(stateCreateErrorResponse);
        });

    };
    $scope.discardStateChanges = function()
    {
        $state.go('manageStates');
    };

});
});