__version__ = VERSION = '0.1.1'
__version_info__ = tuple(__version__.split('.'))

import os
import re
import psycopg2

class Confidence(object):
    EXCELLENT = "excellent"
    FAIR = "fair"
    POOR = "poor"
    NO_MATCH = "no match"

class TigerGeocoder(object):

    def __init__(self, conn_string=None, raise_shared_mem_exc=None):
        self.conn_string = conn_string
        if conn_string is None:
            self.conn_string = os.environ.get("GEOCODER_CONN_STRING")

        if raise_shared_mem_exc is None:
            raise_shared_mem_exc = os.environ.get("GEOCODER_RAISE_SHARED_MEM_EXC", "true").lower() in ['1', 'yes', 'true']
        self.raise_shared_mem_exc = raise_shared_mem_exc

        self.open()

    def open(self):
        self.conn = psycopg2.connect(self.conn_string)

    def close(self):
        self.conn.close()

    def geocode(self, address):
        result = None
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT addy, ST_Y(geomout) As lat, ST_X(geomout) As lon, rating FROM geocode(%s)", [address])
            result = cursor.fetchone()
        except psycopg2.OperationalError as exc:
            if "out of shared memory" not in str(exc):
                raise
            elif self.raise_shared_mem_exc:
                raise
            else:
                cursor.close()
                self.close()
                self.open()
        finally:
            cursor.close()

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
