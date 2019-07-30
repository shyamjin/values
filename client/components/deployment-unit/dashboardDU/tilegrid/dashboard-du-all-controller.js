define(['angular', 'ngResource', 'uiRouter', 'ngCookies','toolTips', 'jquery', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp'], function (app) {
  'use strict';

var dashboardDUAllControllerApp = angular.module('dashboardDUAllControllerApp', ['ui.router','720kb.tooltips', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp']);

dashboardDUAllControllerApp.controller('DashboardDUAllController', function ($scope, $rootScope, $state, $stateParams, DeploymentUnitAll, DUTypesAll,$location, $interval, TicketStatus, TagsAll, DUSetAll, ApprovalStatusAll) {
    $scope.filterType = 'All';
    $scope.statusFlag = true;
    $scope.approvalStatusFlag = false;
    $scope.tagsFlag = false;
    $scope.DusetsFlag = false;
    var statusFilter = [];
    var approvalStatusFilter = [];
    var tagFilter = [];
    var dusetFilter = [];
    var dutypeFilter =[];
    $scope.tags = new TagsAll();
    $scope.isFilterApplied = false;
    $scope.hideShowMoreDus = false;
    $scope.DuTypeFlag = false;
    $scope.deployDUSetData ={
        'du_id':'',
        'duDataList':[]
    };
    $scope.createNewDu = function()
    {
        $state.go("newDU");
    };

    $rootScope.$on("searchDUEvent", function (event, args) {
        var keyword = args.keyword;
        $scope.searchDUWithName(keyword);
    });

    $scope.showDUDetails = function(du_id)
    {
        $state.go('viewDU',{id : du_id});
    };

    $scope.selectedDus = [];
    $scope.selectedDusList = [];

    DeploymentUnitAll.query({
    },
    function(successResponse)
    {
        $scope.applications = successResponse.data.data;
        $scope.currentPage = successResponse.data.page;
        $scope.totalCount = successResponse.data.total;
        for(var m=0; m<successResponse.data.data.length; m++)
        {
            for (var n=0; n<successResponse.data.data[m].data.length; n++)
            {
                $scope.applications[m].data[n].isSelected = false;
            }

        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.duSetDeploy = function(value)
    {
        if(value.build_id !== null && value.build_id !== undefined)
        {
             $scope.deployDUSetData.du_id = value.id;
             $scope.deployDUSetData.duDataList =[];
             $scope.deployDUSetData.duDataList.push({'build_id' :value.build_id,'build_number':value.build_number});
             $state.go('deployDU',{id : JSON.stringify($scope.deployDUSetData)});
        }
        else
        {
            $rootScope.handleResponse('Valid Build is not available for this DU');
            return false;
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

    $scope.showDuTypes = function()
    {
        if($scope.DuTypeFlag === true)
        {
            $scope.DuTypeFlag = false;
        }
        else
        {
            $scope.DuTypeFlag = true;
        }
    };

    $scope.setDuTypeCSS = function(flag)
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

    $scope.DUTypes = DUTypesAll.get({
        page: 0,
        perpage: 0
    },
    function(successResponse)
    {
        $scope.DUTypes = successResponse.data;
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

   $scope.setDuTypeFilter = function(dutype)
   {
        var DuTypeFlag = 0;
        var ind = 0;
        var dutypeFilterLen = dutypeFilter.length;
        if(dutypeFilterLen>0)
        {
            for(var a=0; a<dutypeFilterLen; a++)
            {
                if(dutypeFilter[a] === dutype)
                {
                    ind = a;
                }
                else
                {
                    DuTypeFlag++;
                }
            }

            if(DuTypeFlag === dutypeFilterLen)
            {
                dutypeFilter.push(dutype);
            }
            else
           {
                dutypeFilter.splice(ind, 1);
           }
        }
        else
        {
            dutypeFilter.push(dutype);
        }
   };

   $rootScope.showFilter = function(tab)
   {
        if(document.getElementById("show_dashboard_filter").style.display === "none" || document.getElementById("show_dashboard_filter").style.display === "")
        {
            $('#show_dashboard_filter').show(700);
        }
        else
        {
            $('#show_dashboard_filter').hide(700);
        }
    };

   $scope.resetFilter = function(form)
   {
        statusFilter = [];
        approvalStatusFilter = [];
        tagFilter = [];
        dusetFilter = [];
        dutypeFilter =[];
        $('#show_dashboard_filter').hide(700);
        $scope.isFilterApplied = false;
        $scope.hideShowMoreDus = false;
        DeploymentUnitAll.get({
        },
        function(successResponse)
        {
            $scope.applications = successResponse.data;
            $scope.currentPage = successResponse.page;
            $scope.totalCount = successResponse.total;
            for(var m=0; m<successResponse.data.length; m++)
            {
                for (var n=0; n<successResponse.data[m].data.length; n++)
                {
                    $scope.applications[m].data[n].isSelected = false;
                }

            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
   };

   $scope.closeFilter = function(form)
   {
        $('#show_dashboard_filter').hide(700);
   };

   $scope.applyDuFilters = function()
   {
        var status = '';
        var ApprovalStatus = '';
        var tag = '';
        var duset = '';
        var dutype = '';
        var perpage = 0;

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
        if(dutypeFilter.length>0)
        {
            dutype = dutypeFilter.toString();
        }
        else
        {
            dutype = null;
        }
        if(status === null && ApprovalStatus === null && tag === null && duset === null && dutype === null)
        {
            perpage = null;
            $scope.hideShowMoreDus = false;
            $scope.isFilterApplied = false;
        }
        else
        {
            $scope.hideShowMoreDus = true;
            $scope.isFilterApplied = true;
        }
        DeploymentUnitAll.get({
           status: status,
           approval_status: ApprovalStatus,
           tags: tag,
           duset: duset,
           type: dutype,
           page:0,
           perpage: perpage
        },
        function(successResponse)
        {
            delete $scope.applications;
            $scope.applications = [];
            $('#show_dashboard_filter').hide(700);
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

    $scope.searchDUWithName = function(keyword)
    {
        $rootScope.searchProgress = true;
        $scope.hideShowMoreDus = true;
        delete $scope.applications;
        DeploymentUnitAll.get({
           status: null,
           approval_status: null,
           tags: null,
           duset: null,
           duname: keyword,
           page: 0,
           perpage: 0
        },
        function(successResponse)
        {
            delete $scope.applications;
            delete $rootScope.searchProgress;
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
            delete $rootScope.searchProgress;
        });
    };

    $scope.isPageAvailable = function()
    {
        var duCount = 0;
        if($scope.applications)
        {
            for(var i=0; i<$scope.applications.length; i++)
            {
                duCount = duCount+$scope.applications[i].data.length;
            }
            if($scope.totalCount === duCount)
            {
                return false;
            }
            else
            {
                return true;
            }
        }
        else
        {
            return false;
        }
    };

    $scope.showMoreDU = function()
    {
        var status = '';
        var ApprovalStatus = '';
        var tag = '';
        var duset = '';
        var dutype = '';

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
        if(dutypeFilter.length>0)
        {
            dutype = dutypeFilter.toString();
        }
        else
        {
            dutype = null;
        }
        $scope.currentPage = $scope.currentPage+1;
        $scope.tempDU = [];
        angular.copy($scope.applications, $scope.tempDU);
        delete $scope.application;
        DeploymentUnitAll.get({
            status: status,
            approval_status: ApprovalStatus,
            tags: tag,
            duset: duset,
            dutype: dutype,
            page: $scope.currentPage
        },
        function(successResponse)
        {
            $scope.applications = [];
            $scope.currentPage = successResponse.page;
            $scope.totalCount = successResponse.total;
            for(var a=0; a<successResponse.data.length; a++)
            {
                var typeFlag = 0;
                var typeInd = 0;
                for(var b=0; b<$scope.tempDU.length; b++)
                {
                    if(successResponse.data[a].type === $scope.tempDU[b].type)
                    {
                        typeFlag++;
                        typeInd = b;
                    }
                }
                if(typeFlag === 1)
                {
                    for(var c=0; c<successResponse.data[a].data.length; c++)
                    {
                        var duFlag_3 = 0;
                        var duInd_3 = 0;
                        for (var d=0; d<$scope.tempDU[typeInd].data.length; d++)
                        {
                            if(successResponse.data[a].data[c]._id.$oid !== $scope.tempDU[typeInd].data[d]._id.$oid)
                            {
                                duFlag_3++;
                                duInd_3 = c;
                            }
                        }
                        if(duFlag_3 === $scope.tempDU[typeInd].data.length)
                        {
                            $scope.tempDU[typeInd].data.push(successResponse.data[a].data[duInd_3]);
                        }
                    }                    
                }
                else
                {
                    $scope.tempDU.push(successResponse.data[a]);
                }
            }
            for(var e=0; e<$scope.tempDU.length; e++)
            {
                $scope.applications.push($scope.tempDU[e]);
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.selectDU = function(du)
    {
         var flag = 0;
         var ind = 0;
         var elementId = '';
         var length = $scope.selectedDus.length;
         if(length > 0)
         {
           for(var id=0; id<length; id++)
            {
                if($scope.selectedDus[id].id === du._id.$oid)
                {
                    flag++;
                    ind = id;
                }
            }
            if(flag===0)
            {
                  if(du.build_number)
                  {
                      $scope.selectedDus.push({"id": du._id.$oid, "build_number": du.build_number, "build_id": du.build_id});
                      $scope.selectedDusList.push(du.name);
                      for(var a=0; a<$scope.applications.length; a++)
                      {
                        for (var i=0; i<$scope.applications[a].data.length; i++)
                        {
                           if($scope.applications[a].data[i].name === du.name)
                           {
                                $scope.applications[a].data[i].isSelected = true;
                           }
                        }

                      }
                  }
                  else
                  {
                        $rootScope.handleResponse("Unable to select DU "+du.name+" as it does not have a valid build");
                        elementId = document.getElementById("select_check_"+du.name);
                        elementId.checked = false;
                        return false;
                  }
            }
            else
            {
                for(var b=0; b<$scope.applications.length; b++)
                {
                   for (var j=0; j<$scope.applications[b].data.length; j++)
                    {
                        if($scope.applications[b].data[j].name === $scope.selectedDusList[ind])
                        {
                             $scope.applications[b].data[j].isSelected = false;
                        }
                    }
                }
                $scope.selectedDus.splice(ind, 1);
                $scope.selectedDusList.splice(ind, 1);
            }
         }
          else
          {
             if(du.build_number)
             {
                for(var c=0; c<$scope.applications.length; c++)
                {
                  for (var k=0; k<$scope.applications[c].data.length; k++)
                  {
                    if($scope.applications[c].data[k].name === du.name)
                    {
                        $scope.applications[c].data[k].isSelected = true;
                    }
                  }
                }
                 $scope.selectedDus.push({"id": du._id.$oid, "build_number": du.build_number, "build_id": du.build_id});
                 $scope.selectedDusList.push(du.name);
             }
             else
             {
                $rootScope.handleResponse("Unable to select "+du.name+" as it does not have a valid build");
                elementId = document.getElementById("select_check_"+du.name);
                elementId.checked = false;
                return false;

             }

          }
    };
    $scope.isDUSelected = function(du)
    {
        var flag = 0;
        if(!$scope.selectedDusList.length)
        {
            $scope.selectedDusList =[];
        }
        for(var j=0; j<$scope.selectedDusList.length; j++)
        {
            if(du.name === $scope.selectedDusList[j])
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
    $scope.removeDu = function(du)
    {
        var flag = 0;
        var ind = 0;
        var elementId = '';
        var length = $scope.selectedDus.length;
        if(length>0)
        {
            for(var id=0; id<length; id++)
            {
                if($scope.selectedDusList[id]=== du)
                {
                    flag++;
                    ind = id;
                }
            }
            if(flag===0)
            {
                $scope.selectedDus.push(du._id.$oid);
                $scope.selectedDusList.push(du.name);
                for(var a=0; a<$scope.applications.length; a++)
                {
                  for (var i=0; i<$scope.applications[a].data.length; i++)
                  {
                    if($scope.applications[a].data[i].name === du.name)
                    {
                        $scope.applications[a].data[i].isSelected = true;
                    }
                  }
                }
            }
            else
            {
                for(var b=0; b<$scope.applications.length; b++)
                {
                   for (var j=0; j<$scope.applications[b].data.length; j++)
                   {
                    if($scope.applications[b].data[j].name === $scope.selectedDusList[ind])
                    {
                        $scope.applications[b].data[j].isSelected = false;
                    }
                   }
                }
                $scope.selectedDus.splice(ind, 1);
                $scope.selectedDusList.splice(ind, 1);
            }
        }
        else
        {
            for(var c=0; c<$scope.applications.length; c++)
            {
              for (var k=0; k<$scope.applications[c].data.length; k++)
              {
                if($scope.applications[c].data[k].name === du.name)
                {
                    $scope.applications[c].data[k].isSelected = true;
                }
              }
            }
            $scope.selectedDus.push(du._id.$oid);
            $scope.selectedDusList.push(du.name);
        }
    };


    $scope.selectMultipleDusForDeployment = function(selectedDus)
    {
        if(selectedDus.length>0)
        {
            $state.go('deployMultipleDus', {dus: JSON.stringify(selectedDus)});
        }
    };
});
});