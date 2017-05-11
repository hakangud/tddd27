(function () {
    'use strict';

    angular
        .module('app', ['ngRoute'])
        .config(config)

        config.$inject = ['$routeProvider'];
        function config($routeProvider) {
            //console.log("app.js");
            $routeProvider
                .when('/', {
                    controller: 'LoginController',
                    templateUrl: '/static/login/login.view.html',
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