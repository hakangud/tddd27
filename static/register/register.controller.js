(function () {
    'use strict';

    angular
        .module('app')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['$location'];
    function RegisterController($location) {
        var vm = this;

        vm.register = register;
        console.log("regC");

        function register() {
            console.log("reg");
            UserService.Create(vm.user)
                .then(function (response) {
                    if (response.success) {
                        $location.path('/login');
                    }
                    else {
                        console.log("reg_error");
                    }
                })
        }
    };
})();