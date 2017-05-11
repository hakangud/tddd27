(function () {
    'use strict';

    angular
        .module('app', ['ngRoute'])
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
                templateUrl: '/static/register/register.view.html'
            })

            .when('/home', {
                controller: 'HomeController',
                templateUrl: '/static/home/home.view.html',
                controllerAs: 'vm'
            })

            .otherwise({ redirectTo: '/' });
    };
})();