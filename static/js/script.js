// initialize and add the map
let map;

async function initMap() {
    // request needed libraries
    const { Map } = await google.maps.importLibrary("maps");
    const { PinElement, AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    // show the map, centered at Tsavo national park
    map = new Map(document.getElementById("map"), {
        zoom: 9, // zoom level 1 - 20
        // center the map to show Tsavo park, below are the coordinates 
        center: {lat: -2.8271449279400915, lng: 37.892994380941374},
        mapId: "TSAVO_PARK",
    });

    // change marker background color
    const pinBackground = new PinElement({
        background: "#FBBC04",
        glyph: "PL", // add text to marker
    });
    const pinText = new PinElement({
        glyph: "CL",
        background: "#90ee90",
    });

    // show current location of lion
    // request coordinates from api
    const apiUrlRealTime = "http://127.0.0.1:5000/real-time-location/1";
    fetch(apiUrlRealTime)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to fetch data, status code: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const latitude = Number(data.coordinates.latitude);
        const longitude = Number(data.coordinates.longitude);

        // DISPLAY ON MAP
        const markerCurrentLocation = new AdvancedMarkerElement({
            map: map,
            position: {lat: latitude, lng: longitude},
            title: "Lion Kiboche current location",
            content: pinText.element,
        });
    })
    .catch(error => {
        console.error(`Error: `, error);
    });

    // show predicted location of lion
    // request coordinates from api
    const apiUrlPredictedLocation = "http://127.0.0.1:5000/predict/location/1/time/1";
    fetch(apiUrlPredictedLocation)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to fetch data, status code: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const latitude = Number(data.coordinates.latitude);
        const longitude = Number(data.coordinates.longitude);

        // DISPLAY ON MAP
        const markerPredictedLocation = new AdvancedMarkerElement({
            map: map,
            position: {lat: latitude, lng: longitude},
            title: "Lion Kiboche predicted location",
            content: pinBackground.element,
        });

    })
    .catch(error => {
        console.error(`Error: `, error);
    });
};
initMap();
// end of map code
