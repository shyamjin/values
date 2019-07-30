define(['angular','deploymentPartialControllerApp'],function (app) {
  'use strict';

var DeploymentRequestsFilterControllerApp = angular.module('DeploymentRequestsFilterControllerApp', ['deploymentPartialControllerApp']);

DeploymentRequestsFilterControllerApp.controller('DeploymentRequestsFilterController', function ($scope, $filter, $rootScope,DeploymentRequestView, GetAllMachine, DeploymentUnitAll,Users ) {

     $scope.dateSelected = null;
     $scope.creationDateSelected = null;
     $scope.dateFilterFlag = true;
     $scope.machineFilterFlag = false;
     $scope.duFilterFlag = false;
     $scope.requestByFilterFlag = false;
     $scope.creationDateFilterFlag = false;
     $rootScope.hideDeploymentRequest = false;
     $scope.isFilterApplied = false;
     var creationDateFilter = null;
     var dateFilter =null;
     var machineFilter = [];
     var duFilter = [];
     var requestedUserFilter=[];

     $scope.cancleFilter = function()
     {
        $('#open_filter').hide(700);
     };

     $scope.showDateFilter = function()
     {
        if($scope.dateFilterFlag === true)
        {
            $scope.dateFilterFlag = false;
        }
        else
        {
            $scope.dateFilterFlag = true;
        }
    };
    $scope.showCreationDateFilter = function()
    {
        if($scope.creationDateFilterFlag === true)
        {
            $scope.creationDateFilterFlag = false;
        }
        else
        {
            $scope.creationDateFilterFlag = true;
        }
    };
    $scope.showRequestByFilter = function()
    {
        if($scope.requestByFilterFlag === true)
        {
            $scope.requestByFilterFlag = false;
        }
        else
        {
            $scope.requestByFilterFlag = true;
        }
    };
    $scope.setRequestByFilterCSS = function(flag)
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
    $scope.setDateFilterCSS = function(flag)
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
    $scope.setCreationDateFilterCSS = function(flag)
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
    $scope.showMachineFilter = function()
    {
        if($scope.machineFilterFlag === true)
        {
            $scope.machineFilterFlag = false;
        }
        else
        {
            $scope.machineFilterFlag = true;
        }
    };

    $scope.setMachineFilterCSS = function(flag)
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

    $scope.showDUFilter = function()
    {
        if($scope.duFilterFlag === true)
        {
            $scope.duFilterFlag = false;
        }
        else
        {
            $scope.duFilterFlag = true;
        }
    };

    $scope.setDUFilterCSS = function(flag)
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
    GetAllMachine.get({
    },
    function(successResponse)
    {
        $scope.allMachines = successResponse.data.data;
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
        $scope.applications =[];
        for(var a=0; a<successResponse.data.length; a++)
        {
            for(var b=0; b<successResponse.data[a].data.length; b++)
            {
                $scope.applications.push(successResponse.data[a].data[b]);
            }
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.users = Users.get({
        id:"all"
    },
    function(successResponse)
    {
        $scope.allUsers = successResponse.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.setMachineFilter = function(machine)
    {
        var machineFlag = 0;
        var ind = 0;
        var machineFilterLen = machineFilter.length;
        if(machineFilterLen>0)
        {
            for(var a=0; a<machineFilterLen; a++)
            {
                if(machineFilter[a] === machine)
                {
                    machineFlag++;
                    ind = a;
                }
            }

            if(machineFlag === 0)
            {
                machineFilter.push(machine);
            }
            else
            {
                machineFilter.splice(ind, 1);
            }
        }
        else
        {
            machineFilter = [];
            machineFilter.push(machine);
        }
    };

    $scope.setDUFilter = function(du)
    {
        var duFlag = 0;
        var ind = 0;
        var duFilterLen = duFilter.length;
        if(duFilterLen>0)
        {
            for(var a=0; a<duFilterLen; a++)
            {
                if(duFilter[a] === du)
                {
                    duFlag++;
                    ind = a;
                }
            }

            if(duFlag === 0)
            {
                duFilter.push(du);
            }
            else
            {
                duFilter.splice(ind, 1);
            }
        }
        else
        {
            duFilter =[];
            duFilter.push(du);
        }
    };

    $scope.setRequestByFilter = function(user)
    {
        var userFlag = 0;
        var ind = 0;
        var requestedUserFilterLen = requestedUserFilter.length;
        if(requestedUserFilterLen>0)
        {
            for(var a=0; a<requestedUserFilterLen; a++)
            {
                if(requestedUserFilter[a] === user)
                {
                    userFlag++;
                    ind = a;
                }
            }

            if(userFlag === 0)
            {
                requestedUserFilter.push(user);
            }
            else
            {
                requestedUserFilter.splice(ind, 1);
            }
        }
        else
        {
            requestedUserFilter = [];
            requestedUserFilter.push(user);
        }
    };

    $scope.setDateFilter = function(date)
    {
        dateFilter = date;
    };

    $scope.setCreationDateFilter = function(date)
    {
        creationDateFilter = date;
    };

    $scope.applyDeploymentFilters = function()
    {
        var scheduled_date = "";
        var creation_date = "";
        var machine_id = "";
        var requested_by = "";
        var du_id = "";
        var perpage = 0;

        if(dateFilter !== null && dateFilter!== undefined && dateFilter !== '')
        {
           /* var dateISO = dateFilter.toISOString();
            var lastIndex = dateISO.indexOf("T");
            var dateFormatted = dateISO.substring(0, lastIndex);*/
            var dateFormatted = $filter('date')(dateFilter, 'y-M-d');
            scheduled_date = dateFormatted;
        }
        else
        {
           scheduled_date =null;
        }

        if(creationDateFilter !== null && creationDateFilter!== undefined && creationDateFilter !== '')
        {
           /* var dateISO = dateFilter.toISOString();
            var lastIndex = dateISO.indexOf("T");
            var dateFormatted = dateISO.substring(0, lastIndex);*/
            var creationDateFormatted = $filter('date')(creationDateFilter, 'y-M-d');
            creation_date = creationDateFormatted;
        }
        else
        {
           creation_date =null;
        }

        if(machineFilter.length>0)
        {
            machine_id = machineFilter.toString();
        }
        else
        {
            machine_id = null;
        }

        if(duFilter.length>0)
        {
            du_id = duFilter.toString();
        }
        else
        {
            du_id = null;
        }
        if(requestedUserFilter.length>0)
        {
            requested_by = requestedUserFilter.toString();
        }
        else
        {
            requested_by = null;
        }
        if(scheduled_date === null && creationDateFilter === null && machine_id === null && du_id === null && requested_by === null)
        {
            perpage = null;
            $rootScope.hideDeploymentRequest = false;
            $scope.isFilterApplied = false;
        }
        else
        {
            $rootScope.hideDeploymentRequest = true;
            $scope.isFilterApplied = true;
        }
        var jsonData={
            scheduled_date : scheduled_date,
            create_date : creation_date,
            machine_id : machine_id,
            requested_by : requested_by,
            du_id : du_id,
            page : 0,
            perpage : perpage
        };
        $('#open_filter').hide(700);
        $rootScope.$emit('setDeploymentGroupFilter',jsonData);

    };

    $scope.closeFilter = function(form)
    {
        $scope.dateSelected = null;
        $scope.creationDateSelected = null;
        machineFilter = [];
        duFilter = [];
        requestedUserFilter = [];
        $('#open_filter').hide(700);
        $scope.open_filter = false;
        $rootScope.hideDeploymentRequest = false;
        $scope.isFilterApplied = false;
        $rootScope.$emit('closeDeploymentGroupFilter',0);
    };

 });

});