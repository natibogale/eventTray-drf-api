mapboxgl.accessToken =
  "pk.eyJ1IjoiZ2Vub2JhaXQiLCJhIjoiY2wzZTU0ZWhkMDh3NzNkcDYxOGJnZmJobyJ9.NvY2nXkZCfLy8qYJo1YPMA";

navigator.geolocation.getCurrentPosition(successLocation, errorLocation, {
  enableHighAccuracy: true,
});

function successLocation(position) {
  setupMap([position.coords.longitude, position.coords.latitude]);
}

function errorLocation() {
  setupMap([39.28425, 8.5636666667]);
}

function setupMap(center) {
  const map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/streets-v11",
    center: center,
    zoom: 15,
  });

  const nav = new mapboxgl.NavigationControl();
  map.addControl(nav);

  var directions = new MapboxDirections({
    accessToken: mapboxgl.accessToken,
  });

  map.addControl(directions, "top-left");
}

function validateLatLng(lat, lng) {
  let pattern = new RegExp("^-?([1-8]?[1-9]|[1-9]0)\\.{1}\\d{1,6}");

  return pattern.test(lat) && pattern.test(lng);
}

function getLocation() {
  [].forEach.call(
    document.querySelectorAll(" input[type='text']"),
    function (input) {
      const value = input.value;
      var latlngArray = value.split(",");

      lng = latlngArray[0];
      lat = latlngArray[1];

      if (validateLatLng(lat, lng)) {
        var pick = document.getElementById("location");
        pick.value = value;
      }
    }
  );
}




$(".readonly").on("keydown paste focus mousedown", function (e) {
  if (e.keyCode != 9)
    // ignore tab
    e.preventDefault();
});
