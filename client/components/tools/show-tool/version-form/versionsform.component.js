/*
Author - nlate
Description -
    1. Controller that handles with the details of each version in tool
Methods -
    1. downloadBuild(buildFilePath) - Downloads a build file for the epcific selected version of the tool
    2. showLessVersionReleaseNotesContent() - show less content function for release notes
    3. showMoreVersionReleaseNotesContent - show more content function for release notes
    4. showLessBuildReleaseNotesContent - show more content function for build details
    5. showMoreBuildReleaseNotesContent - show less content function for build details
    6. showLessChecksum - show more content function for checksum
    7. showMoreChecksum - show less content function for checksum
    8. showPrevious(version_index) - Returns the URL and index of the previous image for the selected version
    9. showNext(version_index) - Returns the URL and index of the next image for the selected version
    10. showScreenshot(url) - Shows a screenhot of the url specified in a popup window of screenshot browser
    11. getBuild(buildDetails) - Gets the build details of the selected version
Uses -
    1. Show Tool - components/tools/show-tool/version-form/versionsform.component.html
*/

define(['angular', 'showToolPartialControllerApp'],function (app) {
  'use strict';

var versionComponentControllerApp = angular.module('versionComponentControllerApp', ['showToolPartialControllerApp']);

versionComponentControllerApp.controller('VersionController', function ($scope, $state, $rootScope, $window, GetAllTools,BuildById) {
    $scope.versionData = $rootScope.toolDetailsFactory.getVersionList();
    $scope.selectedMediaIndex = 0;
    $scope.show = false;

    $scope.viewMediaLength = 0;
    $scope.viewMediaLimit = 3;
    $scope.startPoint = 0;
    $scope.endPoint = 3;
    $scope.dependentToolDetails = [];
    $scope.showAllBuildReleaseNotes = true;
    $scope.showLessToolReleaseNotes = false;
    $scope.showAllVersionReleaseNotes = true;
    $scope.showLessVersionReleaseNotes = false;
    $scope.showAllChecksum = true;

    GetAllTools.get({
        id: "all",
        status: "active,indevelopment,deprecated",
        page: 0,
        perpage: 0
    },
    function(application)
    {
        $scope.applications = application.data.data;
        for(var t1=0; t1<$scope.versionData.length; t1++)
        {
            if($scope.versionData[t1].dependent_tools)
            {
                $scope.dependentToolDetails.push({'version_number' : $scope.versionData[t1].version_number, 'dependent_tools' : []});
                for(var t2=0; t2<$scope.versionData[t1].dependent_tools.length; t2++)
                {
                    for(var t3=0; t3<$scope.applications.length; t3++)
                    {
                        if($scope.versionData[t1].dependent_tools[t2].tool_id===$scope.applications[t3]._id.$oid)
                        {
                            for(var t4=0; t4<$scope.applications[t3].versions.length; t4++)
                            {
                                if($scope.versionData[t1].dependent_tools[t2].version_id===$scope.applications[t3].versions[t4].version_id)
                                {
                                    $scope.dependentToolDetails[t1].dependent_tools.push({'tool_name' : $scope.applications[t3].name, 'tool_id' : $scope.applications[t3]._id.$oid, 'version_id' : $scope.applications[t3].versions[t4].version_id, 'version_name' : $scope.applications[t3].versions[t4].version_name, 'version_number' : $scope.applications[t3].versions[t4].version_number});
                                }
                            }
                        }
                    }
                }
            }
        }

        for(var t5=0; t5<$scope.versionData.length; t5++)
        {
            for(var t6=0; t6<$scope.dependentToolDetails.length; t6++)
            {
                if($scope.versionData[t5].version_number===$scope.dependentToolDetails[t6].version_number)
                {
                    delete $scope.versionData[t5].dependent_tools;
                    $scope.versionData[t5].dependent_tools = $scope.dependentToolDetails[t6].dependent_tools;
                }
            }
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.showMoreChecksum = function()
    {
        $scope.showAllChecksum = false;
    };

    $scope.showLessChecksum = function()
    {
        $scope.showAllChecksum = true;
    };

    $scope.showMoreBuildReleaseNotesContent = function()
    {
        $scope.showAllBuildReleaseNotes = false;
        $scope.showLessBuildReleaseNotes = true;
        $('#release_notes_build').removeClass('text--ellipsis');
    };

    $scope.showLessBuildReleaseNotesContent = function()
    {
        $scope.showAllBuildReleaseNotes = true;
        $scope.showLessBuildReleaseNotes = false;
        $('#release_notes_build').addClass('text--ellipsis');
    };

    $scope.showMoreVersionReleaseNotesContent = function()
    {
        $scope.showAllVersionReleaseNotes = false;
        $scope.showLessVersionReleaseNotes = true;
        $('#release_notes_version').removeClass('text--ellipsis');
    };

    $scope.showLessVersionReleaseNotesContent = function()
    {
        $scope.showAllVersionReleaseNotes = true;
        $scope.showLessVersionReleaseNotes = false;
        $('#release_notes_version').addClass('text--ellipsis');
    };

    $scope.showMore = function()
    {
        $scope.show = true;
    };

    $scope.showLess = function()
    {
        $scope.show = false;
    };

    $scope.downloadBuild = function(buildId)
    {
         BuildById.get({
                id: buildId,
                actual_host:true
            },
            function(response){
                $scope.file_path = response.data.file_path;
                $window.open($scope.file_path, '_blank');
            }, 
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            }
         );
    };

    $scope.showScreenshot = function(url)
    {
        if(document.getElementById("view_screenshot").style.display === "none" || document.getElementById("view_screenshot").style.display === "")
        {
            $('#view_screenshot').show(700);
            $(window).scrollTop(0);
            $rootScope.screenshotURL = url;
            for(var s=0; s<$scope.versionData[$rootScope.displayTab].media_file.media_files.length; s++)
            {
                if($scope.versionData[$rootScope.displayTab].media_file.media_files[s].url === url)
                {
                    $rootScope.currentScreenshotURLIndex = s;
                }
            }
        }
        else
        {
           $('#view_screenshot').hide(700);
        }
    };

    $scope.showNext = function(versionIndex)
    {
        if($scope.versionData[versionIndex].media_file)
        {
            var mediaLength = $scope.versionData[versionIndex].media_file.media_files.length;
            if(($scope.endPoint < mediaLength) && ((mediaLength - $scope.endPoint) > 3))
            {
                $scope.startPoint = $scope.endPoint;
                $scope.endPoint = $scope.endPoint + 2;
            }
            else if(($scope.endPoint < mediaLength) && ((mediaLength - $scope.endPoint) <= 3))
            {
                $scope.startPoint = $scope.endPoint+1;
                $scope.endPoint = mediaLength;
            }
            else if($scope.endPoint === mediaLength)
            {
                $scope.startPoint = 0;
                if(mediaLength>3)
                {
                    $scope.endPoint = 3;
                }
                else
                {
                    $scope.endPoint = mediaLength;
                }
            }
        }
    };

    $scope.showPrevious = function(versionIndex)
    {
        if($scope.versionData[versionIndex].media_file)
        {
            var mediaLength = $scope.versionData[versionIndex].media_file.media_files.length;
            if(($scope.startPoint === 0) && (mediaLength > 3))
            {
                $scope.startPoint = mediaLength - 3;
                $scope.endPoint = mediaLength;
            }
            else if($scope.startPoint > 3)
            {
                $scope.endPoint = $scope.startPoint;
                $scope.startPoint = $scope.startPoint -3;
            }
            else if($scope.startPoint <= 3)
            {
                $scope.endPoint = $scope.startPoint;
                $scope.startPoint =0;
            }
        }
    };

    $scope.getBuild = function(selectedBuild)
    {
       $rootScope.isBuildSelected = true;
       $rootScope.buildDetails = JSON.parse(selectedBuild);
       $rootScope.buildToDeploy = $scope.buildDetails;
       $rootScope.buildFilePath = $scope.buildDetails.file_path;
    };
});

});