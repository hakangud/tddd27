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
            console.log(vm.email + " " + vm.password);
            $http.post('/login', { email: vm.email, password: vm.password })
            .then(function (response) {
                console.log(response.data.message);
            },
            function (errResponse) {
                console.log(errResponse.data.message);
            }
            );
            $location.path('/home');
        }
    }
})();

