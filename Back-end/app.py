from flask import Flask, request, jsonify
import urllib 
import json
from flask_cors import CORS
import math
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
import urllib 
app = Flask(__name__)
CORS(app)

# uri = "mongodb+srv://cop:" + urllib.parse.quote("Cityofportland@123") + "@cop.9izbbfh.mongodb.net/?retryWrites=true&w=majority"
# cluster = MongoClient(uri)
cluster = MongoClient('localhost', 27017)
db = cluster["COP"]
mycol_general = db["General"]
mycol_award = db["Award"]
mycol_tender = db["Tender"]
mycol_contract = db["Contract"]
mycol_party = db["Party"]
mycol_vendor = db["Vendor"]

@app.route('/api/connect/', methods=['GET'])
def test_connection():
    res_list = [
    {
        "key": '1',
        "name": 'Test Faison Construction Inc',
        "org": "Portland Parks and Recreation",
        "contract": 31001466,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '2',
        "name": 'James W Fowler Co',
        "org": "Portland Parks and Recreation",
        "contract": 30006946,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '3',
        "name": 'Greenworks Pc',
        "org": "Portland Parks and Recreation",
        "contract": 30006775,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '4',
        "name": 'Faison Construction Inc',
        "org": "Portland Parks and Recreation",
        "contract": 31001592,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '5',
        "name": 'Faison Construction Inc',
        "org": "Portland Parks and Recreation",
        "contract": 31001466,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '6',
        "name": 'James W Fowler Co',
        "org": "Portland Parks and Recreation",
        "contract": 30006946,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '7',
        "name": 'Greenworks Pc',
        "org": "Portland Parks and Recreation",
        "contract": 30006775,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '8',
        "name": 'Faison Construction Inc',
        "org": "Portland Parks and Recreation",
        "contract": 31001592,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '9',
        "name": 'Faison Construction Inc',
        "org": "Portland Parks and Recreation",
        "contract": 31001466,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '10',
        "name": 'James W Fowler Co',
        "org": "Portland Parks and Recreation",
        "contract": 30006946,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '11',
        "name": 'Greenworks Pc',
        "org": "Portland Parks and Recreation",
        "contract": 30006775,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '12',
        "name": 'Faison Construction Inc',
        "org": "Portland Parks and Recreation",
        "contract": 31001592,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '13',
        "name": 'Faison Construction Inc',
        "org": "Portland Parks and Recreation",
        "contract": 31001466,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '14',
        "name": 'James W Fowler Co',
        "org": "Portland Parks and Recreation",
        "contract": 30006946,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '15',
        "name": 'Greenworks Pc',
        "org": "Portland Parks and Recreation",
        "contract": 30006775,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    {
        "key": '16',
        "name": 'Faison Construction Inc',
        "org": "Portland Parks and Recreation",
        "contract": 31001592,
        "cert": "ESB",
        "aval": "80%",
        "tags": ['active'],
    },
    ]
    return json.dumps(res_list, indent=4), 200

@app.route('/api/all_resource/', methods=['GET'])
def get_all_resource():
    documents_list = list(mycol_vendor.find({}, {'_id': 0}))
    # print(documents_list)
    return json.dumps(documents_list, indent=4), 200


@app.route('/api/resource/vendor/<vendor_id>', methods=['GET'])
def get_contract_id_by_vendor_id(vendor_id):
    data = mycol_party.find({'parties.party2.identifier.id': vendor_id})
    res = []
    for doc in data:
        res.append(doc["contract_id"])
    
    return jsonify({'Contract id': res}), 200

@app.route('/api/resource/<resource_id>', methods=['GET'])
def get_resource_by_id(resource_id):
    # collection = mongo.db.Contract
    print("here")
    desired_contract_id = resource_id

    # Use the find_one method to retrieve the document with the specified contract_id
    data_general = mycol_general.find_one({'contract_id': int(desired_contract_id)})
    data_tender = mycol_tender.find_one({'contract_id': int(desired_contract_id)})
    data_award = mycol_award.find_one({'contract_id': int(desired_contract_id)})
    data_party = mycol_party.find_one({'contract_id': int(desired_contract_id)})
    # open contracting id

    #award id & org id = resource_id

    if data_general:
        # open contracting id
        open_contract_id = data_general["general"]["ocid"].split('-')[2]
        # print(open_contract_id)
        org_name = data_general["general"]["buyer"]["name"]
        # print(org_name)
    else:
        open_contract_id = "NULL"
        org_name = "NULL"
        # print('Resource not found in general')
        # return jsonify({'error': 'Resource not found in general'}), 404

    if data_tender:
        # tender start date
        tender_start_date = data_tender["tender"]["tenderPeriod"]["startDate"]
        # print(tender_start_date)
        # tender emd date
        tender_end_date = data_tender["tender"]["tenderPeriod"]["endDate"]
        # print(tender_end_date)
        # procurement method
        procurement_method = data_tender["tender"]["procurementMethod"]
        # print(procurement_method)
        # procurement method details
        procurement_method_details = data_tender["tender"]["procurementMethodDetails"]
        # print(procurement_method_details)

        # duration
        duration = data_tender["tender"]["tenderPeriod"]["durationInDays"]
        # print(duration)

    else:
        tender_start_date = "NULL"
        tender_end_date = "NULL"
        procurement_method = "NULL"
        procurement_method_details = "NULL"
        duration = "NULL"
        # print('Resource not found in tender')
        # return jsonify({'error': 'Resource not found in tender'}), 404
    
    if data_award:
        # amount
        amount = data_award["awards"]["value"]["amount"]
        # print(amount)
        # award start date
        award_start_date = data_award["awards"]["contractPeriod"]["startDate"]
        # print(award_start_date)
        # award end date
        award_end_date = data_award["awards"]["contractPeriod"]["endDate"]
        # print(award_end_date)

        # award description
        award_desctription = data_award["awards"]["description"]
        # print(award_desctription)
        award_vendor_name = data_award["awards"]["suppliers"]["name"]

    else:
        # print('Resource not found in award')
        # return jsonify({'error': 'Resource not found in award'}), 404
        amount = "NULL"
        award_start_date = "NULL"
        award_end_date = "NULL"
        award_desctription = "NULL"
        award_vendor_name = "NULL"

    if data_party:
        # project manager
        pm = data_party["parties"]["party1"]["contactPoint"]["name"]
        # print(pm)
        # certification
        certification = data_party["parties"]["party2"]["details"]["classfication3"]["description"]
        try:
            if math.isnan(certification):
                certification = "NaN"
        except:
            pass
        # print(certification)
    else:
        pm = "NULL"
        certification = "NULL"
        # print('Resource not found in party')
        # return jsonify({'error': 'Resource not found in party'}), 404
     

    return jsonify({'Contract Number': resource_id,
                    'Open Contracting ID':open_contract_id,
                    "Organization Name": org_name,
                    "Tender Start Date": tender_start_date,
                    "Tender End Date": tender_end_date,
                    "Procurement method": procurement_method,
                    "Procurement method details": procurement_method_details,
                    "Award Id": resource_id,
                    "Amount": amount,
                    "Organization ID": resource_id,
                    "Award Start Date": award_start_date,
                    "Award End Date": award_end_date,
                    "Award Description": award_desctription,
                    "Duration": duration,
                    "Project Manager": pm,
                    "Certification": certification,
                    "Vendor Name": award_vendor_name,
                    "Change Order": "4[placeholder]"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8080, debug= True)