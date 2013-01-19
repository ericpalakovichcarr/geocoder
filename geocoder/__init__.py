__version__ = VERSION = '0.1.0'
__version_info__ = tuple(__version__.split('.'))

import re
import psycopg2

class Confidence(object):
    EXCELLENT = "excellent"
    FAIR = "fair"
    POOR = "poor"
    NO_MATCH = "no match"

class TigerGeocoder(object):

    def __init__(self, conn_string):
        self.conn = psycopg2.connect(conn_string)

    def geocode(self, address):
        cursor = self.conn.cursor()
        cursor.execute("SELECT addy, ST_Y(geomout) As lat, ST_X(geomout) As lon, rating FROM geocode(%s)", [address])
        result = cursor.fetchone()

        if result:
            # Recreate the address
            found_address_parts = result[0][1:-1].split(',')
            found_address = ' '.join(found_address_parts[:6]) + ", " + ' '.join(found_address_parts[6:-1])
            found_address = re.sub(' +', ' ', found_address)
            found_address = re.sub(' ,', ',', found_address)

            # Convert the rating into a confidence score
            rating = result[3]
            if rating == 1:
                confidence = Confidence.EXCELLENT
            elif rating <= 50:
                confidence = Confidence.FAIR
            else:
                confidence = Confidence.POOR

            return {
                'address': found_address,
                'lat': result[1],
                'lon': result[2],
                'confidence': confidence
            }
        else:
            return {
                'address': None,
                'lat': None,
                'lon': None,
                'confidence': Confidence.NO_MATCH
            }

    def close(self):
        self.conn.close()