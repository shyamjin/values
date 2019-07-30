define(['angular', 'ngResource', 'uiRouter', 'ngCookies','ngFocus'],function (app) {
  'use strict';

var addNewFlexAttributesControllerApp = angular.module('addNewFlexAttributesControllerApp', ['ui.router','focus-if']);

addNewFlexAttributesControllerApp.controller('AddNewFlexAttributesController', function($scope, $state, $stateParams, $rootScope,createNewFlexAttributes){
    $scope.application = {
        data : {
            name : '',
            title : '',
            description:'',
            entity : '',
            type:'',
            valid_values : [],
            default_value:'',
            is_active:true,
            is_mandatory:false
        }
    };

    $scope.FasEntity =
    [
        "DeploymentUnit",
        "Machine",
        "MachineGroup"
    ];

    $scope.FasTypes = [
        {name: "String", title: "String"},
        {name: "Select", title: "Select"},
        {name: "MultiSelect", title: "Multi Select"}
    ];

    $scope.addFasValidValues =  function()
    {
        $scope.application.data.valid_values.push("");
    };

    $scope.removeValues = function(index)
    {
        $scope.application.data.valid_values.splice(index, 1);
    };

   $scope.addNewFas = function(form)
   {
        var fsData = {};
        if($scope.application.data.entity === undefined || $scope.application.data.entity === '')
        {
            $rootScope.handleResponse('Please select the Entity for flexible attribute');
            return false;
        }
        if($scope.application.data.name === '')
        {
            $rootScope.handleResponse('Please enter the Flexible Attribute Name');
            return false;
        }
        if($scope.application.data.title === '')
        {
            $rootScope.handleResponse('Please enter the Flexible Attribute Title');
            return false;
        }
        if($scope.application.data.type === '' || $scope.application.data.type === undefined)
        {
            $rootScope.handleResponse('Please select the Type for flexible attribute');
            return false;
        }
        else if($scope.application.data.type === "Select" || $scope.application.data.type === "MultiSelect")
        {
            if($scope.application.data.valid_values.length === 0)
            {
                $rootScope.handleResponse("Valid Values can not be empty");
                return false;
            }

            if($scope.application.data.default_value)
            {
                if($scope.application.data.valid_values.indexOf($scope.application.data.default_value) === -1)
                {
                    $rootScope.handleResponse("Please put the default value from valid values");
                    return false;
                }
            }
        }

        var recipientsArray = $scope.application.data.valid_values.sort();
        for(var i=0; i<recipientsArray.length -1; i++)
        {
           if (recipientsArray[i + 1] == recipientsArray[i])
           {
               $rootScope.handleResponse("Duplicate valid values are not allowed");
               return false;
           }
        }

        fsData.entity = $scope.application.data.entity;
        fsData.name = $scope.application.data.name;
        fsData.title = $scope.application.data.title;
        fsData.description = $scope.application.data.description;
        fsData.type = $scope.application.data.type;
        fsData.default_value = $scope.application.data.default_value;
        fsData.is_active = $scope.application.data.is_active;
        fsData.is_mandatory = $scope.application.data.is_mandatory;
        fsData.valid_values = $scope.application.data.valid_values;

        $scope.createFlexAttributes = createNewFlexAttributes.save(fsData,function(fasCreateSuccessResponse)
        {
            $state.go('manageflexattribute');
            $rootScope.handleResponse(fasCreateSuccessResponse);
        },
        function(fasCreateErrorResponse)
        {
            $rootScope.handleResponse(fasCreateErrorResponse);
        });
   };

   $scope.discardFasChanges = function()
   {
        $state.go('manageflexattribute');
   };
});
});