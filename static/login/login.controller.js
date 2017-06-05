(function () {
    'use strict';

    angular
        .module('app')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$rootScope','$location', '$http', 'MsgService', '$scope', 'FridgeService', '$window', 'AuthService', 'SocketService'];
    function LoginController($rootScope, $location, $http, MsgService, $scope, FridgeService, $window, AuthService, SocketService) {
        var vm = this;
        vm.SocketService = SocketService;
        vm.googleLogin = googleLogin;
        vm.login = login;
        function googleLogin() {
            gapi.load('auth2', function() {
                gapi.auth2.init({
                    client_id: '192085420693-gnet8a4sjhn89ll6ejjho1tudv3l2oaa.apps.googleusercontent.com',
                    scope: "profile email"
                }).then(function (auth2) {
                    var auth = gapi.auth2.getAuthInstance();
                    auth.signIn().
                        then(function () {
                            var googleUser = auth.currentUser.get();
                            var id_token = googleUser.getAuthResponse().id_token;
                            AuthService.GoogleServerAuth(id_token)
                                .then(function (response) {
                                    SocketService.initWS(googleUser.getBasicProfile().getEmail());
                                    MsgService.Success(response.data.message);
                                    FridgeService.setHasFridge(response.data.has_fridge);
                                    FridgeService.setFridgeContent(response.data.data);
                                    $location.path('/home');
                                },
                                function (errResponse) {
                                    MsgService.Error(errResponse.data.message);
                                    $location.path('/login');
                                });
                        });
                });
            });
        }

        function login() {
            console.log(vm.email + " " + vm.password);
            $http.post('/login', { email: vm.email, password: vm.password })
            .then(function (response) {
                console.log(response.data.message);
                FridgeService.setHasFridge(response.data.has_fridge);
                FridgeService.setFridgeContent(response.data.data);
                vm.data = response.data.data;
                console.log(vm.data);
                SocketService.initWS(vm.email);
                $location.path('/home');
            },
            function (errResponse) {
                console.log(errResponse.data.message);
                MsgService.Error(errResponse.data.message);
            }
            );
        }
    }

})();