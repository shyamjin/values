require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent','saveExportControllerApp']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent','saveExportControllerApp'],function (app) {
  'use strict';

var importExportControllerApp = angular.module('importExportControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp','saveExportControllerApp']);

importExportControllerApp.controller('ImportExportController', function ($scope, $window, $http, fileUpload, ExportData, $rootScope,ApprovalStatusAll,TagsAll) {
    $scope.isResultVisible = false;
    $rootScope.resultPane = false;
    $rootScope.result = false;
    $rootScope.preLoader = false;
    $scope.external_artifacts = true;
    $scope.currentTab = 'ImportTab';
    $scope.showCurrentTab = function(tab)
    {
        $scope.currentTab = tab;
        if($scope.currentTab !='ImportTab')
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



    $scope.importData = function(form)
    {
        if($scope.fileToImport)
        {
            $scope.isResultVisible = true;
            $rootScope.preLoader = true;
            $rootScope.resultPane = false;
            var jsonData = {};
            var file = $scope.fileToImport;
            if(file)
            {
                console.log('file is ');
                console.dir(file);
                var uploadUrl = "/sync/import";
                fileUpload.uploadFileToUrl(file, uploadUrl, function(){
                });
            }
        }
        else
        {
            $rootScope.handleResponse('Please select a file to import');
            return false;
        }

    };
    $scope.currentDateTime = new Date();
    $scope.currentDateTime.setSeconds(0);
    $scope.currentDateTime.setMilliseconds(0);
    $scope.filtersToApply = {
        type : null,
        time_after :null,
        approval_status : 'Any',
        tags : []
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

    $scope.exportData = function(form)
    {
        $scope.isResultVisible = true;
        $rootScope.preLoader = true;
        $rootScope.resultPane = false;
        var exportRequestInJson = {};
        var jsonData = {
            target_host : $scope.exportForm.target_machine_name.$viewValue,
            filters_to_apply : {
                type : "",
                time_after : "",
                approval_status : [],
                tags : []

            },
            external_artifacts:$scope.external_artifacts
        };
        if($scope.filtersToApply.type !== null && $scope.filtersToApply.type!== undefined && $scope.filtersToApply.type!== "")
        {
            jsonData.filters_to_apply.type = $scope.filtersToApply.type;
        }
        else
        {
            jsonData.filters_to_apply.type ='all';
        }

        if(jsonData.filters_to_apply.type === 'du' || jsonData.filters_to_apply.type === 'all')
        {
            if($scope.filtersToApply.approval_status.length> 0)
            {
            jsonData.filters_to_apply.approval_status = $scope.filtersToApply.approval_status;
            }
            else
            {
            jsonData.filters_to_apply.approval_status.push('any');
            }
        }
        else
        {
            delete jsonData.filters_to_apply.approval_status;
        }

        if($scope.filtersToApply.tags.length>0)
        {
            jsonData.filters_to_apply.tags = $scope.filtersToApply.tags;
        }
        else
        {
            jsonData.filters_to_apply.tags.push('any');
        }
        if($scope.filtersToApply.time_after!== null && $scope.filtersToApply.time_after!== undefined)
        {
            jsonData.filters_to_apply.time_after = $scope.filtersToApply.time_after.toISOString();
        }
        else
        {
            delete jsonData.filters_to_apply.time_after;
        }
        exportRequestInJson= jsonData;
        $scope.export = ExportData.save(exportRequestInJson,
        function(successResponse) {
            $rootScope.resultPane = true;
            $rootScope.preLoader = false;
            $rootScope.result = successResponse;
            $window.location.href = successResponse.data.file_path;
            $rootScope.handleResponse(successResponse);
        },
        function(errorResponse) {
            $rootScope.resultPane = true;
            $rootScope.preLoader = false;
            $rootScope.result = errorResponse.data;
            $rootScope.handleResponse(errorResponse);
        }
        );
    };
});
});