/*
Author - nlate
Description -
    1. Shows the tool general details
    2. Controller that handles with the operations to get and set tool general details
Methods -
    1. setToolData() - Sets tool general details data in factory
    2. validateToolData() - Validates tools general data
    3. addTag(tag) - Adds tag to tool data
    4. showEditLogo() - Shows popup for add/edit logo
    5. closeEditLogo() - Closes popup for add/edit logo without loading logo
    6. loadEditLogo(logoFile) - Loads the selected logo file
    7. loadNewLogo() - Closes popup for add/edit logo without loading logo
    8. showAddTag() - Shows popup for add tag
    9. closeAddTag() - Closes popup for add tag
    10. selectTag(tag) - Selects tag from the tag list
    11. removeTag(tag) - Removes tag from the selected tag list

Uses -
    1. Create Tool - components/tools/create-tools/tool-info/toolinfo.component.html
*/

define(['angular'],function (app) {
  'use strict';

var proposeToolInfoComponentControllerApp = angular.module('proposeToolInfoComponentControllerApp', []);

proposeToolInfoComponentControllerApp.controller('ProposeToolInfoController', function ($scope, $state, $rootScope) {

    $rootScope.toolData = {
        name : '',
        description : '',
        support_details : $rootScope.userProfile.userData.email,
        version : {
            version_name : 'ga',
            version_number : '1.0'
        },
        request_reason : ''
    };
    
    

    $scope.setProposedToolData = function()
    {
        $rootScope.proposedToolDetailsFactory.setProposedToolData($rootScope.toolData);
    };

    $rootScope.$on("setProposedToolData", function (event, args) {
        $rootScope.proposedToolDetailsFactory.setProposedToolData($rootScope.toolData);
    });

});

});