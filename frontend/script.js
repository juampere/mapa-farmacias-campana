const map = L.map('map').setView([-34.1718, -58.9533], 13);

L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles © Esri',
    maxZoom: 16
}).addTo(map);

let capaFarmacias = L.layerGroup().addTo(map);

const iconoFarmacia = L.divIcon({
    html: `<div style="background-color: #2ecc71; width: 24px; height: 24px; border-radius: 50%; border: 2px solid #fff; display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; box-shadow: 0 0 10px rgba(46, 204, 113, 0.6);">✚</div>`,
    className: '',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
});

// Función para cambiar el color verde entre botones
function seleccionarBoton(idActivo) {
    document.getElementById('btn-turno').classList.remove('activo');
    document.getElementById('btn-todas').classList.remove('activo');
    document.getElementById(idActivo).classList.add('activo');
}

async function cargarFarmacias(ruta) {
    try {
        capaFarmacias.clearLayers();
        const respuesta = await fetch(`https://backend-farmacias-cnha.onrender.com/api/${ruta}`);
        const farmacias = await respuesta.json();

        farmacias.forEach(f => {
            const lat = f.latitud; 
            const lng = f.longitud;

            if (lat && lng) {
                const imagenHtml = f.imagen_url ? 
                    `<div style="width: 100%; height: 110px; border-radius: 8px; overflow: hidden; margin-bottom: 10px; border: 1px solid #444;">
                        <img src="${f.imagen_url}" style="width: 100%; height: 100%; object-fit: cover;">
                     </div>` : 
                    `<div style="width: 100%; height: 110px; border-radius: 8px; background: #222; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
                        <span style="color: #666; font-size: 0.7rem;">SIN FOTO</span>
                    </div>`;

                const contenidoPopup = `
                    <div style="text-align: center; font-family: sans-serif; width: 200px; color: #eee;">
                        ${imagenHtml}
                        <b style="font-size: 1.1rem; color: #2ecc71; display: block;">${f.nombre}</b>
                        <p style="margin: 5px 0; font-size: 0.85rem; color: #bbb;">${f.direccion}</p>
                        <div style="margin-top: 10px; border-top: 1px solid #333; padding-top: 10px;">
                            <a href="https://www.google.com/maps?q=${lat},${lng}" 
                               target="_blank" 
                               style="display: block; padding: 10px; background: #2ecc71; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.8rem;">
                               CÓMO LLEGAR
                            </a>
                        </div>
                    </div>
                `;

                const marker = L.marker([lat, lng], { icon: iconoFarmacia });
                marker.bindPopup(contenidoPopup);
                capaFarmacias.addLayer(marker);
            }
        });
    } catch (error) {
        console.error("Error cargando farmacias:", error);
    }
}

// Eventos de botones
document.getElementById('btn-turno').addEventListener('click', () => {
    seleccionarBoton('btn-turno');
    cargarFarmacias('farmacias/turno');
});

document.getElementById('btn-todas').addEventListener('click', () => {
    seleccionarBoton('btn-todas');
    cargarFarmacias('farmacias');
});

// Inicio
seleccionarBoton('btn-turno');
cargarFarmacias('farmacias/turno');