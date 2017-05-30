(function () {
    'use strict';

    angular
        .module('app')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['$location', 'UserService', 'MsgService'];
    function RegisterController($location, UserService, MsgService) {
        var vm = this;

        vm.register = register;

        function register() {
            UserService.Create(vm.user)
                .then(function (response) {
                    MsgService.Success(response.data.message);
                    $location.path('/login');
                },
                function (errResponse) {
                    MsgService.Error(errResponse.data.message);
                }
            );
        }
    }
})();