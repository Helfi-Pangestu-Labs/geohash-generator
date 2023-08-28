import unittest
from geohash_generator.geohash_util import GeohashUtil
import os

class TestConvertGeohashToGeojson(unittest.TestCase):

    def test_read_geohashes(self):
        # Replace with the actual path to your geohash file
        this_script_dir = os.path.dirname(os.path.realpath(__file__))
        source_path = os.path.join(
               this_script_dir,
               '..',
               '..',
                'examples',
                'geohash_example.txt'
            )
        
        # Call the method being tested
        geohashes = GeohashUtil.read_geohashes(source_path)

        # Define the expected geohashes based on the content of your file
        expected_geohashes = ['djjcpxj', 'djjcrjb', 'djjcqc']  # Replace with actual geohashes
        
        # Compare the actual result with the expected result
        self.assertEqual(geohashes, expected_geohashes)

if __name__ == '__main__':
    unittest.main()
