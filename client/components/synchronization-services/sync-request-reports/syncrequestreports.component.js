define(['angular'],function (app) {
  'use strict';

    var syncRequestReportsComponentApp = angular.module('syncRequestReportsComponentApp', ['settingsServicesApp', 'viewSyncRequestComponentApp']);

    syncRequestReportsComponentApp.controller('SyncRequestReportsController', function ($scope, $state, $rootScope, SyncRequestsAll, GetSyncRequestByID, RetrySyncRequest) {

        SyncRequestsAll.get({
            page: 0,
            perpage: 30
        },
        function(successResponse)
        {
            $scope.syncRequests = successResponse.data.data;

            for(var j=0; j<$scope.syncRequests.length; j++)
            {
                if($scope.syncRequests[j].date)
                {
                    $scope.syncRequests[j].date = new Date($scope.syncRequests[j].date);
                }
            }

            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

        $scope.viewSyncRequest = function(sync_id)
        {
            $rootScope.selectedSyncID = sync_id;
            GetSyncRequestByID.get({
                id: sync_id,
                page: 0,
                perpage: 30
            },
            function(successResponse)
            {
                $rootScope.SyncData = successResponse.data;
                $rootScope.pageTotal = [];
                for(var i=1; i<=successResponse.data.page_total; i++)
                {
                    $rootScope.pageTotal.push(i);
                }
                if(successResponse.data.page === 0)
                {
                    $rootScope.add_count = 0;
                }
                $rootScope.currentTotal = successResponse.data.data.length;
                $rootScope.currentInnerPage = successResponse.data.page + 1;
                $rootScope.request_counts = {
                    success : successResponse.data.success,
                    failed : successResponse.data.failed,
                    skipped : successResponse.data.skipped,
                    retry : successResponse.data.retry,
                    new : successResponse.data.new,
                    compared : successResponse.data.compared,
                    total : successResponse.data.total
                };
                $rootScope.status = successResponse.data.status;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        };

        $scope.showMoreRequests = function()
        {
            $scope.currentPage = $scope.currentPage + 1;
            SyncRequestsAll.get({
                page: 0,
                perpage: 30
            },
            function(successResponse)
            {
                for(var a=0; a<successResponse.data.data.length; a++)
                {
                    $scope.tempRequests.push(successResponse.data.data[a]);
                }
                for(var b=0; b<$scope.tempRequests.length; b++)
                {
                    $scope.syncRequests.push($scope.tempRequests[b]);
                }
                for(var j=0; j<$scope.syncRequests.length; j++)
                {
                    if($scope.syncRequests[j].date)
                    {
                        $scope.syncRequests[j].date = new Date($scope.syncRequests[j].date);
                    }
                }
                $scope.currentPage = successResponse.data.page;
                $scope.totalCount = successResponse.data.total;
            },
            function(errorResponse){
                $rootScope.handleResponse(errorResponse);
            });
        };

        $scope.retryFailedSync = function(sync_request_id)
        {
            var jsonData = {
                sync_id : sync_request_id
            };

            RetrySyncRequest.update(jsonData, function(retrySuccessResponse){
                $rootScope.handleResponse(retrySuccessResponse);
                delete $rootScope.SyncData;
                SyncRequestsAll.get({
                    page: 0,
                    perpage: 30
                },
                function(successResponse)
                {
                    $scope.syncRequests = successResponse.data.data;
                    for(var j=0; j<$scope.syncRequests.length; j++)
                    {
                        if($scope.syncRequests[j].date)
                        {
                            $scope.syncRequests[j].date = new Date($scope.syncRequests[j].date);
                        }
                    }
                    $scope.currentPage = successResponse.data.page;
                    $scope.totalCount = successResponse.data.total;
                },
                function(errorResponse)
                {
                    $rootScope.handleResponse(errorResponse);
                });
                $scope.viewSyncRequest($rootScope.selectedSyncID);
            },
            function(retryErrorResponse){
                $rootScope.handleResponse(retryErrorResponse);
            });
        };

    });

});

