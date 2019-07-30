define(['angular', 'uiRouter', 'ngCookies', 'applicationRoutesApp', 'authenticationServicesApp'],function (app) {
  'use strict';

var userRegistrationControllerApp = angular.module('userRegistrationControllerApp', ['ui.router', 'ngCookies', 'authenticationRoutesApp', 'authenticationServicesApp', 'applicationRoutesApp']);

userRegistrationControllerApp.controller('UserRegistrationController', function ($scope, $state, $stateParams, $window, $http, $interval,$rootScope,Registeration, GetAccount) {
    $scope.user=new Registeration();
    $scope.accounts = GetAccount.get({
    },
    function(successResponse) {
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.account = {
        selected : ""
    };
    $scope.addUser = function(form)
    {
        var email = $scope.email;
        var atpos = email.indexOf("@");
        var dotpos = email.lastIndexOf(".");
        if (atpos<1 || dotpos<atpos+2 || dotpos+2>=email.length)
        {
            $rootScope.handleResponse('Please enter valid email address!');
            return false;
        }

        if ($scope.account.selected === "") {
            $('html, body').animate({
                scrollTop: $("#accountSection").offset().top - 50
            }, 1000);
            $rootScope.handleResponse('Please select account!');
            return false;
        }
        var Name = {};
        var PassWord = {};
        var EmployeeID = {};
        var EmailAddress = {};
        var Account = {};

        Name = $scope.name;
        PassWord = $scope.passsword;
        EmployeeID = $scope.employeeid;
        EmailAddress = $scope.email;
        Account = $scope.signUpForm.account_name.$viewValue;

        var jsonData = {};
        jsonData.user=Name;
        jsonData.password = PassWord;
        jsonData.employeeid = EmployeeID;
        jsonData.email = EmailAddress;
        jsonData.account = Account.name;

        $scope.user.data=jsonData;

        Registeration.save(jsonData,function(response){
            $rootScope.handleResponse(response);
            $state.go('login');
         },
         function(errorResponse)
         {
            $rootScope.handleResponse(errorResponse);
         });
     };
});

});