Geocoder Documentation
******************************

This is a bare-bones wrapper around the Tiger Geocoder that comes with PostGIS 2+
(http://postgis.net/docs/manual-2.0/Extras.html).  To use it:

    from mygeocoder import TigerGeocoder, Confidence

    geocoder = TigerGeocoder(conn_string="[your_postgres_conn_string]")
    
    result = geocoder.geocode("1724 Massachusetts Ave NW, Washington DC")

Result looks like this:

    {
        'address': [best match found in geocoder],
        'lat': [latitude of address],
        'lon': [longitude of address],
        'confidence': [Confidence.EXELLENT, Confidence.FAIR, Confidence.POOR, or Confidence.NO_MATCH]
    }

That's it for now.  This is used for some personal stuff, so please don't expect too much from this :)
