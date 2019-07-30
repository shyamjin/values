define(['angular', 'ngResource'], function (app) {
  'use strict';
var changePasswordDirectiveApp = angular.module('changePasswordDirectiveApp', ['userServicesApp']);

changePasswordDirectiveApp.directive('changePassword', function () {
    return {
        restrict: 'E',
        templateUrl :'static/components/directives/change-password/change-password-directive.html',
        scope:{
            atPasswordValueMap: '=',
            onAtLoad : '&'
        },
        controller: function($scope,$rootScope,PasswordUpdate){
            var passwordData = {};
            $scope.useredit_errors= [];
            $scope.selectedData=[];
            $scope.checkPassword = function()
            {
                passwordData._id = {
                    oid : ""
                };
                $scope.useredit_errors.password ='';
                $scope.useredit_errors.confirmpassword ='';
                $scope.useredit_errors.password_mismatch ='';
                if($scope.selectedData.password==='' || $scope.selectedData.password===undefined )
                {
                    $scope.useredit_errors.password ="Please enter password!";
                    return false;
                }
                else if($scope.selectedData.confirmpassword==='' || $scope.selectedData.confirmpassword===undefined )
                {
                    $scope.useredit_errors.confirmpassword ="Please confirm entered password!";
                    return false;
                }
                else if($scope.selectedData.password!=='' &&  $scope.selectedData.confirmpassword!=='' && $scope.selectedData.password!==undefined && $scope.selectedData.confirmpassword!==undefined  && $scope.selectedData.password!==$scope.selectedData.confirmpassword)
                {
                    $scope.useredit_errors.password_mismatch ="Password and Confirm password should match!";
                    return false;
                }
                else if($scope.selectedData.password!=='' &&  $scope.selectedData.confirmpassword!=='' && $scope.selectedData.password!==undefined && $scope.selectedData.confirmpassword!==undefined  && $scope.selectedData.password===$scope.selectedData.confirmpassword)
                {
                    $scope.closePassword();
                }

                $scope.password = $scope.selectedData.password;
                $scope.confirmpassword = $scope.selectedData.confirmpassword;
                if($scope.password && $scope.confirmpassword)
                {
                    if(($scope.password === $scope.confirmpassword) && ($scope.selectedData.password === $scope.password))
                    {
                        passwordData._id.oid = $scope.atPasswordValueMap;
                        passwordData.password = $scope.password;
                    }
                    if(passwordData)
                    {
                        $scope.passwordUpdateStatus = PasswordUpdate.update(passwordData,function(passwordResponse){
                            $rootScope.handleResponse(passwordResponse);
                        },
                        function(passwordErrorResponse) {
                            $rootScope.handleResponse(passwordErrorResponse);
                        });
                    }
                }
            };

            $scope.closePassword = function()
            {
                $scope.onAtLoad();
            };
        }
    };
});
});