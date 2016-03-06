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
					$scope.view2 = true;
					$scope.startMusic();
				});
		}

		$scope.startMusic = function(songName) {

			$scope.audio = new Audio('../static/music/' + songName);
			$scope.audio.play();
		}

		$scope.goToMain = function() {

			$scope.view2 = false;
			$scope.stopSong();
		}

		$scope.stopSong = function() {
			$scope.audio.pause();
		} 

		$scope.getUserRanks = function() {
			console.log("dsadasdsa");
			return appService.getBestUsers()
				.then(function(response) {

					$scope.bestUsers = response;
					$scope.bestUsers.forEach(function(user) {
						console.log(user);
					})
					console.log($scope.bestUsers);
				});
		}

		$scope.displayUser = function(user) {

			console.log(user);
		}
	}
]);