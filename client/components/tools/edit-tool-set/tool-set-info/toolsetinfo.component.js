/*
Author - nlate
Description -
    1. Controller that handles with the required in create tool set for tool set data manipulation
Methods -
    1.
Uses -
    1. Create Tool Set - partials/tools/create-tool-sets/create-tool-sets.partial.html
*/

define(['angular','toolTips'],function (app) {
  'use strict';

var editToolSetInfoComponentControllerApp = angular.module('editToolSetInfoComponentControllerApp', ['720kb.tooltips']);

editToolSetInfoComponentControllerApp.controller("EditToolSetInfoController",function($scope, $state, $rootScope, TagsAll, ToolSetDelete) {
    $rootScope.generalToolSetData = $rootScope.toolSetDetailsFactory.getToolSetData();

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
            remaining_up();
            $('#edit_logo').slideDown();

        }
        else
        {
            $('#edit_logo').slideUp();
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
        if(logo.type==='image/jpeg' || logo.type==='image/png' || logo.type==='image/jpg' || logo.type==='image/bmp' || logo.type==='image/gif')
        {
            $scope.logoFileSelected = logo.name;
            $scope.logoFile = logo;
            srcId = document.getElementById('logoFile');
            srcId.src = URL.createObjectURL(logo);
            $scope.logo = logo;
            $('#edit_logo').hide(700);
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
        if($rootScope.generalToolSetData.tag.length>0)
        {
            for(var c=0;  c<$rootScope.generalToolSetData.tag.length; c++)
            {
                if(tag.name===$rootScope.generalToolSetData.tag[c])
                {
                    tag_flag++;
                    ind = c;
                }
            }

            if(tag_flag===0)
            {
                $rootScope.generalToolSetData.tag.push(tag.name);
            }
            else
            {
                $rootScope.generalToolSetData.tag.splice(ind, 1);
            }

        }
        else
        {
            $rootScope.generalToolSetData.tag = [];
            $rootScope.generalToolSetData.tag.push(tag.name);
        }
    };

    TagsAll.get({
    },
    function(successResponse)
    {
        $scope.allTags = successResponse;
        $scope.tagsAll = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.isTagSelected = function(tag)
    {
        var flag = 0;
        if($rootScope.generalToolSetData.tag)
        {
             for(var j=0; j<$rootScope.generalToolSetData.tag.length; j++)
            {
                if(tag === $rootScope.generalToolSetData.tag[j])
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
        }
    };

    $scope.showAddTool = function()
    {
        if(document.getElementById("show_tools").style.display === "none" || document.getElementById("show_tools").style.display === "")
        {
            $('#show_tools').show(700);
        }
        else
        {
            $('#show_tools').hide(700);
        }
    };

    $scope.closeToolSetModal = function()
    {
        $('#show_tools').hide(700);
    };

    $scope.showRemoveToolSetConfirmationPopup = function(toolset_id)
    {
        $scope.selectedToolSetId = toolset_id;
        $("#show_delete_tool_set_confirmation_popup").show(700);
    };

    $scope.removeToolSet = function()
    {
        $("#show_delete_tool_set_confirmation_popup").hide(700);
        $scope.removeToolSetStatus = ToolSetDelete.remove({
            id : $scope.selectedToolSetId
        },
        function(toolsetDeleteSuccess)
        {
            $rootScope.handleResponse(toolsetDeleteSuccess);
            $state.go('viewAllToolSets');
        },
        function (toolsetDeleteError)
        {
            $rootScope.handleResponse(toolsetDeleteError);
        });
    };

    $scope.closeRemoveToolSetConfirmationPopup = function()
    {
        $("#show_delete_tool_set_confirmation_popup").hide(700);
    };

    $scope.removeToolFromToolList = function(index)
    {
        $rootScope.toolSetDetailsFactory.removeTool($scope.toolList,index);
        $scope.toolList = $rootScope.toolSetDetailsFactory.getToolList();
        $rootScope.$emit('setSelectedToolList', {selectedTools : $scope.toolList});
    };

    $rootScope.$on('updateToolList', function(event, args){
        $scope.toolList = args.selectedTools;
    });

    $rootScope.$on('setToolSetData', function(event, args){
        $rootScope.toolSetDetailsFactory.setToolSetData($rootScope.generalToolSetData);
    });

    $rootScope.$on('setToolListData', function(event, args){
        $rootScope.toolSetDetailsFactory.setToolList($scope.toolList);
    });

    $rootScope.$on('setToolSetLogo', function(event, args){
        $rootScope.toolSetDetailsFactory.setToolSetLogo($scope.logo);
    });
});

});