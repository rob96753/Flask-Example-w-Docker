from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json
import os
import Donors
from datetime import datetime, timedelta
from Configuration import getList, getConfigItem
from Constants import CONFIG_PATH_ENV_VAR

DEFAULT_PATH = '/usr/src/app/'

config = None
donorsList = None

app = (Flask(__name__))
api = Api(app)

class DonationService(Resource):
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

class ProductsService(Resource):
    def get(self):
        return getList('products')


class DonorsService(Resource):
    @app.route('/Donors')
    def get(self):
        return Donors.get()

    def validateDonnor(self, donorObject):
        pass


    @app.route('/Donors/get_donor/<string:donor>')
    def get_donor(self, donor):
        pass
        #donors = Donors.Donors()
        #donor =

    #@app.route('/Donors/put', methods='[POST]')
    def put(self, donor):
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





#api.add_resource(Donors, '/donors/list', endpoint="donors")
#api.add_resource(Donors, '/donors/get/[index]', endpoint="donors")
#api.add_resource(Donors, '/donors/post/[donor]', endpoint="donors")
api.add_resource(DonationService, '/Donations/<donationCount>')
api.add_resource(ProductsService, '/Products', methods=['get'])
api.add_resource(DonorsService, '/Donors', methods=['GET', 'PUT'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
