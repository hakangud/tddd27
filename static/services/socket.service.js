(function () {
    'use strict';

    angular
        .module('ss', [])
        .factory('SocketService', SocketService);

    function SocketService() {
        var service = {};
        var collection = [];
        var actions = [];
        var ws = new WebSocket('ws://' + location.host + '/websocket');
        service.ws = ws;
        service.actions = actions;
        service.collection = collection;
        service.initWS = initWS;
        service.registerCallback = registerCallback;
        service.notifyObservers = notifyObservers;

        //Register a callback function that is executed every time socket
        //receives a message (we only use a single callback, this could be
        //changed in the future if we want to register different callbacks).
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
            actions[0] = JSON.parse(msg.data);
            notifyObservers();
        };

        ws.onclose = function () {
            console.log('socket closed');
        };

        ws.onopen = function () {
            console.log('socket opened');
        };

        function initWS(email) {
            ws.send(JSON.stringify({ data: email}));
        }

        return service;
    }

})();
