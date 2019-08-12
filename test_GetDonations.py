import unittest
import GetDonations
import os
#run this with python -m unittest test_GetDonations.py

CONFIG_PATH_ENV_VAR = 'DONATIONS_CONFIG_PATH'
configFilePath = 'C:/Users/somme/docker/GetDonations/'

def setUpModule():
    os.environ[CONFIG_PATH_ENV_VAR] = configFilePath

def tearDownModule():
    del os.environ[CONFIG_PATH_ENV_VAR]

class TestCalc(unittest.TestCase):

    def test_getConfigItem(self):
        value = GetDonations.getConfigItem('products')
        self.assertTrue(value.upper() == 'BLOODPRODUCTS.JSON')
        value = GetDonations.getConfigItem('donors')
        self.assertTrue(value.upper() == 'DONORS.JSON')
        value = GetDonations.getConfigItem('blood_types')
        self.assertTrue(isinstance(value, list))
        value = GetDonations.getConfigItem('locations')
        self.assertTrue(isinstance(value, dict))

    def test_getList_products(self):

        result = GetDonations.getList('products')
        self.assertTrue(isinstance(result, dict))
        self.assertTrue('products' in result)
        self.assertTrue(isinstance(result['products'], list))

    def test_getList_donors(self):
        result = GetDonations.getList('donors')
        self.assertTrue(isinstance(result, list))
        self.assertFalse('products' in result)
        self.assertTrue(isinstance(result[0], dict))
        self.assertTrue('ltowb' in result[0])
        self.assertTrue('last_name' in result[0])


if __name__ == '__main__':
    unittest.main()