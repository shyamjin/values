require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['deploymentServicesApp']
});

define(['angular'],function (app) {
  'use strict';

var savedRequestsComponentControllerApp = angular.module('savedRequestsComponentControllerApp', ['deploymentServicesApp']);

savedRequestsComponentControllerApp.controller('SavedDeploymentRequestsController', function ($scope, $rootScope, $state, GetAllSavedDeploymentRequests, DeleteSavedDeploymentRequest ) {
    var jsonData={};
    $scope.showLogIndicator = false;
    jsonData._id={
        oid:""
    };
    $scope.showRequestDetails = false;
    var  count = 0 ;

    GetAllSavedDeploymentRequests.get({
    },
    function(response)
    {
        $scope.requestsAll =  response;
    }, 
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.isExpanded = function(flag)
    {
        if(flag === true)
        {
            return 'vp-treeview__dateitem--expanded';
        }
        else
        {
            return '';
        }
    };

    $scope.editSavedDeploymentRequest = function(requestID, deployment_type)
    {
        if(deployment_type === 'toolgroup')
        {
            $state.go('editSavedToolDeploymentRequest', {request_id : requestID});
        }
        else
        {
            $state.go('editSavedDUDeploymentRequest', {request_id : requestID});
        }
    };

    $scope.deleteSavedDeploymentRequest = function(request_id)
    {
        DeleteSavedDeploymentRequest.remove({
            id : request_id
        },
        function (groupDeleteRequest)
        {
            delete $scope.requestsAll;
            GetAllSavedDeploymentRequests.get({
            },
            function(response)
            {
                $scope.requestsAll =  response;
            }, 
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
            $rootScope.handleResponse(groupDeleteRequest);
         },
         function (groupDeleteResponseError)
         {
            $rootScope.handleResponse(groupDeleteResponseError);
         });

    };


});

});