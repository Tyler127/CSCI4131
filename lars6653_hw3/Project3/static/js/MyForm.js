var location = document.getElementById('location');

var map;
var allMarkers = [];
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 44.9727, lng: -93.23540000000003},
        zoom: 16
    });

    infowindow = new google.maps.InfoWindow();

    map.addListener('click', function(event) {
        var geocodingRequestURL = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + event.latLng.lat() + "," + event.latLng.lng() + "&key=AIzaSyAzT6-ldxhAWi5ZIKm20YtkVGobVCfbvmE";
        
        fetch(url).then(response => response.json()).then(data => {
            console.log(data.results[0].formatted_address);
            location.value = data.results[0].formatted_address;
        });
    });
}
