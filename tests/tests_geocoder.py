from unittest import TestCase
from mygeocoder import Confidence, TigerGeocoder

class TigerGeocoderTests(TestCase):
    """
    NOTE: Expects the geocoder database to be up and running.
    """

    def setUp(self):
        self.geocoder = TigerGeocoder("dbname=geocoder user=eric")

    def tearDown(self):
        self.geocoder.close()

    def assertGeocode(self, address, expected_confidence):
        result = self.geocoder.geocode(address)
        self.assertEquals(expected_confidence, result['confidence'])
        if result['confidence'] in [Confidence.EXCELLENT, Confidence.FAIR]:
            self.assertEquals("1724 Massachusetts Ave NW, Washington DC 20036", result['address'])
            self.assertEquals(-77.0393236499317, result['lon'])
            self.assertEquals(38.9081098579959, result['lat'])
        elif result['confidence'] == Confidence.POOR:
            self.assertTrue(result['address'] is not None)
            self.assertTrue(result['lat'] is not None)
            self.assertTrue(result['lon'] is not None)
        else:
            self.assertEquals(None, result['address'])
            self.assertEquals(None, result['lat'])
            self.assertEquals(None, result['lon'])

    def test_excellent_geocode(self):
        self.assertGeocode("1724 Massachusetts Ave NW, Washington DC", Confidence.EXCELLENT)

    def test_fair_geocode(self):
        self.assertGeocode("1724 Massachusetts Ave N, Washington DC", Confidence.FAIR)

    def test_poor_geocode(self):
        self.assertGeocode("1724 Mass Ave, Washington DC", Confidence.POOR)

    def test_no_match_geocode(self):
        self.assertGeocode("Mass Ave", Confidence.NO_MATCH)
        self.assertGeocode("", Confidence.NO_MATCH)
