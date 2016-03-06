angular.module('mainApp')
.controller('appController', ['$scope', 'appService',

	function($scope, appService) {		

		$scope.view2 = false;
		$scope.videoUrl = "";

		$scope.triggerSpeech = function() {
			console.log("here1");
			return appService.triggerSpeech()
				.then(function(response) {
	
					$scope.videoUrl = response[0];
					$scope.song = response[1];
					console.log($scope.song);
					$scope.view2 = true;
					startMusic();
				});
		}

		$scope.startMusic = function(songName) {

			var audio = new Audio('../static/music/' + songName);
			audio.play(); 
		}
	}
]);