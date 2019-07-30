define(['angular', 'ngResource', 'uiRouter', 'ngCookies','ngFocus'],function (app) {
  'use strict';

var editFlexAttributesControllerApp = angular.module('editFlexAttributesControllerApp', ['ui.router','focus-if']);

editFlexAttributesControllerApp.controller('EditFlexAttributesController', function($scope, $state, $stateParams, $rootScope, flexAttributeViewAll,FlexAttributesById,editFlxibleAttribute){
    $scope.fasSelected = false;
    flexAttributeViewAll.get({
    },
    function(successResponse)
    {
        $scope.felxibleAttributes = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.getFaUlClass = function()
    {
        if($scope.fasSelected === true)
        {
            if($scope.displayTab!='/manage/flexibleattributes')
            {
                $scope.fasSelected = false;
            }
            return "vp-userform__fieldslist text--cs03 pr--lg";
        }
         else
         {
            return "vp-userform__fieldslist text--cs03 pr--lg hidden";
         }
    };

    $scope.getFaFormClass = function()
    {
        if($scope.fasSelected === true)
        {
            if($scope.displayTab!='/manage/flexibleattributes')
            {
                $scope.fasSelected = false;
            }
            return "vp-selectedfasform--active vp-userform vp-control max";
        }
        else
        {
            return "vp-selectedfasform vp-userform vp-control max";
        }
    };

    $scope.isFasSelected = function(fas)
    {
        FlexAttributesById.get({
            id:fas._id.$oid
        },
        function(viewFasSuccessResponse)
        {
            $scope.fasSelected = true;
            $scope.application = viewFasSuccessResponse;
        },
        function(viewFasErrorResponse)
        {
           $rootScope.handleResponse(viewFasErrorResponse);
        });
    };

    $scope.addFasValidValues =  function()
    {
        $scope.application.data.valid_values.push("");
    };
    $scope.removeValues = function(index)
    {
        $scope.application.data.valid_values.splice(index, 1);
    };
    $scope.editNewFas = function(form)
    {
        var faData = {
        _id : {
                oid : ''
        }};

        if($scope.application.data.type === "Select" || $scope.application.data.type === "MultiSelect")
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

        faData._id.oid = $scope.application.data._id.$oid;
        faData.name = $scope.application.data.name;
        faData.title = $scope.application.data.title;
        faData.description = $scope.application.data.description;
        faData.entity = $scope.application.data.entity;
        faData.type = $scope.application.data.type;
        faData.default_value = $scope.application.data.default_value;
        faData.is_active = $scope.application.data.is_active;
        faData.is_mandatory = $scope.application.data.is_mandatory;
        faData.valid_values = $scope.application.data.valid_values;

        $scope.editFas = editFlxibleAttribute.update(faData,function(fasUpdateSuccessResponse)
        {
            $state.go('manageflexattribute');
            $scope.fasSelected = false;
            $rootScope.handleResponse(fasUpdateSuccessResponse);
            flexAttributeViewAll.get({
            },
            function(successResponse)
            {
                $scope.felxibleAttributes = successResponse;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        },
        function(fasUpdateErrorResponse)
        {
            $rootScope.handleResponse(fasUpdateErrorResponse);
        });
    };
    $scope.discardChanges = function()
    {
        $scope.fasSelected = false;
        delete $scope.application;
        $state.go('manageflexattribute');
    };
});
});