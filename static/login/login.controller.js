(function () {
    'use strict';

    angular
        .module('app')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$rootScope','$location', '$http', 'MsgService', '$scope', 'FridgeService', '$window', 'AuthService', 'SocketService'];
    function LoginController($rootScope, $location, $http, MsgService, $scope, FridgeService, $window, AuthService, SocketService) {

        var vm = this;

        vm.gmail = {
            username: '',
            email: ''
        };

        vm.auth = '';

        $window.onGoogleLogin = onGoogleLogin;
        //vm.fblogin = fblogin;
        vm.login = login;
        //vm.onSignIn = onSignIn;
        console.log("logC");

        /*function onGoogleLogin() {
            console.log("GOOGLE LOGIN");
            var params = {
                'clientid': '192085420693-gnet8a4sjhn89ll6ejjho1tudv3l2oaa.apps.googleusercontent.com',
                'cookiepolicy': 'single_host_origin',
                'callback': function(result) {
                    console.info(result);
                    if (result['status']['signed_in']) {
                        AuthService.GoogleServerAuth(result['code']);
                        console.log(result['code']);
                        vm.auth = result['code'];
                        var request = gapi.client.plus.people.get(
                            {
                                'userId': 'me'
                            }
                        );
                        request.execute(function (resp) {
                            $rootScope.$apply(function () {
                                vm.gmail.username = resp.displayName;
                                vm.gmail.email = resp.emails[0].value;
                            });
                        });
                    }
                },
                'approvalpromt': 'force',
                'scope': 'https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/plus.profile.emails.read'
            };
            console.log(params);
            gapi.auth.signIn(params);
        }*/

        /*
        FACEBOOK LOGIN, NOT IMPLEMENTED
        function fblogin() {
            console.log("FBLOGINC");
            AuthService.Login();
        }*/

        function onGoogleLogin(googleUser) {
            console.log("google signin");
            var id_token = googleUser.getAuthResponse().id_token;
            AuthService.GoogleServerAuth(id_token);
            console.log(id_token);
            var profile = googleUser.getBasicProfile();
            console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
            console.log('Name: ' + profile.getName());
            console.log('Image URL: ' + profile.getImageUrl());
            console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
        }

        function login() {
            SocketService.init();
            console.log($rootScope.ws);
            console.log(vm.email + " " + vm.password);
            $http.post('/login', { email: vm.email, password: vm.password })
            .then(function (response) {
                console.log(response.data.message);
                FridgeService.setFridgeContent(response.data.data);
                vm.data = response.data.data;
                console.log(vm.data);
                $location.path('/home');

            },
            function (errResponse) {
                console.log(errResponse.data.message);
                MsgService.Error(errResponse.data.message);
            }
            );

        }


        function login2() {
            console.log('du klickade på login2');
        }
    }

})();