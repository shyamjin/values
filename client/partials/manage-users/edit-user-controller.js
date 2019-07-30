define(['angular', 'ngResource', 'uiRouter', 'ngCookies','changePasswordDirectiveApp'],function (app) {
  'use strict';

  var editUserControllerApp = angular.module('editUserControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp','changePasswordDirectiveApp']);
  editUserControllerApp.controller('EditUserController', function ($scope, $rootScope, $state, $location, $stateParams, Users, $interval, Role, GetAccount, UserGroup, UserUpdate, PasswordUpdate, GenerateToken, DeleteToken) {
    $scope.users = [];
    $scope.expiration_at = 'no_expiration';
    $scope.current_time = new Date();
    $scope.scheduled_timestamp = $scope.current_time.toISOString();
    $scope.expirationDateTime = $scope.current_time;
    $scope.userSelected=false;
    $scope.selectedData = {
        role : {}
    };
    $scope.selectedData=[];
    $scope.useredit_errors=[];
    $scope.includedIn = [];
    $scope.myData = new UserUpdate();
    var userData = {};
    var passwordData = {};

    Users.get({
        id:"all"
    },

    function(successResponse)
    {
        $scope.users = successResponse;
    },

    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.isUserSelected=function(check)
    {
        $scope.userSelected=true;
        $scope.editEnableFlag=true;
        $scope.user = Users.get({
            id:"view"+"/"+check._id.$oid
        },
        function(successResponse)
        {
            delete $scope.accessToken;
            if(successResponse.data)
            {
                $scope.selectedData=successResponse.data;
                $scope.atPasswordValueMap = $scope.selectedData._id.$oid;
                $scope.selectedData.role=successResponse.data.roleid;
                $scope.selectedData.employeeid = parseInt(successResponse.data.employeeid, 10);
                $scope.includedIn=successResponse.data.included_in;
                $scope.accountId = successResponse.data.accountid;
                $scope.accessToken = successResponse.data.access_token;
                if(!successResponse.data.homepage)
                {
                    $scope.selectedData.homepage = '';
                }

                $scope.accounts = GetAccount.get({
                },
                function(accountSuccessResponse)
                {
                    for(var i=0; i<accountSuccessResponse.data.length; i++)
                    {
                        if($scope.accountId === accountSuccessResponse.data[i]._id.$oid)
                        {
                            $scope.selectedData.account = accountSuccessResponse.data[i].name;
                        }
                    }
                },
                function(accountErrorResponse)
                {
                    $rootScope.handleResponse(accountErrorResponseaccountErrorResponse);
                });
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.showAddTeam = function()
    {
        if(document.getElementById("add_user_to_team").style.display === "none" || document.getElementById("add_user_to_team").style.display === "")
        {
            document.getElementById("add_user_to_team").style.display = "block";
        }
        else
        {
           document.getElementById("add_user_to_team").style.display = "none";
       }
   };

   $scope.closeAddTeam = function()
   {
    document.getElementById("add_user_to_team").style.display = "none";
    };

$scope.exist=function(item)
{
    var flag=false;
    for(var i=0;i<$scope.includedIn.length;i++)
    {
     if($scope.includedIn[i].team_id === item.team_id)
     {
        flag=true;
        return flag;
    }
    else
    {
     flag=false;
     continue;}
 }
 return flag;
};

$scope.toggleSelection=function(item)
{
    var count=0;
    var group_length = $scope.includedIn.length;

    if(group_length>0)
    {
        for(var a=0; a<group_length; a++)
        {
            if($scope.includedIn[a].team_id === item.team_id)
            {
                $scope.includedIn.splice(a, 1);
            }
            else
            {
                count++;
            }
        }
        if(count===group_length)
        {
         $scope.includedIn.push({'team_id' : item.team_id, 'team_name' : item.team_name});
     }
 }
 else
 {
    $scope.includedIn.push({'team_id' : item.team_id, 'team_name' : item.team_name});
}
};

$scope.isSuspended=function()
{
    var suspendFlag=false;
    if($scope.selectedData)
    {
        if($scope.selectedData.status === "suspended")
        {
            suspendFlag = true;
        }
        else
        {
            suspendFlag = false;
        }
    }
    else
    {
        suspendFlag = false;
    }
    return suspendFlag;
};

$scope.toggleStatus=function()
{
 if($scope.selectedData.status === "suspended")
 {
    $scope.selectedData.status="active";
}
else
{
 $scope.selectedData.status="suspended";
}
};

$scope.userGroupList = [];
$scope.userGroups=UserGroup.get({

},
function(userGroupSuccessResponse)
{
    for(var a=0; a<userGroupSuccessResponse.data.length; a++)
    {
        $scope.userGroupList.push({'team_id' : userGroupSuccessResponse.data[a]._id.$oid,'team_name' : userGroupSuccessResponse.data[a].team_name});
    }
},
function(errorResponse)
{
  $rootScope.handleResponse(errorResponse);
});

$scope.isTeamSelected = function(team)
{
    var flag = 0;
    if(!$scope.includedIn)
    {
        $scope.includedIn = [];
    }
    for(var a=0; a<$scope.includedIn.length; a++)
    {
        if($scope.includedIn[a].team_id === team)
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

$scope.roles = Role.get({
    id:"all"
},
function(successResponse)
{
    if(successResponse)
    {
        $rootScope.handleResponse(successResponse);
    }
},
function(errorResponse)
{
    $rootScope.handleResponse(errorResponse);
});

$scope.status = [
"active",
"suspended"
];

$scope.getRole = function(role, href)
{
    var ref = document.getElementById(href);

    if($rootScope.userProfile.userData.rolename==='SuperAdmin' || role===$rootScope.userProfile.userData.rolename)
    {
        return '';
    }
    else if($rootScope.userProfile.userData.rolename==='Admin' && role==='SuperAdmin')
    {
        document.getElementById(href).removeAttribute("href");
        return 'disabled';
    }
    else if(($rootScope.userProfile.userData.rolename==='Admin' && role==='Operator') || ($rootScope.userProfile.userData.rolename==='Admin' && role==='Guest'))
    {
        return '';
    }
    else
    {
        document.getElementById(href).removeAttribute("href");
        return 'disabled';
    }
};

$scope.editEnableFlag=true;
$scope.checkEditEnable=function()
{
    if($scope.editEnableFlag===false)
    {
        $scope.editEnableFlag=true;
    }
    else if($scope.editEnableFlag===true)
    {
        $scope.editEnableFlag=false;
    }
};

$scope.getAccountId = function(account)
{
    for(var i=0; i<$scope.accounts.data.length; i++)
    {
        if($scope.selectedData.account === $scope.accounts.data[i].name)
        {
            $scope.selectedData.account = $scope.accounts.data[i].name;
            $scope.accountId = $scope.accounts.data[i]._id.$oid;
        }
    }
};

$scope.getUserUlClass = function()
{
    if($scope.userSelected === true)
    {
        if($scope.displayTab!='/users')
        {
            $scope.userSelected = false;
        }
        return "vp-userform__fieldslist text--cs03 pr--lg";
    }
    else
    {
        return "vp-userform__fieldslist text--cs03 pr--lg hidden";
    }
};

$scope.getUserFormClass = function()
{
   if($scope.userSelected === true)
   {
    if($scope.displayTab!='/users')
    {
        $scope.userSelected = false;
    }
    return "vp-selecteduserform--active  vp-userform vp-control max";
}
else
{
    return "vp-selecteduserform vp-userform vp-control max";
}
};


$scope.getAdminRoleClass = function(user)
{
    if(user.rolename==='Admin')
    {
        return "vp-search__item--admin";
    }
    else if(user.rolename==='SuperAdmin')
    {
        return "vp-search__item--superadmin";
    }
    else if(user.rolename==='Operator')
    {
        return "vp-search__item--operator";
    }
    else if(user.rolename==='Guest')
    {
        return "vp-search__item--guest";
    }
};



$scope.showVersionDetailsTab = function(selectedTabName)
{
    $scope.displayTab = selectedTabName;

};

$scope.discardUserData=function(check)
{
    $scope.editEnableFlag=true;
    $scope.userSelected=true;

    $scope.user = Users.get({
        id:"view"+"/"+check._id.$oid
    },
    function(successResponse)
    {
        if(successResponse.data)
        {
            $scope.selectedData=successResponse.data;
            $scope.selectedData.role=successResponse.data.roleid;
            $scope.includedIn=successResponse.data.included_in;
            $rootScope.handleResponse(successResponse);
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });
};

$scope.editNewUser = function(formData)
{
    userData._id = {
        oid : ""
    };

    $scope.useredit_errors.employeeid ='';

    if($scope.selectedData.employeeid==='' || $scope.selectedData.employeeid===undefined || $scope.selectedData.employeeid==='0' || $scope.selectedData.employeeid===null)
    {
        $scope.useredit_errors.employeeid ="Please enter employee id!";
        return false;
    }

    $scope.useredit_errors.email='';
    if($scope.selectedData.email==='')
    {
        $scope.useredit_errors.email="Please enter email address!";
        return false;
    }
    else if($scope.selectedData.email===undefined || $scope.selectedData.email!=='' )
    {
        $scope.useredit_errors.email='';
        if($scope.selectedData.email===undefined)
        {
            $scope.useredit_errors.email ="Please enter valid email address!";
            return false;
        }

        var atpos = $scope.selectedData.email.indexOf("@");
        var dotpos = $scope.selectedData.email.lastIndexOf(".");
        if (atpos<1 || dotpos<atpos+2 || dotpos+2>=$scope.selectedData.email.length)
        {
            $scope.useredit_errors.email ="Please enter valid email address!";
            return false;
        }
    }

    $scope.useredit_errors.role ='';
    if($scope.selectedData.role==='' || $scope.selectedData.role===undefined )
    {
        $scope.useredit_errors.role ="Please select role!";
        return false;
    }

    $scope.useredit_errors.account ='';
    if($scope.selectedData.account==='' || $scope.selectedData.account===undefined)
    {
        $scope.useredit_errors.account ="Please select Account!";
        return false;
    }

    $scope.user_name = $scope.selectedData.user;
    $scope.userid = $scope.selectedData._id.$oid;
    $scope.email = $scope.selectedData.email;
    $scope.employee_id = $scope.selectedData.employeeid;
    if($scope.selectedData.role)
    {
        $scope.roleid = $scope.selectedData.role;
    }
    else
    {
        $scope.roleid = $scope.user.data.roleid;
    }
    if($scope.selectedData.account)
    {
        $scope.account = $scope.selectedData.account;
    }
    else
    {
        $scope.account = $scope.user.data.account;
    }
    if($scope.selectedData.status)
    {
        $scope.status = $scope.selectedData.status;
    }
    else
    {
        $scope.status = $scope.user.data.status;
    }

    userData.user = $scope.user_name;
    userData.employeeid = $scope.employee_id;
    userData.email = $scope.email;
    userData.roleid = $scope.roleid;
    userData.accountid = $scope.accountId;
    userData.status = $scope.status;
    userData._id.oid = $scope.userid;

    var jsonIncludedIn=[];
    for(var i=0;i<$scope.includedIn.length;i++)
    {
     jsonIncludedIn.push($scope.includedIn[i].team_id);
 }
 userData.included_in=jsonIncludedIn;
 if($scope.selectedData.homepage === 'dashboard' || $scope.selectedData.homepage === '' || $scope.selectedData.homepage === null)
 {
    userData.homepage = 'dashboard';
}
else
{
    userData.homepage = 'duDashboard';
}

UserUpdate.update(userData,function(response){
    delete $scope.selectedData;
    $scope.userSelected = false;
    delete $scope.users;
    Users.get({
        id:"all"
    },
    function(successResponse)
    {
        $scope.users = successResponse;
    },
    function(errorResponse)
    {
     $rootScope.handleResponse(errorResponse);
 });
    $state.go('users');
    $rootScope.handleResponse(response);
},
function(errorResponse)
{
    $rootScope.handleResponse(errorResponse);
});
};

$scope.showEditPassword = function()
{
    if(document.getElementById("update_password").style.display === "none" || document.getElementById("update_password").style.display === '')
    {
        document.getElementById("update_password").style.display = "block";
    }
    else
    {
       document.getElementById("update_password").style.display = "none";
   }
};

$scope.showGenerateToken = function()
{
    if(document.getElementById("generate_token").style.display === "none" || document.getElementById("generate_token").style.display === '')
    {
        document.getElementById("generate_token").style.display = "block";
    }
    else
    {
       document.getElementById("generate_token").style.display = "none";
   }
};

$scope.closeGenerateToken = function()
{
    document.getElementById("generate_token").style.display = "none";
};

$scope.setTokenExpiration = function(param)
{
    $scope.expiration_at = param;
};

$scope.generateToken = function()
{
    var jsonData = {
        _id : {
            oid : ''
        }
    };
    jsonData._id.oid = $scope.selectedData._id.$oid;
    if($scope.expiration_at === 'later')
    {
        jsonData.access_exp_date = $scope.expirationDateTime;
    }

    GenerateToken.update(jsonData,function(tokenSuccessResponse){
        $rootScope.handleResponse(tokenSuccessResponse);
        $scope.accessToken = tokenSuccessResponse.data;
        document.getElementById("generate_token").style.display = "none";
    },
    function(tokenErrorResponse)
    {
        $rootScope.handleResponse(tokenErrorResponse);
    });
};

$scope.deleteToken = function()
{
    var jsonData = {
        _id : {
            oid : ''
        }
    };
    jsonData._id.oid = $scope.selectedData._id.$oid;

    DeleteToken.remove({
        id : jsonData._id.oid
    },
    function(tokenDeleteSuccessResponse)
    {
        delete $scope.accessToken;
        delete $scope.selectedData.access_token;
        $rootScope.handleResponse(tokenDeleteSuccessResponse);
    },
    function(tokenDeleteErrorResponse) {
        $rootScope.handleResponse(tokenDeleteErrorResponse);
    });
};

$scope.closePassword = function()
{
    document.getElementById("update_password").style.display = "none";
};

});
});