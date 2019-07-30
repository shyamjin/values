require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var synchronizationServiceControllerApp = angular.module('synchronizationServiceControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

synchronizationServiceControllerApp.controller('synchronizationServiceController', function ($scope, $stateParams, CreateNewSync, $window, $state, $timeout, $rootScope, TestMachine, ApprovalStatusAll, TagsAll) {
    $scope.shell_type = '';
    $scope.time_after = null;
    $scope.reload_command = '';
    $scope.incremental_push_ind = false;
    $scope.incremental_pull_ind = false;
    $scope.syncData = {
        full_sync_flag : false,
        external_artifacts :true
    };
    $scope.shell_types = [
        "/bin/bash -c",
        "/bin/ksh -c",
        "/bin/sh -c",
        "/bin/csh -c"
    ];
    $scope.reload_commands = [
        ". ~/.profile",
        ". ~/.bash_profile",
        ". ~/.bashrc"
    ];
    $scope.showPullStep = false;
    $scope.addPullStep = false;
    $scope.trigger_ind_value = false;
    $scope.isDisable = false;

    $scope.sync_types = [
        "Pull",
        "Push"
    ];

    $scope.pull_types = [
        "URL",
        "File"
    ];

    $scope.incrementalPushIndicators = [
        true,
        false
    ];

    $scope.authtypespull = {
        selected : ""
    };

    $scope.authtypespush = {
         selected : ""
    };

    $scope.synctypes = {
        selected : ""
    };

    $scope.pulltype = {
        selected : ""
    };

    $scope.notification_types = [
        "always",
        "only if fails"
    ];

    $scope.auth_types_pull_url = {
        type : "Telnet"
    };

    $scope.auth_types_pull_file = [
        "SSH" , "Telnet"
    ];

    $scope.auth_types_push = [
        "SSH" , "Telnet"
    ];

    $scope.step = {
        type : ""
    };

    $scope.filtersToApply = {
        type : null,
        approval_status : 'Any',
        tags : [],
        time_after : null
    };

    ApprovalStatusAll.get({
    },
    function(successResponse)
    {
        $scope.approvalStatus = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    TagsAll.get({
    },
    function(successResponse)
    {
        $scope.allTags = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    /*$scope.showAddStatus = function()
    {
        if(document.getElementById("add_status").style.display === "none" || document.getElementById("add_status").style.display === "")
        {
            $('#add_status').slideDown();
        }
        else
        {
           $('#add_status').slideUp();
        }
    };

    $scope.closeAddStatus = function()
    {
         $('#add_status').slideUp();
    };*/

    $scope.selectApprovalStatus = function(status)
    {
        var status_flag = 0;
        var ind = 0;
        if($scope.filtersToApply.approval_status.length>0)
        {
            for(var c=0;  c<$scope.filtersToApply.approval_status.length; c++)
            {
                if(status === $scope.filtersToApply.approval_status[c])
                {
                    status_flag++;
                    ind = c;
                }
            }

            if(status_flag===0)
            {
                $scope.filtersToApply.approval_status.push(status);
            }
            else
            {
                $scope.filtersToApply.approval_status.splice(ind, 1);
            }
        }
        else
        {
            $scope.filtersToApply.approval_status = [];
            $scope.filtersToApply.approval_status.push(status);
        }
    };

    $scope.showAddTag = function()
    {
        if(document.getElementById("add_tag").style.display === "none" || document.getElementById("add_tag").style.display === "")
        {
            $('#add_tag').slideDown();
        }
        else
        {
           $('#add_tag').slideUp();
        }
    };

    $scope.isStatusSelected = function(status)
    {
        var statusFlag = 0;
        for(var j=0; j<$scope.filtersToApply.approval_status.length; j++)
        {
            if(status === $scope.filtersToApply.approval_status[j])
            {
                statusFlag++;
            }
        }
        if(statusFlag>0)
        {
            return true;
        }
        else
        {
            return false;
        }
    };

    $scope.closeAddTag = function()
    {
         $('#add_tag').slideUp();
    };

    $scope.selectTag = function(tag)
    {
        var tag_flag = 0;
        var tag_ind = 0;
        if($scope.filtersToApply.tags.length>0)
        {
            for(var d=0; d<$scope.filtersToApply.tags.length; d++)
            {
                if(tag === $scope.filtersToApply.tags[d])
                {
                    tag_flag++;
                    tag_ind = d;
                }
            }

            if(tag_flag===0)
            {
                $scope.filtersToApply.tags.push(tag);
            }
            else
            {
                $scope.filtersToApply.tags.splice(tag_ind, 1);
            }
        }
        else
        {
            $scope.filtersToApply.tags = [];
            $scope.filtersToApply.tags.push(tag);
        }
    };

    $scope.removeTag = function(tag)
    {
        var tag_flag = 0;
        var tag_ind = 0;
        if($scope.filtersToApply.tags.length>0)
        {
            for(var d=0; d<$scope.filtersToApply.tags.length; d++)
            {
                if(tag === $scope.filtersToApply.tags[d])
                {
                    tag_flag++;
                    tag_ind = d;
                }
            }

            if(tag_flag===0)
            {
                $scope.filtersToApply.tags.push(tag);
            }
            else
            {
                $scope.filtersToApply.tags.splice(tag_ind, 1);
            }
        }
        else
        {
            $scope.filtersToApply.tags = [];
            $scope.filtersToApply.tags.push(tag);
        }
    };

    $scope.isTagSelected = function(tag)
    {
        var tagFlag = 0;
        for(var j=0; j<$scope.filtersToApply.tags.length; j++)
        {
            if(tag === $scope.filtersToApply.tags[j])
            {
                tagFlag++;
            }
        }
        if(tagFlag>0)
        {
            return true;
        }
        else
        {
            return false;
        }
    };

    $scope.machine_port = 22;
    var stepLength = 1;
    $scope.steps_in_pull = [];
    $scope.steps_in_push = [];

    $scope.discardSyncChanges = function()
    {
        $state.go('manageSynchronization');
    };

    $scope.onSyncSelected = function () {
        $scope.steps_in_pull.length = 0;
        $scope.steps_in_push.length = 0;
    };

    $scope.onPullTypeSelected = function () {
        $scope.addPullStep = true;
        $scope.steps_in_pull.length = 0;
        $scope.steps_in_push.length = 0;
    };

    $scope.setTrigger = function()
    {
        if($scope.trigger_ind_value===true)
        {
            $scope.trigger_ind_value = false;
        }
        else
        {
            $scope.trigger_ind_value = true;
        }
    };

    $scope.setDefaultPortInPull = function(step_type, index)
    {
        if($scope.pulltype.selected==='File')
        {
            if(step_type==='SSH')
            {
                $scope.steps_in_pull[index].port = 22;
            }
            else
            {
                delete $scope.steps_in_pull[index].port;
            }
        }
    };

    $scope.isEnable = function(index)
    {
        if($scope.steps_in_push[index].type==='SSH')
        {
            return false;
        }
        else
        {
            return true;
        }
    };

    $scope.setDefaultPortInPush = function(step_type, index)
    {
        if(step_type==='SSH')
        {
            $scope.steps_in_push[index].port = 22;
            return false;
        }
        else
        {
            delete $scope.steps_in_push[index].port;
            return true;
        }
    };

    $scope.addNewStep = function() {
    var newItemNo = $scope.steps_in_push.length+1;

    if($scope.synctypes.selected==='Push')
    {
         $scope.steps_in_push.push({ order : newItemNo});
    }
    else
    {
        if($scope.pulltype.selected==='URL')
        {
            $scope.steps_in_pull = [{type : 'telnet', order : 1}];
            $scope.addPullStep = false;
            $scope.showPullStep = true;
        }
        else
        {
            $scope.steps_in_pull.push({ order : newItemNo});
            $scope.addPullStep = true;
            $scope.showPullStep = true;
        }
    }
  };

    $scope.removeStep = function()
    {
        var lastItem;
        if($scope.synctypes.selected==='Push')
        {
            lastItem = $scope.steps_in_push.length-1;
            $scope.steps_in_push.splice(lastItem);
        }
        else
        {
            if($scope.pulltype.selected==='URL')
            {
                $scope.steps_in_pull.splice(0);
                $scope.addPullStep = true;
                $scope.showPullStep = false;
            }
            else
            {
                lastItem = $scope.steps_in_pull.length-1;
                $scope.steps_in_pull.splice(lastItem);
            }
        }
  };

    $scope.moveStepUp = function(index)
    {
        var elementToMoveUp;
        var elementToMoveDown;
        if($scope.synctypes.selected==='Push')
        {
            elementToMoveUp = $scope.steps_in_push[index];
            elementToMoveDown = $scope.steps_in_push[index-1];
            if(elementToMoveDown!=null)
            {
                $scope.steps_in_push[index-1] = elementToMoveUp;
                $scope.steps_in_push[index] = elementToMoveDown;
            }
        }
        else if($scope.synctypes.selected==='Pull' && $scope.pulltype.selected==='File')
        {
            elementToMoveUp = $scope.steps_in_pull[index];
            elementToMoveDown = $scope.steps_in_pull[index-1];
            if(elementToMoveDown!=null)
            {
                $scope.steps_in_pull[index-1] = elementToMoveUp;
                $scope.steps_in_pull[index] = elementToMoveDown;
            }
        }
    };

    $scope.moveStepDown = function(index)
    {
        var elementToMoveUp;
        var elementToMoveDown;
        if($scope.synctypes.selected==='Push')
        {
            elementToMoveDown = $scope.steps_in_push[index];
            elementToMoveUp = $scope.steps_in_push[index+1];

            if(elementToMoveUp!=null)
            {
                $scope.steps_in_push[index] = elementToMoveUp;
                $scope.steps_in_push[index+1] = elementToMoveDown;
            }
        }
        else if($scope.synctypes.selected==='Pull' && $scope.pulltype.selected==='File')
        {
            elementToMoveDown = $scope.steps_in_pull[index];
            elementToMoveUp = $scope.steps_in_pull[index+1];

            if(elementToMoveUp!=null)
            {
                $scope.steps_in_pull[index] = elementToMoveUp;
                $scope.steps_in_push[index+1] = elementToMoveDown;
            }
        }
    };

    $scope.testConnection = function(form)
    {
        var testMachineData = {};
        if(($scope.createNewSyncForm.machine_host.$viewValue === '' || $scope.createNewSyncForm.machine_host.$viewValue === null || $scope.createNewSyncForm.machine_host.$viewValue === undefined) ||
            ($scope.createNewSyncForm.machine_username.$viewValue === '' || $scope.createNewSyncForm.machine_username.$viewValue === null || $scope.createNewSyncForm.machine_username.$viewValue === undefined) ||
            ($scope.createNewSyncForm.machine_ip.$viewValue === '' || $scope.createNewSyncForm.machine_ip.$viewValue === null || $scope.createNewSyncForm.machine_ip.$viewValue === undefined) ||
            ($scope.createNewSyncForm.authenticate_using.$viewValue === '' || $scope.createNewSyncForm.authenticate_using.$viewValue === null || $scope.createNewSyncForm.authenticate_using.$viewValue === undefined))
        {
            $rootScope.handleResponse('Mandatory fields required to test connection are missing');
            return false;
        }
        else
        {
            if(($scope.createNewSyncForm.authenticate_using.$viewValue === 'password') && ($scope.createNewSyncForm.machine_password.$viewValue === '' || $scope.createNewSyncForm.machine_password.$viewValue === null || $scope.createNewSyncForm.machine_password.$viewValue === undefined))
            {
                $rootScope.handleResponse('Please enter the machine password');
            }
            else
            {
                testMachineData.host = $scope.createNewSyncForm.machine_host.$viewValue;
                testMachineData.ip = $scope.createNewSyncForm.machine_ip.$viewValue;
                testMachineData.username = $scope.createNewSyncForm.machine_username.$viewValue;
                testMachineData.port = parseInt($scope.createNewSyncForm.machine_port.$viewValue,10);
                testMachineData.shell_type = $scope.createNewSyncForm.shell_type.$viewValue;
                testMachineData.reload_command = $scope.createNewSyncForm.reload_command.$viewValue;
                testMachineData.auth_type = $scope.createNewSyncForm.authenticate_using.$viewValue;
                if(testMachineData.auth_type === 'ssh' && (testMachineData.machine_password === null || testMachineData.machine_password === '' || testMachineData.machine_password === undefined))
                {
                    testMachineData.password = '12345';
                }
                else
                {
                    testMachineData.password = $scope.createNewSyncForm.machine_password.$viewValue;
                }

                if(testMachineData.shell_type === ' ' || testMachineData.shell_type === undefined || testMachineData.shell_type === null)
                {
                    testMachineData.shell_type = '';
                }
                if(testMachineData.reload_command === 'not required' || testMachineData.reload_command === undefined)
                {
                    testMachineData.reload_command = '';
                }
                else
                {
                    testMachineData.reload_command = testMachineData.reload_command;
                }

                testMachineData.account_id = $rootScope.userProfile.userData.account_details._id.$oid;

                if($scope.synctypes.selected === 'Pull')
                {
                    if($scope.steps_in_pull.length>0)
                    {
                        testMachineData.steps_to_auth = $scope.steps_in_pull;
                    }
                }

                if($scope.synctypes.selected === 'Push')
                {
                    if($scope.steps_in_push.length>0)
                    {
                        testMachineData.steps_to_auth = $scope.steps_in_push;
                    }
                }

                $scope.testMachineStatus =  TestMachine.save (testMachineData, function (testMachineSuccessResponse){
                    $scope.machineTestResult = testMachineSuccessResponse;
                    $rootScope.handleResponse(testMachineSuccessResponse);
                },
                function(testMachineErrorResponse)
                {
                    $scope.machineTestResult = testMachineErrorResponse.data;
                    $rootScope.handleResponse(testMachineErrorResponse);
                });
            }
        }
    };

    $scope.createNewSync = function(form)
    {
        var ViewSyncRequestInJson = {};
        var jsonData = {};
        jsonData = {
            steps_to_auth : ""
        };

        var finalJsonData = {};
        finalJsonData = {
            filters_to_apply : {
                type : "",
                approval_status : [],
                tags : [],
                time_after : null
            },
            target_dpm_detail : {
                dpm_host : "",
                dpm_port : "",
                dpm_token : "",
                dpm_username : "",
                dpm_password : ""
            }
        };
        $scope.sync_type = $scope.createNewSyncForm.sync_type.$viewValue;

        if($scope.sync_type==='Push')
        {
            $scope.trigger_ind = ""+$scope.createNewSyncForm.trigger_ind.$viewValue+"";
            $scope.dpm_push_folder_location = $scope.createNewSyncForm.dpm_push_folder_location.$viewValue;
          /*  if($scope.createNewSyncForm.incremental_push_ind.$viewValue)
            {
                $scope.incremental_push_ind = $scope.createNewSyncForm.incremental_push_ind.$viewValue;
            }
            else
            {
                $scope.incremental_push_ind = false;
            }*/
        }

        finalJsonData.sync_type = $scope.sync_type;
        /*if($scope.sync_type==='Pull')
        {
            finalJsonData.full_sync_flag = $scope.full_sync;
            finalJsonData.notification_type = $scope.notification_type;
        }*/

        //        Validation starts here...
        for(var i=0; i<$scope.steps_in_push.length;i++)
        {
            if ($scope.steps_in_push[i].type === undefined)
            {
                $('html, body').animate({
                    scrollTop: $("#steps_to_auth_"+[i]).offset().top - 50
                }, 1000);
                $rootScope.handleResponse('Please select auth type!');
                return false;
            }

            if ($scope.steps_in_push[i].type === 'SSH')
            {
                if($scope.steps_in_push[i].port==="" || $scope.steps_in_push[i].port===undefined)
                {
                    $('html, body').animate({
                        scrollTop: $("#steps_to_auth_"+[i]).offset().top - 50
                    }, 1000);
                    $rootScope.handleResponse('Please enter port for gateway!');
                    return false;
                }
                else
                {
                    $scope.steps_in_push[i].port = ($scope.steps_in_push[i].port).toString();
                }

                if($scope.steps_in_push[i].host==="" || $scope.steps_in_push[i].host===undefined)
                {
                    $('html, body').animate({
                        scrollTop: $("#steps_to_auth_"+[i]).offset().top - 50
                    }, 1000);
                    $rootScope.handleResponse('Please enter host for gateway!');
                    return false;
                }

                if($scope.steps_in_push[i].username==="" || $scope.steps_in_push[i].username===undefined)
                {
                    $('html, body').animate({
                        scrollTop: $("#steps_to_auth_"+[i]).offset().top - 50
                    }, 1000);
                    $rootScope.handleResponse('Please enter user for gateway!');
                    return false;
                }

                if($scope.steps_in_push[i].password==="" || $scope.steps_in_push[i].password===undefined)
                {
                    $('html, body').animate({
                        scrollTop: $("#steps_to_auth_"+[i]).offset().top - 50
                    }, 1000);
                    $rootScope.handleResponse('Please enter password for gateway!');
                    return false;
                }
            }
        }

        if($scope.sync_type==='Pull' && $scope.pulltype.selected==='URL')
        {
            $scope.dpm_host_pull = $scope.createNewSyncForm.dpm_host_pull.$viewValue;
            $scope.dpm_port_pull = $scope.createNewSyncForm.dpm_port_pull.$viewValue;
            $scope.dpm_username_pull = $scope.createNewSyncForm.dpm_username_pull.$viewValue;
            $scope.dpm_password_pull = $scope.createNewSyncForm.dpm_password_pull.$viewValue;
            $scope.dpm_unique_token_pull = $scope.createNewSyncForm.dpm_unique_token_pull.$viewValue;

            if($scope.dpm_host_pull===undefined)
            {
                 $rootScope.handleResponse("Please enter the DPM host!");
                 return false;

            }

            if($scope.dpm_port_pull===undefined)
            {
                 $rootScope.handleResponse("Please enter the DPM port!");
                 return false;

            }

            if($scope.dpm_unique_token_pull===undefined)
            {
                 $rootScope.handleResponse("Please enter the DPM Unique token!");
                 return false;

            }

            if($scope.dpm_username_pull===undefined)
            {
                 $rootScope.handleResponse("Please enter the DPM username!");
                 return false;

            }
            if($scope.dpm_password_pull===undefined)
            {
                 $rootScope.handleResponse("Please enter the DPM password!");
                 return false;

            }
        }

        if(($scope.sync_type==='Pull' && $scope.pulltype.selected==='File') || $scope.sync_type==='Push')
        {
            if(($scope.createNewSyncForm.machine_host.$viewValue === '' || $scope.createNewSyncForm.machine_host.$viewValue === null || $scope.createNewSyncForm.machine_host.$viewValue === undefined) ||
                ($scope.createNewSyncForm.machine_username.$viewValue === '' || $scope.createNewSyncForm.machine_username.$viewValue === null || $scope.createNewSyncForm.machine_username.$viewValue === undefined) ||
                ($scope.createNewSyncForm.machine_ip.$viewValue === '' || $scope.createNewSyncForm.machine_ip.$viewValue === null || $scope.createNewSyncForm.machine_ip.$viewValue === undefined) ||
                ($scope.createNewSyncForm.authenticate_using.$viewValue === '' || $scope.createNewSyncForm.authenticate_using.$viewValue === null || $scope.createNewSyncForm.authenticate_using.$viewValue === undefined))
            {
                $rootScope.handleResponse('Mandatory fields required to test machine connection are missing');
                return false;
            }
            else
            {
                if(($scope.createNewSyncForm.authenticate_using.$viewValue === 'password') && ($scope.createNewSyncForm.machine_password.$viewValue === '' || $scope.createNewSyncForm.machine_password.$viewValue === null || $scope.createNewSyncForm.machine_password.$viewValue === undefined))
                {
                    $rootScope.handleResponse('Please enter the machine password');
                }
                else
                {
                    $scope.machine_host = $scope.createNewSyncForm.machine_host.$viewValue;
                    $scope.machine_port = parseInt($scope.createNewSyncForm.machine_port.$viewValue,10);
                    $scope.machine_ip = $scope.createNewSyncForm.machine_ip.$viewValue;
                    $scope.machine_username = $scope.createNewSyncForm.machine_username.$viewValue;
                    $scope.auth_type = $scope.createNewSyncForm.authenticate_using.$viewValue;
                    if($scope.auth_type === 'ssh' && ($scope.machine_password === null || $scope.machine_password === '' || $scope.machine_password === undefined))
                    {
                        $scope.machine_password = '12345';
                    }
                    else
                    {
                        $scope.machine_password = $scope.createNewSyncForm.machine_password.$viewValue;
                    }
                }
            }

            if($scope.sync_type==='Pull')
            {
                $scope.distribution_list_pull = $scope.createNewSyncForm.distribution_list_pull.$viewValue;
            }
            else
            {
                $scope.distribution_list_push = $scope.createNewSyncForm.distribution_list_push.$viewValue;
            }

            if($scope.sync_type==='Pull' && $scope.pulltype.selected==='File')
            {
                $scope.remote_source_location_pull = $scope.createNewSyncForm.remote_source_location_pull.$viewValue;
                if($scope.remote_source_location_pull === '' || $scope.remote_source_location_pull === null || $scope.remote_source_location_pull === undefined)
                {
                    $rootScope.handleResponse('Please enter the remote source location');
                    return false;
                }
            }

            if($scope.machine_host===undefined)
            {
                 $rootScope.handleResponse("Please enter the target machine host name!");
                 return false;
            }
            if($scope.machine_port===undefined || $scope.machine_port===null)
            {
                 $rootScope.handleResponse("Please enter the target machine port!");
                 return false;
            }
            if (!(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test($scope.machine_ip)))
            {
                $rootScope.handleResponse("Please enter valid IP Address!!");
                return false;

            }

            if($scope.machine_username===undefined)
            {
                 $rootScope.handleResponse("Please enter the target machine user name!");
                 return false;
            }

            if($scope.distribution_list_pull)
            {
                var atpos = $scope.distribution_list_pull.indexOf("@");
                var dotpos = $scope.distribution_list_pull.lastIndexOf(".");
                if (atpos<1 || dotpos<atpos+2 || dotpos+2>=$scope.distribution_list_pull.length) {
                    $rootScope.handleResponse('Please enter valid email address in distribution list!');
                    return false;
                }
            }
        }
        if($scope.distribution_list_push)
        {
            var atpos_1 = $scope.distribution_list_push.indexOf("@");
            var dotpos_1 = $scope.distribution_list_push.lastIndexOf(".");
            if (atpos_1<1 || dotpos_1<atpos_1+2 || dotpos_1+2>=$scope.distribution_list_push.length) {
                $rootScope.handleResponse('Please enter valid email address in distribution list!');
                return false;
            }
        }

        if($scope.sync_type==='Push' && $scope.trigger_ind_value===true)
        {
            $scope.dpm_host_push = $scope.createNewSyncForm.dpm_host_push.$viewValue;
            $scope.dpm_port_push = $scope.createNewSyncForm.dpm_port_push.$viewValue;
            $scope.dpm_username_push = $scope.createNewSyncForm.dpm_username_push.$viewValue;
            $scope.dpm_password_push = $scope.createNewSyncForm.dpm_password_push.$viewValue;
            $scope.dpm_unique_token_push = $scope.createNewSyncForm.dpm_unique_token_push.$viewValue;

            if($scope.dpm_host_push===undefined)
            {
                 $rootScope.handleResponse("Please enter the DPM host!");
                 return false;

            }

            if($scope.dpm_port_push===undefined)
            {
                 $rootScope.handleResponse("Please enter the DPM port!");
                 return false;

            }

            if($scope.dpm_unique_token_push===undefined)
            {
                 $rootScope.handleResponse("Please enter the DPM Unique token!");
                 return false;

            }

            if($scope.dpm_username_push===undefined)
            {
                 $rootScope.handleResponse("Please enter the DPM username!");
                 return false;

            }
            if($scope.dpm_password_push===undefined)
            {
                 $rootScope.handleResponse("Please enter the DPM password!");
                 return false;

            }
        }
        if($scope.sync_type==='Pull')
        {
            if($scope.steps_in_pull.length>=1)
            {
                for(var j=0; j<$scope.steps_in_pull.length;j++)
                {
                    if ($scope.steps_in_pull[i].type === 'SSH')
                    {
                        $scope.steps_in_pull[i].port = ($scope.steps_in_pull[i].port).toString();
                    }
                }
                finalJsonData.steps_to_auth = $scope.steps_in_pull;
            }
            else
            {
                delete finalJsonData.steps_to_auth;
            }
            finalJsonData.full_sync_flag = $scope.full_sync;
            finalJsonData.notification_type = $scope.createNewSyncForm.notification_type.$viewValue;

            /*if($scope.full_sync === 'true')
            {
                if($scope.createNewSyncForm.notification_type.$viewValue === undefined ||$scope.createNewSyncForm.notification_type.$viewValue === null || $scope.createNewSyncForm.notification_type.$viewValue ==='')
                {
                    $rootScope.handleResponse("Please select valid notification type");
                    return false;
                }
                finalJsonData.notification_type = $scope.createNewSyncForm.notification_type.$viewValue;
            }*/

            finalJsonData.pull_type = $scope.pulltype.selected;

            if(finalJsonData.pull_type==='File')
            {
                finalJsonData.remote_source_location = $scope.createNewSyncForm.remote_source_location_pull.$viewValue;
                finalJsonData.machine_name = $scope.machine_name;
                finalJsonData.host = $scope.machine_host;
                finalJsonData.port = $scope.machine_port;
                finalJsonData.ip = $scope.machine_ip;
                finalJsonData.username = $scope.machine_username;
                finalJsonData.auth_type = $scope.auth_type;
                finalJsonData.password = $scope.machine_password;
                finalJsonData.shell_type = $scope.createNewSyncForm.shell_type.$viewValue;
                finalJsonData.reload_command = $scope.createNewSyncForm.reload_command.$viewValue;

                if(finalJsonData.shell_type === '' || finalJsonData.shell_type === undefined || finalJsonData.shell_type === null)
                {
                    finalJsonData.shell_type = '';
                }
                if(finalJsonData.reload_command === 'not required' || finalJsonData.reload_command === undefined)
                {
                    finalJsonData.reload_command = '';
                }
                else
                {
                    finalJsonData.reload_command = finalJsonData.reload_command;
                }

                delete finalJsonData.target_dpm_detail;
                finalJsonData.target_dpm_detail = {};
            }
            else
            {
                finalJsonData.target_dpm_detail.dpm_host = $scope.dpm_host_pull;
                finalJsonData.target_dpm_detail.dpm_port = $scope.dpm_port_pull;
                finalJsonData.target_dpm_detail.dpm_token = $scope.dpm_unique_token_pull;
                finalJsonData.target_dpm_detail.dpm_username = $scope.dpm_username_pull;
                finalJsonData.target_dpm_detail.dpm_password = $scope.dpm_password_pull;
                if($scope.createNewSyncForm.incremental_pull_ind.$viewValue)
                {
                    finalJsonData.incremental_pull_ind = $scope.createNewSyncForm.incremental_pull_ind.$viewValue;
                }
                else
                {
                    finalJsonData.incremental_pull_ind = false;
                }

                if($scope.filtersToApply.time_after !== null || $scope.filtersToApply.time_after !== undefined)
                {
                    finalJsonData.filters_to_apply.time_after = $scope.filtersToApply.time_after.toISOString();
                }
                else
                {
                    delete finalJsonData.time_after
                }
            }
            if($scope.createNewSyncForm.distribution_list_pull.$viewValue === null || $scope.createNewSyncForm.distribution_list_pull.$viewValue === undefined || $scope.createNewSyncForm.distribution_list_pull.$viewValue === '')
            {
                $rootScope.handleResponse("Please enter the valid email id in distribution list");
                return false;
            }
            else
            {
                var support = $scope.createNewSyncForm.distribution_list_pull.$viewValue;
                var atposition = support.indexOf("@");
                var dotposition = support.lastIndexOf(".");
                if (atposition<1 || dotposition<atposition+2 || dotposition+2>=support.length) {
                    $rootScope.handleResponse('Please enter valid email address!');
                    return false;
                }
                else
                {
                    finalJsonData.distribution_list = $scope.createNewSyncForm.distribution_list_pull.$viewValue;
                }
            }
        }
        else
        {
            finalJsonData.steps_to_auth = $scope.steps_in_push;
            finalJsonData.machine_name = $scope.machine_name;
            finalJsonData.host = $scope.machine_host;
            finalJsonData.port = $scope.machine_port;
            finalJsonData.ip = $scope.machine_ip;
            finalJsonData.username = $scope.machine_username;
            finalJsonData.auth_type = $scope.auth_type;
            finalJsonData.password = $scope.machine_password;
            finalJsonData.shell_type = $scope.createNewSyncForm.shell_type.$viewValue;
            finalJsonData.reload_command = $scope.createNewSyncForm.reload_command.$viewValue;
            finalJsonData.external_artifacts = $scope.syncData.external_artifacts;
            if($scope.createNewSyncForm.incremental_push_ind.$viewValue)
            {
                finalJsonData.incremental_push_ind = $scope.createNewSyncForm.incremental_push_ind.$viewValue;
            }
            else
            {
                finalJsonData.incremental_push_ind = false;
            }

            if(finalJsonData.shell_type === ' ' || finalJsonData.shell_type === undefined || finalJsonData.shell_type === null)
            {
                finalJsonData.shell_type = '';
            }
            if(finalJsonData.reload_command === 'not required' || finalJsonData.reload_command === undefined)
            {
                finalJsonData.reload_command = '';
            }
            else
            {
                finalJsonData.reload_command = finalJsonData.reload_command;
            }

            finalJsonData.trigger_ind = $scope.trigger_ind_value;

            if($scope.trigger_ind_value===true)
            {
                finalJsonData.target_dpm_detail.dpm_host = jsonData.dpm_host;
                finalJsonData.target_dpm_detail.dpm_username = jsonData.dpm_username;
                finalJsonData.target_dpm_detail.dpm_token = jsonData.dpm_token;
                finalJsonData.target_dpm_detail.dpm_password = jsonData.dpm_password;
                finalJsonData.target_dpm_detail.dpm_port = jsonData.dpm_port;
            }
            else
            {
                delete finalJsonData.target_dpm_detail;
                finalJsonData.target_dpm_detail = {};
            }

            finalJsonData.folder_location = $scope.dpm_push_folder_location;
            if($scope.createNewSyncForm.distribution_list_push.$viewValue === null || $scope.createNewSyncForm.distribution_list_push.$viewValue === undefined || $scope.createNewSyncForm.distribution_list_push.$viewValue === '')
            {
                $rootScope.handleResponse("Please enter the valid email id in distribution list");
                return false;
            }
            else
            {
                finalJsonData.distribution_list = $scope.createNewSyncForm.distribution_list_push.$viewValue;
            }
            if($scope.filtersToApply.time_after !== null && $scope.filtersToApply.time_after !== undefined)
            {
                finalJsonData.filters_to_apply.time_after = $scope.filtersToApply.time_after.toISOString();
            }
            else
            {
                delete finalJsonData.time_after
            }
        }

        if($scope.filtersToApply.type !== null && $scope.filtersToApply.type!== undefined && $scope.filtersToApply.type!== "")
        {
            finalJsonData.filters_to_apply.type = $scope.filtersToApply.type;
        }
        else
        {
            finalJsonData.filters_to_apply.type = 'all';
        }

        if(finalJsonData.filters_to_apply.type === 'du' || finalJsonData.filters_to_apply.type === 'all')
        {
            if($scope.filtersToApply.approval_status.length>0)
            {
                finalJsonData.filters_to_apply.approval_status = $scope.filtersToApply.approval_status;
            }
            else
            {
                finalJsonData.filters_to_apply.approval_status.push('any');
            }
        }
        else
        {
            delete finalJsonData.filters_to_apply.approval_status;
        }

        if($scope.filtersToApply.tags.length>0)
        {
            finalJsonData.filters_to_apply.tags = $scope.filtersToApply.tags;
        }
        else
        {
            finalJsonData.filters_to_apply.tags.push('any');
        }

        ViewSyncRequestInJson = finalJsonData;

        $scope.dataSync = CreateNewSync.save(ViewSyncRequestInJson,function(successResponse){
            $rootScope.handleResponse(successResponse);
            $state.go('manageSynchronization');
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

 });
 });