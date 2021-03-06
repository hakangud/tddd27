(function () {
    'use strict';

    angular
        .module('us', [])
        .factory('UserService', UserService);

    UserService.$inject = ['$http'];
    function UserService($http) {
        var service = {};
        service.Create = Create;

        return service;

        function Create(user) {
            return $http.post('/register', user);
        }
    }

})();
