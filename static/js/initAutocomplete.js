//Create a map window with a SearchBox and associated InfoBoxes
//Center on the U.S.
function initAutocomplete() {
	var map = new google.maps.Map(document.getElementById('map'), {
	center: {lat: 37.09024, lng: -95.71289100000001},
	zoom: 4,
	mapTypeId: google.maps.MapTypeId.ROADMAP
	});

	// Create the search box and link it to the UI element.
	var input = document.getElementById('pac-input');
	var searchBox = new google.maps.places.SearchBox(input);
	map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

	// Bias the SearchBox results towards current map's viewport.
	map.addListener('bounds_changed', function() {
		searchBox.setBounds(map.getBounds());
	});

	var markers = [];
	  // [START region_getplaces]
	  // Listen for the event fired when the user selects a prediction and retrieve
	  // more details for that place.
	searchBox.addListener('places_changed', function() {
		var places = searchBox.getPlaces();

		if (places.length == 0) {
			return;
		} else if (places.length > 1) {
			return;
		}

		// Clear out the old markers.
		markers.forEach(function(marker) {
			marker.setMap(null);
		});
		markers = [];

		// For each place, get the icon, name and location.
		var bounds = new google.maps.LatLngBounds();
		
		
		//Identify each place found, send that back to the server, process the data,
		//and return the results in the form of markers to the map
		places.forEach(function(place) {
		
			//Get location data from queried location
			var position_lat = place.geometry.location.lat().toString();
			var position_lng = place.geometry.location.lng().toString();
			console.log(position_lat)
			console.log(position_lng)
			
			
			//Send location data to server to be processed by Python script
			$.ajax({
					type: "POST",
					url: '/get_markers', 
					data: JSON.stringify({
						lat: position_lat.toString(),
						lng: position_lng.toString()
						}),
					contentType:"application/json; charset=utf-8",
					dataType: "json",
					
					//Before sending data to server create a loading modal
					beforeSend: function() {
						$("#dialog-message").dialog({
							width: 200,
							height: 50,
							position: { my: "left bottom", at: "left bottom", of: $( "#map" ) },
							closeOnEscape: false,
							open: function(event, ui) { $(".ui-dialog-titlebar-close").hide(); }
						})
					},
					
					success: function(result) {
						
						$("#dialog-message").dialog("close")
						
						//Result is in JSON format
						//Loop through results to allow access to individual arrays
						var search = [];
						for (var item in result){
							var value = result[item];
							search.push(value);
						}
						
						var marker_loc = search[0][0];
						var marker_name = search[0][1];
						var marker_desc = search[0][2];
						var marker_url = search[0][3];
						
						console.log(marker_url[0])
						
						var content = "<table class='table table-bordered'><tr><th>Location Name</th><th>URL</th></tr>";
						
						for (var i = 0; i < marker_name.length; i++) {
							content += '<tr><td>' + marker_name[i] + '</td><td><a href=' + marker_url[i] + '>' + marker_url[i] + '</a></td></tr>';							
						};
						
						content += '</table>';
						console.log(content)
						document.getElementById('marker_list').innerHTML = '';
						$('#marker_list').append(content);
						//$("#marker_list").append("Hello Mo Fo");
						//document.getElementById('map').innerHTML = '<p>Come on!</p>';

						
						//Iteratively create each marker returned from server
						for(var i = 0; i < marker_loc.length; i++ ){
							//Create marker
							var marker = new google.maps.Marker({
								position: new google.maps.LatLng(marker_loc[i][0], marker_loc[i][1]),
								map: map,
								title: marker_name[i]
							});
							
							
							//Create InfoWindow
							//When clicked this will contain information about the marker
							var infowindow = new google.maps.InfoWindow({
								//content: marker_summary[i]
							});
							
							google.maps.event.addListener(marker, 'click', (function (marker, i) {
								return function () {
									var contentString = '<div id="content">'+
										'<div id="siteNotice">'+
										'</div>'+
										'<h1>'+
										marker_name[i]+
										'</h1><hr></hr>'+
										'<div id="bodyContent">'+
										'<p>'+
										marker_desc[i]+
										'</p><hr>'+
										'</div>'+
										'<div id="urls">'+
										'<p>'+
										'<a href="'+
										marker_url[i]+
										'">'+
										marker_url[i]+
										'</a>'+
										'</p>'+
										'</div>'+
										'</div>';
									
									infowindow.setContent(contentString);
									infowindow.open(map, marker);
								}
							}) 
							
							(marker, i));
							
							//Add marker to array to allow the markers to be cleared
							//with a new search
							markers.push(marker);
							
							
						}
						
										
					}
			});
			
		});
		
		
		places.forEach(function(place) {
			//Set the location of the map to the recently searched location
			if (place.geometry.viewport) {
			// Only geocodes have viewport.
				bounds.union(place.geometry.viewport);
			} else {
				bounds.extend(place.geometry.location);
			}
		});
	
		map.fitBounds(bounds);
	});
	// [END region_getplaces]
}