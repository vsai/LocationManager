var uberOffice = new google.maps.LatLng(37.78853, -122.395144);

function initMap() { 
	var mapProp = {
		center: uberOffice,
		zoom:7,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById("map_canvas"),mapProp);
}

var locs = [];

var getCenterLatLng = function(locations) {
	if (locations.models.length < 1) {
		return uberOffice;
	}
	var minLat = locations.models[0].attributes.latitude;
	var maxLat = locations.models[0].attributes.latitude;
	var minLng = locations.models[0].attributes.longitude;
	var maxLng = locations.models[0].attributes.longitude;


	for (var i=0 ; i < locations.models.length ; i++) {
		var lat = locations.models[i].attributes.latitude;
		var lng = locations.models[i].attributes.longitude;

		if (lat < minLat) {
			minLat = lat;
		} else if (lat > maxLat) {
			maxLat = lat;
		}

		if (lng < minLng) {
			minLng = lng;
		} else if (lng > maxLng) {
			maxLng = lng;
		}
	}
	var midLat = (minLat + maxLat) /2;
	var midLng = (minLng + maxLng) /2;
	return new google.maps.LatLng(midLat, midLng);
}

var reRenderMap = function(locations) {
	console.log("in reRenderMap");
	var mapProp = {
		// center: uberOffice,
		center: getCenterLatLng(locations), //should now readjust center based on locations availables
		zoom:7,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById("map_canvas"),mapProp);
	var infowindow = new google.maps.InfoWindow();

	var marker, i;
	console.log("adding markers");
	console.log(locations.length);

	for (i = 0; i < locations.length; i++) {
		// debugger
		console.log('adding: ' + locations.models[i].attributes.name);
      	marker = new google.maps.Marker({
        	position: new google.maps.LatLng(locations.models[i].attributes.latitude, locations.models[i].attributes.longitude),
        	map: map,
        	draggable: true, 
        	animation: google.maps.Animation.DROP
      	});
		google.maps.event.addListener(marker, 'click', (function(marker, i) {
        	return function() {
          		infowindow.setContent("Name: " + locations[i].name);
          		infowindow.open(map, marker);
        	}
      	})(marker, i));
	}
}
google.maps.event.addDomListener(window, 'load', initMap);
