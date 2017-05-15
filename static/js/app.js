(function () {
    'use strict';

    angular
        .module('app', ['ngRoute', 'ngCookies', 'vpwd'])
        .config(config);

    config.$inject = ['$routeProvider'];
    function config($routeProvider) {
        $routeProvider
            .when('/', {
                controller: 'LoginController',
                templateUrl: '/static/login/login.view.html',
                controllerAs: 'vm'
            })

            .when('/register', {
                controller: 'RegisterController',
                templateUrl: '/static/register/register.view.html',
                controllerAs: 'vm'
            })

            .when('/home', {
                controller: 'HomeController',
                templateUrl: '/static/home/home.view.html',
                controllerAs: 'vm'
            })

            .otherwise({ redirectTo: '/' });
    };
})();