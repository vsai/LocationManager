var getCoordinates = (function(address) {
	console.log("trying to get coordinates: " + address);
	var url = 'http://maps.googleapis.com/maps/api/geocode/json' +
				'?address=' + encodeURIComponent(address) + 
				'&sensor=' + encodeURIComponent(false);
	console.log(url);
	$.getJSON(url, function(data) { 
		console.log(data);
		console.log(data.status);
		console.log(data.results.length);
		if (data.results.length === 1) {
			console.log("Received 1 option of address");
		} else if (data.results.length === 0) {
			console.log("ERROR: Did not receive a valid address");
			return null;
		} else {
			console.log("Received more than one option of address");
			console.log("Returning the first option");
			// return data[1];
		}
		var loc_obj = data.results[0].geometry.location;
		console.log("location obj: " + loc_obj.lat + " ; " + loc_obj.lng);
		return loc_obj;
	});
});




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
			"click #add-location":  "collectLocation",
		},

		collectLocation: function () {
			console.log("in collectionLocation");
			var loc_name = $('input[name=name]').val();
			var loc_addr = $('input[name=address]').val();
			console.log("collected: " + loc_name + " " + loc_addr);
			var loc_coords = getCoordinates(loc_addr);
			console.log("return from loc_coords");
			console.log(loc_coords);
			console.log("printed loc_coords");
			if (loc_coords === null) {
				alert("Not a valid address");
				return;
			}
			var loc_model = new Loc({name: loc_name, address: loc_addr, latitude: loc_coords.lat, longitude: loc_coords.lng});
			this.locations.add( loc_model );

			$('input[name=name]').val('');
			$('input[name=address]').val('');
		},
		
		addLocationLi: function (model) {
			//The parameter passed is a reference to the model that was added
			$("#location-list").append("<li>" + model.get('name') + " : " + model.get('address') + "</li>");
			//Use .get to receive attributes of the model
		}
	});

	var appview = new AppView;

})(jQuery);