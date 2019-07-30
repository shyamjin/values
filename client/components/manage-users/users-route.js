require.config({
    baseUrl: "",
    waitSeconds: 0
});

define(['angular', 'ngResource', 'uiRouter', 'manageUsersControllerApp',
    'addUsersControllerApp',
    'addBulkUsersControllerApp',
    'createUserGroupControllerApp',
    'editUserGroupControllerApp',
    'deleteUserGroupControllerApp',
    'manageUserGroupControllerApp',
    'deleteRoleControllerApp',
    'userListControllerApp',
    'deleteUserControllerApp',
    'manageRolesControllerApp',
    'editRoleControllerApp',
    'editUserControllerApp'],
    function (app) {
  'use strict';

var userRoutesApp = angular.module('userRoutesApp', ['ui.router', 'manageUsersControllerApp', 'addUsersControllerApp',
    'addBulkUsersControllerApp',
    'createUserGroupControllerApp',
    'editUserGroupControllerApp',
    'deleteUserGroupControllerApp',
    'manageUserGroupControllerApp',
    'deleteRoleControllerApp',
    'userListControllerApp',
    'deleteUserControllerApp',
    'manageRolesControllerApp',
    'editRoleControllerApp',
    'editUserControllerApp']
    ).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('users', {
        url: '/users',
        views: {
            "main": {
                 templateUrl: 'static/partials/manage-users/manageusers.partial.html',
                controller: 'ManageUsersController'
            }
        },
        data: {
            pageTitle: 'Manage Users'

        }
    }).state('addUser', {
        url: '/adduser',
        views: {
            "main": {
                 templateUrl: 'static/partials/manage-users/addusers.partial.html',
                controller: 'AddNewUserController'
            }
        },
        data: {
            pageTitle: 'Create New User'

        }
    }).state('editUser', {
        url: '/edit/user/:id',
        views: {
            "main": {
                controller: 'UserListController'
            }
        },
        data: {
            pageTitle: 'Edit User'

        }
    }).state('deleteUser', {
        url: '/delete/user/:id',
        views: {
            "main": {
                 templateUrl: 'Admin/user-list.tpl.html',
                controller: 'DeleteUserController'
            }
        },
        data: {
            pageTitle: 'All Users'

        }
    }).state('manageRoles', {
        url: '/manageroles',
        views: {
            "main": {
                 templateUrl: 'static/partials/manage-users/managerole.partial.html',
                controller: 'ManageRolesController'
            }
        },
        data: {
            pageTitle: 'Manage Role'

        }
    }).state('addRole', {
        url: '/addrole',
        views: {
            "main": {
                 templateUrl: 'Admin/roles-manage.tpl.html',
                controller: 'ManageRolesController'
            }
        },
        data: {
            pageTitle: 'Manage Role1'

        }
    }).state('editRole', {
        url: '/editrole/:id',
        views: {
            "main": {
                 templateUrl: 'Admin/role-edit.tpl.html'
//                controller: 'EditRoleController'
            }
        },
        data: {
            pageTitle: 'Edit Role Permissions'

        }
    }).state('deleteRole', {
        url: '/deleterole/:id',
        views: {
            "main": {
                 templateUrl: 'Admin/role-list.tpl.html',
                controller: 'DeleteRoleController'
            }
        },
        data: {
            pageTitle: 'Manage Role'

        }
    })
    /* Added By Dipak  For Adding State for User Group Start*/
    .state('manageUserGroups', {
        url: '/manage/users/groups',
        views: {
            "main": {
                 templateUrl: 'static/partials/manage-users/manageusergroup.partial.html',
                controller: 'ManageUserGroupsController'
            }
        },
        data: {
            pageTitle: 'Manage User Groups'

        }
    }).state('createUserGroup', {
        url: '/create/user/group',
        views: {
            "main": {
                templateUrl: 'static/partials/manage-users/addusergroup.partial.html',
                controller: 'CreateUserGroupController'
            }
        },
        data: {
            pageTitle: 'Create New User Group'
        }
    }).state('editUserGroup', {
        url: '/edit/user/group/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/manage-users/editusergroup.partial.html',
                controller: 'EditUserGroupController'
            }
        },
        data: {
            pageTitle: 'Edit User Group'
        }
    }).state('deleteUserGroup', {
        url: '/delete/user/group/:id',
        views: {
            "main": {
                templateUrl: 'Admin/manage-user-groups.tpl.html',
                controller: 'DeleteUserGroupController'
            }
        },
        data: {
            pageTitle: 'Manage User Groups1'
        }
    }).state('viewUserGroup', {
        url: '/team/view/:id',
        views: {
            "main": {
                controller: 'ViewUserGroupController'
            }
        },
        data: {
            pageTitle: 'View User Group'

        }
    }).state('addBulkUser', {
        url: '/users/import',
        views: {
            "main": {
                templateUrl: 'static/partials/manage-users/addbulkuser.partial.html',
                controller:'AddBulkUsersController'
            }
        },
        data: {
            pageTitle: 'Create Bulk User'

        }
    })
    /* Added By Dipak  For Adding State for User Group End*/
    .state('notificationService', {
        url: '/notificationservice',
        views: {
            "main": {
                 templateUrl: 'Admin/notification-service.tpl.html'
                //controller: 'ManageRolesController'
            }
        },
        data: {
            pageTitle: 'Notification Service'

        }
    });
});

});