import unittest
import GetDonations
from GetDonations import Donors
import os
from unittest import mock


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

    def test_get_compatible_products(self):
        result = GetDonations.getConfigItem('compatableProducts')
        self.assertTrue(isinstance(result, dict))
        self.assertTrue('RBC' in result)
        self.assertTrue('FRBC' in result)
        products = GetDonations.getList('products')

    def test_get_eligible_donors(self):
        NUMBER_DONORS_REQUESTED = 5
        d = Donors()
        result = d.getEligibleDonors(NUMBER_DONORS_REQUESTED)
        self.assertTrue(isinstance(result, list))
        self.assertTrue(len(result) <= NUMBER_DONORS_REQUESTED)

    def test_find_donor(self):
        d = Donors()
        result = d.findDonor('SOMMERSET', '991-92-9392', "2 MAY 1977")
        self.assertTrue(isinstance(result, list))
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0]['surname'] == 'SOMMERSET', 'Donor Not Found')
        self.assertRaises(ValueError, d.findDonor, 'TUGG', '980-55-1018', "")
        self.assertRaises(Exception, d.findDonor, '', '', "21 JUN 1987")
        self.assertRaises(Exception, d.findDonor, '', '980-55-1018', "21 JUN 1987")


if __name__ == '__main__':
    unittest.main()