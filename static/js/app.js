document.addEventListener('DOMContentLoaded', function() {
    let map = L.map('map').setView([34.7597, 113.6319], 4);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
        maxZoom: 18,
    }).addTo(map);

    let citySelect = document.getElementById('city-select');
    let goBtn = document.getElementById('go-btn');
    let cityInput = document.getElementById('city-input');
    let currentCityLayer = null;

    cityInput.addEventListener('input', function() {
        let keyword = this.value;
        if (keyword) {
            fetch(`/search_cities?keyword=${encodeURIComponent(keyword)}`)
                .then(response => response.json())
                .then(data => {
                    let html = '';
                    for (let city of data) {
                        html += `<div class="city-item" data-city="${city}">${city}</div>`;
                    }
                    citySelect.innerHTML = html;
                });
        } else {
            citySelect.innerHTML = '';
        }
    });

    citySelect.addEventListener('click', function(event) {
        if (event.target.classList.contains('city-item')) {
            let city = event.target.dataset.city;
            cityInput.value = event.target.innerText;
            citySelect.innerHTML = '';
            fetch('/get_city_bounds', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({city: city})
            })
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    if (currentCityLayer) {
                        map.removeLayer(currentCityLayer);
                    }
                    // 将 [lng, lat] 格式转换为 [lat, lng] 格式
                    let latLngs = data.map(coord => [coord[1], coord[0]]);
                    currentCityLayer = L.polygon(latLngs).addTo(map);
                    map.fitBounds(currentCityLayer.getBounds());
                    goBtn.hidden = false;
                } else {
                    alert('未找到该城市的地图数据');
                }
            });
        }
    });

    goBtn.addEventListener('click', function() {
        if (currentCityLayer) {
            let bounds = currentCityLayer.getLatLngs()[0];
            console.log('Bounds:', bounds);
            // 将 LatLng 对象转换为 [lng, lat] 格式
            let lngLatBounds = bounds.map(coord => [coord.lng, coord.lat]);
            console.log('Sending bounds:', lngLatBounds);
            fetch('/get_random_point', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({bounds: lngLatBounds})
            })
            .then(response => response.json())
            .then(data => {
                let [lon, lat] = data;
                map.flyTo([lat, lon], 12);
                L.marker([lat, lon]).addTo(map);
            });
        }
    });
});