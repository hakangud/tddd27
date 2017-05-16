(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['$location'];
    function HomeController($location) {
        var vm = this;
        console.log("homeC");
    };
})();