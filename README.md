# csv2map
A fork of fail2ban-analyse providing more generic point location mapping from CSV containing coordinates and a label

Currently only supports 3 column CSV input - latitude,longitude,label.  Must have exactly one header line, and third element (header entry for labels) will be used to title all the labels (pop-ups)

See header comments for more information (and fail2ban-analyse README)

## Use

- run _scripts/csv2geojson.py_ specifying input CSV file
- Copy resulting output GeoJSON file and _web/locations-map.html_ into your web server directory
- edit _locations-map.html_ to enter your unique Mapbox API key
- View web page in a browser :)

## References

- https://leafletjs.com/
- https://www.mapbox.com/
- https://www.openstreetmap.org/
- https://github.com/jawj/OverlappingMarkerSpiderfier-Leaflet
