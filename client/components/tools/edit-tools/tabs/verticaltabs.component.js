/*
Author - nlate
Description -
    1. Controller that handles with the toggling between version tabs of the tool
Methods -
    1. showVersionDetailsTab(index) - Sets a version index as active selected version and resets the defalt build details
    2. getActiveTab(index) - Returns the Active tab CSS class
    3. deployTool(version_id, build_id) - function to redirect to deploy tool page
Uses -
    1. Show Tool - components/tools/show-tool/tabs/verticaltabs.component.js
*/

define(['angular'],function (app) {
  'use strict';

var editToolVerticalTabComponentControllerApp = angular.module('editToolVerticalTabComponentControllerApp', []);

editToolVerticalTabComponentControllerApp.controller('EditToolVerticalTabController', function ($scope, $state, $rootScope) {
    $rootScope.versionData = $rootScope.toolDetailsFactory.getVersionList();
    var lastIndex = $rootScope.versionData.length - 1;
    $rootScope.activeVersion = $rootScope.versionData[lastIndex].version_number;
    $rootScope.displayTab = 0;
    $rootScope.vIndex = 0;

    $scope.showVersionDetailsTab = function(version_index)
    {
        $rootScope.displayTab = version_index;
        $rootScope.vIndex = version_index;
    };

    $scope.getActiveTab = function(index)
    {
        if($rootScope.displayTab === index)
        {
             return "vp-tabsvertical__tab--active";
        }
    };

    $scope.addNewVersion = function()
    {
        var index = $rootScope.versionData.length;
        $scope.addVersion = false;
        var newVersionData = {};
        var activeVersionData = $rootScope.toolDetailsFactory.getActiveVersionData();
        //  copy the data of the latest version as the first values for the newly added version
        newVersionData = activeVersionData;
        newVersionData.version_number = activeVersionData.version_number;
    //    Add empty values to the newly added version
        var todayDate = new Date();
        delete newVersionData._id;
        newVersionData.version_name = activeVersionData.version_name;
        newVersionData.version_number = '';
        newVersionData.version_date = todayDate;
        newVersionData.pre_requiests = activeVersionData.pre_requiests;
        newVersionData.gitlab_repo = activeVersionData.gitlab_repo;
        newVersionData.gitlab_branch = activeVersionData.gitlab_branch;
        newVersionData.jenkins_job = activeVersionData.jenkins_job;
        newVersionData.backward_compatible = activeVersionData.backward_compatible;
        newVersionData.status = activeVersionData.status;
        newVersionData.mps_certified = activeVersionData.mps_certified;
        newVersionData.release_notes = activeVersionData.release_notes;
        if(activeVersionData.document!== null)
        {
            if(activeVersionData.document.documents)
            {
                newVersionData.document = {
                    documents : activeVersionData.document.documents
                };
            }
        }
        if(activeVersionData.deployment_field)
        {
            newVersionData.deployment_field = {
                fields : activeVersionData.deployment_field.fields
            };
        }

        delete newVersionData.media_file;

        if(activeVersionData.status==='1')
        {
            newVersionData.status = "Active";
        }
        else
        {
            newVersionData.status = "Deprecated";
        }

        $rootScope.toolDetailsFactory.addNewVersion(newVersionData);
        $rootScope.versionData = $rootScope.toolDetailsFactory.getVersionList();
//        $rootScope.displayTab = $rootScope.versionData.length - 1;
    };

    $scope.removeVersion = function()
    {
        var lastItem = $rootScope.versionData.length;
        var ind = 0;
        for(var l=0; l<lastItem; l++)
        {
            if(!$rootScope.versionData[l]._id)
            {
                ind = l;
            }
        }

        $rootScope.toolDetailsFactory.removeVersion(ind);
        $rootScope.versionData = $rootScope.toolDetailsFactory.getVersionList();
    };
});

});