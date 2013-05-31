var marker;
var uberOffice = new google.maps.LatLng(37.78853, -122.395144);
function initMap() { 
	var mapProp = {
		// center: new google.maps.LatLng(51.508742,-0.120850),
		center: uberOffice,
		zoom:5,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById("map_canvas"),mapProp);
	marker = new google.maps.Marker({
		map: map,
		draggable: true,
		animation: google.maps.Animation.DROP,
		position: new google.maps.LatLng(37.78853, -122.395144)
	});
	marker.setMap(map);
	google.maps.event.addListener(marker, 'mouseover', function() {
		if (marker.getAnimation() != null) {
			marker.setAnimation(null);
		} else {
			marker.setAnimation(google.maps.Animation.BOUNCE);
		}
	});
	google.maps.event.addListener(marker, 'mouseout', function() {
		marker.setAnimation(null);
	});
}

google.maps.event.addDomListener(window, 'load', initMap);