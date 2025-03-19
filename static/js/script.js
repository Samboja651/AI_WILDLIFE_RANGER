document.getElementById("tryThisButton").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent form submission default behavior

    // Get rowId from input field
    let rowId = document.getElementById("rowId").value || 1;
    if (Number(rowId) < 1 || Number(rowId) > 500) {
        alert(`${rowId} not within the range 1-500. Defaulting to 1.`)
        rowId = 1;
    }

    // Reload the page with rowId as a URL parameter
    window.location.href = `${window.location.pathname}?rowId=${rowId}`;
});

// Function to get the value of rowId from the URL
function getRowIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("rowId") || 1; // Default to 1 if not found
}

// Set the input field to match the rowId from the URL
document.getElementById("rowId").value = getRowIdFromUrl();

let map;

// Fetch and initialize the map using the rowId from the URL
async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    const { PinElement, AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    map = new Map(document.getElementById("map"), {
        zoom: 10,
        center: { lat: -3.7510485752976925, lng: 38.64665170514073 },
        mapId: "TSAVO_PARK",
    });

    const pinBackground = new PinElement({
        background: "#FBBC04",
        glyph: "PL",
    });

    const pinText = new PinElement({
        glyph: "CL",
        background: "#90ee90",
    });

    // Get rowId from URL
    const rowId = getRowIdFromUrl();

    // Construct API URLs dynamically
    const apiUrlRealTime = `/real-time-location/${rowId}`;
    const apiUrlPredictedLocation = `/predict/location/${rowId}/time/2`;

    // Fetch real-time location
    fetch(apiUrlRealTime)
        .then(response => response.ok ? response.json() : Promise.reject(`Error ${response.status}`))
        .then(data => {
            new AdvancedMarkerElement({
                map: map,
                position: { lat: Number(data.coordinates.latitude), lng: Number(data.coordinates.longitude) },
                title: "Lion Kiboche current location",
                content: pinText.element,
            });
        })
        .catch(error => console.error("Error:", error));

    // Fetch predicted location
    fetch(apiUrlPredictedLocation)
        .then(response => response.ok ? response.json() : Promise.reject(`Error ${response.status}`))
        .then(data => {
            new AdvancedMarkerElement({
                map: map,
                position: { lat: Number(data.coordinates.latitude), lng: Number(data.coordinates.longitude) },
                title: "Lion Kiboche predicted location",
                content: pinBackground.element,
            });

            // Check if lion has crossed boundaries
            getCountyWithOpenCage(Number(data.coordinates.latitude), Number(data.coordinates.longitude)).then(county => {
                if (county.toLowerCase() === "kwale") {
                    console.log(`Predicted lion location is in ${county} county. Raise an alert!`);
                    sendAlertEmail();
                } else {
                    console.log(`Predicted lion location is in ${county} county.`);
                }
            });

            document.getElementById("rowId").value = "";

        })
        .catch(error => console.error("Error:", error));
}

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