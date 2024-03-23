var locationForm = document.getElementById('location');

var map;
var allMarkers = [];
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 44.9727, lng: -93.23540000000003},
        zoom: 16
    });

    infowindow = new google.maps.InfoWindow();

    map.addListener('click', function(event) {
        var geocodingRequestURL = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + 
                                   event.latLng.lat() + "," + event.latLng.lng() + 
                                   "&key=AIzaSyAzT6-ldxhAWi5ZIKm20YtkVGobVCfbvmE";
        fetch(geocodingRequestURL)
        .then(response => response.json())
        .then(jsonData => {
            console.log(jsonData.results[0].formatted_address);
            locationForm.value = jsonData.results[0].formatted_address;
        });
    });
}
