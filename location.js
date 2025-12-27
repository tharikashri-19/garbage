var map;
var marker;

function initMap() {
    // Default location (Coimbatore)
    map = L.map('map').setView([11.0168, 76.9558], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

function getLocation() {
    if (!navigator.geolocation) {
        alert("Geolocation not supported");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        position => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const accuracy = position.coords.accuracy;

            document.getElementById("lat").value = lat;
            document.getElementById("lon").value = lon;

            // Remove old marker if exists
            if (marker) {
                map.removeLayer(marker);
            }

            // Add new marker
            marker = L.marker([lat, lon]).addTo(map)
                .bindPopup(
                    "Your Location<br>Accuracy: " +
                    Math.round(accuracy) + " meters"
                )
                .openPopup();

            map.setView([lat, lon], 16);

            alert("Location captured with accuracy: " + Math.round(accuracy) + " meters");
        },
        error => {
            alert("Error getting location. Please enable GPS.");
        },
        {
            enableHighAccuracy: true,   // 🔴 VERY IMPORTANT
            timeout: 10000,
            maximumAge: 0
        }
    );
}
