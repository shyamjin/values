define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

var createNewTagControllerApp = angular.module('createNewTagControllerApp', ['ui.router','tagsServicesApp']);
createNewTagControllerApp.controller('CreateNewTagController', function($scope, $state, $rootScope, CreateTag){
    $scope.activeTab = 'Add New Tag To List';
    $scope.getActiveTab = function(tab)
    {
        if($scope.activeTab===tab)
        {
            return 'vp-tabs__tab--active';
        }
    };
    var jsonData = {};

    $scope.tagData = {
        name : ''
    };

    $scope.createNewTag = function(form)
    {
        if($scope.tagData.name === '' || $scope.tagData.name === null || $scope.tagData.name === undefined)
        {
            $rootScope.handleResponse('Tag name can not be empty');
            return false;
        }
        jsonData = $scope.tagData;
        $scope.createNewTagStatus = CreateTag.save(jsonData, function(tagCreateSuccessResponse)
        {
            $state.go('manageTags');
            $scope.showActiveTab('/manage/tags');
            $rootScope.handleResponse(tagCreateSuccessResponse);
        },
        function(tagCreateErrorResponse)
        {
            $rootScope.handleResponse(tagCreateErrorResponse);
        });
    };
});
});