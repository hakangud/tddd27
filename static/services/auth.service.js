(function () {
    'use strict';

    angular
        .module('auth', [])
        .factory('AuthService', AuthService);

    AuthService.$inject = ['$rootScope', '$http'];
    function AuthService($rootScope, $http) {
        var service = {};

        //service.WatchLoginChange = WatchLoginChange;
        //service.GetUserInfo = GetUserInfo;
        service.GoogleServerAuth = GoogleServerAuth;
        //service.Logout = Logout;

        return service;

        function GoogleServerAuth(token) {
            $http.post('/googleauth', { data: token })
                .then(function (response) {
                    console.log(response);
                })
        }


        /* FACEBOOK, NOT USED

        function Logout() {
            var vm = this;

            FB.logout(function (res) {
                console.log(res);
                $rootScope.$apply(function () {
                    $rootScope.user = vm.user = {};
                });
            });
        }

        function Login() {
            console.log("FBLOGIN");
            FB.login(function (res) {
                if (res === 'connected') {
                    console.info(res);
                    console.log(res);
                }
            });
        }

        function WatchLoginChange() {
            var vm = this;

            FB.Event.subscribe('auth.authResponseChange', function (res) {
                if (res.status === 'connected') {
                    // FORTSÄTT HÄR
                    FB.api('/me', function (res) {
                        $rootScope.$apply(function () {
                            console.log(res);
                            //$rootScope.user = vm.user = res;
                        });
                    });

                    console.log(res.authResponse);
                }
                else {
                    // destroy user session on server
                    console.log("not logged in");
                }
            });
        }*/
    }

})();