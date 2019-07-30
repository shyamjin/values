require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var distributionServiceControllerApp = angular.module('distributionServiceControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

distributionServiceControllerApp.controller('DistributionServiceController', function ($scope, $rootScope, $stateParams, $state, $timeout, $location, GetConfigSchedule, DeleteDistributionService, ResendDistributionService, DistributionService, UpdateConfigDistribution, AddCloneDistribution, Machine, UpdateCloneDistribution, RunAllDistributionService, GetAllMachine) {
    $scope.enableFlag='false';
    $scope.selectedData=[];
    $scope.userSelected=false;
    $scope.isSelectedFlag=false;
    $rootScope.preLoader = false;
    $scope.distributionSelected=false;
    $scope.distributionForm=[];
    $scope.currentTab = 'DistributionMcList';
    $scope.showCurrentTab = function(tab)
    {
        $scope.currentTab = tab;
        if($scope.currentTab !='DistributionMcList')
        {
           $scope.userSelected=false;
           $scope.isSelectedFlag=false;
        }
    };

    $scope.getCurrentTab = function(tab)
    {
        if($scope.currentTab === tab)
        {
            return 'vp-tabs__tab vp-tabs__tab--active pointer pr--sm pl--sm left';
        }
        else
        {
            return 'vp-tabs__tab pointer pr--sm pl--sm left';
        }
    };


    $scope.exist=function()
    {
        var flag=false;

         if($scope.enableFlag === 'true')
         {
            flag=true;
            return flag;
         }
         else
         {
             flag=false;
          }

         return flag;
    };

    $scope.toggleSelection=function()
    {
        if($scope.enableFlag==='true')
        {
            $scope.configSchedule.data[0].enable='false';
        }
        else
        {
            $scope.configSchedule.data[0].enable='true';
        }

    };


        $scope.machine = [];

        $scope.configSchedule = GetConfigSchedule.get({

        },
        function(configScheduleSuccessResponse)
        {
            $scope.enableFlag=configScheduleSuccessResponse.data[0].enable+"";
            $scope.requesttype.selected=configScheduleSuccessResponse.data[0].type;
        },
        function(configScheduleErrorResponse)
        {
            $rootScope.handleResponse(configScheduleErrorResponse);
        });
        $scope.timeValue = {
            default_value : '00:00:AM'
        };

        $scope.time = {
            hh : '',
            mm : '',
            ts : ''
        };

        $scope.requesttype = {
            selected : ''
        };
        $scope.requestType = [
            "interval",
            "scheduled"
        ];

        $scope.getTime = function()
        {
            $scope.timeValue.default_value = $scope.time.hh+":"+$scope.time.mm+":"+$scope.time.ts;
        };

        $scope.updateConfigDistribution = function()
        {
            $scope.distributionsettingsadd_errors=[];
            var jsonData = {};
            var a = $("form").serializeArray();
            $.each(a, function () {
                        if (jsonData[this.name]) {
                            if (!jsonData[this.name].push) {
                                jsonData[this.name] = [jsonData[this.name]];
                            }
                            jsonData[this.name].push(this.value || '');
                        } else {
                            jsonData[this.name] = this.value || '';
                        }
                    });
            var distributionData = {};
            distributionData._id = {
                oid : ''
            };
            distributionData._id.oid = $scope.configSchedule.data[0]._id.$oid;
            distributionData.enable = ""+$scope.configSchedule.data[0].enable+"";
            distributionData.type = $scope.requesttype.selected;

            $scope.distributionsettingsadd_errors.requesttype='';
            if(distributionData.type===undefined || distributionData.type==='')
            {
                $scope.distributionsettingsadd_errors.requesttype="Please select request type";
                return false;
            }

            if(distributionData.type==='scheduled')
            {
                distributionData.hrs = parseFloat(jsonData.hrs);
                distributionData.min = parseFloat(jsonData.min);
                distributionData.intervalGiven = parseFloat($scope.configSchedule.data[0].intervalGiven);

                $scope.distributionsettingsadd_errors.hrs='';
                if (distributionData.hrs<0 || distributionData.hrs>23) {
                    $scope.distributionsettingsadd_errors.hrs='Please enter valid hours!';
                    return false;
                }

                 $scope.distributionsettingsadd_errors.min='';
                if (distributionData.min<0 || distributionData.min>59) {
                    $scope.distributionsettingsadd_errors.min='Please enter valid minutes!';
                    return false;
                }
            }
            else
            {
                distributionData.intervalGiven = parseFloat(jsonData.intervalGiven);
                 $scope.distributionsettingsadd_errors.intervalGiven='';
                if (distributionData.intervalGiven<0 || distributionData.intervalGiven>23) {
                    $scope.distributionsettingsadd_errors.intervalGiven='Please enter valid interval!';
                    return false;
                }

                distributionData.hrs = parseFloat($scope.configSchedule.data[0].hrs);
                distributionData.min = parseFloat($scope.configSchedule.data[0].min);

            }
            $scope.updateDistributionStatus = UpdateConfigDistribution.update(distributionData, function(updateDistributionSuccessResponse){
                $state.transitionTo($state.current, $stateParams, {
                     reload: true, inherit: false, notify: true
                });
                $rootScope.handleResponse(updateDistributionSuccessResponse);
                },
            function(updateDistributionErrorResponse)
            {
                $rootScope.handleResponse(updateDistributionErrorResponse);
                return false;
            });
        };

        $scope.getStatusClass = function(request)
        {
            if($scope.isSelectedFlag===true)
            {
                if(request.status==='on')
                {
                    return "vp-machinessearch__item vp-machinessearch__item--act selectedObj";
                }
                else
                {
                    return "vp-machinessearch__item vp-machinessearch__item--inact selectedObj";
                }
            }
            else
            {
                 if(request.status==='on')
                 {
                    return "vp-machinessearch__item vp-machinessearch__item--act";
                 }
                 else
                 {
                    return "vp-machinessearch__item vp-machinessearch__item--inact";
                 }
            }
        };

        $scope.getUserUlClass = function()
        {
            if($scope.userSelected === true)
            {
                if($scope.currentTab!='DistributionMcList')
                {
                    $scope.userSelected = false;
                }
                return "vp-distributionform__selecteddistributionform__fieldslist text--cs03 pr--lg";
            }
            else
            {
                return "vp-distributionform__selecteddistributionform__fieldslist text--cs03 pr--lg hidden";
            }
        };

        $scope.getUserFormClass = function()
        {
            if($scope.userSelected === true)
            {
                if($scope.currentTab!='DistributionMcList')
                {
                    $scope.userSelected = false;
                }
                return "vp-distributionform__selecteddistributionform--active  vp-distributionform vp-control max";
            }
            else
            {
                return "vp-selecteddistributionform vp-distributionform vp-control max";
            }
        };


        $scope.isMachineSelected = function(requestObj)
        {
            $scope.userSelected = true;
            $scope.isSelectedFlag = true;
            $scope.editEnableFlag = true;
            $scope.distributionSelected=true;
            $scope.selectedData.id = requestObj._id.$oid;
            $scope.selectedData.host = requestObj.host;
            $scope.selectedData.machine_id = requestObj.machine_id;
            $scope.selectedData.status = requestObj.status;
            $scope.selectedData.distribution_status = requestObj.distribution_status;
            $scope.selectedData.update_date = requestObj.update_date.$date;

        };

        $scope.addCloneRequestDistribution = function()
        {

            var cloneDistributionData = {};
            var selectedMcDetails = $scope.machine.selected.split("_");
            cloneDistributionData.machine_id = selectedMcDetails[0];
            cloneDistributionData.host = selectedMcDetails[1];
            cloneDistributionData.status = "on";

            $scope.addCloneDistributionStatus = AddCloneDistribution.save(cloneDistributionData, function(addCloneDistributionSuccessResponse){
                $state.go('dashboard');
                $rootScope.handleResponse(addCloneDistributionSuccessResponse);
            },
            function(addCloneDistributionErrorResponse)
            {
                $rootScope.handleResponse(addCloneDistributionErrorResponse);
                return false;
            });
        };

        DistributionService.get({
        },
        function(distributionSuccessResponse)
        {
            $scope.distributionService = distributionSuccessResponse;
        },
        function(distributionErrorResponse)
        {
            $rootScope.handleResponse(distributionErrorResponse);
        });

        $scope.machines = GetAllMachine.get({
        },
        function(machineSuccessResponse)
        {
        },
        function(machineErrorResponse)
        {
            $rootScope.handleResponse(machineErrorResponse);
        });

        $scope.updateCloneRequestDistribution = function(_id, _oldStatus, _machine_id, hostname)
        {
            var request_id = _id;
            var oldStatus = _oldStatus;
            var machine_id = _machine_id;
            var host = hostname;
            var updateCloneDistributionData = {};
            updateCloneDistributionData._id = {
                oid : ''
            };
            updateCloneDistributionData._id.oid = request_id;
            updateCloneDistributionData.machine_id = machine_id;
            updateCloneDistributionData.host = hostname;
            if(oldStatus==='off')
            {
                updateCloneDistributionData.status = "on";
            }
            else
            {
                updateCloneDistributionData.status = "off";
            }

            $scope.updateCloneDistributionStatus = UpdateCloneDistribution.update(updateCloneDistributionData, function(updateCloneDistributionSuccessResponse){
                $scope.selectedData.status=updateCloneDistributionData.status;

                $scope.distributionService = DistributionService.get({

                },
                function(distributionSuccessResponse) {
                    $rootScope.handleResponse(distributionSuccessResponse);
                },
                function(distributionErrorResponse) {
                    $rootScope.handleResponse(distributionErrorResponse);
                });

                $state.transitionTo($state.current, $stateParams, {
                    reload: true, inherit: false, notify: true
                });
                $rootScope.handleResponse(updateCloneDistributionSuccessResponse);
            },
            function(updateCloneDistributionErrorResponse)
            {
                $rootScope.handleResponse(updateCloneDistributionErrorResponse);
                return false;
            });
        };

        $scope.requestResendDistributionData = function(id)
        {
            $rootScope.preLoader = true;
            $scope.requestResendDistribution = ResendDistributionService.get({
                id :   id
            },
            function (DistributionResendSuccessResponse)
            {
                $rootScope.preLoader = false;
                delete $scope.distributionService;
                $rootScope.handleResponse(DistributionResendSuccessResponse);
                $scope.distributionSelected=false;
                DistributionService.get({
                },
                function(distributionSuccessResponse)
                {
                    $scope.distributionService = distributionSuccessResponse;
                },
                function(distributionErrorResponse)
                {
                    $rootScope.handleResponse(distributionErrorResponse);
                });

            },
            function (DistributionResendErrorResponse)
            {
                $rootScope.handleResponse(DistributionResendErrorResponse);
            });
        };

        $scope.requestDeletionData=function(id)
        {
            $scope.requestDeletion = DeleteDistributionService.remove({
                id :   id
            },
            function(DistributionDeleteSuccessResponse)
            {
                $scope.distributionService = DistributionService.get({
                },
                function(distributionSuccessResponse)
                {

                },
                function(distributionErrorResponse) {
                  $rootScope.handleResponse(distributionErrorResponse);
                });
                $state.go('dashboard');
                $rootScope.handleResponse(DistributionDeleteSuccessResponse);
            },
            function(DistributionDeleteErrorResponse)
            {
                $scope.distributionService = DistributionService.get({
                },
                function(distributionSuccessResponse)
                {
                },
                function(distributionErrorResponse) {
                  $rootScope.handleResponse(distributionErrorResponse);
                });
                $state.go('distribution');
                $rootScope.handleResponse(DistributionDeleteErrorResponse);
            });
        };

        $scope.openModal = function()
        {
            $scope.distributionResult = {
                message:''
            };

            $scope.distributionResult = {
                result:''
            };
            $scope.distributionResultPane = false;
            $scope.distributionModal = true;

            $scope.requestDistributionAll = RunAllDistributionService.get({
            },
            function (DistributionRunSuccessResponse)
            {
                $scope.distributionModal = false;
                $scope.distributionResultPane = true;
                $scope.distributionResult.message = DistributionRunSuccessResponse.Message;
                $scope.distributionResult.result = DistributionRunSuccessResponse.result;

                for(var i=0;i<DistributionRunSuccessResponse.data.length;i++)
                {
                    if(DistributionRunSuccessResponse.data[i]._id.$oid===$scope.selectedData.id)
                    {
                        $scope.selectedData.distribution_status=DistributionRunSuccessResponse.data[i].distribution_status;
                    }
                }

                $scope.distributionService = DistributionService.get({
                },
                function(distributionSuccessResponse)
                {
                },
                function(distributionErrorResponse)
                {
                    $rootScope.handleResponse(distributionErrorResponse);
                });

                $rootScope.handleResponse(DistributionRunSuccessResponse);
            },
            function (DistributionRunErrorResponse)
            {
                $scope.distributionModal = false;
                $scope.distributionResultPane = true;

                $scope.distributionResult.message = DistributionRunErrorResponse.data.message;
                $scope.distributionResult.result = DistributionRunErrorResponse.data.result;

                $scope.distributionService = DistributionService.get({
                },
                function(distributionSuccessResponse)
                {
                },
                function(distributionErrorResponse) {
                    $rootScope.handleResponse(distributionErrorResponse);
                });

                $rootScope.handleResponse(DistributionRunErrorResponse);
            });
        };

 });
 });