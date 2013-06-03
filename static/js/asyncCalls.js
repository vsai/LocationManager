$(function() {
    $.ajaxSetup({
        error: function(err, exception) {
            if (err.status === 0) {
            	console.log('Not connect. Verify network');
            } else if (err.status == 404) {
                console.log('Requested page not found. [404]');
            } else if (err.status == 500) {
                console.log('Internal Server Error [500].');
            } else if (err.status == 400) {
                console.log('Bad Request [400].');
            } else if (exception === 'parsererror') {
                console.log('Requested JSON parse failed.');
            } else if (exception === 'timeout') {
                console.log('Time out error.');
            } else if (exception === 'abort') {
                console.log('Ajax request aborted.');
            } else {
                console.log('Uncaught Error.\n' + jqXHR.responseText);
            }
        }
    });
});

// google Maps get Address
var googleAddress = function(address){
	var search_url = 'http://maps.googleapis.com/maps/api/geocode/json' +
					'?address=' + encodeURIComponent(address) + 
					'&sensor=' + encodeURIComponent(false);
	var result;
	$.ajax({
		url: search_url,
		type: 'get',
		datatype: 'jsonp',
		async: false,
		success: function(data){
			console.log("Successfully got json");
			console.log(data);
			result = data;
		}
	});
	return result;
};

// // web server url
// var server_url = 'http://127.0.0.1:5000/locations'
// // create

// // read Single
// var readSingle = function(id){
// 	$.ajax({
// 		url: server_url + '/' + id.toString(),
// 		type : 'get',
// 		dataType: 'application/json',
// 		success: function(data){
// 			console.log("Success read");
// 			console.log(data);
// 		}
// 	});
// };

// // read All
// var readAll = function() {
// 	$.ajax({
// 		url: server_url,
// 		type: 'get',
// 		success: function(data){
// 			console.log("Success reads");
// 			console.log(data);
// 		}
// 	});
// };

// // update
// var updateSingle = function(id, name, address, lng, lat) {
// 	$.ajax({
// 		url: server_url + "/" + id.toString(),
// 		type: 'PUT',
// 		data: {'name':name, 'address':address, 'lng':lng, 'lat':lat},
// 		success: function(data){
// 			console.log("Success update");
// 			console.log(data);
// 		}
// 	});

// };
// updateSingle(10, 'yolo', 'swag', 'yeah', 'boi');
// delete