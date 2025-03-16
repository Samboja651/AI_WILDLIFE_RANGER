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
    const apiUrlRealTime = "/real-time-location/150";
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
    const apiUrlPredictedLocation = "/predict/location/150/time/2";
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
        // check if lion has crossed its boundary
        getCountyWithOpenCage(latitude, longitude).then(county => {
            if(county.toLowerCase() === 'kwale'){
                //send email alert
                console.log("Predicted lion location is in",county," county. Raise an alert!");
                sendAlertEmail();
                
            } else{
                console.log("Predicted lion location is in",county," county.");
            }
        });
    })
    .catch(error => {
        console.error(`Error: `, error);
    });
};
initMap();
// end of map code


async function getCountyWithOpenCage(lat, lng) {
    try {
        // Fetch API key from backend
        const configResponse = await fetch('/config');
        const configData = await configResponse.json();
        const apiKey = configData.opencage_apiKey;

        if (!apiKey) {
            throw new Error("API Key not found in backend response.");
        }

        // Construct the OpenCage API URL
        const url = `https://api.opencagedata.com/geocode/v1/json?q=${lat}%2C+${lng}&key=${apiKey}`;

        // Fetch data from OpenCage API
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`OpenCage API error: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();

        if (data.results && data.results.length > 0) {
            const components = data.results[0].components;
            const county = components.state || "County not found";
            return county;
        }

        return "County not found";
    } catch (error) {
        console.error("Error fetching county data:", error);
        return "Error fetching data";
    }
}

// Function to request the backend to send an email
async function sendAlertEmail() {
    try {
        const response = await fetch('/send-alert', { method: 'POST' });
        const result = await response.json();
        console.log(result.message);
        return "Message sent."
    } catch (error) {
        console.error("Error sending alert email:", error);
    }
}