define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

var editTagControllerApp = angular.module('editTagControllerApp', ['ui.router','tagsServicesApp']);
editTagControllerApp.controller('EditTagController', function($scope, $state, $stateParams, $rootScope, TagsAll, ViewTag, EditTag, DeleteTag){
    $scope.tagSelected = false;
    $scope.activeTab = 'Tag List';
    $scope.showActiveTab = function(tab)
    {
        $scope.activeTab = tab;
    };

    $scope.getActiveTab = function(tab)
    {
        if($scope.activeTab===tab)
        {
            return 'vp-tabs__tab--active';
        }
    };

    $scope.getUserFormClass = function()
    {
        if($scope.tagSelected === true)
        {
            if($scope.activeTab!='Tag List')
            {
                $scope.tagSelected = false;
            }
            return "vp-distributionform__selectedtagform--active  vp-distributionform vp-control max";
        }
        else
        {
            return "vp-selecteddistributionform vp-distributionform vp-control max";
        }
    };

    $scope.getUserUlClass = function()
    {
        if($scope.tagSelected === true)
        {
            if($scope.activeTab != 'Tag List')
            {
                $scope.tagSelected = false;
            }
            return "vp-distributionform__selectedtagform__fieldslist text--cs03 pr--lg";
        }
        else
        {
            return "vp-distributionform__selectedtagform__fieldslist text--cs03 pr--lg hidden";
        }
    };

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

    $scope.selectTag = function(tag_id)
    {
        $scope.id = tag_id;
        $scope.tagSelected = true;
        ViewTag.get({
            id : $scope.id
        },
        function(successResponse)
        {
            $scope.tagData = successResponse;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.editTag = function(form)
    {
        if($scope.tagData.data.name === '' || $scope.tagData.data.name === null || $scope.tagData.data.name === undefined)
        {
            $rootScope.handleResponse('Tag name can not be empty');
        }

        var tagData = {
            _id : {
                oid : ''
            }
        };

        tagData._id.oid = $scope.id;
        tagData.name = $scope.tagData.data.name;

        $scope.editTagStatus = EditTag.update(tagData, function(tagEditSuccessResponse)
        {
            $state.go('manageTags');
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
            $scope.tagSelected = false;
            $rootScope.handleResponse(tagEditSuccessResponse);
        },
        function(tagEditErrorResponse)
        {
            $rootScope.handleResponse(tagEditErrorResponse);
        });
    };

    $scope.discardTagChanges = function()
    {
        delete $scope.id;
        $scope.tagSelected = false;
        $state.go('manageTags');
    };

    $scope.openDeleteTagConfirmationPopup = function(tag_id)
    {
        $scope.tag_id = tag_id;
        $('#show_delete_tag_confirmation_popup').show(700);
    };

    $scope.closeDeleteTagConfirmationPopup = function()
    {
        $('#show_delete_tag_confirmation_popup').hide(700);
    };

    $scope.deleteTag = function(tag_id)
    {
        $scope.deleteTagStatus = DeleteTag.remove({
            id :   $scope.tag_id
        },
        function (tagDeleteSuccess)
        {
            $state.go('manageTags');
            delete $scope.id;
            $scope.tagSelected = false;
            $scope.closeDeleteTagConfirmationPopup();
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
            $rootScope.handleResponse(tagDeleteSuccess);
        },
        function (tagDeleteError)
        {
            $scope.closeDeleteTagConfirmationPopup();
            $rootScope.handleResponse(tagDeleteError);
        });
    };
});
});