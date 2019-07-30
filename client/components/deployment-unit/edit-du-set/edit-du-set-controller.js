define(['angular', 'ngResource', 'uiRouter', 'ngCookies','toolTips', 'jquery', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp'], function (app) {
  'use strict';

var editDUSetControllerApp = angular.module('editDUSetControllerApp', ['ui.router','720kb.tooltips', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp']);

editDUSetControllerApp.controller('EditDUSetController', function ($scope, $rootScope, $state, $stateParams, $cookieStore, DUTypesAll, PrerequisitesViewAll, ApprovalStatusAll, UserDetails, ViewDUSet, EditDUSet, DeploymentUnitAll, TagsAll,duLogoFileUpload, DUSetAll, GetAllDUBuildData) {
    var date = new Date();
    $scope.prerequisites = [];
    $scope.filterType = 'All';
    $scope.statusFlag = true;
    $scope.approvalStatusFlag = false;
    $scope.tagsFlag = false;
    $scope.DusetsFlag = false;
    var statusFilter = [];
    var approvalStatusFilter = [];
    var tagFilter = [];
    var dusetFilter = [];
    $scope.tags = new TagsAll();
    $scope.userData = $rootScope.userFactory.getUserDetails();
    $scope.application = {
        data : {
            name : '',
            tag : [],
            release_notes : '',
            pre_requiests : [],
            du_set : []
        }
    };
    $scope.selectedDU = [];
    $scope.arrangedDU = [];
    $scope.selectedDUToArrange = [];
    $scope.duList = [];
    $scope.duIndexToArrange = [];
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

    ViewDUSet.get({
        id : $stateParams.id
    },
    function(viewDUSetSuccessResponse)
    {
        $scope.application = viewDUSetSuccessResponse;
        if(viewDUSetSuccessResponse.data.logo)
        {
            var logoFileName = viewDUSetSuccessResponse.data.logo;
            var lenLogo = logoFileName.length;
            $scope.logoFilename = logoFileName.substring(20, lenLogo);
            $scope.logoFileSelected = $scope.logoFilename;
        }
        GetAllDUBuildData.get({
            id : viewDUSetSuccessResponse.data._id.$oid
        },
        function(viewDUBuildSuccessResponse)
        {
            var duList = viewDUBuildSuccessResponse.data.du_set_details;
            $scope.oldStatus = $scope.application.data.approval_status;
            $scope.clearLogo = function()
            {  $scope.logo = null;
                var logoFileName = viewDUSetSuccessResponse.data.logo;
                var lenLogo = logoFileName.length;
                $scope.logoFilename = logoFileName.substring(20, lenLogo);
                $scope.logoFileSelected = $scope.logoFilename;
            };
            for(var i=0; i<duList.length; i++)
            {
                if(duList[i].build)
                {
                    $scope.duList.push({'du_id' : duList[i]._id.$oid, 'name' : duList[i].name,'build_number':duList[i].build[0].build_number, 'type' : duList[i].type, 'approval_status' : duList[i].approval_status, 'dependent' : duList[i].dependent, 'order' : duList[i].order, 'tag' : duList[i].tag});
                    $scope.selectedDU.push({'du_id' : duList[i]._id.$oid, 'name' : duList[i].name,'build_number':duList[i].build[0].build_number, 'type' : duList[i].type, 'approval_status' : duList[i].approval_status, 'dependent' : duList[i].dependent, 'order' : duList[i].order, 'tag' : duList[i].tag});
                }
                else
                {
                    $scope.duList.push({'du_id' : duList[i]._id.$oid, 'name' : duList[i].name,'type' : duList[i].type, 'approval_status' : duList[i].approval_status, 'dependent' : duList[i].dependent, 'order' : duList[i].order, 'tag' : duList[i].tag});
                    $scope.selectedDU.push({'du_id' : duList[i]._id.$oid, 'name' : duList[i].name, 'type' : duList[i].type, 'approval_status' : duList[i].approval_status, 'dependent' : duList[i].dependent, 'order' : duList[i].order, 'tag' : duList[i].tag});

                }
                $scope.originalDUList = [];
                angular.copy($scope.duList, $scope.originalDUList);
            }
        },
        function(viewDUBuildErrorResponse)
        {
            $rootScope.handleResponse(viewDUBuildErrorResponse);
        });

    },
    function(viewDUErrorResponse)
    {
        $rootScope.handleResponse(viewDUErrorResponse);
    });

    ApprovalStatusAll.get({
    },
    function(successResponse)
    {
        $scope.approvalStatusAll = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    DUTypesAll.get({
    },
    function(successResponse)
    {
        $scope.DUTypes = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    DeploymentUnitAll.get({
        page: 0,
        perpage: 0
    },
    function(successResponse)
    {
        $scope.applications = successResponse.data;
        $scope.currentPage = successResponse.page;
        $scope.totalCount = successResponse.total;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.isDUSelected = function(du)
    {
        var flag = 0;
        if(!$scope.selectedDU.length)
        {
            $scope.selectedDU =[];
        }
        for(var j=0; j<$scope.selectedDU.length; j++)
        {
            if(du.name === $scope.selectedDU[j].name)
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

    $scope.allowDrop = function(ev) {
        ev.preventDefault();
    };

    $scope.drag = function(ev, du) {
        ev.dataTransfer.setData("text", ev.target.id);
    };

    $scope.drop = function(ev) {
        ev.preventDefault();
        var data = ev.dataTransfer.getData("text");
        ev.target.appendChild(document.getElementById(data));
    };

    $scope.dropSuccessHandler = function($event,index,array){
        array.splice(index,1);
    };

    $scope.onDrop = function($event,$data,array){
        array.push($data);
    };

    $scope.setMargin = function(index)
    {
        if(index>3)
        {
            return 'mt--xxxxl';
        }
        else
        {
            return '';
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

     $scope.showEditLogo = function()
    {
        if(document.getElementById("edit_logo").style.display === "none" || document.getElementById("edit_logo").style.display === "")
        {

            $('#edit_logo').slideDown();

        }
        else
        {
            $('#edit_logo').slideUp();
        }
    };

    $scope.selectTag = function(tag)
    {
        var tag_flag = 0;
        var ind = 0;
        if($scope.application.data.tag.length>0)
        {
            for(var c=0;  c<$scope.application.data.tag.length; c++)
            {
                if(tag.name===$scope.application.data.tag[c])
                {
                    tag_flag++;
                    ind = c;
                }
            }

            if(tag_flag===0)
            {
                $scope.application.data.tag.push(tag.name);
            }
            else
            {
                $scope.application.data.tag.splice(ind, 1);
            }
        }
        else
        {
            $scope.application.data.tag = [];
            $scope.application.data.tag.push(tag.name);
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
        if(!$scope.application.data.tag)
        {
            $scope.application.data.tag = [];
        }
        for(var j=0; j<$scope.application.data.tag.length; j++)
        {
            if(tag === $scope.application.data.tag[j])
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

    $scope.isPrerequisiteSelected = function(prerequisite)
    {
        var flag = 0;
        if(!$scope.application.data.pre_requiests)
        {
            $scope.application.data.pre_requiests = [];
        }
        for(var j=0; j<$scope.application.data.pre_requiests.length; j++)
        {
            if((prerequisite.prerequisites_name === $scope.application.data.pre_requiests[j].name) && (prerequisite.version === $scope.application.data.pre_requiests[j].version))
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

    $scope.showEditPrerequisites = function(index)
    {
        $scope.vIndex = index;
        if(document.getElementById("edit_prerequisite").style.display === "none" || document.getElementById("edit_prerequisite").style.display === "")
        {
             remaining_up();
             $('#edit_prerequisite').slideDown();
        }
        else
        {
           $('#edit_prerequisite').slideUp();
        }
    };

    $scope.closeEditPrerequisites = function()
    {
        $('#edit_prerequisite').slideUp();
    };

    $scope.showSettings = function()
    {
        if(document.getElementById("add_settings").style.display === "none" || document.getElementById("add_settings").style.display === "")
        {
            document.getElementById("add_settings").style.display = "block";
            $scope.addNewField();
        }
        else
        {
           document.getElementById("add_settings").style.display = "none";
        }
    };

    $scope.showEditSettings = function(index)
    {
        $scope.fieldIndex = index;
        if(document.getElementById("add_settings").style.display === "none" || document.getElementById("add_settings").style.display === "")
        {
            document.getElementById("add_settings").style.display = "block";
        }
        else
        {
           document.getElementById("add_settings").style.display = "none";
        }
    };

    $scope.closeSettings = function(vIndex)
    {
        document.getElementById("add_settings").style.display = "none";
    };

    $scope.showAddDU = function()
    {
        if(document.getElementById("show_du_list").style.display === "none" || document.getElementById("show_du_list").style.display === "")
        {
            document.getElementById("show_du_list").style.display = "block";
        }
        else
        {
           document.getElementById("show_du_list").style.display = "none";
        }
    };

    $scope.showDUOrderModal = function()
    {
        if(document.getElementById("show_du_arrangement").style.display === "none" || document.getElementById("show_du_arrangement").style.display === "")
        {
            document.getElementById("show_du_arrangement").style.display = "block";
            if($scope.arrangedDU.length === 0 && ($scope.selectedDU.length === $scope.duList.length))
            {
                $scope.selectedDUToArrange = [];
                angular.copy($scope.selectedDU, $scope.selectedDUToArrange);
            }
            else if($scope.duList.length < $scope.selectedDU.length)
            {
                $scope.arrangedDU = [];
                angular.copy($scope.duList, $scope.arrangedDU);
                for(var a=0; a<$scope.selectedDU.length; a++)
                {
                    var duFlag_1 = 0;
                    var duInd_1 = 0;
                    for(var b=0; b<$scope.duList.length; b++)
                    {
                        if($scope.selectedDU[a].du_id !== $scope.duList[b].du_id)
                        {
                            duFlag_1++;
                            duInd_1 = a;
                        }
                    }
                    if(duFlag_1 === $scope.duList.length)
                    {
                        if($scope.selectedDUToArrange)
                        {
                            var duFlag_2 = 0;
                            var duInd_2 = 0;
                            for(var c=0; c<$scope.selectedDUToArrange.length; c++)
                            {
                                if($scope.selectedDUToArrange[c].du_id !== $scope.selectedDU[duInd_1].du_id)
                                {
                                    duFlag_2++;
                                    duInd_2 = c;
                                }
                            }
                            if(duFlag_2 === $scope.selectedDUToArrange.length)
                            {
                                $scope.selectedDUToArrange.push($scope.selectedDU[duInd_1]);
                            }
                            else
                            {
                                $scope.selectedDUToArrange = [];
                                $scope.selectedDUToArrange.push($scope.selectedDU[duInd_1]);
                            }
                        }
                    }
                }
            }
        }
        else
        {
           document.getElementById("show_du_arrangement").style.display = "none";
        }
    };

    $scope.closeDUSetModal = function()
    {
        document.getElementById("show_du_list").style.display = "none";
    };

    $scope.closeDUSetOrderModal = function()
    {
        document.getElementById("show_du_arrangement").style.display = "none";
    };


    $scope.openFilter = function()
    {
        if(document.getElementById("open_filter").style.display === "none" || document.getElementById("open_filter").style.display === "")
        {
            document.getElementById("open_filter").style.display = "block";
            $scope.open_filter = true;
        }
        else
        {
            document.getElementById("open_filter").style.display = "none";
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

    $scope.updateDUSetList = function()
    {
        $scope.arranegDUOrderMessage = false;
        document.getElementById("show_du_list").style.display = "none";
        if($scope.duList.length === 0 && $scope.arrangedDU.length === 0)
        {
            angular.copy($scope.selectedDU, $scope.duList);
        }
        else
        {
            for(var a=0; a<$scope.selectedDU.length; a++)
            {
                var duFlag_1 = 0;
                var duInd_1 = 0;
                for(var b=0; b<$scope.duList.length; b++)
                {
                    if($scope.selectedDU[a].du_id !== $scope.duList[b].du_id)
                    {
                        duFlag_1++;
                        duInd_1 = a;
                    }
                }
                if(duFlag_1 === $scope.duList.length)
                {
                    if($scope.selectedDUToArrange)
                    {
                        var duFlag_2 = 0;
                        var duInd_2 = 0;
                        for(var c=0; c<$scope.selectedDUToArrange.length; c++)
                        {
                            if($scope.selectedDUToArrange[c].du_id !== $scope.selectedDU[duInd_1].du_id)
                            {
                                duFlag_2++;
                                duInd_2 = c;
                            }
                        }
                        if(duFlag_2 === $scope.selectedDUToArrange.length)
                        {
                            $scope.selectedDUToArrange.push($scope.selectedDU[duInd_1]);
                            $scope.arranegDUOrderMessage = true;
                        }
                        else
                        {
                            $scope.selectedDUToArrange = [];
                            $scope.selectedDUToArrange.push($scope.selectedDU[duInd_1]);
                            $scope.arranegDUOrderMessage = true;
                        }
                    }
                }
            }
        }
    };

    $scope.cancelDUSetList = function()
    {
        document.getElementById("show_du_list").style.display = "none";
        if($scope.duList.length <= $scope.selectedDU.length)
        {
            $scope.selectedDU = [];
            for(var a=0; a<$scope.duList.length; a++)
            {
                var duFlag_1 = 0;
                var duInd_1 = 0;
                for(var b=0; b<$scope.selectedDU.length; b++)
                {
                    if($scope.duList[a].du_id === $scope.selectedDU[b].du_id)
                    {
                        duFlag_1++;
                        duInd_1 = a;
                    }
                }
                if(duFlag_1 <1)
                {
                    $scope.selectedDU.push($scope.duList[duInd_1]);
                }
            }
        }

        if($scope.selectedDUToArrange.length>0)
        {
            for(var c=0; c<$scope.selectedDUToArrange.length; c++)
            {
                var duFlag_2 = 0;
                for(var d=0; d<$scope.selectedDU.length; d++)
                {
                    if($scope.selectedDUToArrange[c].du_id === $scope.selectedDU[d].du_id)
                    {
                        duFlag_2++;
                    }
                }
                if(duFlag_2 <1)
                {
                    $scope.selectedDU.push($scope.selectedDUToArrange[c]);
                }
            }
        }
    };

    $scope.deleteDUSetOrderList = function()
    {
        document.getElementById("show_du_arrangement").style.display = "none";
    };

    $scope.updateDUSetOrderList = function()
    {
        if($scope.arrangedDU.length>0)
        {
            document.getElementById("show_du_arrangement").style.display = "none";
            $scope.duList = [];
            $scope.application.data.du_set = [];
            angular.copy($scope.arrangedDU, $scope.duList);
            angular.copy($scope.arrangedDU, $scope.application.data.du_set);
        }
    };

    $scope.addDU = function(du)
    {
        var duset_flag = 0;
        var du_length = $scope.selectedDU.length;
        var ind = 0;
        if(du_length>0)
        {
            for(var c=0;  c<$scope.selectedDU.length; c++)
            {
                if((du._id.$oid===$scope.selectedDU[c].du_id))
                {
                    duset_flag++;
                    ind = c;
                }
            }
            if(duset_flag===0)
            {
                $scope.selectedDU.push({'du_id' : du._id.$oid, 'name' : du.name,'build_number' : du.build_number, 'type' : du.type, 'approval_status' : du.approval_status, 'dependent' : false, 'order' : $scope.selectedDU.length+1, 'tag' : du.tag});
            }
        }
        else
        {
             $scope.selectedDU = [];
             $scope.selectedDU.push({'du_id' : du._id.$oid, 'name' : du.name, 'build_number' : du.build_number,'type' : du.type, 'approval_status' : du.approval_status, 'dependent' : false, 'order' : $scope.selectedDU.length+1, 'tag' : du.tag});
        }
    };

    $scope.removeDU = function(du)
    {
        var duset_flag_1 = 0;
        var duset_flag_2 = 0;
        var duset_flag_3 = 0;
        var duset_flag_4 = 0;
        var ind_1 = 0;
        var ind_2 = 0;
        var ind_3 = 0;
        var ind_4 = 0;

        for(var d=0;  d<$scope.duList.length; d++)
        {
            if(($scope.duList[d].du_id===du.du_id))
            {
                duset_flag_1++;
                ind_1 = d;
            }
        }

        for(var e=0;  e<$scope.selectedDU.length; e++)
        {
            if(($scope.selectedDU[e].du_id===du.du_id))
            {
                duset_flag_2++;
                ind_2 = e;
            }
        }

        for(var f=0;  f<$scope.arrangedDU.length; f++)
        {
            if(($scope.arrangedDU[f].du_id===du.du_id))
            {
                duset_flag_3++;
                ind_3 = f;
            }
        }

        for(var g=0;  g<$scope.selectedDUToArrange.length; g++)
        {
            if(($scope.selectedDUToArrange[g].du_id===du.du_id))
            {
                duset_flag_4++;
                ind_4 = g;
            }
        }

        if(duset_flag_1===1)
        {
            $scope.duList.splice(ind_1, 1);
        }

        if(duset_flag_2===1)
        {
            $scope.selectedDU.splice(ind_2, 1);
        }

        if(duset_flag_3===1)
        {
            $scope.arrangedDU.splice(ind_3, 1);
        }

        if(duset_flag_4===1)
        {
            $scope.selectedDUToArrange.splice(ind_4, 1);
        }
    };

    $scope.addAllDU = function()
    {
        if($scope.selectedDUToArrange.length>0)
        {
            var tempDU = [];
            angular.copy($scope.selectedDUToArrange, tempDU);
            angular.forEach(tempDU, function(du){
                $scope.arrangedDU.push(du);
            });

            $scope.selectedDUToArrange = [];
        }
    };

    $scope.removeAllDU = function()
    {
        if($scope.arrangedDU.length>0)
        {
            var tempDU = [];
            angular.copy($scope.arrangedDU, tempDU);
            angular.forEach(tempDU, function(du){
                $scope.selectedDUToArrange.push(du);
            });
            $scope.arrangedDU = [];
        }
    };

    $scope.selectDUToAddDU = function(du)
    {
        for(var d=0;  d<$scope.selectedDUToArrange.length; d++)
        {
            if((du.du_id===$scope.selectedDUToArrange[d].du_id))
            {
                if($scope.selectedDUToArrange[d].dependent === false || $scope.selectedDUToArrange[d].dependent === 'false')
                {
                    $scope.selectedDUToArrange[d].dependent = true;
                }
                else
                {
                    $scope.selectedDUToArrange[d].dependent = false;
                }
            }
        }
    };

    $scope.addDUToArrangeList = function(du)
    {
        var duset_flag_old = 0;
        var duset_flag_new = 0;
        var ind = 0;
        for(var d=0;  d<$scope.arrangedDU.length; d++)
        {
            if(($scope.arrangedDU[d].du_id===du.du_id))
            {
                duset_flag_new++;
            }
        }
        for(var e=0;  e<$scope.selectedDUToArrange.length; e++)
        {
            if(($scope.selectedDUToArrange[e].du_id===du.du_id))
            {
                duset_flag_old++;
                ind = e;
            }
        }
        if(duset_flag_new===0)
        {
            $scope.arrangedDU.push({'du_id' : du.du_id, 'name' : du.name, 'build_number' : du.build_number,'type' : du.type, 'approval_status' : du.approval_status, 'dependent' : du.dependent, 'order' : $scope.arrangedDU.length+1, 'tag' : du.tag});
        }
        else
        {
            $rootScope.handleResponse('Please select DU to add to arrange list');
        }

        if(duset_flag_old===1)
        {
            $scope.selectedDUToArrange.splice(ind, 1);
        }
    };

    $scope.manageDU = function(du)
    {
        for(var d=0;  d<$scope.arrangedDU.length; d++)
        {
            if((du.du_id===$scope.arrangedDU[d].du_id))
            {
                if($scope.arrangedDU[d].dependent === false || $scope.arrangedDU[d].dependent === 'false')
                {
                    $scope.arrangedDU[d].dependent = true;
                }
                else
                {
                    $scope.arrangedDU[d].dependent = false;
                }
            }
        }
    };

    $scope.removeDUFromArrangeList = function(du)
    {
        var duset_flag_old = 0;
        var duset_flag_new = 0;
        var ind = 0;
        for(var d=0;  d<$scope.selectedDUToArrange.length; d++)
        {
            if(($scope.selectedDUToArrange[d].du_id===du.du_id))
            {
                duset_flag_old++;
            }
        }
        for(var e=0;  e<$scope.arrangedDU.length; e++)
        {
            if(($scope.arrangedDU[e].du_id===du.du_id))
            {
                duset_flag_new++;
                ind = e;
            }
        }
        if(duset_flag_old===0)
        {
            $scope.selectedDUToArrange.push({'du_id' : du.du_id, 'name' : du.name,'build_number' : du.build_number, 'type' : du.type, 'approval_status' : du.approval_status, 'dependent' : du.dependent, 'order' : $scope.arrangedDU.length+1, 'tag' : du.tag});
        }
        else
        {
            $rootScope.handleResponse('Please select DU to add to arrange list');
        }

        if(duset_flag_new===1)
        {
            $scope.arrangedDU.splice(ind, 1);
        }
    };

    $scope.moveArrangeListUp = function()
    {
        var duset_flag = 0;
        var du_length = $scope.arrangedDU.length;
        var ind = 0;
        if(du_length>0)
        {
            for(var d=0; d<$scope.duIndexToArrange.length; d++)
            {
                var elementToMoveForward = $scope.arrangedDU[d];
                var elementToMoveBackward = $scope.arrangedDU[d+1];
                if(elementToMoveBackward!=null)
                {
                    $scope.arrangedDU[d+1] = elementToMoveForward;
                    $scope.arrangedDU[d] = elementToMoveBackward;
                }
            }
        }
        else
        {
            $rootScope.handleResponse('Please select DU to perform action');
        }
    };

    $scope.moveArrangeListDown = function()
    {
        var duset_flag = 0;
        var du_length = $scope.arrangedDU.length;
        var ind = 0;
        if(du_length>0)
        {
            for(var d=0; d<$scope.duIndexToArrange.length; d++)
            {
                if($scope.duIndexToArrange[d] != (du_length-1))
                {
                    var elementToMoveBackward = $scope.arrangedDU[d+1];
                    var elementToMoveForward = $scope.arrangedDU[d];

                    if(elementToMoveForward!=null)
                    {
                        $scope.arrangedDU[d+1] = elementToMoveForward;
                        $scope.arrangedDU[d] = elementToMoveBackward;
                    }
                }
            }
        }
        else
        {
            $rootScope.handleResponse('Please select DU to perform action');
        }
    };

    $scope.setBackground = function(type)
    {
        if(type === 'Fast Track')
        {
            return 'bg--cs17';
        }
        else if(type === 'Hot Fix')
        {
            return 'bg--cs13';
        }
        else
        {
            return 'bg--cs01';
        }
    };

    $scope.setOrderBackground = function(index)
    {
        if(index%2 === 0)
        {
            return 'bg--cs17';
        }
        else
        {
            return 'bg--cs14';
        }
    };

    $scope.addApproval = function(approval_status)
    {
        var flag = 0;
        var approval_flag = false;
        var newStatus = JSON.parse(approval_status);
        $scope.userData = JSON.parse(sessionStorage.getItem('ga_userprofile'));
        for(var e=0; e<$scope.application.data.approval_list.length; e++)
        {
            if(newStatus.name !== $scope.application.data.approval_list[e].approval_status)
            {
                flag++;
            }
        }
        if(flag === $scope.application.data.approval_list.length)
        {
            $scope.application.data.approval_list.push({
                'approval_status' : newStatus.name,
                'approved_by' : $scope.userData.user,
                'approved_date' : date.toISOString()
            });
            $scope.application.data.approval_status = newStatus.name;
        }
        else
        {
            var length = $scope.application.data.approval_list.length;
            $scope.application.data.approval_status = $scope.application.data.approval_list[length-1].approval_status;
        }
    };

    $scope.moveForward = function(index)
    {
        var elementToMoveForward = $scope.duList[index];
        var elementToMoveBackward = $scope.duList[index+1];
        if(elementToMoveBackward!=null)
        {
            $scope.duList[index+1] = elementToMoveForward;
            $scope.duList[index] = elementToMoveBackward;
        }
    };

    $scope.moveArrangedListForward = function(index)
    {
        var elementToMoveForward = $scope.arrangedDU[index];
        var elementToMoveBackward = $scope.arrangedDU[index+1];
        if(elementToMoveBackward!=null)
        {
            $scope.arrangedDU[index+1] = elementToMoveForward;
            $scope.arrangedDU[index] = elementToMoveBackward;
        }
    };

    $scope.moveBackward = function(index)
    {
        var elementToMoveBackward = $scope.selectedDU[index];
        var elementToMoveForward = $scope.selectedDU[index-1];

        if(elementToMoveForward!=null)
        {
            $scope.selectedDU[index] = elementToMoveForward;
            $scope.selectedDU[index-1] = elementToMoveBackward;
            $scope.arrangedDU[index] = elementToMoveForward;
            $scope.arrangedDU[index-1] = elementToMoveBackward;
        }
    };

    $scope.moveArrangedListBackward = function(index)
    {
        var elementToMoveBackward = $scope.arrangedDU[index];
        var elementToMoveForward = $scope.arrangedDU[index-1];

        if(elementToMoveForward!=null)
        {
            $scope.arrangedDU[index] = elementToMoveForward;
            $scope.arrangedDU[index-1] = elementToMoveBackward;
        }
    };

    $scope.prerequisiteData = PrerequisitesViewAll.get({
    },
    function(prerequisiteSuccessResponse){
        for(var a=0; a<$scope.prerequisiteData.data.length; a++)
        {
            for(var b=0; b<$scope.prerequisiteData.data[a].version_list.length; b++)
            {
                $scope.prerequisites.push({'prerequisites_name' : $scope.prerequisiteData.data[a].prerequisites_name, 'version' : $scope.prerequisiteData.data[a].version_list[b]});
            }

        }
    },function(prerequisiteErrorResponse){
           $rootScope.handleResponse(prerequisiteErrorResponse);
    });

    var duData = {};
    var Deployment_fields = {};

    $scope.input_types = [
        "text",
        "password",
        "email",
        "date",
        "checkbox",
        "dropdown",
        "radio",
        "number"
    ];

    $scope.addNewChoice = function(index, name, version)
    {
        if($scope.application.data.pre_requiests)
        {
            $scope.application.data.pre_requiests.push({'name' : name, 'version' : version});
        }
        else
        {
            $scope.application.data.pre_requiests = [];
            $scope.application.data.pre_requiests.push({'name' : name, 'version' : version});
        }
    };

    $scope.addNewField = function()
    {
        if($scope.application.data.deployment_field.fields.length === 0)
        {
            $scope.fieldIndex = $scope.application.data.deployment_field.fields.length;
            $scope.application.data.deployment_field.fields.push({
                order_id : 1,
                valid_values : []
            });

        }
        else
        {
            $scope.fieldIndex = $scope.application.data.deployment_field.fields.length;
            $scope.application.data.deployment_field.fields.push({
                order_id : $scope.fieldIndex,
                valid_values : []
            });

        }
    };

    $scope.addNewValidValueField = function(index, version)
    {
        if($scope.application.data.deployment_field.fields[index].valid_values)
        {
            var len = ($scope.application.data.deployment_field.fields[index].valid_values).length;
        }
        else
        {
            $scope.application.data.deployment_field.fields[index].valid_values = [];
        }

        $scope.application.data.deployment_field.fields[index].valid_values.push("");
    };

    $scope.removeChoice = function(index)
    {
        var lastItem = $scope.application.data.pre_requiests.length-1;
        $scope.application.data.pre_requiests.splice(lastItem);
    };

    $scope.removeField = function(index) {
        $scope.application.data.deployment_field.fields.splice(index, 1);
    };

    $scope.removeValidValueField = function(index, version) {
        var lastItem = $scope.application.data.deployment_field.fields[index].valid_values.length-1;
        $scope.application.data.deployment_field.fields[index].valid_values.splice(lastItem,1);
    };

    $scope.selectPrerequisite = function(prerequisite)
    {
        var prerequisite_flag = 0;
        var ind = 0;
        if($scope.application.data.pre_requiests)
        {
            for(var c=0;  c<$scope.application.data.pre_requiests.length; c++)
            {
                if((prerequisite.prerequisites_name===$scope.application.data.pre_requiests[c].name) && (prerequisite.version===$scope.application.data.pre_requiests[c].version))
                {
                    prerequisite_flag++;
                    ind = c;
                }
            }

            if(prerequisite_flag===0)
            {
                $scope.application.data.pre_requiests.push({'name' : prerequisite.prerequisites_name, 'version' : prerequisite.version});
            }
            else
            {
                $scope.application.data.pre_requiests.splice(ind, 1);
            }

        }
        else
        {
            $scope.application.data.pre_requiests = [];
            $scope.application.data.pre_requiests.push({'name' : prerequisite.prerequisites_name, 'version' : prerequisite.version});
        }
    };

   $scope.editDUSet = function(form)
   {
        var duSetData = {
            _id : {
                oid : ''
            },
            du_set : []
        };
//      Client-side validations starts here..
        if($scope.application.data.name === '')
        {
            $rootScope.handleResponse('Please enter the DU Package name');
            return false;
        }

        if($scope.application.data.tag === '')
        {
            $rootScope.handleResponse('Please enter the tags');
            return false;
        }

        if($scope.duList.length<1)
        {
            $rootScope.handleResponse('Please select atleast one DU to add in DU Package');
            return false;
        }


//      Validation end here..
        duSetData._id.oid = $scope.application.data._id.$oid;
        duSetData.name = $scope.application.data.name;
        if(!angular.isArray($scope.application.data.tag))
        {
            duSetData.tag = $scope.application.data.tag.split(",");
        }
        else
        {
            duSetData.tag = $scope.application.data.tag;
        }

        if(!$scope.logo)
        {
            duSetData.logo = $scope.application.data.logo;
        }

        duSetData.approval_status = $scope.application.data.approval_status;
        duSetData.release_notes = $scope.application.data.release_notes;
        duSetData.pre_requiests = $scope.application.data.pre_requiests;
        duSetData.approval_list = [];
        $scope.userData = $rootScope.userFactory.getUserDetails();
        duSetData.approval_list = $scope.application.data.approval_list;

        for(var a=0; a<$scope.duList.length; a++)
        {
            duSetData.du_set.push({'du_id' : $scope.duList[a].du_id, 'dependent' : $scope.duList[a].dependent.toString(), 'order' : a+1});
        }

        $scope.editDUStatus = EditDUSet.update(duSetData, function(duSetEditSuccessResponse)
        {
             var file = $scope.logo;
            if(file)
            {    file.duset_id= duSetData._id.oid;
                var uploadUrl = "/deploymentunitset/upload/logo";
                duLogoFileUpload.uploadeditDuSetLogoFileToUrl(file, uploadUrl);
            }

            $state.go('duDashboard');
            $rootScope.handleResponse(duSetEditSuccessResponse);
        },
        function(duSetEditErrorResponse)
        {
            $rootScope.handleResponse(duSetEditErrorResponse);
        });
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

    $scope.showApprovalStatus = function()
    {
            if($scope.approvalStatusFlag === true)
            {
                $scope.approvalStatusFlag = false;
            }
            else
            {
                $scope.approvalStatusFlag = true;
            }
    };

    $scope.setApprovalStatusCSS = function(flag)
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

    $scope.showDusets = function()
    {
            if($scope.DusetsFlag === true)
            {
                $scope.DusetsFlag = false;
            }
            else
            {
                $scope.DusetsFlag = true;
            }
    };

    $scope.setDusetsCSS = function(flag)
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
    $scope.tagsAll = TagsAll.get({
    },
        function(tags)
        {
            $scope.tagsAll = tags;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
    });


    $scope.approvalStatus = ApprovalStatusAll.get({
    },
    function(successResponse)
    {
        $scope.approvalStatus = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.dusetsAll = DUSetAll.get({
        page: 0,
        perpage: 0
    },
    function(dusetSuccessResponse)
    {
        $scope.dusetsAll = dusetSuccessResponse.data.data;
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

    $scope.setApprovalStatusFilter = function(ApprovalStatus)
    {
        var approvalStatusFlag = 0;
        var ind = 0;
        var approvalStatusFilterLen = approvalStatusFilter.length;
        if(approvalStatusFilterLen>0)
        {
            for(var a=0; a<approvalStatusFilterLen; a++)
            {
                if(approvalStatusFilter[a] === ApprovalStatus)
                {
                    ind = a;
                }
                else
                {
                    approvalStatusFlag++;
                }
            }

            if(approvalStatusFlag === approvalStatusFilterLen)
            {
                approvalStatusFilter.push(ApprovalStatus);
            }
            else
            {
                approvalStatusFilter.splice(ind, 1);
            }
        }
        else
        {
            approvalStatusFilter.push(ApprovalStatus);
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

   $scope.setDusetFilter = function(duset)
   {
        var DusetsFlag = 0;
        var ind = 0;
        var dusetFilterLen = dusetFilter.length;
        if(dusetFilterLen>0)
        {
            for(var a=0; a<dusetFilterLen; a++)
            {
                if(dusetFilter[a] === duset)
                {
                    ind = a;
                }
                else
                {
                    DusetsFlag++;
                }
            }

            if(DusetsFlag === dusetFilterLen)
            {
                dusetFilter.push(duset);
            }
            else
            {
                dusetFilter.splice(ind, 1);
            }
        }
        else
        {
            dusetFilter.push(duset);
        }
   };

   $scope.closeFilter = function(form)
   {
         statusFilter = [];
         approvalStatusFilter = [];
         tagFilter = [];
         dusetFilter = [];
        $('#open_filter').hide(700);
   };

   $scope.applyDuFilters = function()
   {
        var status = '';
        var ApprovalStatus = '';
        var tag = '';
        var duset = '';
        $scope.tempDU = [];
        if(statusFilter.length>0)
        {
            status = statusFilter.toString();
        }
        else
        {
            status = null;
        }
        if(approvalStatusFilter.length>0)
        {
            ApprovalStatus = approvalStatusFilter.toString();
        }
        else
        {
            ApprovalStatus = null;
        }

        if(tagFilter.length>0)
        {
            tag = tagFilter.toString();
        }
        else
        {
            tag = null;
        }

        if(dusetFilter.length>0)
        {
            duset = dusetFilter.toString();
        }
        else
        {
            duset = null;
        }

        DeploymentUnitAll.get({
           status: status,
           approval_status: ApprovalStatus,
           tags: tag,
           duset: duset
        },
        function(successResponse)
        {
            delete $scope.applications;
            $scope.applications = [];
            $scope.currentPage = successResponse.page;
                $scope.totalCount = successResponse.total;
            
            for(var d=0; d<successResponse.data.length; d++)
            {
                $scope.applications.push(successResponse.data[d]);
            }
            $scope.$watch(function(scope) {
                return scope.applications;
            },
            function(newValue, oldValue) {
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

});
});