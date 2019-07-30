define(['angular','auditPartialControllerApp','auditServicesApp','angular-smart-table'],function (app) {
  'use strict';

var auditInfoControllerApp = angular.module('auditInfoControllerApp', ['auditPartialControllerApp','auditServicesApp','smart-table']);

auditInfoControllerApp.controller('auditInfoController', function ($scope,$window,$rootScope, $http, auditsViewAll,auditsViewById) {
	$scope.loading = false;
	$scope.getData = function() {
		$scope.loading = true;
		auditsViewAll.get({
        },
        function(successResponse)
        {
            $scope.auditsDataAll = successResponse.data;
			$scope.loading = false;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
	}
	$scope.getData();

    $scope.viewAuditDetailsById = function(id)
    {
        auditsViewById.get({
        id:id
        },
        function(successResponse)
        {
            $('#view_audits_details').show(700);
            $scope.auditDataById = successResponse.data;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.closeAuditsDetailsModal = function()
    {
        $('#view_audits_details').hide(700);
    };

    $scope.exportAudits = function()
    {
        var uri = 'data:application/vnd.ms-excel;base64,';
        var template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--><meta http-equiv="content-type" content="text/plain; charset=UTF-8"/></head><body><table>{table}</table></body></html>';
        var base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) };
        var format = function(s, c)
        {
            return s.replace(/{(\w+)}/g, function(m, p)
            {
                  return c[p];
            })
        };
        var table = $('#auditexport');
        var ctx={worksheet:'AuditReport',table: table.htm()};
        var href=uri+base64(format(template,ctx));
        $window.open(href, '_blank');
    };

 });

});