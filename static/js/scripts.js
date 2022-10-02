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
async function getapi(url) {
    
    // Storing response
    const response = await fetch(url);
    
    // Storing data in form of JSON
    var data = await response.json();
    console.log(data);
    if (response) {
        //hideloader();
    }
    show(data);
}

// Function to hide the loader
function hideloader() {
    document.getElementById('loading').style.display = 'none';
}
function show(data) {
    // Loop to access all rows 
    for (let r of data) {
        var marker1;
        
        var txt = `
            <h1>${r[1]}</h1>
            <p>LATITUDE : ${r[2]}</P>
            <p>LONGITUDE : ${r[3]}</P>
                
        `;
        if (r.length == 6) {
            txt += `<p>DET TYPE : ${r[4]}</p>
                <p>ARMY NO : ${r[5]}</p>
            `;
        } else if (r.length == 7) {
            txt += `<p>NAME OF REGT : ${r[4]}</p>
            <p>VEH TYPE : ${r[5]}</p>
            <p>NATURE OF CAS : ${r[6]}</p>
            `;
        }
        console.log(r);
        if(r.length > 4) { 
            marker1 = L.marker([r[2], r[3]], { icon : ((r.length == 6) ? icons['det'] : icons['cas'])});
            marker1.bindPopup(txt).openPopup 
        }
        else {
            marker1 = L.marker([r[2], r[3]], { icon : icons[r[1]] });
        }
        marker1.addTo(map)
    }
}
