define(['angular', 'ngResource'], function (app) {
  'use strict';
var retainBuildDirectiveApp = angular.module('retainBuildDirectiveApp', ['userServicesApp','toolServicesApp']);

retainBuildDirectiveApp.directive('retainBuild', ['BuildMarkup',function () {
    return {
        restrict: 'E',
        templateUrl :'static/components/directives/retain-build/retain-build-directive.html',
        scope:{
            toolVersionData: '=',
            onAtLoad : '&',
            toolId: '@',
            toolVersionSelectedBuild: '=',
            onBuildSubmit: '&'
        },
        controller: function($scope,$rootScope,PasswordUpdate,BuildMarkup){
            $scope.toolVersionDataDetails = {};
            $scope.toolVersionDataDetailsOriginal = {};
            $scope.toolVersionDataDetails = JSON.parse(JSON.stringify($scope.toolVersionData));
            $scope.toolVersionDataDetailsOriginal = JSON.parse(JSON.stringify($scope.toolVersionData));
            $scope.selectedVersionIndex = $scope.toolVersionDataDetails.length > 0? 0:-1;
            $scope.updateToolVersionBuild = function()
            {
               $scope.toolVersionSelectedBuild = {};
               $scope.toolVersionSelectedBuild = $scope.updateBuild;
               if(Object.keys($scope.toolVersionSelectedBuild).length < 1)
                 $rootScope.handleResponse("Please select at least one build");
               else{
                    let versionList = Object.keys($scope.toolVersionSelectedBuild);
                    let showAtMaxLimitError = false;
                    let versionIds='';
                    for (let i=0; i<versionList.length ; i++){
                        let count=0;
                        for( let buildIndex = 0; buildIndex< $scope.toolVersionSelectedBuild[versionList[i]].length; buildIndex++){

                            if($scope.toolVersionSelectedBuild[versionList[i]][buildIndex].retain_build_indicator === true)
                                count++;
                        }
                        if( count>5){
                        showAtMaxLimitError = true;
                        versionIds= versionIds +', '+versionList[i];

                        }
                    }
                    if(showAtMaxLimitError === true)
                         $rootScope.handleResponse("Please select at max 5 builds for version "+versionIds);
                    else
//                         $scope.onBuildSubmit();
                            $scope.addVerBuildAsMarkup();

               }

            };
            $scope.toggleSelection = function toggleSelection(versionIndex,buildIndex) {
                 $scope.updateBuild={};
                 $scope.toolVersionDataDetails[versionIndex].build[buildIndex].retain_build_indicator = !$scope.toolVersionDataDetails[versionIndex].build[buildIndex].retain_build_indicator;

                 for (let i = 0; i < $scope.toolVersionDataDetails.length; i++) {

                    if($scope.toolVersionDataDetails[i].status != 0){

                        for (let buildIndex = 0; buildIndex < $scope.toolVersionDataDetails[i].build.length; buildIndex++) {
                                // check and store value
                                // in new variable
                             if($scope.compareBuildMarkup($scope.toolVersionDataDetails[i].build[buildIndex],$scope.toolVersionDataDetailsOriginal[i].build[buildIndex]))
                             {
                                     if(typeof $scope.updateBuild[$scope.toolVersionDataDetails[i]._id.$oid] === 'undefined')
                                        $scope.updateBuild[$scope.toolVersionDataDetails[i]._id.$oid]=[];

                                        $scope.updateBuild[$scope.toolVersionDataDetails[i]._id.$oid].push({
                                            'build_number' : $scope.toolVersionDataDetails[i].build[buildIndex].build_number,
                                            'status' : $scope.toolVersionDataDetails[i].build[buildIndex].status,
                                            'package_type':$scope.toolVersionDataDetails[i].build[buildIndex].package_type,
                                            'retain_build_indicator' : $scope.toolVersionDataDetails[i].build[buildIndex].retain_build_indicator,
                                            'file_path': $scope.toolVersionDataDetails[i].build[buildIndex].file_path,
                                            'file_size':$scope.toolVersionDataDetails[i].build[buildIndex].file_size,
                                            'type':$scope.toolVersionDataDetails[i].build[buildIndex].type,
                                            'additional_info':$scope.toolVersionDataDetails[i].build[buildIndex].additional_info,
                                            'package_name':$scope.toolVersionDataDetails[i].build[buildIndex].package_name
                                        })
                             }
                        }

                    }
                 }
            };

            $scope.compareBuildMarkup = function(modifiedBuild,originalBuild){
                    if(typeof modifiedBuild.retain_build_indicator === 'undefined' )
                        modifiedBuild.retain_build_indicator =false

                    if(typeof originalBuild.retain_build_indicator === 'undefined' )
                        originalBuild.retain_build_indicator =false
                    if((modifiedBuild.retain_build_indicator) != (originalBuild.retain_build_indicator))
                      return(true);
                    else
                      return(false);

            };

            $scope.showVersionDetailsTab = function( indexNo)
            {
                $scope.selectedVersionIndex = indexNo;
            };

            $scope.getActiveTab = function(activeTabNo)
            {
                if($scope.selectedVersionIndex===activeTabNo)
                    return "vp-toolversion_active";
            };

            $scope.closeRetainBuild = function()
            {
                 $scope.toolVersionDataDetails = JSON.parse(JSON.stringify($scope.toolVersionData));
                $scope.onAtLoad();
            };

            $scope.addVerBuildAsMarkup = function()
            {
                $scope.parameter ={
                    updateMarkupBuild: $scope.toolVersionSelectedBuild
                }
                BuildMarkup.save($scope.parameter, function(updateBuildMarkupSuccessResponse){

                        $rootScope.handleResponse(updateBuildMarkupSuccessResponse);
                        $scope.toolVersionData = JSON.parse(JSON.stringify($scope.toolVersionDataDetails));
                        document.getElementById("retain_build_popup_screen").style.display = "none";
                    },
                    function(updateBuildMarkupErrorResponse)
                    {
                        $rootScope.handleResponse(updateBuildMarkupErrorResponse);
                        return false;
                    });
            };
        }
    };
}]);
});