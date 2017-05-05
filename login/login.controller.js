(function) () {
    'use strict';

    angular
        .module('app')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$location', 'Flashservice'];
    function LoginController($location, Flashservice) {
        var vm = this;
        vm.login = login;

        function login() {
            vm.dataLoading = true;
            console.log("asdasdas");
            Flashservice.Error("FELFELFELFLEFLFELFEFL");
        };
    };
})();