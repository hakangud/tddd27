(function () {
    'use strict';

    angular
        .module('app', ['ngRoute'])
        .config(['$routeProvider',
            function($routeProvider) {
            //console.log("app.js");
            $routeProvider
                .when('/', {
                    templateUrl: '/static/home/home.view.html'
                })

                .when('/login', {
                    templateUrl: '/static/login/login.view.html'
                })

                .otherwise({ redirectTo: '/' });
        }]);
})();