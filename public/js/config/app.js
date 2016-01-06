'use strict';

// Declare app level module which depends on filters, and services
var app = angular.module('advdb', [
  'advdb.filters',
  'advdb.services',
  'advdb.directives',
  'advdb.controllers',
  'ngRoute'
]);


app.config(['$routeProvider',function($routeProvider) {

	var resolveLogin = function($q, $location, Login) {
		var deferred = $q.defer(); 
		deferred.resolve();
		if( !Login.user )
			$location.path('/login');
		return deferred.promise;
	};

	$routeProvider.when('/login', {
		templateUrl: 'public/partials/login.html',
		controller: 'loginCtrl'
	}).when('/home', {
		templateUrl: 'public/partials/home.html',
		controller: 'homeCtrl',
		resolve: {
			data: resolveLogin
		}
	}).when('/profile', {
		templateUrl: 'public/partials/profile.html',
		controller: 'profileCtrl',
		resolve: {
			data: resolveLogin
		}
	}).when('/matches', {
		templateUrl: 'public/partials/matches.html',
		controller: 'matchesCtrl',
		resolve: {
			data: resolveLogin
		}
	}).otherwise({
		redirectTo: '/login'
	});
}]);