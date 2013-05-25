// var getCoordinates = (function(address) {
// 	console.log("trying to get coordinates: " + address);
// 	var url = 'http://maps.googleapis.com/maps/api/geocode/json' +
// 				'?address=' + encodeURIComponent(address) + 
// 				'&sensor=' + encodeURIComponent(false);
// 	console.log(url);

// 	// callback function to Google Maps API
// 	// to retrieve the longitude and latitude

// 	// Backbone.sync()
// 	// Backbone.ajax = function(data) {
// 	// 	console.log(data);
// 	// }
// 	$.getJSON(url, function(data) { 
// 		console.log(data);

// 		if (data.status !== 'OK') {
// 			console.log("ERROR: Did not receive a valid address");
// 			console.log("Retrieved status: " + data.status);
// 			return null;
// 		}

// 		if (data.results.length < 1) {
// 			console.log("ERROR: UNKNOWN LEN(RESULTS) < 1. Should not have returned OK");
// 			return null;
// 		} else if (data.results.length === 1) {
// 			console.log("Received 1 result");
// 		} else {
// 			console.log("Received more than one result. Returning first option.");
// 		}

// 		var loc_obj = data.results[0].geometry.location;
// 		console.log("location obj: " + loc_obj.lat + " ; " + loc_obj.lng);
// 		return loc_obj;
// 	});
// });

(function ($) {

	Loc = Backbone.Model.extend({
		//Create a model to hold location atribute
		name: null,
		address: null,
		latitude: null,
		longitude: null
	});

	Locs = Backbone.Collection.extend({
	//This is our Locs collection and holds our Loc models
		initialize: function (models, options) {
			console.log("Initialize locs");
			this.bind("add", options.view.addLocationLi);
			//Listen for new additions to the collection and call a view function if so
		}
	});


	AppView = Backbone.View.extend({
		el: $("body"),
		initialize: function () {
			console.log("Initialize AppView");
			this.locations = new Locs( null, { view: this });
			//Create a friends collection when the view is initialized.
			//Pass it a reference to this view to create a connection between the two
		},
		
		events: {
			"click #add-location":  "addLocation",
			"click #delete-location":  "deleteLocation",
		},

		addLocation: function () {
			console.log("in addLocation");
			var loc_name = $('input[name=name]').val();
			var loc_addr = $('input[name=address]').val();
			// var loc_coords = getCoordinates(loc_addr);

			// if (loc_coords === null) {
			// 	alert("Not a valid address");
			// 	return;
			// }
			var loc_model = new Loc({name: loc_name, address: loc_addr});
			// var loc_model = new Loc({name: loc_name, address: loc_addr, latitude: loc_coords.lat, longitude: loc_coords.lng});
			this.locations.add( loc_model );

			$('input[name=name]').val('');
			$('input[name=address]').val('');
		},

		deleteLocation: function() {
			console.log("in deleteLocation");
			// var loc_name = $('input[name=name]').val();
			// var p = this.locations.where({'name' : loc_name});
			// var p = this.locations.fetch({'name':loc_name});
			// console.log(p);
			console.log("deleted");
		},

		
		addLocationLi: function (model) {
			//The parameter passed is a reference to the model that was added
			$("#location-list").append("<li>" + model.get('name') + " : " + model.get('address') + "</li>");
		}
	});

	var appview = new AppView;
})(jQuery);