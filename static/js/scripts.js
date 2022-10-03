// Map initialization 
var map = L.map('map').setView([28.0229, 73.3119], 5);
    
//osm layer
var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});
osm.addTo(map);

// google street 
googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});
googleStreets.addTo(map);

var loc_types = [
    'FMN Headquarters', 
    'EME Dets Wksp Main', 
    'EME Dets AWD', 
    'Ordnance Unit', 
    'Supply Point', 
    'ADS',
    'cas',
    'det', 
    'AVT LR', 
    'AVT FR',
    'Own Forces', 
    'EN Forces', 
    'Eng Det', 
    'AAD', 
    'Signal', 
    'Artillery',
]

var icons = {}
for(let loc_type of loc_types) {
    icons[loc_type] = L.icon({
        iconUrl: `static/images/${loc_type}.png`,
        iconSize: [50, 50],
    });
}
// fetching data 
// Defining async function
async function getapi(url, type = 'none') {
    
    // Storing response
    const response = await fetch(url);
    
    // Storing data in form of JSON
    var data = await response.json();
    console.log(data);
    if (response) {
        //hideloader();
    }
    show(data, type);
}

// Function to hide the loader
function hideloader() {
    document.getElementById('loading').style.display = 'none';
}
function show(data, type) {
    // Loop to access all rows 
    for (let r of data) {
        var marker1;
        var icon_key = r[1];

        var txt = `
            <h2>${r[1]}</h2>
            <p>LATITUDE : ${r[2]}</P>
            <p>LONGITUDE : ${r[3]}</P>
                
        `;
        if (type == 'det') {
            txt += `<p>DET TYPE : ${r[4]}</p>
                <p>ARMY NO : ${r[5]}</p>
            `;
            icon_key = 'det';
        } else if (type == 'cas') {
            txt += `<p>VEH TYPE : ${r[4]}</p>
            <p>NATURE OF CAS : ${r[5]}</p>
            `;
            icon_key = 'cas';
        }
        console.log(r);
        
        marker1 = L.marker([r[2], r[3]], { icon : icons[icon_key] });
        marker1.bindPopup(txt).openPopup;
        marker1.addTo(map)
    }
}

var paths = window.location.href.split('/');
var route = `${paths[0]}//${paths[2]}/`; 
        