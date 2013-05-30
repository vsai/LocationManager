(function ($) {

	LocationModel = Backbone.Model.extend({
		//Create a model to hold location atribute
		defaults: {
			id: null,
        	name: null,
			address: null,
			latitude: null,
			longitude: null
    	}
	});

	LocationCollection = Backbone.Collection.extend({
	//This is our Location collection and holds our Location models
		model: LocationModel,
		// url: 'http://127.0.0.1:5000',
		url: '/locations',

		//Parse the response
		parse: function (response) {
			console.log("Inside Parse");
			console.log(Object.keys(response));
			console.log(response.results);
			var location;
			var results_length = response.results.length;
			console.log(this);
			var x = [];
			for (var i = 0; i < results_length; i++) {
				console.log(JSON.stringify(response.results[i]));
				x.push(response.results[i]);
				// this.models.push(response.results[i]);
			}
			// console.log(this.toJSON());
			console.log("Returning from parse:");
			console.log(x);
			console.log(JSON.stringify(x));
			console.log(this.models);
			console.log("Leaving parse");
			// return this.models;
			// var myJsonString = JSON.stringify(x);
			// return myJsonString;
			return x;
		},

		initialize: function (models, options) {
			console.log("Initialize location collection");
			this.bind("add", options.view.addLocationLi);
			this.bind("remove", options.view.removeLocationLi);
		}
	});

	// LocationView = Backbone.View.extend({

	// });

	AppView = Backbone.View.extend({
		el: $("body"),
		initialize: function () {
			console.log("Initialize AppView");
			this.locations = new LocationCollection( null, { view: this });
			this.locations.fetch({
				success: function(data, xhr) {
					console.log("PLEASE LET THIS WORK!!!!!!!!");
					console.log(data);
					console.log(typeof data);
					console.log(JSON.stringify(data));
				},
                error: function(errorResponse) {
                	console.log("NOOOOOOOOOOO");

                },
				processData: true
			});
			console.log("fetching locations");
			console.log(this.locations.length);
		//Pass it a reference to this view to create a connection between the two
		},

		events: {
			"click #add-location":  "addLocation",
			"click #remove-location":  "removeLocation",
		},

		addLocation: function () {
			console.log("in addLocation");
			var loc_name = $("input[name=name]").val();
			var loc_address = $("input[name=address]").val();
			$("#add_location_form > input[name=name]").val('');
			$("#add_location_form > input[name=address]").val('');

			// var self = this; //to be able to access the locations collection
			var data = googleAddress(loc_address);
			if (data.status !== 'OK') {
					console.log("ERROR: Did not receive a valid address");
					console.log("Retrieved status: " + data.status);
					addAlertBox("No such address found. Please try again", "error");
					return;
				}
			var loc_obj;
			if (data.results.length < 1) {
				console.log("ERROR: UNKNOWN LEN(RESULTS) < 1. Should not have returned OK");
				addAlertBox("No such address found. Please try again", "error");
				return;
			} else if (data.results.length === 1) {
				console.log("Received 1 result");
				loc_obj = data.results[0];
			} else {
				console.log("Received more than one result. Returning first option.");
				loc_obj = addressSelect(data.results);
			}
			loc_address = loc_obj.formatted_address;
			console.log("Formatted Address: " + loc_address);
			var loc_coords = loc_obj.geometry.location;
			if (loc_coords === null) {
				addAlertBox("No such address found. Please try again", "error");
				return;
			}
			console.log("location coords: " + loc_coords.lat + " ; " + loc_coords.lng);
			var loc_model = new LocationModel({name: loc_name, address: loc_address, latitude: loc_coords.lat, longitude: loc_coords.lng});
			console.log("created location model. adding to collection");
			var abc = this.locations.create(loc_model);
			console.log(abc);
			// this.locations.add(loc_model);
		},

		removeLocation: function() {
			console.log("in removeLocation");
			bootbox.confirm("Are you sure you want to remove this location?", function(result) {
				console.log(result);
  				if (result) {
  					console.log("send remove request to server");
  					console.log("remove from list");
  				}
  			});
			console.log("removed");
			// this.locations.remove(elem);
		},
		
		addLocationLi: function (model) {
			//The parameter passed is a reference to the model that was added
			var name = "<td>" + model.get('name') + "</td>";
			var address =  "<td>" + model.get('address') + "</td>";
			var moreOptions = "<td>button here</td>";
			var remove = "<td><button onclick='removeLocation()' class='btn'>X</button></td>";
			$("#loc_display_table").append("<tr>" + name + address + moreOptions + remove + "</tr>");
		},

		removeLocationLi: function (model) {
			//The parameter passed is a reference to the model that was removed

		}
	});
	var appview = new AppView;

})(jQuery);


function addressSelect(gMapsResults) {
	$('#myModal').modal('toggle');
	var result_address;
	for (var i = 0; i < gMapsResults.length; i++) {
		result_address = gMapsResults[i].formatted_address;
		$("#modal_address_options").append("<input type='radio' name='address' value='" + i.toString() + "'>" + result_address + "</input><br>");
	}
	// ////////////////////////////////////
	// TO FIX
	// ////////////////////////////////////
	return gMapsResults[0];
}

function closeModal(method) {
	if (method === "submit") {
		var select;
	} else {
	}
	$('#myModal').modal('toggle');
	$("#add_location_form > input[name=name]").val('');
	$("#add_location_form > input[name=address]").val('');
}

function submitModal() {
	var add_selected = $("#modal_address_options > input[name='address']:checked").val();
	console.log("YOLOSWAG");
	console.log(add_selected);
	closeModal("submit");
}

function addAlertBox(message, level) {
	// level = "success" || "error" || "info"
	deleteAlertBox();
	if (level !== "success" || level !=="error" || level !== "info") {
		level = "error";
	}
	console.log("adding alert box");
	var close_btn = "<button type = 'button' class='close' data-dismiss='alert'>&times;</button>";
	var alertBox = "<div class='alert alert-" + level + "' id='alertbox'>" + close_btn + "<p>" + message + "</p></div>";
	$("#alertbox_wrap").append(alertBox);
}

function deleteAlertBox() {
	var parent=document.getElementById("alertbox_wrap");
	var child=document.getElementById("alertbox");
	if (child === null) {
		console.log("no child alert box");
	} else {
		console.log("removing child alert box");
		parent.removeChild(child);
	}
}
