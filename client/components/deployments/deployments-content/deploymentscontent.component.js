define(['angular','deploymentPartialControllerApp'],function (app) {
  'use strict';

var deploymentRequestGridControllerApp = angular.module('deploymentRequestGridControllerApp', ['deploymentPartialControllerApp']);

deploymentRequestGridControllerApp.controller('DeploymentRequestsGridController', function ($timeout, $scope, $rootScope, $state, $filter, $stateParams,   DeploymentRequestView, OneDeploymentRequestView, SingleDeploymentRequestDetails, RetryDeploymentRequestGroup, $interval, UndeployDeploymentRequestGroup,RevertDeploymentGroup) {
    $scope.showSkippedRequests = false;
    var showTabIndex = false;
    var jsonData={};

    jsonData._id={
        oid:""
    };
    $scope.isFilterApplied = false;
    $scope.showRevertScreen = false;

    $scope.changeSkippedRequests = function()
    {
        if($scope.showSkippedRequests === false)
        {
            $scope.showSkippedRequests = true;
        }
        else
        {
            $scope.showSkippedRequests = false;
            $scope.SingleData ="";
            $scope.selectedIndex="";
        }
    };

    $scope.openFilter = function()
     {
        if(document.getElementById("open_filter").style.display === "none" || document.getElementById("open_filter").style.display === "")
        {
            $('#open_filter').show();
            $scope.open_filter = true;
        }
        else
        {
            $('#open_filter').hide();
            $scope.open_filter = false;
        }
     };

     $scope.openFilterMove = function(param)
     {
        if(param === 'modal' && $scope.open_filter === true)
        {
            return 'move_list';
        }
        else if(param ==='footer' && $scope.open_filter === true)
        {
            return 'move_footer';
        }
     };
    $scope.unDeployGroup = function(requestId)
    {
        $scope.undeployDeploymentGroup = requestId;
        if(document.getElementById("delete_attenation_popup").style.display === "none" || document.getElementById("delete_attenation_popup").style.display === "")
        {
            $('#delete_attenation_popup').show(700);
        }
        else
        {
            $('#delete_attenation_popup').hide(700);
        }
    };
    $scope.cancelUndeployGroup = function()
    {
        $('#delete_attenation_popup').hide(700);
    };
    //Deployments Code Start
    $scope.selectedGroup = 0;
    $scope.showRequestDetails = false;
    $scope.collapsed = false;

    $scope.setRequestVisibility = function(request, showSkippedRequestsIndicator, index)
    {
        if(request.skipped_ind === undefined || request.skipped_ind === false || !request.skipped_ind)
        {
            //$scope.selectedIndex = index;
            return true;
        }
        else
        {
            if(showSkippedRequestsIndicator === true)
            {
                //$scope.selectedIndex = index;
                return true;
            }
            else
            {
                return false;
            }
        }
    };

    DeploymentRequestView.get({
        page : 0
    },
    function(response)
    {
        $scope.deployments = response;
        $scope.currentPage = response.data.page;
        $scope.totalCount = response.data.total;
    }, 
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });


    $scope.selectDeploymentGroup = function (groupid) {
        $scope.selectedGroupID = groupid;
        $scope.deploymentGroup = OneDeploymentRequestView.get({
                id: groupid
        },
        function (successResponse)
        {
            $scope.GroupData = successResponse.data;
            $scope.SingleData="";
           /* if($scope.GroupData.details.length>1)
            {
                for(var ind=0; ind<$scope.GroupData.details.length; ind++)
                {
                    if($scope.GroupData.details[ind].skipped_ind === false || $scope.GroupData.details[ind].skipped_ind === undefined)
                    {
                        $scope.selectedIndex = ind;
                        showTabIndex = true;
                        break;
                    }
                }
            }

            $rootScope.$emit('setVerticalTabIndex',$scope.selectedIndex);
            $scope.selectDeployment($scope.selectedIndex);*/
        },
        function (errorResponse){
            $rootScope.handleResponse(errorResponse);
        });
    };
    if($stateParams.id)
    {
        $scope.selectDeploymentGroup($stateParams.id);
    }

    // selectDeployment
    $scope.selectDeployment = function (index)
    {
        $scope.showRevertScreen = false;
        $scope.SingleRequestData = $scope.GroupData.details[index].deployment_id;
        $scope.reqIndex = index;
        $scope.selectedIndex=index;
        $scope.deploymentRequestDetails = SingleDeploymentRequestDetails.get({
            id: $scope.SingleRequestData
        },
        function (response)
        {
            $scope.SingleData = response.data;
            $scope.CurrentDeployment = response.data;
            $scope.CurrentDeploymentlogs = response.data.logs;
        },
        function (errorResponse){
            $rootScope.handleResponse(errorResponse);
        });
    };
    $rootScope.$on("setIndexOfFirstTab", function(event, args){
          $scope.selectDeployment(args);
    });
    $rootScope.$on("setDeploymentGroup", function(event, args){
          $scope.selectDeploymentGroup(args);
    });
    $rootScope.$on("setDeploymentGroupFilter", function(event, args){
          $scope.deploymentGroupFilter(args);
    });
    $rootScope.$on("closeDeploymentGroupFilter", function(event, args){
          $scope.closeDeploymentGroupFilter(args);
    });

    $scope.deploymentGroupFilter = function(data)
    {
        DeploymentRequestView.get({
            scheduled_date : data.scheduled_date,
            create_date : data.create_date,
            machine_id : data.machine_id,
            du_id : data.du_id,
            requested_by : data.requested_by,
            page : 0,
            perpage : data.perpage
        },
        function(response)
        {
            delete $scope.deployments;
            delete $scope.GroupData;
            $scope.deployments = response;
            $scope.currentPage = response.data.page;
            $scope.totalCount = response.data.total;
            $scope.$watch(function(scope) {
                return scope.requestsAll;
            },
            function(newValue, oldValue) {
            });
        }, 
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };
    $scope.closeDeploymentGroupFilter = function(data)
    {
        DeploymentRequestView.get({
            page: data
        },
        function(response)
        {
            delete $scope.GroupData;
            $scope.deployments = response;
            $scope.currentPage = response.data.page;
            $scope.totalCount = response.data.total;
        }, 
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.retryGroup = function(requestId)
    {
        jsonData._id.oid = requestId;
        $scope.retryDeploymentRequestGroup = RetryDeploymentRequestGroup.update(jsonData,function(retryDeploymentRequestGroupResponse){
            $rootScope.handleResponse(retryDeploymentRequestGroupResponse);
            DeploymentRequestView.get({
                page: 0
            },
            function(response){
                $scope.deployments = response;
                $scope.currentPage = response.data.page;
                $scope.totalCount = response.data.total;
            }, 
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
            $scope.selectDeploymentGroup($scope.selectedGroupID);
            $scope.selectDeployment($scope.selectedIndex);
        },
        function(retryDeploymentRequestGroupErrorResponse){
            $rootScope.handleResponse(retryDeploymentRequestGroupErrorResponse);
        });
    };
    $scope.continueUndeployGroup = function()
    {
        $('#delete_attenation_popup').hide(700);
        jsonData._id.oid = $scope.undeployDeploymentGroup;
        $scope.undeployDeploymentRequestGroup = UndeployDeploymentRequestGroup.save(jsonData,function(undeployDeploymentRequestGroupResponse){
            $rootScope.handleResponse(undeployDeploymentRequestGroupResponse);
            DeploymentRequestView.get({
                page: 0
            },
            function(response){
                $scope.deployments = response;
                $scope.currentPage = response.data.page;
                $scope.totalCount = response.data.total;
            }, 
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
            $scope.selectDeploymentGroup(undeployDeploymentRequestGroupResponse.data._id);
            $scope.selectDeployment($scope.selectedIndex);
        },
        function(undeployDeploymentRequestGroupErrorResponse){
            $rootScope.handleResponse(undeployDeploymentRequestGroupErrorResponse);
        });
    };
    $scope.showMoreDeployments = function()
    {
        $scope.currentPage = $scope.currentPage+1;
        $scope.tempDeployments = [];
        angular.copy($scope.deployments, $scope.tempDeployments);
        delete $scope.deployments;
        DeploymentRequestView.get({
            page: $scope.currentPage
        },
        function(response)
        {
            $scope.deployments = {
                'data' : {
                    'requests_count' : {},
                    'list' : []
                }
            };
            for(var a=0; a<response.data.list.length; a++)
            {
                $scope.tempDeployments.data.list.push(response.data.list[a]);
            }
            for(var b=0; b<$scope.tempDeployments.data.list.length; b++)
            {
                $scope.deployments.data.list.push($scope.tempDeployments.data.list[b]);
            }
            $scope.currentPage = response.data.page;
            $scope.totalCount = response.data.total;
        }, 
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.isPageAvailable = function()
    {
        if($scope.deployments)
        {
            if($scope.totalCount === $scope.deployments.data.list.length)
            {
                return false;
            }
            else
            {
                return true;
            }
        }
    };

    $scope.revertGroup = function(id)
    {
        $scope.showRevertScreen = true;
        RevertDeploymentGroup.get({
            id: id
        },
        function(response)
        {
            $scope.deploymentsGroupData = response;
            for (var i=0; i <$scope.deploymentsGroupData.data.du_set_details.length; i++)
            {
                $scope.deploymentsGroupData.data.du_set_details[i]["old_deployment_details"] = null;
                $scope.deploymentsGroupData.data.du_set_details[i]["machine_id_list"] = [];
                if($scope.GroupData.details)
                {
                    for(var k=0; k<$scope.GroupData.details.length; k++)
                    {
                        if($scope.deploymentsGroupData.data.du_set_details[i]._id.$oid ===  $scope.GroupData.details[k].parent_entity_id)
                        {
                             $scope.deploymentsGroupData.data.du_set_details[i]["machine_id_list"].push($scope.GroupData.details[k].machine_id);
                             $scope.deploymentsGroupData.data.du_set_details[i]["old_deployment_details"] = {};
                             if($scope.GroupData.details[k].state)
                             {
                                 $scope.deploymentsGroupData.data.du_set_details[i]["old_deployment_details"]["old_state_name"]=$scope.GroupData.details[k].state.name;
                                 $scope.deploymentsGroupData.data.du_set_details[i]["old_deployment_details"]["old_state_id"]=$scope.GroupData.details[k].state._id.$oid;
                                 $scope.deploymentsGroupData.data.du_set_details[i]["old_deployment_details"]["old_build_id"]=$scope.GroupData.details[k].build_id;
                                 $scope.deploymentsGroupData.data.du_set_details[i]["old_deployment_details"]["old_build_number"]=$scope.GroupData.details[k].build_number;
                                 $scope.deploymentsGroupData.data.du_set_details[i]["old_deployment_details"]["parent_entity_set_id"]=$scope.GroupData.parent_entity_set_id;
                             }
                             else
                             {
                                 $scope.deploymentsGroupData.data.du_set_details[i]["old_deployment_details"]["old_build_id"]=$scope.GroupData.details[k].build_id;
                                 $scope.deploymentsGroupData.data.du_set_details[i]["old_deployment_details"]["old_build_number"]=$scope.GroupData.details[k].build_number;
                             }
                        }
                    }
                }
            }
            $rootScope.$emit('revertDeploymentGroup',$scope.deploymentsGroupData);
        }, 
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

    };

})
 });