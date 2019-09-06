from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json
import os
from datetime import datetime, timedelta

DEFAULT_PATH = '/usr/src/app/'
DONATIONS = 'donations.json'
CONFIG_PATH_ENV_VAR = 'DONATIONS_CONFIG_PATH'

config = None
donorsList = None

app = (Flask(__name__))
api = Api(app)

def getConfigItem(key):
    item = None
    if not CONFIG_PATH_ENV_VAR in os.environ.keys():
        raise Exception(f'The Environment Must Contain  {CONFIG_PATH_ENV_VAR} As the Path to the Configuration File')
    try:
        configFilePath = os.environ.get(CONFIG_PATH_ENV_VAR)
        with open(os.path.join(configFilePath, DONATIONS), "r+") as cfp:
            config = json.load(cfp)
            if key in config.keys():
                item = config[key]
            else:
                raise Exception(f'Exception in getConfigItem for {key}')
        return item
    except json.JSONDecodeError as jex:
        raise Exception("getConfigItem: JSON Decode Error {jex.msg} {jex.doc} {jex.pos}")
    except Exception as ex:
        raise Exception(f'Exception in getItem for {key} "{str(ex)}"')

def getList(key):
    listOfValues = {}
    cfp = None
    listfp = None

    if not CONFIG_PATH_ENV_VAR in os.environ.keys():
        raise Exception(f'The Environment Must Contain  {CONFIG_PATH_ENV_VAR} As the Path to the Configuration File')
    try:
        configFilePath = os.environ.get(CONFIG_PATH_ENV_VAR)
        with open(os.path.join(configFilePath, DONATIONS), "r+") as cfp:
            config = json.load(cfp)
            if key in config.keys():
                with open(os.path.join(configFilePath, config[key]), "r+") as listfp:
                    listOfValues = json.load(listfp)
            return listOfValues
    except json.JSONDecodeError as jex:
        raise Exception("getList: JSON Decode Error {jex.msg} {jex.doc} {jex.pos}")
    except Exception as ex:
        raise Exception(f'Exception in getList for {key} {str(ex)}')

class Donations(Resource):
    defaultDonation = {}
    def __init__(self):
        self.defaultDonation = {
            "first_name": "",
            "last_name": "",
            "donor_ssn": "",
            "donor_dob": "",
            "donor_dodid": "",
            "gender": "M",
            "blood_type": "",
            "ltowb": "",
            "nationality": "",
            "branch": "",
            "military_unit": "",
            "din": "",
            "product": "",
            "donation_date": "",
            "expire_date": ""
        }

    def get(self, numberDonations):
        return self.defaultDonation

donorTemplate = {
    "first_name": "",
    "middle_name": "",
    "last_name": "",
    "ssn": "",
    "dodid": "",
    "blood_type": "",
    "nationality": "United States of America",
    "military_unit": "",
    "ltowb": "N",
    "gender": "",
    "race": "",
    "dob": "28 JAN 1989",
    "service": "",
    "mos": "",
    "rank": "",
    "paygrade": "",
    "last_donation": "15 May 2019",
    "donor_original_index": "0"
}
#@app.route('/donors/list', methods=['GET'])

class Products(Resource):
    def get(self):
        return getList('products')

class Donors(Resource):
    def get(self):
        return getList('donors')

    def put(self):
        data = request.get_json(force=True)        

        donorsFileName = getConfigItem('donors')
        if not CONFIG_PATH_ENV_VAR in os.environ.keys():
            raise Exception(
                f'The Environment Must Contain  {CONFIG_PATH_ENV_VAR} As the Path to the Configuration File')
        try:
            configFilePath = os.environ.get(CONFIG_PATH_ENV_VAR)
            with open(os.path.join(configFilePath, donorsFileName), "r+") as json_file:
                donors = json.load(json_file)
            with open(os.path.join(configFilePath, donorsFileName), "w") as out_file:
                donors.append(data)
                out_file.write(json.dumps(donors, sort_keys=False, indent=4))
        except Exception as ex:
            raise Exception(f'Exception in Donors.put {str(ex)}')

        return True

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



#api.add_resource(Donors, '/donors/list', endpoint="donors")
#api.add_resource(Donors, '/donors/get/[index]', endpoint="donors")
#api.add_resource(Donors, '/donors/post/[donor]', endpoint="donors")
api.add_resource(Donations, '/Donations/<donationCount>')
api.add_resource(Products, '/Products', methods=['get'])
api.add_resource(Donors, '/Donors', methods=['GET', 'PUT'])



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
