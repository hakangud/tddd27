(function () {
    'use strict';

    angular
        .module('app')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$location', '$http'];
    function LoginController($location, $http) {
        var vm = this;
        vm.login = login;
        console.log("logC");

        function login() {
            console.log(vm.username + " " + vm.password);
            $http.post('/login', { username: vm.username, password: vm.password })
                .then(function (response) {
                    console.log(response.data.message);
                });
            $location.path('/home');
        }
    }
})();