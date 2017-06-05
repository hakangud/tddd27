(function () {
    'use strict';

    angular
        .module('auth', [])
        .factory('AuthService', AuthService);

    AuthService.$inject = ['$http'];
    function AuthService($http) {
        var service = {};
        service.GoogleServerAuth = GoogleServerAuth;
        return service;
        function GoogleServerAuth(token) {
            return $http.post('/googleauth', { data: token });
        }
    }

})();