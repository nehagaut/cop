
from pymongo.mongo_client import MongoClient
import urllib 
import json
import sys

uri = "mongodb+srv://cop:" + urllib.parse.quote("Cityofportland@123") + "@cop.9izbbfh.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(uri)
db = cluster["COP"]
mycol_general = db["General"]
mycol_award = db["Award"]
mycol_tender = db["Tender"]
mycol_contract = db["Contract"]
mycol_party = db["Party"]
# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def get_general_json_by_id(contract_id):
    desired_contract_id = contract_id

    data = mycol_general.find_one({'contract_id': int(desired_contract_id)})
    if data:
        return data["general"]
    else:
        print('Data not found')

def get_award_json_by_id(contract_id):
    desired_contract_id = contract_id

    data = mycol_award.find_one({'contract_id': int(desired_contract_id)})
    if data:
        return data["awards"]
    else:
        print('Data not found')

def get_tender_json_by_id(contract_id):
    desired_contract_id = contract_id

    data = mycol_tender.find_one({'contract_id': int(desired_contract_id)})
    if data:
        return data["tender"]
    else:
        print('Data not found')

def get_party_json_by_id(contract_id):
    desired_contract_id = contract_id

    data = mycol_party.find_one({'contract_id': int(desired_contract_id)})
    if data:
        return data["parties"]
    else:
        print('Data not found')

def get_contract_json_by_id(contract_id):
    desired_contract_id = contract_id

    data = mycol_contract.find_one({'contract_id': int(desired_contract_id)})
    if data:
        return data["contracts"]
    else:
        print('Data not found')

def get_contract_id_by_vendor_id(vender_id):
    data = mycol_party.find({'parties.party2.identifier.id': vender_id})
    for doc in data:
        print(doc["contract_id"])

def main(contract_id):
    print("general")
    general_json = get_general_json_by_id(contract_id)
    with open(f"{contract_id}_general.json", 'w', encoding='utf-8') as file:
        json.dump(general_json, file, ensure_ascii=False, indent=4)

    print("award")
    award_json = get_award_json_by_id(contract_id)
    with open(f"{contract_id}_award.json", 'w', encoding='utf-8') as file:
        json.dump(award_json, file, ensure_ascii=False, indent=4)

    print("tender")
    tender_json = get_tender_json_by_id(contract_id)
    with open(f"{contract_id}_tender.json", 'w', encoding='utf-8') as file:
        json.dump(tender_json, file, ensure_ascii=False, indent=4)

    print("party")
    party_json = get_party_json_by_id(contract_id)
    with open(f"{contract_id}_party.json", 'w', encoding='utf-8') as file:
        json.dump(party_json, file, ensure_ascii=False, indent=4)

    print("contract")
    contract_json = get_contract_json_by_id(contract_id)
    with open(f"{contract_id}_contract.json", 'w', encoding='utf-8') as file:
        json.dump(contract_json, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python mongodb_connect.py <contract_id>")
        sys.exit(1)
    contract_id = sys.argv[1]
    try:
        main(int(contract_id))
    except ValueError:
        print("Please provide a valid contract_id as an integer.")