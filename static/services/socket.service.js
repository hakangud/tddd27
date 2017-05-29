(function () {
    'use strict';

    angular
        .module('ss', [])
        .factory('SocketService', SocketService);

    SocketService.$inject = ['$rootScope', '$timeout', 'FridgeService'];
    function SocketService($rootScope, $timeout, FridgeService) {
        var service = {};
        var collection = [];
        var actions = [];
        var ws = new WebSocket('ws://' + location.host + '/websocket');

        service.actions = actions;
        service.collection = collection;
        service.initWS = initWS;
        service.registerCallback = registerCallback;
        service.notifyObservers = notifyObservers;

        function registerCallback(callback) {
            collection.push(callback);
        }

        function notifyObservers() {
            angular.forEach(collection, function (callback) {
                callback();
            });
        }

        ws.onmessage = function(msg) {
            console.log('onmessage');
            console.log(msg.data);
            actions[0] = JSON.parse(msg.data);
            notifyObservers();
        };

        function initWS(email) {
            ws.send(JSON.stringify({ data: email}));
        }

        return service;

        /*function listener(data) {
            var messageObj = data;
            console.log("Received data from websocket: ", messageObj);
            // If an object exists with callback_id in our callbacks object, resolve it
            if(callbacks.hasOwnProperty(messageObj.callback_id)) {
                console.log(callbacks[messageObj.callback_id]);
                $rootScope.$apply(callbacks[messageObj.callback_id].cb.resolve(messageObj.data));
                delete callbacks[messageObj.callbackID];
            }
        }*/

        /*function init(email) {
            var fc = FridgeService.getFridgeContent;
            $rootScope.ws = new WebSocket('ws://' + location.host + '/websocket');
            $rootScope.ws.binaryType = 'arraybuffer';

            $rootScope.ws.onopen = function () {
                console.log('connected');
                $rootScope.ws.send(email);
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
        }*/

        function listener(data) {
            var messageObj = data;
            console.log("Received data from websocket: ", messageObj);
            // If an object exists with callback_id in our callbacks object, resolve it
        }

    }

})();
