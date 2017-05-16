(function () {
    'use strict';

    angular
        .module('app')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$location'];
    function LoginController($location) {
        var vm = this;
        vm.login = login;

        function login() {
            $location.path('/home');
            console.log("logC");
        };
    };
})();