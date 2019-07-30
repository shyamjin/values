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

var createToolInfoComponentControllerApp = angular.module('createToolInfoComponentControllerApp', []);

createToolInfoComponentControllerApp.controller('CreateToolInfoController', function ($scope, $state, $rootScope, TagsAll) {
    $scope.indicators = [
        "true",
        "false"
    ];

    $scope.toolData = {
        name : '',
        tag : [],
        description : '',
        support_details : '',
        is_tool_cloneable : 'false',
        artifacts_only : 'false'
    };

    $scope.toolDataError = {
        logo:''
    };

    $scope.setToolData = function()
    {
        $rootScope.toolDetailsFactory.setToolData($scope.toolData);
    };

    $scope.validateToolData = function(toolData)
    {
        // tool general details validations
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

    //function for slideUp of all inactive button
    window.onclick=function ()
    {
        if(event.target.classList.contains('skip_slideup'))
        {
        }
        else
        {
            var allElements = document.getElementsByClassName('tag_popup');
            if (allElements.length > 0)
            {
                for(var i = 0; i < allElements.length; i++)
                {
                    $(allElements[i]).slideUp();
                }
            }
        }
    };

    function remaining_up()
    {
        var allElements = document.getElementsByClassName('tag_popup');
        for(var i = 0; i < allElements.length; i++)
        {
            $(allElements[i]).slideUp();
        }
    }

    $scope.showEditLogo = function()
    {
        if(document.getElementById("edit_logo").style.display === "none" || document.getElementById("edit_logo").style.display === "")
        {
            $('#edit_logo').show(700);
        }
        else
        {
            $('#edit_logo').hide(700);
        }
    };

    $scope.closeEditLogo = function()
    {
        $('#edit_logo').hide(700);
        $scope.logo = null;
        $scope.logoFilename = null;
        $scope.logoFileSelected = null;
    };

    $scope.loadEditLogo = function(logo)
    {
        var srcId = null;
        if(!logo)
        {
            $scope.toolDataError.logo = 'Please select a logo for tool to upload';
            return false;
        }
        else if(logo.type==='image/jpeg' || logo.type==='image/png' || logo.type==='image/jpg' || logo.type==='image/bmp' || logo.type==='image/gif')
        {
            $scope.logoFileSelected = logo.name;
            $scope.logoFile = logo;
            srcId = document.getElementById('logoFile');
            srcId.src = URL.createObjectURL(logo);
            $scope.logo = logo;
            $('#edit_logo').hide(700);
            $scope.toolDataError.logo = '';
        }
        else
        {
            srcId = document.getElementById('logoFile');
            srcId.src = null;
            $scope.logo = null;
            $scope.logoFilename = null;
            $scope.logoFileSelected = null;
        }
    };

    $scope.loadNewLogo = function()
    {
        $('#edit_logo').hide(700);
    };

    $scope.showAddTag = function()
    {
        if(document.getElementById("add_tag").style.display === "none" || document.getElementById("add_tag").style.display === "")
        {
            remaining_up();
            $('#add_tag').slideDown();
        }
        else
        {
            $('#add_tag').slideUp();
        }
    };

    $scope.closeAddTag = function()
    {
        $('#add_tag').slideUp();
    };


    $scope.selectTag = function(tag)
    {
        var tag_flag = 0;
        var ind = 0;
        if($scope.toolData.tag.length>0)
        {
            for(var c=0;  c<$scope.toolData.tag.length; c++)
            {
                if(tag.name===$scope.toolData.tag[c])
                {
                    tag_flag++;
                    ind = c;
                }
            }

            if(tag_flag===0)
            {
                $scope.toolData.tag.push(tag.name);
            }
            else
            {
                $scope.toolData.tag.splice(ind, 1);
            }

        }
        else
        {
            $scope.toolData.tag = [];
            $scope.toolData.tag.push(tag.name);
        }
    };

    $scope.removeTag = function(tag)
    {
        var tag_flag = 0;
        var ind = 0;
        for(var c=0;  c<$scope.toolData.tag.length; c++)
        {
            if(tag===$scope.toolData.tag[c])
            {
                tag_flag++;
                ind = c;
            }
        }

        if(tag_flag > 0)
        {
            $scope.toolData.tag.splice(ind, 1);
        }
    };

    $scope.isTagSelected = function(tag)
    {
        var flag = 0;
        for(var j=0; j<$scope.toolData.tag.length; j++)
        {
            if(tag === $scope.toolData.tag[j])
            {
                flag++;
            }
        }
        if(flag>0)
        {
            return true;
        }
        else
        {
            return false;
        }
    };

    $scope.clearLogo = function()
    {
        $scope.logo = null;
        var logoFileName = $scope.toolData.logo;
        var lenLogo = logoFileName.length;
        $scope.logoFilename = logoFileName.substring(20, lenLogo);
        $scope.logoFileSelected = $scope.logoFilename;
    };

    $rootScope.$on("setToolData", function (event, args) {
        $rootScope.toolDetailsFactory.setToolData($scope.toolData);
    });

    $rootScope.$on("setToolLogo", function (event, args) {
        $rootScope.toolDetailsFactory.setToolLogo($scope.logo);
    });

});

});