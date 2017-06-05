(function () {
    'use strict';

    angular
        .module('app', ['ngRoute', 'ngCookies', 'vpwd', 'ss', 'us', 'msg', 'auth', 'fs', 'ui.bootstrap', 'ui.bootstrap.tpls'])
        .config(config)
        .run(run);

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
    }

    run.$inject = ['$rootScope', '$window'];
    function run($rootScope, $window) {
        /*$window.onLoadFunction = function () {
            gapi.client.setApiKey('AIzaSyAcyC_XY9QBTct_r45E9yUNFaSILAY81kA');
            gapi.client.load('plus', 'v1', function() {});
        };

        (function () {
            var p = document.createElement('script');
            p.type = 'text/javascript';
            p.async = true;
            p.src = 'https://apis.google.com/js/client.js?onload=onLoadFunction';
            var s = document.getElementsByTagName('script')[0];
            s.parentNode.insertBefore(p, s);
        })();*/

        /* FACEBOOK

        $rootScope.user = {};

        $window.fbAsyncInit = function () {
            FB.init({
                appId: '734104520105087',
                status: true,
                xfbml: true,
                version: 'v2.8'
            });

            //sAuth.watchAuthenticationStatusChange();

        };
        
        (function (d) {
            var js,
                id = 'facebook-jssdk',
                ref = d.getElementsByTagName('script')[0];
            if (d.getElementById(id)) {
                return;
            }

            js = d.createElement('script');
            js.id = id;
            js.async = true;
            js.src = "//connect.facebook.net/en_US/all.js";

            ref.parentNode.insertBefore(js, ref);

        }(document));*/
    }

})();