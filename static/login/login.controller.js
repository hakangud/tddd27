(function () {
    'use strict';

    angular
        .module('app')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$location'];
    function LoginController($location) {
        var vm = this;
        vm.login = login;
        console.log("logC");

        function login() {

            $location.path('/home');
        };
    };
})();