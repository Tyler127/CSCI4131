/* MY SCHEDULE */
function updateImage(imageName) {
    // console.log('image hovered: ' + imageName);

    image = document.getElementById('myScheduleImg');

    switch (imageName) {
        case 'anderson':
            image.setAttribute('src', '/img/anderson.jpg');
            break;
        
        case 'akerman':
            image.setAttribute('src', '/img/akerman.jpg');
            break;

        case 'rec':
            image.setAttribute('src', '/img/rec.jpg');
            break;

        case 'smith':
            image.setAttribute('src', '/img/smith.jpg');
            break;

        case 'tate':
            image.setAttribute('src', '/img/Tate.png');
            break;
        
        case 'walter':
            image.setAttribute('src', '/img/walter.jpg');
            break;

        case 'zoom':
            image.setAttribute('src', '/img/zoom.jpg');
            break;
    }

    image.setAttribute('height', '500px');
    image.setAttribute('width', '500px');
}

function toggleKeywordsField() {
    var category = document.getElementById('category').value;
    var keywordsField = document.getElementById('keywords');

    if (category === 'other') {
        keywordsField.removeAttribute('disabled');
    } else {
        keywordsField.setAttribute('disabled', 'disabled');
    }
}



/* GOOGLE MAPS API CODE */
var map;
var allMarkers = [];
var directionsService;
var directionsRenderer;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 44.9727, lng: -93.23540000000003},
        zoom: 16
    });
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);
    directionsRenderer.setPanel(document.getElementById('directionsPanel'));
    infowindow = new google.maps.InfoWindow();
}

/* Removes all current markers from the map. */
function clearMarkers() {
    for (var i = 0; i < allMarkers.length; i++) {
        allMarkers[i].setMap(null);
    }
    allMarkers = [];
}

/* Takes HTML form input, then removes old markers and adds new ones for 
the search */
function searchPlaces() {
    clearMarkers();

    var query = document.getElementById('category').value;
    const radius = document.getElementById('radius').value;

    var keywords = "";
    if (query === 'other') {
        keywords = document.getElementById('keywords').value;
        getPlaces(query, radius, keywords);
    }

    getPlaces(query, radius);
}

/* Takes a query and radius then creates a marker on the map for each resulting 
place in that radius. */
function getPlaces(query, radius, keywords="") {
    var request;
    if (keywords === "") {
        request = {
            location: map.getCenter(),
            radius: radius,
            type: [query]
        };
    } else {
        request = {
            location: map.getCenter(),
            radius: radius,
            keyword: keywords
        };
    }
    
    service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, function(results, status) {
    if (status === google.maps.places.PlacesServiceStatus.OK && results) {
        console.log(results.length);

        for (let i = 0; i < results.length; i++) {
            createMarker(results[i]);
        }

        map.setCenter(results[0].geometry.location);
    }
    });
}

/* Creates a marker on the map using a place returned by the Places API. */
function createMarker(place) {
    if (!place.geometry || !place.geometry.location) return;

    console.log(place);

    var infowindow = new google.maps.InfoWindow();
    infowindow.setContent(place.name + "<br>" + place.vicinity);

    var marker = new google.maps.Marker({ map: map, 
                                        position: place.geometry.location,
                                        title: place.name});
    
    marker.addListener('click', function(){infowindow.open(map,marker);});
    allMarkers.push(marker);
}

/* Finds the coordinates of a location's top result in the Places API and 
calls the callback function with the coordinates as the parameter. */
function getCoords(location, callback) {
    var service = new google.maps.places.PlacesService(map);

    // Ensure that the address of the marker is an address
    if (typeof location !== 'string' || location == "Remote") {
        callback("ERROR")
    }

    //console.log("querying: " + location);

    var request = {
        query: location,
        fields: ['name', 'geometry'],
    };

    service.findPlaceFromQuery(request, function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK && results) {
            callback(results[0].geometry.location);
        }
    })
}

/* Creates a marker on the map using a list of marker data that contains 
the following: name, time, address */ 
function createMarkerFromData(markerData) {
        let name = markerData[0];
        let time = markerData[1];
        let address = markerData[2];

        getCoords(address, function(coords) {
            if (coords === "ERROR") return;

            //console.log("Creating marker with: " + name + " " + time + " " + address + " " + coords);

            var infowindow = new google.maps.InfoWindow();
            infowindow.setContent(name + "<br>" + time + "<br>" + address);

            var marker = new google.maps.Marker({ map: map, 
                                                position: coords,
                                                title: name});
            
            marker.addListener('click', function(){infowindow.open(map,marker);});
            allMarkers.push(marker);
        });
}

/* Creates a route on the map from the user's location to the destination 
specified in the input form using the specified mode of transportation. */
function createRoute() {
    getUserLocation(function(position) {
        var origin = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        var destination = document.getElementById('destination').value;
        var travelMode = $('input[name=mode]:checked').val();

        // console.log(position.coords.latitude);
        // console.log(position.coords.longitude);
        // console.log(destination);
        // console.log(travelMode);

        var request = {
            origin: origin,
            destination: destination,
            travelMode: travelMode
        }

        directionsService.route(request, function(result, status) {
            if (status == 'OK') {
                directionsRenderer.setDirections(result);
            }
        });
    });
}

/* Gets the user's location and calls the callback function with the position */
function getUserLocation(callback) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(callback);
    } else {
        console.log("ERROR: Geolocation not enabled");
    }
}

$(document).ready(function() {
    // Find all <tr> elements
    var trs = $('tr');
    markersData = [];

    // Loop over each <tr>
    trs.each(function() {
        // Find all child <td> elements
        var tds = $(this).find('td');
        var rowData = [];

        // Loop over each <td> and add its text to the array
        tds.each(function() {
            rowData.push($(this).text());
        });

        // Push an array with the name, time, and address to markersData
        markersData.push([rowData[1], rowData[2], rowData[3]])
    });

    //console.log(markersData);

    // Create a marker for each parsed <tr>
    for (let i = 1; i < markersData.length; i++) {
        createMarkerFromData(markersData[i]);
    }
});
