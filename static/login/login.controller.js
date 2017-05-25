(function () {
    'use strict';

    angular
        .module('app')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$location', '$http', 'MsgService', '$scope', 'FridgeService'];
    function LoginController($location, $http, MsgService, $scope, FridgeService) {
        var vm = this;
        vm.login = login;
        console.log("logC");

        function login() {
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