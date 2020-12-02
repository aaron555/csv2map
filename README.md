# csv2map
A fork of fail2ban-analyse providing more generic point location mapping from CSV containing coordinates and a label

Currently only supports 3 column CSV input - latitude,longitude,label.  Must have exactly one header line, and third element (header entry for labels) will be used to title all the labels (pop-ups)

See header comments for more information (and fail2ban-analyse README)

## References

- https://leafletjs.com/
- https://www.mapbox.com/
- https://www.openstreetmap.org/
- https://github.com/jawj/OverlappingMarkerSpiderfier-Leaflet
