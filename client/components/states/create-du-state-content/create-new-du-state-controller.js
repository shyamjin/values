require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent'],function (app) {
  'use strict';

var addNewDUStateControllerApp = angular.module('addNewDUStateControllerApp', ['ui.router','statesServicesApp','deploymentUnitsServicesApp','stateTabsComponent']);

addNewDUStateControllerApp.controller('CreateNewDUStateController', function($timeout, $scope, $rootScope, $state, $location, $stateParams, $http, DeploymentUnitAll, ApprovalStatusAll, ViewDU, createState) {
     $scope.application = {
        data : {
            statename : '',
            du : '',
            approval_status:'',
            build_id:'',
            deployment_field : {
                fields : []
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
    $scope.showAll = true;
    $scope.showLess = false;
    $scope.hideBuildInfo = false;
    $scope.selectedBuild = '';
    var Deployment_fields = {};
    $scope.input_types = [
        "text",
        "password",
        "email",
        "date",
        "checkbox",
        "dropdown",
        "radio",
        "number"
    ];
    DeploymentUnitAll.get({
        page: 0,
        perpage: 0
    },
    function(successResponse)
    {
        $scope.AllDU = [];
        for(var a=0; a<successResponse.data.length; a++)
        {
            for(var b=0; b<successResponse.data[a].data.length; b++)
            {
                $scope.AllDU.push(successResponse.data[a].data[b]);
            }
        }
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

    $scope.getDUById = function(id)
    {
        ViewDU.get({
        id : id
        },
        function(viewDUSuccessResponse)
        {
            $scope.deployment = viewDUSuccessResponse;
            $scope.hideBuildInfo = true;
            $scope.application.data.deployment_field.fields =[];
            angular.copy(viewDUSuccessResponse.data.deployment_field.fields, $scope.application.data.deployment_field.fields);
            if(viewDUSuccessResponse.data.deployment_field)
            {
                for(var d=0; d<viewDUSuccessResponse.data.deployment_field.fields.length; d++)
                {
                    if(viewDUSuccessResponse.data.deployment_field.fields[d].input_type === 'date')
                    {
                        var date = new Date(viewDUSuccessResponse.data.deployment_field.fields[d].default_value);
                        delete viewDUSuccessResponse.data.deployment_field.fields[d].default_value;
                        viewDUSuccessResponse.data.deployment_field.fields[d].default_value = date;
                    }
                }
            }
        },
        function(viewDUErrorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };
    $scope.closeSettings = function(vIndex)
    {
        $scope.removeField(vIndex);
        document.getElementById("add_settings").style.display = "none";
    };

    $scope.saveSettings = function(fieldIndex)
    {
        if($scope.application.data.deployment_field.fields[fieldIndex].input_type === 'checkbox' || $scope.application.data.deployment_field.fields[fieldIndex].input_type === 'radio' || $scope.application.data.deployment_field.fields[fieldIndex].input_type === 'dropdown'  )
        {
            if($scope.application.data.deployment_field.fields[fieldIndex].valid_values.length>0)
            {
                 var validFieldFlag = 0;
                 for(var validFieldIndex = 0; validFieldIndex<$scope.application.data.deployment_field.fields[fieldIndex].valid_values.length; validFieldIndex++)
                 {
                    if($scope.application.data.deployment_field.fields[fieldIndex].valid_values[validFieldIndex] === '' || $scope.application.data.deployment_field.fields[fieldIndex].valid_values[validFieldIndex] === null || $scope.application.data.deployment_field.fields[fieldIndex].valid_values[validFieldIndex] === undefined)
                    {
                       validFieldFlag++;
                    }
                 }
                 if(validFieldFlag>0)
                 {
                     $scope.du_errors.deployment_field_errors.valid_values = 'Options can not be empty for this field';
                     return false;
                 }
                 else
                 {
                 $scope.du_errors.deployment_field_errors.valid_values = '';
                 $('#add_settings').hide(700);
                 }
            }
            else
            {
                $scope.du_errors.deployment_field_errors.valid_values = 'Please provide options for this field';
                 $('#add_settings').hide(700);
            }
        }
        else
        {
          $('#add_settings').hide(700);
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

//        for(var valueIndex=0; valueIndex<$scope.application.data.deployment_field.fields[fieldIndex].default_value.length; valueIndex++)
//        {
//
//        }
    };

    $scope.showBuildDetails = function(value)
    {
        $scope.hideBuildInfo = false;
        $scope.buildDetails = JSON.parse(value);
        $scope.application.data.build_id ='';
        $scope.application.data.build_id= $scope.buildDetails._id.$oid;
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
     $scope.showSettings = function()
    {
        if(document.getElementById("add_settings").style.display === "none" || document.getElementById("add_settings").style.display === "")
        {
            document.getElementById("add_settings").style.display = "block";
            $scope.addNewField();
        }
        else
        {
           document.getElementById("add_settings").style.display = "none";
        }
    };

    $scope.showEditSettings = function(index)
    {
        $scope.fieldIndex = index;
        if(document.getElementById("add_settings").style.display === "none" || document.getElementById("add_settings").style.display === "")
        {
            document.getElementById("add_settings").style.display = "block";
        }
        else
        {
           document.getElementById("add_settings").style.display = "none";
        }
    };

    $scope.closeSettings = function(vIndex)
    {
        document.getElementById("add_settings").style.display = "none";
    };

    $scope.removeValidValue = function(fieldIndex, valueIndex)
    {
        $scope.application.data.deployment_field.fields[fieldIndex].valid_values.splice(valueIndex, 1);
    };

    $scope.addNewField = function()
    {
        if($scope.application.data.deployment_field !== null)
        {
            if($scope.application.data.deployment_field.fields.length === 0)
            {
               $scope.application.data.deployment_field = {
                    fields : []
                };
                $scope.fieldIndex = $scope.application.data.deployment_field.fields.length;
                $scope.application.data.deployment_field.fields.push({
                    order_id : $scope.fieldIndex,
                    valid_values : []
                });
            }
            else
            {
                $scope.fieldIndex = $scope.application.data.deployment_field.fields.length;
                $scope.application.data.deployment_field.fields.push({
                    order_id : $scope.fieldIndex,
                    valid_values : []
                });
            }
        }
        else
        {
            $scope.application.data.deployment_field = {
                fields : []
            };
            $scope.fieldIndex = $scope.application.data.deployment_field.fields.length;
            $scope.application.data.deployment_field.fields.push({
                order_id : $scope.fieldIndex,
                valid_values : []
            });
        }
    };
    $scope.addNewValidValueField = function(index, version)
    {
        if($scope.application.data.deployment_field.fields[index].valid_values)
        {
            var len = ($scope.application.data.deployment_field.fields[index].valid_values).length;
        }
        else
        {
            $scope.application.data.deployment_field.fields[index].valid_values = [];
        }

        $scope.application.data.deployment_field.fields[index].valid_values.push("");
    };

    $scope.removeField = function(index)
    {
        $scope.application.data.deployment_field.fields.splice(index, 1);
    };

    $scope.removeValidValueField = function(index, version)
    {
        var lastItem = $scope.application.data.deployment_field.fields[index].valid_values.length-1;
        $scope.application.data.deployment_field.fields[index].valid_values.splice(lastItem,1);
    };

   $scope.createNewState = function(form)
   {
        var duData = {};
        if($scope.application.data.statename === '')
        {
            $rootScope.handleResponse('Please enter the State name');
            return false;
        }

        if($scope.application.data.du === "")
        {
            $rootScope.handleResponse('Please enter the DU Name');
            return false;
        }
        if($scope.application.data.build_id === "" || $scope.application.data.build_id===undefined || $scope.application.data.build_id===null)
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

        duData.name = $scope.application.data.statename;
        duData.parent_entity_id = $scope.application.data.du;
        duData.build_id = $scope.application.data.build_id;
        duData.approval_status = $scope.application.data.approval_status;
        duData.deployment_field = $scope.application.data.deployment_field;

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