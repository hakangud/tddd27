(function () {
    'use strict';

    angular
        .module('msg', [])
        .factory('MsgService', MsgService);

    MsgService.$inject = ['$rootScope', '$timeout'];
    function MsgService($rootScope, $timeout) {
        var service = {};
        service.Success = Success;
        service.Error = Error;

        return service;

        function Success(message) {
            $timeout.cancel($rootScope.timer);
            $rootScope.flash = {
                message: message,
                type: 'success'
            };
            $rootScope.timer = $timeout(function () {
                delete $rootScope.flash;
            }, 5000);
        }

        function Error(message) {
            $timeout.cancel($rootScope.timer);
            $rootScope.flash = {
                message: message,
                type: 'error'
            };
            $rootScope.timer = $timeout(function () {
                delete $rootScope.flash;
            }, 5000);
        }
    }

})();
