(function () {
    'use strict';

    angular
        .module('ss', [])
        .factory('SocketService', SocketService);

    SocketService.$inject = ['$rootScope', '$timeout'];
    function SocketService($rootScope, $timeout) {
        var service = {};

        service.init = init;

        return service;

        function init() {
            $rootScope.ws = new WebSocket('ws://' + location.host + '/websocket');
            $rootScope.ws.binaryType = 'arraybuffer';

            $rootScope.ws.onopen = function () {
                console.log('connected');
                $rootScope.ws.send("123");
            };
            $rootScope.ws.onmessage = function (evt) {
                listener(evt);
                $rootScope.$apply(function () {
                    var message = json.parse(evt.data);
                    console.log(message.action);
                });
            };
            $rootScope.ws.onclose = function () {
                console.log('connection closed');
            };
        }

        function listener(data) {
            var messageObj = data;
            console.log("Received data from websocket: ", messageObj);
            // If an object exists with callback_id in our callbacks object, resolve it
        }

    }

})();
