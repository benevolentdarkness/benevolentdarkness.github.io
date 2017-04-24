var ChatApp = angular.module('ChatApp', []);

ChatApp.controller('ChatController', function($scope){
    var socket = io.connect('https://' + document.domain + ':' 
    +location.port);
    
    $scope.sugs = [];
    $scope.messages = [];
    $scope.name = '';
    $scope.text = '';
    $scope.sometext = '';
    
    $scope.send = function send(){
        console.log($scope.msg);
        socket.emit('send', $scope.msg);
    };
    
    socket.on('message', function(msg){
       console.log(msg);
       $scope.messages.push(msg);
       $scope.$apply();
       var elem = document.getElementById('msgpane');
       if(elem != null){
           console.log("Working");
            elem.scrollTop = elem.scrollHeight;
       }
       else{
           console.log("Not working");
       }
    });
    
    $scope.setText = function setText(){
        console.log($scope.msg);
        socket.emit('test', $scope.msg);
    };
    
    $scope.plusOne = function(index){
        console.log("Voted");
        socket.emit('votes', index);
        $scope.sugs[index].likes += 1;
    };
    
    socket.on('suggest', function(msg){
       console.log(msg);
       $scope.sugs.push(msg);
       $scope.$apply();
       var elem = document.getElementById('msgpane');
       if(elem != null){
           console.log("Working");
            elem.scrollTop = elem.scrollHeight;
       }
       else{
           console.log("Not working");
       }
    });
});