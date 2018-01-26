<script>
var map;
var markers = [];
var bounds;
var myLng, myLat;
var map_height;

map_height = $(window).height() - 60;
$("#map").height(map_height);

window.addEventListener('resize', function(event) {
  console.log("Window resize");
  map_height = $(window).height() - 60;
  $("#map").height(map_height);
});

$("#btn_my_location").click(function(evt){
  evt.preventDefault();
  if (typeof myLat != 'undefined'){
    window.location.href = "{% url 'blog:current_location' %}?lat=" + myLat + "&lng=" + myLng;
  } else {
    alert("Geolocation is blocked by broswer, please check the broswer setting.")
  }
});

function initMap() {

  map = new google.maps.Map(document.getElementById('map'), {
      zoom: 6,
      center: {lat: 36.44, lng: 120.13}
  });

  var infoWindow = new google.maps.InfoWindow({map: map});
  
  bounds = new google.maps.LatLngBounds();

  if (navigator.geolocation){
    navigator.geolocation.getCurrentPosition(function(position){

      var lat = position.coords.latitude;
      var lng = position.coords.longitude;
        // console.log(myLat, myLng);
      var tempPos = transform(lat, lng);
      console.log("Index html" + tempPos);
      myLat = tempPos[0];
      myLng = tempPos[1];

      var pos = {
        lat: myLat,
        lng: myLng
      };
      var marker = new google.maps.Marker({
        position: pos,
        label: 'My',
        map: map
      });

      markers.push(marker);
      bounds.extend(marker.position);

    }, function() {
      handleLocationError(true, infoWindow, map.getCenter());
    });
  } else {
    handleLocationError(false, infoWindow, map.getCenter());
  }

  function handleLocationError(browserHasGeolocation, infoWindow, pos) {
          infoWindow.setPosition(pos);
          infoWindow.setContent(browserHasGeolocation ?
                                'Error: The Geolocation service failed.' :
                                'Error: Your browser doesn\'t support geolocation.');
  }

  var locations = [
    {% for post in post_list %}
      {% if post.lat and post.lat != 0.0 and post.lat is not None %}
        {id: {{post.id}}, location: {lat: {{post.lat}}, lng: {{post.lng}} } },
      {% endif %}
    {% endfor %}
  ];
  
  function getCircle(color){
    return {
      path: "M27.648 -41.399q0 -3.816 -2.7 -6.516t-6.516 -2.7 -6.516 2.7 -2.7 6.516 2.7 6.516 6.516 2.7 6.516 -2.7 2.7 -6.516zm9.216 0q0 3.924 -1.188 6.444l-13.104 27.864q-0.576 1.188 -1.71 1.872t-2.43 0.684 -2.43 -0.684 -1.674 -1.872l-13.14 -27.864q-1.188 -2.52 -1.188 -6.444 0 -7.632 5.4 -13.032t13.032 -5.4 13.032 5.4 5.4 13.032z",
      scale: 0.6,
      strokeWeight: 0.2,
      strokeColor: 'black',
      strokeOpacity: 1,
      fillColor: color,
      fillOpacity: 0.85,
    }
  }

  var infoWindow = new google.maps.InfoWindow();

  for (var i = 0; i < locations.length; i++) {
      var position = locations[i].location;
      var id = locations[i].id;
      var title = locations[i].title;
      var color = '#ac00e0';


      var marker = new google.maps.Marker({
          map: map,
          position: position,
          icon: getCircle(color),
          animation: google.maps.Animation.DROP,
          id: id
      });

      marker.addListener('click',  function() {
          populateInfoWindow(this, infoWindow)
      });

      markers.push(marker);
      bounds.extend(marker.position);
  }

  map.fitBounds(bounds)

  // Add a marker clusterer to manage the markers.
  // var markerCluster = new MarkerClusterer(map, markers,
  //     {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}

$(document).on('click', '.maptag', function(){
  url = $(this).attr('data-url') + "?lat=" + myLat + "&lng=" + myLng;
  window.location.href = url;
})
</script>