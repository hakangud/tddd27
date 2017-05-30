(function () {
    'use strict';

    angular
        .module('auth', [])
        .factory('AuthService', AuthService);

    AuthService.$inject = ['$rootScope', '$http'];
    function AuthService($rootScope, $http) {
        var service = {};

        service.GoogleServerAuth = GoogleServerAuth;

        return service;

        function GoogleServerAuth(token) {
            return $http.post('/googleauth', { data: token });
        }
    }

})();