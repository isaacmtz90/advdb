'use strict';

// Declare app level module which depends on filters, and services
var app = angular.module('advdb', [
  'advdb.filters',
  'advdb.services',
  'advdb.directives',
  'advdb.controllers',
  'ngRoute'
]);

app.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider.
		when('/login', {
			templateUrl: 'public/partials/login.html',
			controller: 'loginCtrl'
		}).
		when('/home', {
			templateUrl: 'public/partials/home.html',
			controller: 'homeCtrl'
		}).
		otherwise({
			redirectTo: '/login'
		});
	}]
);