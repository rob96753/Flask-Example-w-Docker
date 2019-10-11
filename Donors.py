import json
import os
from datetime import datetime, timedelta
from Configuration import getList, getConfigItem
from Constants import CONFIG_PATH_ENV_VAR

class Donors:

    def __init__(self):
        pass

    def getAllDonorsList(self):
        return getList('donors')

    def set(self, donors):
        self._donors = donors

    def get(self):
        return self._donors

    def findDonor(self, lastName, ssn, dob):
        """
        Finds a donor from the list of donors, returning a list of matching donor records

        Business Rule
        if surname is empty or both dob and ssn are empty, throw an exception. Need at least
        the last name and DOB or SSN to identify a donor.
        :param lastName:
        :param ssn:
        :param dob:
        :return:
        """
        try:
            if not datetime.strptime(dob, '%d %b %Y'):
                dob = ''

            if lastName.strip() == '' or (dob.strip() == '' and ssn.strip() == ''):
                raise Exception(f"Last Name {lastName} and SSN {ssn} can't Be Empty")
            donor = None
            donor = list(filter(lambda x: x.get('surname','').upper() == lastName.upper() and x.get('ssn').upper() == ssn.upper() and x.get('dob', '') .upper() == dob.upper(), self.get()))
            return donor
        except ValueError as vex:
            raise ValueError(f'Exception Occurred in findDonor surName="{lastName}" ssn="{ssn}" dob="{dob}" {str(vex)}')
        except Exception as ex:
            raise Exception(f'Exception Occurred in findDonor surName="{lastName}" ssn="{ssn}" dob="{dob}" {str(ex)}')

    def computeDaysSinceDonation(self, x):
        """
        Helper function used with filter to identify the date of the last donation.
        This is an alternative to using a complex lambda function.
        :param x:
        :return:
        """
        try:
            donationFrequency = int(getConfigItem('donation_frequency'))
            if x.get('last_donation', '').strip() == '':
                lastDonation = datetime.now() - timedelta(days=donationFrequency)
            else:
                lastDonation = datetime.strptime(x.get('last_donation', '01 JAN 2019'), '%d %b %Y')
            return (datetime.now() - lastDonation).days > donationFrequency
        except Exception as ex:
            print(f'Exception Occurred in computeDaysSinceDonation {str(ex)}')
            return False

    def getEligibleDonors(self, numberDonors):
        """
        This uses the filter with a lambda to select blood donors. This isn't a good use of the lambda since
        the implementation is too complex. It would probably be better to use a function.
        :param numberDonors:
        :return:
        """
        #donors = list(filter(lambda x: (datetime.now() - datetime.strptime(x.get('last_donation', '01 JAN 2019') if len(x.get('last_donation', '01 JAN 2019').strip()) > 10 else '02 JAN 2019', '%d %b %Y')).days > 56, self.get()))
        try:
            donors = list(filter(lambda x: self.computeDaysSinceDonation(x), self.get()))
            return donors[0:numberDonors]
        except Exception as ex:
            raise Exception(f'Exception Occurred in computeDaysSinceDonation {str(ex)}')

    def reprJSON(self):
        return [dict(first_name=d['first_name'],  last_name=d['surname'],  ssn=d['ssn'],  blood_type=d['blood_type'], nationality=d['nationality'],  dob=d['dob'], service=d['service'], military_unit=d['military_unit']) for d in self.get()]
