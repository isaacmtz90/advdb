'use strict';

/* Directives */
var Directives = angular.module('advdb.directives', []);

Directives.directive("advdb", [function () {
    return {
        restrict: 'E',
        templateUrl: 'partials/directive.html',
        link: function (scope, element, attributes) {

        },
        controller: ['$scope',function($scope){

        }]
    }
}]);

Directives.directive("matchHeader", [function () {
    return {
        restrict: 'E',
        templateUrl: 'partials/header.html',
        scope: {},
        link: function (scope, element, attributes) {
            scope.noLogin = true;
        },
        controller: ['$scope','Login',function($scope,Login){
            Login.registerScope($scope);
            Login.success = function(){
                $scope.noLogin = false;
                $scope.data = {
                    user: Login.user,
                    Login: Login
                };
                window.location = '#/home';
            };
            Login.fail = function(){
                alert('fail');
            };
        }]
    }
}]);

Directives.directive("matchFooter", [function () {
    return {
        restrict: 'E',
        templateUrl: 'partials/footer.html',
        scope: {},
        link: function (scope, element, attributes) {
    
        },
        controller: ['$scope',function($scope){
   
        }]
    }
}]);