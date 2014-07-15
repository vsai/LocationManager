// Improvements:
// Don't re-render the entire list on a single change
// 		> How to re-render just the necessary element?

(function ($) {
	var LocModel = Backbone.Model.extend({
		// Model to hold location attributes
		defaults: {
			name: null,
			address: null,
			latitude: null,
			longitude: null
		},
		initialize: function() {
			// console.log("This model has been initialized");
		}
	});

	var LocList = Backbone.Collection.extend({
		model: LocModel,
		url: 'locations',

		parse: function (response) {
			console.log("Inside Parse");
			if (response.status === "OK") {
				return response.results;
			} else {
				return response;
			}
		},

		initialize: function (models, options) {
			this.bind("change", options.view.render, options.view);
			console.log("initialized location list");
		}
	});

	var LocModelView = Backbone.View.extend({
		tagName: 'tr',
		template: _.template($('#locationViewTemplate').html()),

		events: {
			"click .delete_location" : "deleteLocation",
			"dblclick .updateName" : "updateName", 
			"dblclick .updateAddress" : "updateAddress"
		}, 

		initialize: function() {
			this.listenTo(this.model, "change", this.render);
		},

		render: function() {
			var data = this.model.toJSON();
			var html = this.template(data);
			this.$el.html(html);
			return this;
		},

		updateName: function() {
			var self = this;
			bootbox.prompt("Enter new name:", function(result) {
				if (result === null) {

				} else {
					console.log('changing this models name to: ' + result);
					self.model.set({name: result});
					self.model.save();
				}
			});
		},

		updateAddress: function() {
			var self = this;
			bootbox.prompt("Enter new address:", function(result) {
				if (result === null) {
				} else {
					console.log('change this models address to: ' + result);
					var newAdd = searchAddress(result);
					if (newAdd === null) {
						bootbox.alert("not a valid address");
					} else {
						self.model.set({address: newAdd.formattedAddress, longitude: newAdd.lng, latitude: newAdd.lat});
						self.model.save();
					}
				}
			})
		},

		deleteLocation: function() {
			console.log("in deleteLocation");
			var self = this;
			bootbox.confirm("Are you sure you want to remove this location?", function(result) {
				console.log(result);
  				if (result) {
  					console.log("Deleting: " + this);
					self.model.destroy();
					self.remove();
  				}
  			});
		}
	});

	var LocListView = Backbone.View.extend({
		el: $('body'),

		events: {
			"click #add-location" : "addLocation"
		},

		initialize: function() {
			var self = this;
			this.collection = new LocList(null, {view: this});
			this.collection.fetch({
				success: function(data, xhr) {
					// console.log("YESSSS");
					self.render();
					return data;
				},
				error: function(errorResponse) {
					// console.error("NOOOOOO");
				}
			});
			// debugger
			console.log("initialized location list view");
		},

		addLocation: function() {
			console.log("Location List View - adding location");
			var new_name = $("#add_location_form > input[name=name]").val();
			var new_address = $("#add_location_form > input[name=address]").val();
			$("#add_location_form > input[name=name]").val('');
			$("#add_location_form > input[name=address]").val('');

			var new_location = searchAddress(new_address);

			if (new_location === null) {
				// console.warn("NO ADDRESS COULD BE FOUND");
				addAlertBox('No such address found. Please try again.', 'error');
				return;
			}

			var new_model = new LocModel({name: new_name, 
										address: new_location.formattedAddress,
										longitude: new_location.lng,
										latitude: new_location.lat});

			var self = this;
			this.collection.create(new_model, {
				wait: true,
				success: function(resp) {
					console.log('success callback for collection create');
					self.render();
					// return resp;

				},
				error: function(err) {
					console.error('error callback for collection create');
					console.error(err);
					addAlertBox('did not store to db successfully', 'error');
					// return err;
				}
			});
			console.log("added");
		},

		render: function(){
			console.log("Location List View - rendering");
			$('#location_list_view').empty();
			this.collection.each(function(item) {
				this.renderLocation(item);
			}, this);
			reRenderMap(this.collection);
			console.log("Exiting rendering");
		},

		renderLocation: function(item) {
			var locationView = new LocModelView({model:item});
			var vHtml = locationView.render().el;
			$('#location_list_view').append(vHtml);
		}
	});

	var LocationListView = new LocListView();

})(jQuery);

var searchAddress = function(address) {
	var data = googleAddress(address);
	if (data.status !== 'OK') {
		console.log("ERROR: Not valid address. Retrieved status: " + data.status);
		return null;
	}
	var obj;
	if (data.results.length < 1) {
		console.log("ERROR: UNKNOWN LEN(RESULTS) < 1. Should not have returned OK");
		return null;
	} else if (data.results.length === 1) {
		obj = data.results[0];
	} else {
		console.warn("Received more than one result");
		obj = data.results[0];
	}
	if (obj.geometry.location === null){
		return null;
	}

	var ret_obj = {};
	// debugger
	ret_obj['formattedAddress'] = obj.formatted_address;
	ret_obj['lng'] = obj.geometry.location.lng;
	ret_obj['lat'] = obj.geometry.location.lat;
	return ret_obj;

};

var addAlertBox = function(message, level) {
	// level = "success" || "error" || "info"
	deleteAlertBox();
	if (level !== "success" || level !=="error" || level !== "info") {
		level = "error";
	}
	console.log("adding alert box");
	var close_btn = "<button type = 'button' class='close' data-dismiss='alert'>&times;</button>";
	var alertBox = "<div class='alert alert-" + level + "' id='alertbox'>" + close_btn + "<p>" + message + "</p></div>";
	$("#alertbox_wrap").append(alertBox);
};

var deleteAlertBox = function() {
	var parent=document.getElementById("alertbox_wrap");
	var child=document.getElementById("alertbox");
	if (child === null) {
		console.log("no child alert box");
	} else {
		console.log("removing child alert box");
		parent.removeChild(child);
	}
};
