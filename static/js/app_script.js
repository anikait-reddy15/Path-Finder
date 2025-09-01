document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const startSelect = document.getElementById('start-location');
    const endSelect = document.getElementById('end-location');
    const findPathBtn = document.getElementById('find-path-btn');
    const routeText = document.getElementById('route-text');
    const distanceText = document.getElementById('distance-text');
    const canvas = document.getElementById('map-canvas');
    const ctx = canvas.getContext('2d');

    let locations = {}; // To store location data including positions

    // --- Canvas and Drawing Functions ---

    // Resize canvas to fit its container
    function resizeCanvas() {
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
        drawMap(); // Redraw map after resizing
    }

    // Main drawing function
    function drawMap(path = []) {
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
        drawNodes();
        if (path.length > 0) {
            drawPath(path);
        }
    }

    // Draw all location nodes
    function drawNodes() {
        if (!locations) return;

        Object.keys(locations).forEach(loc => {
            const { pos } = locations[loc];
            const x = (pos[0] / 100) * canvas.width;
            const y = (pos[1] / 100) * canvas.height;

            // Draw node circle
            ctx.beginPath();
            ctx.arc(x, y, 8, 0, 2 * Math.PI);
            ctx.fillStyle = '#BE29EC'; // Accent color
            ctx.fill();
            ctx.strokeStyle = '#F0F0F0';
            ctx.lineWidth = 2;
            ctx.stroke();

            // Draw label
            ctx.fillStyle = '#F0F0F0'; // Primary text color
            ctx.font = 'bold 14px Poppins';
            ctx.textAlign = 'center';
            ctx.fillText(loc, x, y - 15);
        });
    }

    // Draw the calculated path
    function drawPath(path) {
        if (path.length < 2) return;

        ctx.beginPath();
        const startLoc = locations[path[0]];
        const startX = (startLoc.pos[0] / 100) * canvas.width;
        const startY = (startLoc.pos[1] / 100) * canvas.height;
        ctx.moveTo(startX, startY);

        path.slice(1).forEach(locName => {
            const loc = locations[locName];
            const x = (loc.pos[0] / 100) * canvas.width;
            const y = (loc.pos[1] / 100) * canvas.height;
            ctx.lineTo(x, y);
        });

        ctx.strokeStyle = '#E040FB'; // Bright accent color for path
        ctx.lineWidth = 5;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.stroke();
    }


    // --- API and Logic Functions ---

    // Fetch all locations and populate dropdowns
    async function initializeApp() {
        try {
            const response = await fetch('/api/locations');
            locations = await response.json();

            // Clear existing options
            startSelect.innerHTML = '';
            endSelect.innerHTML = '';
            
            const locationNames = Object.keys(locations).sort();

            locationNames.forEach(loc => {
                const option1 = new Option(loc, loc);
                const option2 = new Option(loc, loc);
                startSelect.add(option1);
                endSelect.add(option2);
            });

            // Set a default different selection
            if (locationNames.length > 1) {
                endSelect.value = locationNames[1];
            }

            // Initial setup
            resizeCanvas();
        } catch (error) {
            console.error('Failed to load locations:', error);
            routeText.textContent = 'Error: Could not load campus data.';
        }
    }

    // Handle the "Find Path" button click
    async function handleFindPath() {
        const start = startSelect.value;
        const end = endSelect.value;

        if (start === end) {
            routeText.textContent = "Start and destination cannot be the same.";
            distanceText.textContent = "";
            drawMap(); // Redraw with no path
            return;
        }

        // Display a loading message
        routeText.textContent = 'Calculating shortest path...';
        distanceText.textContent = '';
        
        try {
            const response = await fetch(`/api/find_path?start=${start}&end=${end}`);
            const data = await response.json();

            if (data.error) {
                routeText.textContent = data.error;
                distanceText.textContent = "";
                drawMap();
            } else {
                routeText.textContent = data.path.join(' → ');
                distanceText.textContent = `Total Distance: ${Math.round(data.distance)} meters`;
                drawMap(data.path);
            }
        } catch (error) {
            console.error('Error finding path:', error);
            routeText.textContent = 'An error occurred while finding the path.';
        }
    }


    // --- Event Listeners ---
    findPathBtn.addEventListener('click', handleFindPath);
    window.addEventListener('resize', resizeCanvas);

    // --- Start the App ---
    initializeApp();
});