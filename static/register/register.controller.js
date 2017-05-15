(function () {
    'use strict';

    angular
        .module('app')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['$location'];
    function RegisterController($location) {
        var vm = this;
        console.log("regC");
    };
})();