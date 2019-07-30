require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var editSynchronizationServiceControllerApp = angular.module('editSynchronizationServiceControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

editSynchronizationServiceControllerApp.controller('EditSynchronizationServiceController', function ($scope, $stateParams, ViewSyncRequest, UpdateSyncRequest, $window, $state, $rootScope, TestMachine, SyncOnDemand, ApprovalStatusAll, TagsAll, DeleteSyncRequest) {
        $scope.showPullStep = false;
        $scope.removePullStep = false;
        $scope.addPullStep = true;
        $scope.machineTestResult = '';
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

        $scope.showAddStatus = function()
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
        };

        /*$scope.selectApprovalStatus = function(status)
        {
            var status_flag = 0;
            var ind = 0;
            if($scope.syncRequestDetails.data.filters_to_apply.approval_status.length>0)
            {
                for(var c=0;  c<$scope.syncRequestDetails.data.filters_to_apply.approval_status.length; c++)
                {
                    if(status === $scope.syncRequestDetails.data.filters_to_apply.approval_status[c])
                    {
                        status_flag++;
                        ind = c;
                    }
                }

                if(status_flag===0)
                {
                    $scope.syncRequestDetails.data.filters_to_apply.approval_status.push(status);
                }
                else
                {
                    $scope.syncRequestDetails.data.filters_to_apply.approval_status.splice(ind, 1);
                }
            }
            else
            {
                $scope.syncRequestDetails.data.filters_to_apply.approval_status = [];
                $scope.syncRequestDetails.data.filters_to_apply.approval_status.push(status);
            }
        };*/

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

        /*$scope.isStatusSelected = function(status)
        {
            var statusFlag = 0;
            if($scope.syncRequestDetails.data.filters_to_apply.approval_status)
            {
                for(var j=0; j<$scope.syncRequestDetails.data.filters_to_apply.approval_status.length; j++)
                {
                    if(status === $scope.syncRequestDetails.data.filters_to_apply.approval_status[j])
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
            }
            else
            {
                return false;
            }
        };*/

        $scope.closeAddTag = function()
        {
             $('#add_tag').slideUp();
        };

        $scope.selectTag = function(tag)
        {
            var tag_flag = 0;
            var tag_ind = 0;
            if($scope.syncRequestDetails.data.filters_to_apply.tags.length>0)
            {
                for(var d=0; d<$scope.syncRequestDetails.data.filters_to_apply.tags.length; d++)
                {
                    if(tag === $scope.syncRequestDetails.data.filters_to_apply.tags[d])
                    {
                        tag_flag++;
                        tag_ind = d;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.syncRequestDetails.data.filters_to_apply.tags.push(tag);
                }
                else
                {
                    $scope.syncRequestDetails.data.filters_to_apply.tags.splice(tag_ind, 1);
                }
            }
            else
            {
                $scope.syncRequestDetails.data.filters_to_apply.tags = [];
                $scope.syncRequestDetails.data.filters_to_apply.tags.push(tag);
            }
        };

        $scope.removeTag = function(tag)
        {
            var tag_flag = 0;
            var tag_ind = 0;
            if($scope.syncRequestDetails.data.filters_to_apply.tags.length>0)
            {
                for(var d=0; d<$scope.syncRequestDetails.data.filters_to_apply.tags.length; d++)
                {
                    if(tag === $scope.syncRequestDetails.data.filters_to_apply.tags[d])
                    {
                        tag_flag++;
                        tag_ind = d;
                    }
                }

                if(tag_flag===0)
                {
                    $scope.syncRequestDetails.data.filters_to_apply.tags.push(tag);
                }
                else
                {
                    $scope.syncRequestDetails.data.filters_to_apply.tags.splice(tag_ind, 1);
                }
            }
            else
            {
                $scope.syncRequestDetails.data.filters_to_apply.tags = [];
                $scope.syncRequestDetails.data.filters_to_apply.tags.push(tag);
            }
        };

        $scope.isTagSelected = function(tag)
        {
            var tagFlag = 0;
            if($scope.syncRequestDetails.data.filters_to_apply.tags)
            {
                for(var j=0; j<$scope.syncRequestDetails.data.filters_to_apply.tags.length; j++)
                {
                    if(tag === $scope.syncRequestDetails.data.filters_to_apply.tags[j])
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
            }
            else
            {
                return false;
            }
        };

        $scope.syncDataAll = ViewSyncRequest.get({
              id :   "all"
        },
        function (syncDataSuccessRequest)
        {
            $scope.syncData = syncDataSuccessRequest;
        },
        function (syncDataErrorResponse)
        {
            $rootScope.handleResponse(syncDataErrorResponse);
        });

        $scope.setSyncTypeCSS = function(sync_type)
        {
            return 'vp-search__item--'+sync_type.toLowerCase();
        };

         $scope.discardSyncChanges = function()
         {
            delete $scope.syncRequestDetails;
            $state.go('manageSynchronization');
         };

         $scope.getSyncRequestDetails = function(syncId)
         {
            $scope.syncId = syncId;
            $scope.machineTestResult = '';
            $scope.syncRequestDetails = ViewSyncRequest.get({
              id :   "view/"+syncId
             },
             function (syncDataSuccessRequest)
             {
                if(syncDataSuccessRequest.data.filters_to_apply)
                {
                    var filters = syncDataSuccessRequest.data.filters_to_apply;
                    if(filters.type)
                    {
                        $scope.syncRequestDetails.data.filters_to_apply.type = filters.type;
                    }
                    if(filters.approval_status)
                    {
                        $scope.syncRequestDetails.data.filters_to_apply.approval_status = filters.approval_status;
                    }
                    else
                    {
                        $scope.syncRequestDetails.data.filters_to_apply.approval_status = [];
                    }
                    if(filters.tags)
                    {
                        $scope.syncRequestDetails.data.filters_to_apply.tags = filters.tags;
                    }
                    else
                    {
                        $scope.syncRequestDetails.data.filters_to_apply.tags = [];
                    }
                    if(filters.time_after)
                    {
                        $scope.syncRequestDetails.data.filters_to_apply.time_after = new Date(filters.time_after);
                    }
                    else
                    {
                        $scope.syncRequestDetails.data.filters_to_apply.time_after = null;
                    }
                }
                else
                {
                    $scope.syncRequestDetails.data.filters_to_apply = {
                        type : null,
                        approval_status : [],
                        tags : [],
                        time_after : null
                    };
                }

                if(syncDataSuccessRequest.data.sync_type==='Pull' && syncDataSuccessRequest.data.pull_type==='URL' && !syncDataSuccessRequest.data.steps_to_auth)
                {
                    $scope.removePullStep = false;
                    $scope.addPullStep = true;
                }
                else if(syncDataSuccessRequest.data.sync_type==='Pull' && syncDataSuccessRequest.data.pull_type==='URL' && syncDataSuccessRequest.data.steps_to_auth)
                {
                    $scope.removePullStep = true;
                    $scope.addPullStep = false;
                }
                else
                {
                    $scope.removePullStep = true;
                    $scope.addPullStep = true;
                }

                if(syncDataSuccessRequest.data.sync_type==='Pull' && syncDataSuccessRequest.data.pull_type==='URL')
                {
                    $scope.syncRequestDetails.data.target_dpm_detail.dpm_port = parseInt($scope.syncRequestDetails.data.target_dpm_detail.dpm_port, 10);
                }

                if((syncDataSuccessRequest.data.sync_type==='Pull' && syncDataSuccessRequest.data.pull_type==='File') || (syncDataSuccessRequest.data.sync_type==='Push'))
                {
                    $scope.syncRequestDetails.data.port = parseInt($scope.syncRequestDetails.data.port, 10);
                    if((!$scope.syncRequestDetails.data.auth_type) || $scope.syncRequestDetails.data.auth_type === '' || $scope.syncRequestDetails.data.auth_type === null || $scope.syncRequestDetails.data.auth_type === undefined)
                    {
                        $scope.syncRequestDetails.data.auth_type = 'password';
                    }
                }

                if(syncDataSuccessRequest.data.sync_type==='Pull' && (syncDataSuccessRequest.data.full_sync_flag === true || syncDataSuccessRequest.data.full_sync_flag === "true"))
                {
                    syncDataSuccessRequest.data.full_sync_flag = true;
                }
                else
                {
                    syncDataSuccessRequest.data.full_sync_flag = false;
                }


                if($scope.syncRequestDetails.data.steps_to_auth)
                {
                    for(var a=0; a<$scope.syncRequestDetails.data.steps_to_auth.length;a++)
                    {
                        if ($scope.syncRequestDetails.data.steps_to_auth[a].port !== '' || $scope.syncRequestDetails.data.steps_to_auth[a].port !== null || $scope.syncRequestDetails.data.steps_to_auth[a].port !== undefined)
                        {
                            $scope.syncRequestDetails.data.steps_to_auth[a].port = parseInt($scope.syncRequestDetails.data.steps_to_auth[a].port, 10);
                        }
                    }
                }
                if(syncDataSuccessRequest.data.sync_type==='Push')
                {
                    if(syncDataSuccessRequest.data.trigger_ind==='true')
                    {
                        syncDataSuccessRequest.data.trigger_ind = true;
                    }
                    else
                    {
                        syncDataSuccessRequest.data.trigger_ind = false;
                    }
                }
             },
             function (syncDataErrorResponse){
                $rootScope.handleResponse(syncDataErrorResponse);
             });
        };

        $scope.activateSync = function(id)
        {
            var _id = id;
            var activateViewSyncRequest = {};
            activateViewSyncRequest._id = {
                oid : ""
            };

            activateViewSyncRequest._id.oid = _id;
            activateViewSyncRequest.status = "active";

            $scope.activateStatus = UpdateSyncRequest.update(activateViewSyncRequest,function(activateSuccessResponse){
                $state.go('manageSynchronization');
                delete $scope.syncData;
                $scope.syncDataAll = ViewSyncRequest.get({
                    id :   "all"
                },
                function (syncDataSuccessRequest)
                {
                    delete $scope.syncRequestDetails;
                    $scope.syncData = syncDataSuccessRequest;
                    $scope.getSyncRequestDetails(_id);
                },
                function (syncDataErrorResponse)
                {
                    $rootScope.handleResponse(syncDataErrorResponse);
                });

                $rootScope.handleResponse(activateSuccessResponse);
            },
            function(activateErrorResponse)
            {
                $rootScope.handleResponse(activateErrorResponse);
            });
        };

        $scope.suspendSync = function(id)
        {
            var _id = id;
            var suspendViewSyncRequest = {};
            suspendViewSyncRequest._id = {
                    oid : ""
            };

            suspendViewSyncRequest._id.oid = _id;
            suspendViewSyncRequest.status = "suspended";

            $scope.suspendStatus = UpdateSyncRequest.update(suspendViewSyncRequest,function(suspendSuccessResponse){
                $state.transitionTo($state.current, $stateParams, {
                    reload: true, inherit: false, notify: true
                });
                delete $scope.syncRequestDetails;
                $scope.getSyncRequestDetails(_id);
                delete $scope.syncData;
                $scope.syncDataAll = ViewSyncRequest.get({
                    id :   "all"
                },
                function (syncDataSuccessRequest)
                {
                    $scope.syncData = syncDataSuccessRequest;
                },
                function (syncDataErrorResponse)
                {
                    $rootScope.handleResponse(syncDataErrorResponse);
                });
                $rootScope.handleResponse(suspendSuccessResponse);
            },
            function(suspendErrorResponse)
            {
                $rootScope.handleResponse(suspendErrorResponse);
            }
            );
        };

        $scope.runSyncNow = function(id)
        {
            $('#show_request_progress_modal').show(700);
            var _id = id;
            SyncOnDemand.get({
                id: _id
            },
            function(syncRunSuccessResponse){
                $state.transitionTo($state.current, $stateParams, {
                    reload: true, inherit: false, notify: true
                });
                $('#show_request_progress_modal').hide(700);
                delete $scope.syncRequestDetails;
                $scope.getSyncRequestDetails(_id);
                delete $scope.syncDataAll;
                $scope.syncDataAll = ViewSyncRequest.get({
                    id :   "all"
                },
                function (syncDataSuccessRequest)
                {
                    $scope.syncData = syncDataSuccessRequest;
                },
                function (syncDataErrorResponse)
                {
                    $rootScope.handleResponse(syncDataErrorResponse);
                });
                $rootScope.handleResponse(syncRunSuccessResponse);
            },
            function(syncRunErrorResponse)
            {
                $('#show_request_progress_modal').hide(700);
                $rootScope.handleResponse(syncRunErrorResponse);
            }
            );
        };
        $scope.closeRunningRequestDetails = function()
        {
            $('#show_request_progress_modal').hide(700);
        };

        $scope.deleteSyncRequest = function(syncId)
        {
            DeleteSyncRequest.remove({
                id : syncId
            },
            function(syncDeleteSuccessResponse)
            {
                $state.go('manageSynchronization');
                delete $scope.syncRequestDetails;
                delete $scope.syncDataAll;
                $scope.syncDataAll = ViewSyncRequest.get({
                    id :   "all"
                },
                function (syncDataSuccessRequest)
                {
                    $scope.syncData = syncDataSuccessRequest;
                },
                function (syncDataErrorResponse)
                {
                    $rootScope.handleResponse(syncDataErrorResponse);
                });
                $rootScope.handleResponse(syncDeleteSuccessResponse);
            },
            function(syncDeleteErrorResponse)
            {
                $rootScope.handleResponse(syncDeleteErrorResponse);
            });
        };

        $scope.testConnection = function(form)
        {
            var testMachineData = {};
            if(($scope.syncRequestDetails.data.host === '' || $scope.syncRequestDetails.data.host === null || $scope.syncRequestDetails.data.host === undefined) ||
            ($scope.syncRequestDetails.data.username === '' || $scope.syncRequestDetails.data.username === null || $scope.syncRequestDetails.data.username === undefined) ||
            ($scope.syncRequestDetails.data.ip === '' || $scope.syncRequestDetails.data.ip === null || $scope.syncRequestDetails.data.ip === undefined) ||
            ($scope.syncRequestDetails.data.auth_type === '' || $scope.syncRequestDetails.data.auth_type === null || $scope.syncRequestDetails.data.auth_type === undefined))
        {
            $rootScope.handleResponse('Mandatory fields required to test connection are missing');
            return false;
        }
        else
        {
            if(($scope.syncRequestDetails.data.auth_type === 'password') && ($scope.syncRequestDetails.data.password === '' || $scope.syncRequestDetails.data.password === null || $scope.syncRequestDetails.data.password === undefined))
            {
                $rootScope.handleResponse('Please enter the machine password');
            }
            else
            {
                testMachineData.host = $scope.syncRequestDetails.data.host;
                testMachineData.ip = $scope.syncRequestDetails.data.ip;
                testMachineData.username = $scope.syncRequestDetails.data.username;
                testMachineData.password = $scope.syncRequestDetails.data.password;
                testMachineData.port = $scope.syncRequestDetails.data.port;
                testMachineData.shell_type = $scope.syncRequestDetails.data.shell_type;
                testMachineData.reload_command = $scope.syncRequestDetails.data.reload_command;
                testMachineData.account_id = $rootScope.userProfile.userData.account_details._id.$oid;
                testMachineData.auth_type = $scope.syncRequestDetails.data.auth_type;

                if(testMachineData.auth_type === 'ssh' && (testMachineData.password === null || testMachineData.password === '' || testMachineData.password === undefined))
                {
                    testMachineData.password = '12345';
                }
                else
                {
                    testMachineData.password = $scope.syncRequestDetails.data.password;
                }
            }
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

            if((testMachineData.host === '' || testMachineData.host === null || testMachineData.host === undefined) || (testMachineData.username === '' || testMachineData.username === null || testMachineData.username === undefined) || (testMachineData.password === '' || testMachineData.password === null || testMachineData.password === undefined) || (testMachineData.ip === '' || testMachineData.ip === null || testMachineData.ip === undefined) || (testMachineData.reload_command === null || testMachineData.reload_command === undefined))
            {
                $rootScope.handleResponse('Mandatory fields required to test connection are missing');
                return false;
            }

            if($scope.syncRequestDetails.data.steps_to_auth)
            {
                if($scope.syncRequestDetails.data.steps_to_auth.length > 0)
                {
                    testMachineData.steps_to_auth = $scope.syncRequestDetails.data.steps_to_auth;
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
        };

    $scope.sync_types = [
        "Pull",
        "Push"
    ];

    $scope.pull_types = [
        "URL",
        "File"
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
        "SSH", "Telnet"
    ];
    var stepLength = 1;
    $scope.steps_in_pull = [];
    $scope.steps_in_push = [];

    $scope.onSyncSelected = function () {
        $scope.steps_in_push.length = 0;
    };

    $scope.onPullTypeSelected = function () {
        $scope.syncRequestDetails.data.steps_to_auth.length = 0;
        $scope.addPullStep = true;
    };

    $scope.isEnable = function(index)
    {
        if($scope.syncRequestDetails.data.steps_to_auth[index].type==='SSH')
        {
            return false;
        }
        else
        {
            return true;
        }
    };

    $scope.setDefaultPortInPull = function(step_type, index)
    {
        if($scope.syncRequestDetails.data.pull_type==='File')
        {
            if(step_type==='SSH')
            {
                $scope.syncRequestDetails.data.steps_to_auth[index].port = 22;
            }
            else
            {
                delete $scope.syncRequestDetails.data.steps_to_auth[index].port;
            }
        }
    };

    $scope.setDefaultPortInPush = function(step_type, index)
    {
        if(step_type==='SSH')
        {
            $scope.syncRequestDetails.data.steps_to_auth[index].port = 22;
            return false;
        }
        else
        {
            delete $scope.syncRequestDetails.data.steps_to_auth[index].port;
            return true;
        }
    };

    $scope.addNewStep = function()
    {
        var newItemNo;
        if($scope.syncRequestDetails.data.sync_type==='Push')
        {
                newItemNo = $scope.syncRequestDetails.data.steps_to_auth.length+1;
                $scope.syncRequestDetails.data.steps_to_auth.push({order : newItemNo});
        }
        else
        {
            if($scope.syncRequestDetails.data.pull_type==='URL')
            {
                $scope.syncRequestDetails.data.steps_to_auth = [{type : 'telnet', order : 1}];
                $scope.addPullStep = false;
                $scope.showPullStep = true;
            }
            else
            {
                if($scope.syncRequestDetails.data.steps_to_auth)
                {
                    $scope.syncRequestDetails.data.steps_to_auth.push({ order : newItemNo});
                    $scope.addPullStep = true;
                    $scope.showPullStep = true;
                }
                else
                {
                    $scope.syncRequestDetails.data.steps_to_auth = [];
                    $scope.syncRequestDetails.data.steps_to_auth.push({ order : newItemNo});
                    $scope.addPullStep = true;
                    $scope.showPullStep = true;
                }
            }
        }
    };

    $scope.removeStep = function()
    {
        var lastItem;
        if($scope.syncRequestDetails.data.sync_type==='Push')
        {
            lastItem = $scope.syncRequestDetails.data.steps_to_auth.length-1;
            $scope.syncRequestDetails.data.steps_to_auth.splice(lastItem);
        }
        else
        {
            if($scope.syncRequestDetails.data.pull_type==='URL')
            {
                $scope.addPullStep = true;
                $scope.showPullStep = false;
                $scope.removePullStep = false;
                $scope.syncRequestDetails.data.steps_to_auth.splice(0);
            }
            else
            {
                lastItem = $scope.syncRequestDetails.data.steps_to_auth.length-1;
                $scope.addPullStep = true;
                $scope.showPullStep = true;
                $scope.removePullStep = true;
                $scope.syncRequestDetails.data.steps_to_auth.splice(lastItem);
            }

        }
    };

    $scope.moveStepUp = function(index)
    {
        var elementToMoveUp;
        var elementToMoveDown;
        if($scope.syncData.data.syc_type==='Push')
        {
            elementToMoveUp = $scope.syncRequestDetails.data.steps_to_auth[index];
            elementToMoveDown = $scope.syncRequestDetails.data.steps_to_auth[index-1];
            if(elementToMoveDown!=null)
            {
                $scope.syncRequestDetails.data.steps_to_auth[index-1] = elementToMoveUp;
                $scope.syncRequestDetails.data.steps_to_auth[index] = elementToMoveDown;
            }
        }
        else if($scope.syncRequestDetails.data.syc_type==='Pull' &&  $scope.syncRequestDetails.data.pull_type==='File')
        {
            elementToMoveUp = $scope.syncRequestDetails.data.steps_to_auth[index];
            elementToMoveDown = $scope.syncRequestDetails.data.steps_to_auth[index-1];
            if(elementToMoveDown!=null)
            {
                $scope.syncRequestDetails.data.steps_to_auth[index-1] = elementToMoveUp;
                $scope.syncRequestDetails.data.steps_to_auth[index] = elementToMoveDown;
            }
        }

    };

    $scope.moveStepDown = function(index)
    {
        var elementToMoveUp;
        var elementToMoveDown;
        if($scope.syncData.data.syc_type==='Push')
        {
            elementToMoveDown = $scope.syncRequestDetails.data.steps_to_auth[index];
            elementToMoveUp = $scope.syncRequestDetails.data.steps_to_auth[index+1];

            if(elementToMoveUp!=null)
            {
                $scope.syncRequestDetails.data.steps_to_auth[index] = elementToMoveUp;
                $scope.syncRequestDetails.data.steps_to_auth[index+1] = elementToMoveDown;
            }
        }
        else if($scope.syncRequestDetails.data.syc_type==='Pull' &&  $scope.syncRequestDetails.data.pull_type==='File')
        {
            elementToMoveDown = $scope.syncRequestDetails.data.steps_to_auth[index];
            elementToMoveUp = $scope.syncRequestDetails.data.steps_to_auth[index+1];

            if(elementToMoveUp!=null)
            {
                $scope.syncRequestDetails.data.steps_to_auth[index] = elementToMoveUp;
                $scope.syncRequestDetails.data.steps_to_auth[index+1] = elementToMoveDown;
            }
        }

    };

    $scope.getSynchronizationData = function(form)
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
                tags : []
            },
            target_dpm_detail : {
                dpm_host : "",
                dpm_port : "",
                dpm_token : "",
                dpm_username : "",
                dpm_password : ""
            },
            _id : {
                oid : ""
                }
        };

        $scope.sync_type = $scope.syncRequestDetails.data.sync_type;
        if($scope.sync_type==='Pull')
        {
            $scope.full_sync = ""+$scope.syncRequestDetails.data.full_sync_flag+"";
            $scope.notification_type = $scope.syncRequestDetails.data.notification_type;
            if($scope.syncRequestDetails.data.incremental_pull_ind)
            {
                $scope.incremental_pull_ind = $scope.syncRequestDetails.data.incremental_pull_ind;
            }
            else
            {
                $scope.incremental_pull_ind = false;
            }
        }
        else if($scope.sync_type==='Push')
        {
            if($scope.syncRequestDetails.data.incremental_push_ind)
            {
                $scope.incremental_push_ind = $scope.syncRequestDetails.data.incremental_push_ind;
            }
            else
            {
                $scope.incremental_push_ind = false;
            }
            $scope.trigger_ind = ""+$scope.syncRequestDetails.data.trigger_ind+"";
            $scope.dpm_push_folder_location = $scope.syncRequestDetails.data.dpm_push_folder_location;
        }

        finalJsonData.sync_type = $scope.sync_type;
        if($scope.sync_type==='Pull')
        {
            finalJsonData.full_sync_flag = $scope.full_sync;
            finalJsonData.notification_type = $scope.notification_type;
        }
        //        Validation starts here...
        if($scope.syncRequestDetails.data.steps_to_auth)
        {
            for(var i=0; i<$scope.syncRequestDetails.data.steps_to_auth.length;i++)
            {
                if ($scope.syncRequestDetails.data.steps_to_auth[i].type === undefined)
                {
                    $('html, body').animate({
                        scrollTop: $("#steps_to_auth_"+[i]).offset().top - 50
                    }, 1000);
                    $rootScope.handleResponse('Please select auth type!');
                    return false;
                }

                if ($scope.syncRequestDetails.data.steps_to_auth[i].type === 'SSH')
                {
                    if($scope.syncRequestDetails.data.steps_to_auth[i].port==="" || $scope.syncRequestDetails.data.steps_to_auth[i].port===undefined)
                    {
                        $('html, body').animate({
                            scrollTop: $("#steps_to_auth_"+[i]).offset().top - 50
                        }, 1000);
                        $rootScope.handleResponse('Please enter port for gateway!');
                        return false;
                    }
                    else
                    {
                        $scope.syncRequestDetails.data.steps_to_auth[i].port = $scope.syncRequestDetails.data.steps_to_auth[i].port;
                    }

                    if($scope.syncRequestDetails.data.steps_to_auth[i].host==="" || $scope.syncRequestDetails.data.steps_to_auth[i].host===undefined)
                    {
                        $('html, body').animate({
                            scrollTop: $("#steps_to_auth_"+[i]).offset().top - 50
                        }, 1000);
                        $rootScope.handleResponse('Please enter host for gateway!');
                        return false;
                    }

                    if($scope.syncRequestDetails.data.steps_to_auth[i].username==="" || $scope.syncRequestDetails.data.steps_to_auth[i].username===undefined)
                    {
                        $('html, body').animate({
                            scrollTop: $("#steps_to_auth_"+[i]).offset().top - 50
                        }, 1000);
                        $rootScope.handleResponse('Please enter user for gateway!');
                        return false;
                    }

                    if($scope.syncRequestDetails.data.steps_to_auth[i].password==="" || $scope.syncRequestDetails.data.steps_to_auth[i].password===undefined)
                    {
                        $('html, body').animate({
                            scrollTop: $("#steps_to_auth_"+[i]).offset().top - 50
                        }, 1000);
                        $rootScope.handleResponse('Please enter password for gateway!');
                        return false;
                    }
                }
            }
        }

        if($scope.syncRequestDetails.data.sync_type==='Pull' && $scope.syncRequestDetails.data.pull_type==='URL')
        {
            if($scope.syncRequestDetails.data.target_dpm_detail.dpm_host===undefined)
            {
                 $rootScope.handleResponse('Please enter the DPM host!');
                 return false;

            }

            if($scope.syncRequestDetails.data.target_dpm_detail.dpm_port===undefined)
            {
                 $rootScope.handleResponse('Please enter the DPM port!');
                 return false;

            }

            if($scope.syncRequestDetails.data.target_dpm_detail.dpm_token===undefined)
            {
                 $rootScope.handleResponse('Please enter the DPM Unique token!');
                 return false;

            }

            if($scope.syncRequestDetails.data.target_dpm_detail.dpm_username===undefined)
            {
                 $rootScope.handleResponse('Please enter the DPM username!');
                 return false;

            }
            if($scope.syncRequestDetails.data.target_dpm_detail.dpm_password===undefined)
            {
                 $rootScope.handleResponse('Please enter the DPM password!');
                 return false;

            }
        }

        if(($scope.syncRequestDetails.data.sync_type==='Pull' && $scope.syncRequestDetails.data.pull_type==='File') || $scope.syncRequestDetails.data.sync_type==='Push')
        {
            if($scope.syncRequestDetails.data.host===undefined)
            {
                 $rootScope.handleResponse('Please enter the target machine host name!');
                 return false;
            }
            if($scope.syncRequestDetails.data.port===undefined)
            {
                 $rootScope.handleResponse('Please enter the target machine host name!');
                 return false;
            }
            if(!(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test($scope.syncRequestDetails.data.ip)))
            {
                $rootScope.handleResponse('Please enter valid IP Address!!');
                return false;

            }
            if($scope.syncRequestDetails.data.username===undefined)
            {
                 $rootScope.handleResponse('Please enter the target machine user name!');
                 return false;
            }
            if($scope.syncRequestDetails.data.auth_type===undefined)
            {
                 $rootScope.handleResponse('Please enter the target auth type!');
                 return false;
            }
            if($scope.syncRequestDetails.data.auth_type === 'password' && ($scope.syncRequestDetails.data.password === '' || $scope.syncRequestDetails.data.password === null || $scope.syncRequestDetails.data.password === undefined))
            {
                 $rootScope.handleResponse('Please enter the target machine password!');
                 return false;
            }
            if($scope.syncRequestDetails.data.distribution_list)
            {
                var atpos = $scope.syncRequestDetails.data.distribution_list.indexOf("@");
                var dotpos = $scope.syncRequestDetails.data.distribution_list.lastIndexOf(".");
                if (atpos<1 || dotpos<atpos+2 || dotpos+2>=$scope.syncRequestDetails.data.distribution_list.length) {
                    $rootScope.handleResponse('Please enter valid email address in distribution list!');
                    return false;
                }
            }
        }

        if($scope.syncRequestDetails.data.sync_type==='Pull' && $scope.syncRequestDetails.data.pull_type==='File')
        {
            if($scope.syncRequestDetails.data.remote_source_location === '' || $scope.syncRequestDetails.data.remote_source_location === null || $scope.syncRequestDetails.data.remote_source_location === undefined)
            {
                $rootScope.handleResponse('Please enter the remote source location');
                return false;
            }
        }

        if($scope.syncRequestDetails.data.sync_type==='Push' && $scope.syncRequestDetails.data.trigger_ind_value===true)
        {
            if($scope.syncRequestDetails.data.target_dpm_detail.dpm_host===undefined)
            {
                 $rootScope.handleResponse('Please enter the DPM host!');
                 return false;

            }

            if($scope.syncRequestDetails.data.target_dpm_detail.dpm_port===undefined)
            {
                 $rootScope.handleResponse('Please enter the DPM port!');
                 return false;

            }

            if($scope.syncRequestDetails.data.target_dpm_detail.dpm_token===undefined)
            {
                 $rootScope.handleResponse('Please enter the DPM Unique token!');
                 return false;

            }

            if($scope.syncRequestDetails.data.target_dpm_detail.dpm_username===undefined)
            {
                 $rootScope.handleResponse('Please enter the DPM username!');
                 return false;

            }
            if($scope.syncRequestDetails.data.target_dpm_detail.dpm_password===undefined)
            {
                 $rootScope.handleResponse('Please enter the DPM password!');
                 return false;

            }
        }
//        Validation ends here...

        $scope.sync_type = $scope.syncRequestDetails.data.sync_type;

        if($scope.sync_type==='Pull')
        {
            $scope.full_sync = ""+$scope.syncRequestDetails.data.full_sync_flag+"";
            $scope.notification_type = $scope.syncRequestDetails.data.notification_type;
            $scope.pull_type = $scope.syncRequestDetails.data.pull_type;
            finalJsonData.pull_type = $scope.pull_type;
            if($scope.pull_type==='File')
            {
                $scope.remote_source_location = $scope.syncRequestDetails.data.remote_source_location;
                finalJsonData.remote_source_location = $scope.remote_source_location;
            }
        }
        else if($scope.sync_type==='Push')
        {
            $scope.trigger_ind = ""+$scope.syncRequestDetails.data.trigger_ind+"";
        }

        finalJsonData.sync_type = $scope.sync_type;

        if($scope.sync_type==='Pull')
        {
            finalJsonData.full_sync_flag = JSON.parse($scope.full_sync);
            finalJsonData.notification_type = $scope.notification_type;
        }
        finalJsonData._id.oid = $scope.syncId;

        if($scope.sync_type==='Pull')
        {
            if(finalJsonData.pull_type==='File')
            {
                finalJsonData.remote_source_location = $scope.syncRequestDetails.data.remote_source_location;
                finalJsonData.host = $scope.syncRequestDetails.data.host;
                finalJsonData.port = $scope.syncRequestDetails.data.port;
                finalJsonData.ip = $scope.syncRequestDetails.data.ip;
                finalJsonData.username = $scope.syncRequestDetails.data.username;
                finalJsonData.auth_type = $scope.syncRequestDetails.data.auth_type;
                if(finalJsonData.auth_type === 'ssh')
                {
                    finalJsonData.password = '12345';
                }
                else
                {
                    finalJsonData.password = $scope.syncRequestDetails.data.password;
                }
                if($scope.syncRequestDetails.data.shell_type === ' ' || $scope.syncRequestDetails.data.shell_type === undefined || $scope.syncRequestDetails.data.shell_type === null)
                {
                    finalJsonData.shell_type = '';
                }
                else
                {
                    finalJsonData.shell_type = $scope.syncRequestDetails.data.shell_type;
                }
                if($scope.syncRequestDetails.data.reload_command === 'not required' || $scope.syncRequestDetails.data.reload_command === undefined)
                {
                    finalJsonData.reload_command = '';
                }
                else
                {
                    finalJsonData.reload_command = $scope.syncRequestDetails.data.reload_command;
                }
                delete finalJsonData.target_dpm_detail;
                finalJsonData.target_dpm_detail = {};
            }
            else
            {
                if($scope.syncRequestDetails.data.target_dpm_detail)
                {
                    finalJsonData.target_dpm_detail.dpm_host = $scope.syncRequestDetails.data.target_dpm_detail.dpm_host;
                    finalJsonData.target_dpm_detail.dpm_username = $scope.syncRequestDetails.data.target_dpm_detail.dpm_username;
                    finalJsonData.target_dpm_detail.dpm_token = $scope.syncRequestDetails.data.target_dpm_detail.dpm_token;
                    finalJsonData.target_dpm_detail.dpm_password = $scope.syncRequestDetails.data.target_dpm_detail.dpm_password;
                    finalJsonData.target_dpm_detail.dpm_port = $scope.syncRequestDetails.data.target_dpm_detail.dpm_port;
                }
            }
            finalJsonData.distribution_list = $scope.distribution_list_pull;
            finalJsonData.incremental_pull_ind = $scope.incremental_pull_ind;
        }
        else
        {
            finalJsonData.host = $scope.syncRequestDetails.data.host;
            finalJsonData.port = $scope.syncRequestDetails.data.port;
            finalJsonData.ip = $scope.syncRequestDetails.data.ip;
            finalJsonData.username = $scope.syncRequestDetails.data.username;
            finalJsonData.incremental_push_ind = $scope.incremental_push_ind;
            finalJsonData.auth_type = $scope.syncRequestDetails.data.auth_type;
            finalJsonData.external_artifacts = $scope.syncRequestDetails.data.external_artifacts;
            if(finalJsonData.auth_type === 'ssh')
            {
                finalJsonData.password = '12345';
            }
            else
            {
                finalJsonData.password = $scope.syncRequestDetails.data.password;
            }
            if($scope.syncRequestDetails.data.shell_type === ' ' || $scope.syncRequestDetails.data.shell_type === undefined || $scope.syncRequestDetails.data.shell_type === null)
            {
                finalJsonData.shell_type = '';
            }
            else
            {
                finalJsonData.shell_type = $scope.syncRequestDetails.data.shell_type;
            }
            if($scope.syncRequestDetails.data.reload_command === 'not required' || $scope.syncRequestDetails.data.reload_command === undefined)
            {
                finalJsonData.reload_command = '';
            }
            else
            {
                finalJsonData.reload_command = $scope.syncRequestDetails.data.reload_command;
            }
            finalJsonData.trigger_ind = $scope.trigger_ind;

            if($scope.trigger_ind===true || $scope.trigger_ind==='true')
            {
                finalJsonData.target_dpm_detail.dpm_host = $scope.syncRequestDetails.data.target_dpm_detail.dpm_host;
                finalJsonData.target_dpm_detail.dpm_username = $scope.syncRequestDetails.data.target_dpm_detail.dpm_username;
                finalJsonData.target_dpm_detail.dpm_token = $scope.syncRequestDetails.data.target_dpm_detail.dpm_token;
                finalJsonData.target_dpm_detail.dpm_password = $scope.syncRequestDetails.data.target_dpm_detail.dpm_password;
                finalJsonData.target_dpm_detail.dpm_port = $scope.syncRequestDetails.data.target_dpm_detail.dpm_port;
            }
            else
            {
                delete finalJsonData.target_dpm_detail;
                finalJsonData.target_dpm_detail = {};
            }

            if($scope.syncRequestDetails.data.folder_location !== '')
            {
                finalJsonData.folder_location = $scope.syncRequestDetails.data.folder_location;
            }
            finalJsonData.folder_location = $scope.syncRequestDetails.data.folder_location;
        }

        finalJsonData.distribution_list = jsonData.distribution_list;

        if($scope.sync_type==='Pull' && $scope.pull_type=='URL')
        {
            if($scope.syncRequestDetails.data.steps_to_auth)
            {
                if($scope.syncRequestDetails.data.steps_to_auth.length===1)
                {
                    finalJsonData.steps_to_auth = $scope.syncRequestDetails.data.steps_to_auth;
                }
                else
                {
                    delete finalJsonData.steps_to_auth;
                }
            }
        }
        else
        {
            finalJsonData.steps_to_auth = $scope.syncRequestDetails.data.steps_to_auth;
        }
        if($scope.sync_type==='Push' && $scope.trigger_ind!=null)
        {
            finalJsonData.trigger_ind = $scope.trigger_ind;
        }
        else
        {
            finalJsonData.trigger_ind = "false";
        }

        if($scope.syncRequestDetails.data.filters_to_apply.type !== null && $scope.syncRequestDetails.data.filters_to_apply.type!== "" && $scope.syncRequestDetails.data.filters_to_apply.type!== undefined )
        {
            finalJsonData.filters_to_apply.type = $scope.syncRequestDetails.data.filters_to_apply.type;
        }
        else
        {
            finalJsonData.filters_to_apply.type = 'all';
        }

        if(finalJsonData.filters_to_apply.type === 'du' || finalJsonData.filters_to_apply.type === 'all')
        {
            if($scope.syncRequestDetails.data.filters_to_apply.approval_status.length>0)
            {
                finalJsonData.filters_to_apply.approval_status = $scope.syncRequestDetails.data.filters_to_apply.approval_status;
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

        if($scope.syncRequestDetails.data.filters_to_apply.tags.length>0)
        {
            finalJsonData.filters_to_apply.tags = $scope.syncRequestDetails.data.filters_to_apply.tags;
        }
        else
        {
            finalJsonData.filters_to_apply.tags = 'any';
        }
        if($scope.syncRequestDetails.data.filters_to_apply.time_after !== null && $scope.syncRequestDetails.data.filters_to_apply.time_after !== undefined)
        {
            finalJsonData.filters_to_apply.time_after = $scope.syncRequestDetails.data.filters_to_apply.time_after.toISOString();
        }
        else
        {
            delete finalJsonData.time_after
        }
        finalJsonData.distribution_list = $scope.syncRequestDetails.data.distribution_list;
        ViewSyncRequestInJson = finalJsonData;

        $scope.suspendStatus = UpdateSyncRequest.update(ViewSyncRequestInJson,function(suspendSuccessResponse){
            delete $scope.syncRequestDetails;
            $state.go('manageSynchronization');
            $rootScope.handleResponse(suspendSuccessResponse);
        },
        function(suspendErrorResponse)
        {
                $rootScope.handleResponse(suspendErrorResponse);
        });
    };
 });
 });