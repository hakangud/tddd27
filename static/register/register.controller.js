(function () {
    'use strict';

    angular
        .module('app')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['$location', 'UserService'];
    function RegisterController($location, UserService) {
        var vm = this;

        vm.register = register;
        console.log("regC");

        function register() {
            console.log("reg");
            UserService.Create(vm.user)
                .then(function (response) {
                    console.log(response);
                    console.log(response.data);
                    $location.path('/login');
                },
                function (errResponse) {
                    console.log("reg_error");
                }
            );
        }
    }
})();