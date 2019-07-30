define(['angular'],function (app) {
  'use strict';

    var viewSyncRequestComponentApp = angular.module('viewSyncRequestComponentApp', ['settingsServicesApp']);

    viewSyncRequestComponentApp.controller('ViewSyncRequestDataController', function ($scope, $state, $rootScope, GetSyncRequestByID, RetrySyncRequest, SyncRequestsAll) {
        $scope.isFilterApplied = false;
        $scope.statusFilterFlag = false;
        var statusFilter = [];
        $scope.operationFilterFlag = false;
        var operationFilter = [];
        $scope.SyncStatus = ["success", "failed", "new", "compared", "skipped", "retry"];

        $scope.showThisPage = function(page_no)
        {
            var status = "";
            var operation = "";
            if(statusFilter.length>0)
            {
                status = statusFilter.toString();
            }
            else
            {
                status = null;
            }
            if(operationFilter.length>0)
            {
                operation = operationFilter.toString();
            }
            else
            {
                operation = null;
            }

            delete $rootScope.SyncData;
            GetSyncRequestByID.get({
                id: $rootScope.selectedSyncID,
                page: page_no-1,
                perpage: 30,
                status : status,
                operation : operation
            },
            function(successResponse)
            {
                $rootScope.SyncData = successResponse.data;
                $rootScope.request_counts = {
                    success : successResponse.data.success,
                    failed : successResponse.data.failed,
                    skipped : successResponse.data.skipped,
                    retry : successResponse.data.retry,
                    new : successResponse.data.new,
                    compared : successResponse.data.compared
                };
                $rootScope.status = successResponse.data.status;
                if($rootScope.currentInnerPage === 0)
                {
                    $rootScope.add_count = 0;
                }
                else if(page_no<$rootScope.currentInnerPage)
                {
                    $rootScope.add_count = $rootScope.add_count - 30;
                }
                else
                {
                    $rootScope.add_count = $rootScope.add_count + 30;
                }
                $rootScope.currentInnerPage = page_no;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        };

        $scope.retryFailedSyncForEntity = function(request_id)
        {
            var jsonData = {
                _id : request_id
            };

            RetrySyncRequest.update(jsonData, function(retrySuccessResponse){
                $rootScope.handleResponse(retrySuccessResponse);
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
                $scope.showThisPage($rootScope.currentInnerPage);
            },
            function(retryErrorResponse){
                $rootScope.handleResponse(retryErrorResponse);
            });
        };

        $scope.setStatusFilterCSS = function(flag)
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

        $scope.showStatusFilter = function()
        {
                if($scope.statusFilterFlag === true)
                {
                    $scope.statusFilterFlag = false;
                }
                else
                {
                    $scope.statusFilterFlag = true;
                }
        };

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

        $scope.setOperationFilterCSS = function(flag)
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

        $scope.showOperationFilter = function()
        {
                if($scope.operationFilterFlag === true)
                {
                    $scope.operationFilterFlag = false;
                }
                else
                {
                    $scope.operationFilterFlag = true;
                }
        };

        $scope.setOperationFilter = function(operation)
        {
            var operationFlag = 0;
            var ind = 0;
            var operationFilterLen = operationFilter.length;
            if(operationFilterLen>0)
            {
                for(var a=0; a<operationFilterLen; a++)
                {
                    if(operationFilter[a] === operation)
                    {
                        ind = a;
                    }
                    else
                    {
                        operationFlag++;
                    }
                }

                if(operationFlag === operationFilterLen)
                {
                    operationFilter.push(operation);
                }
                else
                {
                    operationFilter.splice(ind, 1);
                }
            }
            else
            {
                operationFilter.push(operation);
            }
        };

        $scope.showFilter = function(tab)
        {
            if(document.getElementById("show_sync_filter").style.display === "none" || document.getElementById("show_sync_filter").style.display === "")
            {
                $('#show_sync_filter').show(700);
            }
            else
            {
                $('#show_sync_filter').hide(700);
            }
        };

        $scope.resetFilter = function(form)
        {
            statusFilter = [];
            operationFilter = [];
            $('#show_sync_filter').hide(700);
            $scope.isFilterApplied = false;
            delete $rootScope.SyncData;
            GetSyncRequestByID.get({
                id: $rootScope.selectedSyncID,
                page: 0,
                perpage: 30
            },
            function(successResponse)
            {
                $rootScope.SyncData = successResponse.data;
                $rootScope.currentInnerPage = 0;
                $rootScope.request_counts = {
                    success : successResponse.data.success,
                    failed : successResponse.data.failed,
                    skipped : successResponse.data.skipped,
                    retry : successResponse.data.retry,
                    new : successResponse.data.new,
                    compared : successResponse.data.compared
                };
                $rootScope.status = successResponse.data.status;
                if($rootScope.currentInnerPage === 0)
                {
                    $rootScope.add_count = 0;
                }
                else if(page_no<$rootScope.currentInnerPage)
                {
                    $rootScope.add_count = $rootScope.add_count - 30;
                }
                else
                {
                    $rootScope.add_count = $rootScope.add_count + 30;
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        };

       $scope.closeFilter = function()
       {
            $('#show_sync_filter').hide(700);
       };

       $scope.applySyncFilters = function()
       {
            var status = '';
            var operation = '';

            if(statusFilter.length>0)
            {
                status = statusFilter.toString();
            }
            else
            {
                status = null;
            }
            if(operationFilter.length>0)
            {
                operation = operationFilter.toString();
            }
            else
            {
                operation = null;
            }

            delete $rootScope.SyncData;
            GetSyncRequestByID.get({
                id: $rootScope.selectedSyncID,
                page: 0,
                perpage: 0,
                status: status,
                operation : operation
            },
            function(successResponse)
            {
                $rootScope.SyncData = successResponse.data;
                $rootScope.pageTotal = [];
                for(var i=1; i<=successResponse.data.page_total; i++)
                {
                    $rootScope.pageTotal.push(i);
                }
                $rootScope.currentTotal = successResponse.data.data.length;
                $rootScope.currentInnerPage = successResponse.data.page + 1;
                $rootScope.status = successResponse.data.status;

                $rootScope.request_counts = {
                    success : successResponse.data.success,
                    failed : successResponse.data.failed,
                    skipped : successResponse.data.skipped,
                    retry : successResponse.data.retry,
                    new : successResponse.data.new,
                    compared : successResponse.data.compared
                };
                $rootScope.status = successResponse.data.status;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        };
    });
});

