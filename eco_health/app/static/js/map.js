// app/static/js/map.js
let map;

async function initMap() {
    // Inicializar mapa centrado en México
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 23.6345, lng: -102.5528 },
        zoom: 5
    });

    // Obtener datos de contaminación
    const response = await fetch('/api/pollution/cities');
    const pollutionData = await response.json();

    // Añadir marcadores para cada ciudad
    for (const city in pollutionData) {
        const data = pollutionData[city];
        
        // Determinar color basado en nivel de contaminación
        const color = getPollutionColor(data.aqi);
        
        new google.maps.Circle({
            map: map,
            center: data.location,
            radius: 50000,
            fillColor: color,
            fillOpacity: 0.35,
            strokeWeight: 0
        });
    }
}

function getPollutionColor(aqi) {
    if (aqi <= 50) return '#00E400';      // Bueno
    if (aqi <= 100) return '#FFFF00';     // Moderado
    if (aqi <= 150) return '#FF7E00';     // Dañino para grupos sensibles
    if (aqi <= 200) return '#FF0000';     // Dañino
    if (aqi <= 300) return '#8F3F97';     // Muy dañino
    return '#7E0023';                     // Peligroso
}