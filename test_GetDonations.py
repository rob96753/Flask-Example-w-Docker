import unittest
import Services
from Donors import Donors
from Donation import Donation
import os
from BloodProducts import BloodProducts
import Configuration
from unittest import mock


"""
Note: It's poor unit test design to include multiple assert calls within a single test case. It's better
to split the asserts into one/two asserts per test case.

Arrange
    Set up the object to be tested and the collaborators
Act
    Exercise the unit under test

Assert
    Make claims about what happened
    
"""
#run this with python -m unittest test_GetDonations.py

CONFIG_PATH_ENV_VAR = 'DONATIONS_CONFIG_PATH'
configFilePath = 'C:/Users/somme/docker/GetDonations/'

def setUpModule():
    os.environ[CONFIG_PATH_ENV_VAR] = configFilePath

def tearDownModule():
    del os.environ[CONFIG_PATH_ENV_VAR]

class TestCalc(unittest.TestCase):

    def test_get_config_item_products_filename_from_file(self):
        value = Configuration.getConfigItem('products')
        self.assertTrue(value.upper() == 'BLOODPRODUCTS.JSON')

    def test_get_config_item_donors_filename_from_file(self):
        value = Configuration.getConfigItem('donors')
        self.assertTrue(value.upper() == 'DONORS.JSON')

    def test_get_config_item_blood_types_list_from_file(self):
        value = Configuration.getConfigItem('blood_types')
        self.assertTrue(isinstance(value, list))

    def test_get_config_item_locations_dictionary_from_file(self):
        value = Configuration.getConfigItem('locations')
        self.assertTrue(isinstance(value, dict))

    def test_get_config_item_donation_frequency_from_file(self):
        value = Configuration.getConfigItem('donation_frequency')
        self.assertTrue(value.isnumeric(), 'Value should be a numeric')

    def test_get_config_item_donation_frequency_raise_exceptio (self):
        with self.assertRaises(Exception):
            value = Configuration.getConfigItem('xdonation_frequency')

    def test_getList_products_returns_dictionary(self):
        result = Configuration.getList('products')
        self.assertTrue(isinstance(result, dict), 'Type returned for products should be a dictionary')
        self.assertTrue('products' in result)

    def test_getList_products_returns_dictionary_in_result(self):
        result = Configuration.getList('products')
        self.assertTrue(isinstance(result['products'], dict), 'Type contained in prodcuts should be a dictionary')

    def test_getList_donors(self):
        result = Configuration.getList('donors')
        self.assertTrue(isinstance(result, list))
        self.assertNotIn('products', result, 'Products erroneously in the donors dictionary.')

    def test_get_list_donors_record(self):
        result = Configuration.getList('donors').pop(0)
        self.assertTrue(isinstance(result, dict))
        self.assertIn('ltowb', result, 'ltowb should be included in the donors dictionary')
        self.assertIn('surname', result, 'surname should be included in the donors dictionary')

    def test_get_compatible_products(self):
        result = Configuration.getConfigItem('compatableProducts')
        self.assertTrue(isinstance(result, dict))
        self.assertTrue('RBC' in result)
        self.assertTrue('FRBC' in result)

    def test_get_eligible_donors(self):
        NUMBER_DONORS_REQUESTED = 5
        d = Donors()
        d.set(d.getAllDonorsList())
        result = d.getEligibleDonors(NUMBER_DONORS_REQUESTED)
        self.assertTrue(isinstance(result, list))
        self.assertTrue(len(result) <= NUMBER_DONORS_REQUESTED)

    def test_find_donor(self):
        d = Donors()
        d.set(d.getAllDonorsList())
        result = d.findDonor('SOMMERSET', '991-92-9392', "2 MAY 1977")
        self.assertTrue(isinstance(result, list))

    def test_find_donor_one_result(self):
        d = Donors()
        d.set(d.getAllDonorsList())
        result = d.findDonor('SOMMERSET', '991-92-9392', "2 MAY 1977")
        self.assertFalse(len(result) < 1, 'Expected Entry Not Found')
        self.assertFalse(len(result) > 1, 'Duplicate Entries in Donors')


    def test_find_donor_sommerset(self):
        d = Donors()
        d.set(d.getAllDonorsList())
        result = d.findDonor('SOMMERSET', '991-92-9392', "2 MAY 1977")
        self.assertTrue(result[0]['surname'] == 'SOMMERSET', 'Donor Not Found')

    def test_find_donor_raise_value_error(self):
        d = Donors()
        d.set(d.getAllDonorsList())
        with self.assertRaises(ValueError):
            d.findDonor('TUGG', '980-55-1018', "")

    def test_find_donor_missing_name_ssn_raise_exception(self):
        d = Donors()
        d.set(d.getAllDonorsList())
        with self.assertRaises(Exception):
            d.findDonor('', '', "21 JUN 1987")

    def test_find_donor_missing_name_ssn_raise_exception(self):
        d = Donors()
        d.set(d.getAllDonorsList())
        with self.assertRaises(Exception):
            d.findDonor('', '980-55-1018', "21 JUN 1987")

    def test_json_REPR(self):
        d = Donors()
        d.set(d.getAllDonorsList())
        result = d.reprJSON()
        self.assertTrue(isinstance(result, list), 'Expected type list, got type {isinstance(result)')
        self.assertFalse('dodid' in result[0], "dodid shouldn't be included in the results")
        donation = Donation()
        donation.createDonation(result[0], 'Z', '03 SEP 2019', 'W1HHAA')

    def test_get_blood_products(self):
        value = Configuration.getConfigItem('products')
        productsFullPath = os.path.join(configFilePath, value)
        bp = BloodProducts(productsFullPath)
        self.assertTrue("E0206V00" in bp.get_products())
        self.assertTrue('frozen' in bp.get_joined_products())
        details = bp.get_product_details('frozen')
        self.assertTrue(isinstance(details, dict))
        self.assertTrue("E5078V00" in details)



    def test_create_donation(self):
        d = Donors()
        d.set(d.getAllDonorsList())
        donor = d.findDonor('SOMMERSET', '991-92-9392', "2 MAY 1977")
        donationDate = '20190913'
        donationSite = 'WD2KAA'
        products = "fresh"


if __name__ == '__main__':
    unittest.main()