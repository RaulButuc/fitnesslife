angular.module('mainApp')
.service('appService', ['$http', function($http) {

	return {

		triggerSpeech: function() {

			var url = '/listen';

			return $http.get(url)
				.then(function(response) {
					console.log("here2");
					return response.data;

				}, function(response) {});
		},

		getBestVideos: function() {

			var url = '/getBestVideos';

			return $http.get(url)
				.then(function(response) {
					return response.data;

				}, function(response) {});
		},
		
		getBestVideos: function() {

			var url = '/getUserRanks';

			return $http.get(url)
				.then(function(response) {
					return response.data;

				}, function(response) {});
		},

		getMyProfile: function(userId) {

			var url = '/getMyProfile';

			return $http.get(url)
				.then(function(response) {
					return response.data;

				}, function(response) {});
		},		

		increaseVideoCount: function(userId) {

			var url  = '/increseVideoView';
			var data = {'user_id' : userId};

			$http.post(url, data)
				.then(function(response) {
					return response.data;

				}, function(response) {});
		},

		increaseUserRank: function(userId) {

			var url  = '/increseUserRank';
			var data = {'user_id' : userId};

			$http.post(url, data)
				.then(function(response) {
					return response.data;

				}, function(response) {});
		},
		
	}
}]);