/* Created by Nilesh Late */
require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['cloneServicesApp']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'jquery', 'cloneServicesApp'],function (app) {
  'use strict';

var createAccountControllerApp = angular.module('createAccountControllerApp', ['ui.router', 'cloneServicesApp']);

createAccountControllerApp.controller('CreateAccountController', function ($scope, $state, GetAllTools, Machine, $stateParams, $window, $http, $interval, Account, CloneRequestStatus, MachineAdd, CloneRequest, $rootScope, AccountDelete, MachineDelete, $timeout, TestMachine, TagsAll, AllToolSet, GetAllMachineTypes) {
        $scope.toolList = [];
        $scope.filterType = 'Active';
        $scope.statusFlag = true;
        $scope.tagsFlag = false;
        $scope.toolsetsFlag = false;
        var statusFilter = [];
        var tagFilter = [];
        var toolsetFilter = [];
        $scope.tags = new TagsAll();
        $scope.accountDetails = {
            account_name : '',
            mps_version : 0
        };
        $scope.shell_type = [
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
        $scope.machineDetails = {
            machine_name : '',
            host : '',
            user_name : '',
            password : '',
            ip : '',
            shell_type : 'not required',
            reload_command : 'not required',
            port : 22
        };
        $scope.currentTab = 'CloneRequestTab';
        $scope.selectedTools = [];
        $scope.toolList = [];
        $scope.allTools = [];
        GetAllTools.get({
            id: "all",
            status: "active",
            page: 0,
            perpage: 0
        },
        function(successResponse)
        {
            for(var t1=0; t1<successResponse.data.data.length; t1++)
            {
                for(var t2=0; t2<successResponse.data.data[t1].versions.length; t2++)
                {
                    $scope.allTools.push({'tool_id' : successResponse.data.data[t1]._id.$oid, 'tool_name' : successResponse.data.data[t1].name, 'is_tool_cloneable' : successResponse.data.data[t1].is_tool_cloneable, 'artifacts_only' : successResponse.data.data[t1].artifacts_only, 'tool_version' : successResponse.data.data[t1].name+' '+successResponse.data.data[t1].versions[t2].version_number, 'version_id' : successResponse.data.data[t1].versions[t2].version_id, 'version_name' : successResponse.data.data[t1].versions[t2].version_name, 'version_number' : successResponse.data.data[t1].versions[t2].version_number});
                }
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

        $scope.showCurrentTab = function(tab)
        {
            $scope.currentTab = tab;
            if($scope.currentTab !='CloneRequestTab')
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

        $scope.showStatus = function()
        {
            if($scope.statusFlag === true)
            {
                $scope.statusFlag = false;
            }
            else
            {
                $scope.statusFlag = true;
            }
        };

        $scope.setStatusCSS = function(flag)
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

        $scope.showTags = function()
        {
            if($scope.tagsFlag === true)
            {
                $scope.tagsFlag = false;
            }
            else
            {
                $scope.tagsFlag = true;
            }
        };

        $scope.setTagsCSS = function(flag)
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

        $scope.showToolsets = function()
        {
            if($scope.toolsetsFlag === true)
            {
                $scope.toolsetsFlag = false;
            }
            else
            {
                $scope.toolsetsFlag = true;
            }
        };

        $scope.setToolsetsCSS = function(flag)
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

        TagsAll.get({

        },
        function(successResponse)
        {
            $scope.tagsAll = successResponse;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

        AllToolSet.get({
            page: 0,
            perpage: 0
        },
        function(alltoolsets)
        {
            $scope.toolsetsAll = alltoolsets.data.data;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

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

        $scope.setTagFilter = function(tag)
        {
            var tagFlag = 0;
            var ind = 0;
            var tagFilterLen = tagFilter.length;
            if(tagFilterLen>0)
            {
                for(var a=0; a<tagFilterLen; a++)
                {
                    if(tagFilter[a] === tag)
                    {
                        ind = a;
                    }
                    else
                    {
                        tagFlag++;
                    }
                }

                if(tagFlag === tagFilterLen)
                {
                    tagFilter.push(tag);
                }
                else
                {
                    tagFilter.splice(ind, 1);
                }
            }
            else
            {
                tagFilter.push(tag);
            }
        };

        $scope.setToolsetFilter = function(toolset)
        {
            var toolsetFlag = 0;
            var ind = 0;
            var toolsetFilterLen = toolsetFilter.length;
            if(toolsetFilterLen>0)
            {
                for(var a=0; a<toolsetFilterLen; a++)
                {
                    if(toolsetFilter[a] === toolset)
                    {
                        ind = a;
                    }
                    else
                    {
                        toolsetFlag++;
                    }
                }

                if(toolsetFlag === toolsetFilterLen)
                {
                    toolsetFilter.push(toolset);
                }
                else
                {
                    toolsetFilter.splice(ind, 1);
                }
            }
            else
            {
                toolsetFilter.push(toolset);
            }
        };

        $scope.applyToolFilters = function()
        {
            var status = '';
            var tag = '';
            var toolset = '';

            if(statusFilter.length>0)
            {
                status = statusFilter.toString();
            }
            else
            {
                status = null;
            }

            if(tagFilter.length>0)
            {
                tag = tagFilter.toString();
            }
            else
            {
                tag = null;
            }

            if(toolsetFilter.length>0)
            {
                toolset = toolsetFilter.toString();
            }
            else
            {
                toolset = null;
            }

            $scope.applicationsAll = GetAllTools.get({
               id: "all",
               status: status,
               tags: tag,
               toolset: toolset
            },
            function(successResponse)
            {
                for(var t1=0; t1<successResponse.data.data.length; t1++)
                {
                    for(var t2=0; t2<successResponse.data.data[t1].versions.length; t2++)
                    {
                        $scope.allTools.push({'tool_id' : successResponse.data.data[t1]._id.$oid, 'tool_name' : successResponse.data.data[t1].name, 'is_tool_cloneable' : successResponse.data.data[t1].is_tool_cloneable, 'artifacts_only' : successResponse.data.data[t1].artifacts_only, 'tool_version' : successResponse.data.data[t1].name+' '+successResponse.data.data[t1].versions[t2].version_number, 'version_id' : successResponse.data.data[t1].versions[t2].version_id, 'version_name' : successResponse.data.data[t1].versions[t2].version_name, 'version_number' : successResponse.data.data[t1].versions[t2].version_number});
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        };

        $scope.testConnection = function(form)
        {
            var testMachineData = {};
            testMachineData.host = $scope.machineDetails.host;
            testMachineData.username = $scope.machineDetails.user_name;
            testMachineData.password = $scope.machineDetails.password;
            testMachineData.ip = $scope.machineDetails.ip;
            testMachineData.port = $scope.machineDetails.port;
            testMachineData.machine_type = $scope.machine_type;
            testMachineData.shell_type = $scope.machineDetails.shell_type;
            testMachineData.reload_command = $scope.machineDetails.reload_command;
            testMachineData.auth_type = $scope.machineDetails.auth_type;
            testMachineData.account_id = "Dummy"

            if(testMachineData.shell_type === ' ' || testMachineData.shell_type === undefined || testMachineData.shell_type === null || testMachineData.shell_type === 'not required')
            {
                testMachineData.shell_type = '';
            }
            if(testMachineData.reload_command === 'not required')
            {
                testMachineData.reload_command = '';
            }
            else
            {
                testMachineData.reload_command = testMachineData.reload_command;
            }

            if(testMachineData.auth_type === 'ssh' && (testMachineData.password === null || testMachineData.password === '' || testMachineData.password === undefined))
            {
                testMachineData.password = '12345';
            }

            if(((testMachineData.host === '' || testMachineData.host === null || testMachineData.host === undefined) || (testMachineData.username === '' || testMachineData.username === null || testMachineData.username === undefined) || (testMachineData.ip === '' || testMachineData.ip === null || testMachineData.ip === undefined) || (testMachineData.auth_type === '' || testMachineData.auth_type === null || testMachineData.auth_type === undefined) || (testMachineData.reload_command === null || testMachineData.reload_command === undefined) || (testMachineData.shell_type === null || testMachineData.shell_type === undefined)) || ((testMachineData.auth_type === 'password') && (testMachineData.password === '' || testMachineData.password === null || testMachineData.password === undefined)))
            {
                $rootScope.handleResponse('Mandatory fields required to test connection are missing');
                return false;
            }

            TestMachine.save (testMachineData, function (testMachineSuccessResponse){
               $scope.machineTestResult = testMachineSuccessResponse;
               $rootScope.handleResponse(testMachineSuccessResponse);
            },
            function(testMachineErrorResponse){
                $scope.machineTestResult = testMachineErrorResponse.data.message;
                $rootScope.handleResponse(testMachineErrorResponse);
            });
        };

      $scope.start_status=false;
      $scope.stop_status=true;
      $scope.Timer = null;
      $scope.isFormVisible = false;
      $scope.isStatusVisible = false;
      var promise;

      $scope.requestForm=true;
      $scope.requestStatusMessages=[];
      $scope.requestSubmitted=false;
      $scope.responseRec= false;
      $scope.requestSubmissionStatus= " Not Submitted";

      $scope.getRequestStatus = function ()
      {
            var status  =  CloneRequestStatus.get({
                  id : $scope.requestID
            },
            function(response) {
                if(response.data.status=='Failed')
                {
                    $rootScope.handleResponse(response);
                    $scope.stopRequestStatus();
                }
                else
                {
                    $scope.toolDeploymentRequestStatus= response.data.status_message;
                    if($scope.requestStatusMessages.indexOf(response.data.status_message)<=-1)
                    {
                        $scope.requestStatusMessages.push(response.data.status_message);
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
      };

      $scope.getStatus = function()
      {
        $scope.start_status=!$scope.start_status;
        $scope.stop_status=!$scope.stop_status;
        promise = $interval( function(){ $scope.getRequestStatus(); }, 7000);
      };

      $scope.stopRequestStatus = function ()
      {
                  $scope.start_status=!$scope.start_status;
                  $scope.stop_status=!$scope.stop_status;
                  console.log('invoking stop ticket status');

                  $interval.cancel(promise);
                  console.log('stopped ticket status');
      };

      $scope.showAddTool = function()
     {
        if(document.getElementById("show_tools").style.display === "none" || document.getElementById("show_tools").style.display === "")
        {
            $('#show_tools').show(700);
            if(($scope.toolList.length>0) && ($scope.selectedTools.length === 0))
            {
                $scope.selectedTools = $scope.toolList;
            }
        }
        else
        {
            $('#show_tools').hide(700);
        }
     };

        $scope.openFilterMove = function(param)
     {
        if(param === 'modal' && $scope.open_filter === true)
        {
            return 'move_modal';
        }
        else if(param ==='footer' && $scope.open_filter === true)
        {
            return 'move_footer';
        }
     };

         $scope.closeToolSetModal = function()
         {
            $('#show_tools').hide(700);
         };


          $scope.openFilter = function()
         {
            if(document.getElementById("open_filter").style.display === "none" || document.getElementById("open_filter").style.display === "")
            {
                $('#open_filter').show(500);
                $scope.open_filter = true;
            }
            else
            {
                $('#open_filter').hide(500);
                $scope.open_filter = false;
            }
         };

         $scope.openFilterMove = function(param)
         {
            if(param === 'modal' && $scope.open_filter === true)
            {
                return 'move_modal';
            }
            else if(param ==='footer' && $scope.open_filter === true)
            {
                return 'move_footer';
            }
         };



          $scope.addTool = function(tool)
            {
                var toolset_flag = 0;
                var tools_length = $scope.selectedTools.length;
                var ind = 0;
                if(tools_length>0)
                {
                    for(var c=0;  c<$scope.selectedTools.length; c++)
                    {
                        if((tool.tool_id===$scope.selectedTools[c].tool_id))
                        {
                            toolset_flag++;
                            ind = c;
                        }
                    }

                    if(toolset_flag===0)
                    {
                        $scope.selectedTools.push(tool);
                    }

                }
                else
                {
                     $scope.selectedTools = [];
                     $scope.selectedTools.push(tool);
                }
            };

            $scope.removeToolFromSelectedTools = function(tool_id)
            {
                for(var a=0; a<$scope.selectedTools.length; a++)
                {
                    if($scope.selectedTools[a].tool_id === tool_id)
                    {
                        $scope.selectedTools.splice(a, 1);
                    }
                }
            };

            $scope.removeToolFromToolList = function(tool_id)
            {
                for(var a=0; a<$scope.toolList.length; a++)
                {
                    if($scope.toolList[a].tool_id === tool_id)
                    {
                        $scope.toolList.splice(a, 1);
                    }
                }

                for(var b=0; b<$scope.selectedTools.length; b++)
                {
                    if($scope.selectedTools[b].tool_id === tool_id)
                    {
                        $scope.selectedTools.splice(b, 1);
                    }
                }
            };

            $scope.updateToolsetList = function()
            {
                $('#show_tools').hide(700);
                $scope.toolList = [];
                $scope.toolList = $scope.selectedTools;
            };

            $scope.deleteToolsetList = function()
            {
                $('#show_tools').hide(700);
                for(var a=0; a<$scope.toolList.length; a++)
                {
                    var toolFlag = 0;
                    $scope.selectedTools = [];
                    for(var b=0; b<$scope.selectedTools.length; b++)
                    {
                        $scope.selectedTools.push($scope.toolList[a]);
                    }
                }
            };

            $scope.selectMachineType = function(machine_type)
            {
                $scope.machine_type = machine_type;
            };


          $scope.types = GetAllMachineTypes.get({
          },
          function(typeSuccessResponse)
          {
            $scope.types=typeSuccessResponse.data;
          },
          function(errorResponse)
          {
            $rootScope.handleResponse(errorResponse);
          });

        $scope.sendCloneRequest = function(form)
        {
    //        if (!(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test($scope.IP)))
    //        {
    //            Materialize.toast("Please enter correct IP Address!! ",5000);
    //            return false;
    //        }

            $scope.requestForm=true;
            var machineData = {};
            var accountData = {};
            $scope.tool_list = [];
            var cloneReqData = {};
            cloneReqData.tool_list = [];
            machineData.machine_name = $scope.machineDetails.machine_name;
            machineData.host = $scope.machineDetails.host;
            machineData.username = $scope.machineDetails.user_name;
            machineData.password = $scope.machineDetails.password;
            machineData.auth_type = $scope.machineDetails.auth_type;
            machineData.ip = $scope.machineDetails.ip;
            machineData.port = $scope.machineDetails.port;
            machineData.machine_type = $scope.machine_type;
            accountData.name = $scope.accountDetails.account_name;
            accountData.mps_version = $scope.accountDetails.mps_version;

            machineData.shell_type = $scope.machineDetails.shell_type;
            machineData.reload_command = $scope.machineDetails.reload_command;

            if(machineData.shell_type === 'not required')
            {
                machineData.shell_type = '';
            }
            if(machineData.reload_command === 'not required')
            {
                machineData.reload_command = '';
            }
            else
            {
                machineData.reload_command = machineData.reload_command;
            }

            if(machineData.auth_type === 'ssh' && (machineData.password === null || machineData.password === '' || machineData.password === undefined))
            {
                machineData.password = '12345';
            }


            if(((machineData.host === '' || machineData.host === null || machineData.host === undefined) || (machineData.username === '' || machineData.username === null || machineData.username === undefined) || (machineData.ip === '' || machineData.ip === null || machineData.ip === undefined) || (machineData.auth_type === '' || machineData.auth_type === null || machineData.auth_type === undefined) || (machineData.reload_command === null || machineData.reload_command === undefined) || (machineData.shell_type === null || machineData.shell_type === undefined)) || ((machineData.auth_type === 'password') && (machineData.password === '' || machineData.password === null || machineData.password === undefined) || (machineData.machine_type === '' || machineData.machine_type === null || machineData.machine_type === undefined)))
            {
                $rootScope.handleResponse('Mandatory fields required to create a clone request are missing');
                return false;
            }

            if($scope.toolList.length>0)
            {
                for(var i=0;i<$scope.toolList.length;i++)
                {
                    cloneReqData.tool_list.push({ status:"requested", version_id: $scope.toolList[i].version_id, artifacts_only: $scope.toolList[i].artifacts_only});
                }
            }
            else
            {
                cloneReqData.tool_list = [];
            }

            cloneReqData.requested_by = $rootScope.userProfile.userData.user;
            cloneReqData.distribution_list = $rootScope.userProfile.userData.email;

            $scope.requestSubmitted=true;
            $scope.responseRec= false;
            $scope.requestSubmissionStatus= "Request is being sent to Server";

            $scope.createAccountStatus = Account.save(accountData, function(AccountCreateResponse){
                $rootScope.handleResponse( AccountCreateResponse);
                machineData.account_id = AccountCreateResponse.data.id;
                cloneReqData.account_id = AccountCreateResponse.data.id;
                cloneReqData.account_name = accountData.name;

                $scope.machine_add = MachineAdd.save(machineData, function(MachineCreateResponse){
                        $rootScope.handleResponse( MachineCreateResponse);
                        cloneReqData.machine_id = MachineCreateResponse.data.id;
                        $scope.requestSubmissionStatus =  CloneRequest.save (cloneReqData, function (CloneResponse) {
                        $state.go('dashboard');
                        $scope.responseMessage = CloneResponse;
                        $scope.responseRec= true;
                        $scope.requestID = CloneResponse.data.id;
                        promise = $interval( function(){ $scope.getRequestStatus(); }, 3000);
                        $scope.requestForm = false;
                        $scope.requestStatusMessages.push(CloneResponse.message);
                        $rootScope.handleResponse(CloneResponse);
                        $scope.isFormVisible=true;
                        $scope.isStatusVisible=true;
                        $scope.requestSubmitted=true;
                        $scope.responseRec= false;
                    },
                    function(clonerequestError) {
                        var cloneErr = clonerequestError.data;
                        $rootScope.handleResponse(clonerequestError);
                        $scope.requestStatusMessages.push(cloneErr.message);
                        $scope.stopRequestStatus();

                        $scope.accountDeletion = AccountDelete.remove({
                            id :  AccountCreateResponse.data.id
                        },
                        function (accountDeleteRequestSuccess){
                            $rootScope.handleResponse(accountDeleteRequestSuccess);
                        },
                        function (accountDeleteResponseError){
                            $rootScope.handleResponse(accountDeleteResponseError);
                        });

                       $scope.machineDeletion = MachineDelete.remove({
                            id :  MachineCreateResponse.data.id
                       },
                       function (machineDeleteRequestSuccess){
                            $rootScope.handleResponse(machineDeleteRequestSuccess);
                       },
                       function (accountDeleteRequestError){
                            $rootScope.handleResponse(accountDeleteRequestError);
                       });
                    });

                },
                function(machineAddRequestError) {
                    // If Machine Add failed, delete the account created
                    var machineError = machineAddRequestError.data;
                    $scope.accountDeletion = AccountDelete.remove({
                        id :  AccountCreateResponse.data.id
                    },
                    function (accountDeleteRequestSuccess){
                       $rootScope.handleResponse(accountDeleteRequestSuccess);
                    },
                    function (accountDeleteRequestError){
                       $rootScope.handleResponse(accountDeleteRequestError);
                    });
                    $scope.stopRequestStatus();
                });
            },
            function(accountCreateErrorResponse) {
                $rootScope.handleResponse(accountCreateErrorResponse);
                $scope.stopRequestStatus();
            });
        };
        $rootScope.$on('$stateChangeSuccess', function() {
            $scope.stopRequestStatus();
        });
});
});