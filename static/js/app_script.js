// Global variables for the map and markers
let map;
let allLocations = {};
let allMarkers = [];
let pathPolyline = null;

// Flags to ensure both the DOM and Google Maps API are ready
let isMapReady = false;
let isDomReady = false;

// This function is called by the Google Maps API script when it has loaded
function initMap() {
    const mapOptions = {
        // Center the map on your campus coordinates
        center: { lat: 17.3917, lng: 78.3195 },
        zoom: 18, // Zoom in closer for a campus view
        mapId: 'PATHFINDER_MAP_ID', // A unique ID for custom styling if needed
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    isMapReady = true;

    // If the DOM is also ready, run the main app logic
    if (isDomReady) {
        runAppLogic();
    }
}

// Add an event listener to know when the HTML page content is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    isDomReady = true;
    // If the map has also finished loading, run the main app logic
    if (isMapReady) {
        runAppLogic();
    }
});

// This function holds the core logic and only runs when everything is ready
async function runAppLogic() {
    const startSelect = document.getElementById('start-location');
    const endSelect = document.getElementById('end-location');
    const findPathBtn = document.getElementById('find-path-btn');
    const routeText = document.getElementById('route-text');

    try {
        const response = await fetch('/api/locations');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        allLocations = await response.json();

        // Populate dropdowns now that we know the <select> elements exist
        const locationNames = Object.keys(allLocations).sort();
        startSelect.innerHTML = '';
        endSelect.innerHTML = '';
        locationNames.forEach(loc => {
            startSelect.add(new Option(loc, loc));
            endSelect.add(new Option(loc, loc));
        });
        if (locationNames.length > 1) {
            endSelect.value = locationNames[1];
        }

        // Create a custom HTML marker for each location
        allMarkers = locationNames.map(loc => {
            const locData = allLocations[loc];

            // 1. Create the main marker element (the dot)
            const markerElement = document.createElement('div');
            markerElement.className = 'custom-marker';

            // 2. Create the text label and append it to the marker
            const labelElement = document.createElement('span');
            labelElement.className = 'marker-label';
            labelElement.textContent = loc;
            markerElement.appendChild(labelElement);
            
            // 3. Create the Advanced Marker with the custom HTML content
            return new google.maps.marker.AdvancedMarkerElement({
                position: { lat: locData.lat, lng: locData.lng },
                map: map,
                content: markerElement,
                title: loc // Adding title for accessibility and hover effects
            });
        });

    } catch (error) {
        console.error('Failed to load locations:', error);
        routeText.textContent = 'Error: Could not load campus data from the server.';
    }

    findPathBtn.addEventListener('click', handleFindPath);
}

// This function handles finding the path after a user clicks the button
async function handleFindPath() {
    const start = document.getElementById('start-location').value;
    const end = document.getElementById('end-location').value;
    const routeText = document.getElementById('route-text');
    const distanceText = document.getElementById('distance-text');

    // Clear previous route drawn on the map
    if (pathPolyline) {
        pathPolyline.setMap(null);
    }

    if (start === end) {
        routeText.textContent = "Start and destination cannot be the same.";
        distanceText.textContent = "";
        return;
    }

    routeText.textContent = 'Calculating shortest path...';
    distanceText.textContent = '';

    try {
        const response = await fetch(`/api/find_path?start=${start}&end=${end}`);
        const data = await response.json();

        if (data.error) {
            routeText.textContent = `Error: ${data.error}`; // Show the specific error from the server
        } else {
            routeText.textContent = data.path.join(' → ');
            distanceText.textContent = `Total Distance: ${data.distance} meters`;
            
            // Get coordinates for the new path
            const pathCoordinates = data.path.map(locName => {
                const locData = allLocations[locName];
                return { lat: locData.lat, lng: locData.lng };
            });

            // Draw the new path on the Google Map
            pathPolyline = new google.maps.Polyline({
                path: pathCoordinates,
                geodesic: true,
                strokeColor: '#E040FB', // Accent color
                strokeOpacity: 1.0,
                strokeWeight: 4,
            });

            pathPolyline.setMap(map);
        }
    } catch (error) {
        console.error('Error finding path:', error);
        routeText.textContent = 'An error occurred while communicating with the server.';
    }
}