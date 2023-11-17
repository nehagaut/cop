import pandas as pd
import json
from datetime import datetime
import pytz
import pymongo
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
import urllib 
import math
import warnings

warnings.filterwarnings('ignore')
cluster = MongoClient('localhost', 27017)
db = cluster["COP"]
mycol = db["Award"]
mycol_general = db["General"]
mycol_tender = db["Tender"]
mycol_party = db["Party"]
mycol_contract = db["Contract"]
mycol_vendor = db["Vendor"]


def po_progress_data_transfer(date_string):
    date_object = datetime.strptime(date_string,"%Y-%m-%d %H:%M:%S.%f")
    desired_timezone = pytz.timezone("US/Pacific")
    localized_datetime = desired_timezone.localize(date_object.replace(hour=0, minute=0, second=0, microsecond=0))
    formatted_date = localized_datetime.isoformat()
    return formatted_date

def contract_date_transfer(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    desired_timezone = pytz.timezone("US/Pacific")
    localized_datetime = desired_timezone.localize(date_object.replace(hour=0, minute=0, second=0))
    formatted_date = localized_datetime.isoformat()
    return formatted_date

def bid_date_transfer(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    desired_timezone = pytz.timezone("US/Pacific")
    localized_datetime = desired_timezone.localize(date_object.replace(hour=10, minute=24, second=0, microsecond=0))
    formatted_date = localized_datetime.isoformat()
    return formatted_date

def bid_open_date_transfer(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    desired_timezone = pytz.timezone("US/Pacific")
    localized_datetime = desired_timezone.localize(date_object.replace(hour=14, minute=0, second=0, microsecond=0))
    formatted_date = localized_datetime.isoformat()
    return formatted_date

def cal_duration_date(start_date_str, end_date_str):

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
    delta = end_date - start_date
    days_difference = delta.days
    return days_difference

def get_award_json(df_byspeed, df_sap_contract, df_sap_po):
    idx = 0
    # awards/date
    awards_date = po_progress_data_transfer(str(df_byspeed.iloc[0]["PO - In Progress Date"]))
    # print(awards_date)

    # awards/id
    awards_id = df_sap_contract.iloc[0]["Purchasing Document"]
    # print(awards_id)

    # awards/status
    if df_sap_po.iloc[0]["Delivery date"]:
        awards_status = "active"
    # print(awards_status)

    # awards/value/amount
    awards_value_amount = df_sap_po.iloc[idx]["Order Quantity"]
    # print(awards_value_amount)

    # awards/value/currency
    awards_value_currency = "USD"
    # print(awards_value_currency)

    # awards/suppliers/name
    awards_suppliers_name = df_sap_po.iloc[idx]["Name 1"].title()
    # print(awards_suppliers_name)

    # awards/suppliers/id
    vendor_id = df_sap_po.iloc[idx]["Vendor"]
    awards_suppliers_id = f"pdx-vendor-{vendor_id}"
    # print(awards_suppliers_id)

    # awards/contractPeriod/startDate
    awards_contractPeriod_startDate = contract_date_transfer(str(df_sap_contract.iloc[0]["Validity Per. Start"]))
    # print(awards_contractPeriod_startDate)

    # awards/contractPeriod/endDate
    awards_contractPeriod_endDate = contract_date_transfer(str(df_sap_contract.iloc[0]["Validity Period End"]))
    # print(awards_contractPeriod_endDate)

    # awards/title
    awards_title = df_sap_contract.iloc[0]["Short Text"].title()
    # print(awards_title)

    # awards/description
    awards_description = "Agreement for  construction services."
    # print(awards_description)
    # Create awards library

    awards = {
        "date": awards_date,
        "id": str(awards_id),
        "status": awards_status,
        "value":{
            "amount": awards_value_amount,
            "currency": awards_value_currency
        },
        "suppliers":{
            "name": awards_suppliers_name,
            "id": awards_suppliers_id
        },
        "contractPeriod":{
            "startDate": awards_contractPeriod_startDate,
            "endDate": awards_contractPeriod_endDate
        },
        "title": awards_title,
        "description": awards_description
    }
    awards_json = {
        "contract_id": int(awards_id),
        "awards": awards
    }
    # print(awards)
    # file_name = "awards.json"
    # insert it into the database
    mycol.insert_one(awards_json)
    # print(mycol.insert_one(awards))
    # Use a context manager to open the file and write the JSON data
    # with open(file_name, 'w') as json_file:
    #     json.dump(awards, json_file, indent=4)  # Serialize and write the data to the file with indentation

def get_tender_json(contract_id, df_byspeed,df_bureau_ref, df_procurement_ref):
    # tender/id
    # print(df_byspeed.loc[idx,"Bid Number"])
    idx = 0
    tender_id = int(df_byspeed.iloc[idx]["Bid Number"])

    # tender/tenderPeriod/startDate
    # print(bid_date_transfer(df_byspeed.loc[0,"Bid - In Progress Date"]))
    tender_startDate = bid_date_transfer(str(df_byspeed.iloc[0]["Bid - In Progress Date"]))

    # tender/tenderPeriod/endDate
    tender_endDate = bid_open_date_transfer(str(df_byspeed.iloc[0]["Bid - Opened Date"]))

    # tender/tenderPeriod/durationInDays
    # print(cal_duration_date(df_byspeed.loc[0,"Bid - In Progress Date"], df_byspeed.loc[0,"Bid - Opened Date"]))
    tender_durationDay = cal_duration_date(str(df_byspeed.iloc[0]["Bid - In Progress Date"]), str(df_byspeed.iloc[0]["Bid - Opened Date"]))

    # tender/procuringEntity/name
    # tender/procuringEntity/id
    
    search_value=df_byspeed.iloc[0][" Req Header Column 1 Value"]
    matching_row = df_bureau_ref.loc[df_bureau_ref['BuySpeed Abbreviation '] == search_value]
    if not matching_row.empty:
        # print(matching_row.iloc[0]['Buyer/Name'])
        # print(matching_row.iloc[0]['Buyer/id'])
        tender_entity_name = matching_row.iloc[0]['Buyer/Name']
        tender_entity_id = matching_row.iloc[0]['Buyer/id']
    else:
        # print("NOTV FOUND")
        pass

    # tender/procurementMethod
    # tender/procurementMethodDetails
    # tender/mainProcurementCategory
    tender_method = "Selective"
    tender_methodDetail = ""
    tender_category = ""
    po_type_code = df_byspeed.iloc[0]['PO Type Code'].rstrip()
    # print(po_type_code)
    matching_row = df_procurement_ref.loc[df_procurement_ref["Description"] == po_type_code]
    if not matching_row.empty:
        tender_methodDetail = matching_row.iloc[0][2]
    else:
        # print("NOTV FOUND")
        pass

    if "Construction" in po_type_code:
        tender_category = "works"
    elif "G&S" in po_type_code:
        tender_category = "goods"
    elif "PTE" in po_type_code:
        tender_category = "services"
    
    # tender/title
    tender_title = df_byspeed.iloc[0][4]
    tender = {
        "id": str(tender_id),
        "tenderPeriod":{
            "startDate": tender_startDate,
            "endDate": tender_endDate,
            "durationInDays": tender_durationDay
        },
        "procuringEntity":{
            "name": tender_entity_name,
            "id": tender_entity_id
        },
        "procurementMethod": tender_method,
        "procurementMethodDetails": tender_methodDetail,
        "mainProcurementCategory": tender_category,
        "title": tender_title
    }

    tender_json = {
        "contract_id": contract_id,
        "tender": tender
    }
    mycol_tender.insert_one(tender_json)
    # file_name = "tender.json"
    # # Use a context manager to open the file and write the JSON data
    # with open(file_name, 'w') as json_file:
    #     json.dump(tender, json_file, indent=4)  # Serialize and write the data to the file with indentation

def get_general_json(contract_id, df_byspeed, df_bureau_ref):
    # Open Contracting ID
    req_num = int(df_byspeed.iloc[0]["REQ_NBR"])
    ocid_prefix = "{ocid-prefix}"  # 将这里替换成你的实际前缀
    general_ocid = f"{ocid_prefix}-{req_num}-master"
    # print(general_ocid)
    # Release ID
    general_id = "1"
    # Release Date
    general_date = ""
    # tag
    tag = []
    if(df_byspeed.iloc[0]["Bid Number"]):
        tag.append("tender")
    if(df_byspeed.iloc[0]["PO - In Progress Date"]):
        tag.append("award")
    if(df_byspeed.iloc[0]["Alternate Id"]):
        tag.append("contract")
    general_tag = ";".join(tag)
    # print(general_tag)
    # initiationType
    general_initiationType = ""
    if(df_byspeed.iloc[0]["Bid Number"]):
        general_initiationType = "tender"
    # print(general_initiationType)
    # buyer/name & buyer/id
    search_value=df_byspeed.iloc[0][" Req Header Column 1 Value"]
    matching_row = df_bureau_ref.loc[df_bureau_ref['BuySpeed Abbreviation '] == search_value]
    if not matching_row.empty:
        # print(matching_row.iloc[0]['Buyer/Name'])
        # print(matching_row.iloc[0]['Buyer/id'])
        general_buyer_name = matching_row.iloc[0]['Buyer/Name']
        general_buyer_id = matching_row.iloc[0]['Buyer/id']
        # print(general_buyer_name)
        # print(general_buyer_id)
    else:
        general_buyer_name = ""
        general_buyer_id = ""
        # print("NOTV FOUND")
    # language
    general_language = "en"
    # print(general_language)
    general = {
        "ocid": general_ocid,
        "id": general_id,
        "date": general_date,
        "tag": general_tag,
        "initiationType": general_initiationType,
        "buyer": {
            "name": general_buyer_name,
            "id": general_buyer_id
        },
        "language": general_language    
    }

    general_json = {
        "contract_id": contract_id,
        "general": general
    }
    # insert it into the database
    mycol_general.insert_one(general_json)
    # print(general)
    # file_name = "general.json"
    # # Use a context manager to open the file and write the JSON data
    # with open(file_name, 'w') as json_file:
    #     json.dump(general, json_file, indent=4)  # Serialize and write the data to the file with indentation

def get_contract_json(contract_id_input, df_sap_contract, df_sap_po):
    # contracts/id
    contracts_id = df_sap_contract.iloc[0]["Purchasing Document"]
    # print(contracts_id)

    # contracts/awardID
    award_id = contracts_id
    # print(award_id)

    # contracts/titlex
    contracts_titlex = df_sap_contract.iloc[0]["Short Text"].title()
    # print(contracts_titlex)

    # contracts/description
    contract_description = ""

    # contract/status
    if df_sap_po.iloc[0]["Delivery date"]:
        contracts_status = "active"
    # print(contracts_status)

    # contracts/period/startDate
    contract_contractPeriod_startDate = contract_date_transfer(str(df_sap_contract.iloc[0]["Validity Per. Start"]))
    # print(contract_contractPeriod_startDate)

    # contracts/period/endDate
    contracts_contractPeriod_endDate = contract_date_transfer(str(df_sap_contract.iloc[0]["Validity Period End"]))
    # print(contracts_contractPeriod_endDate)

    # contracts/period/durationInDays
    contracts_duration = cal_duration_date(str(df_sap_contract.iloc[0]["Validity Per. Start"]), str(df_sap_contract.iloc[0]["Validity Period End"]) )
    # print(contracts_duration)

    # contracts/value/amount
    contract_value_amount = df_sap_po.iloc[0]["Order Quantity"]
    # print(contract_value_amount)

    # contracts/value/currency
    contracts_value_currency = "USD"
    # print(contracts_value_currency)
    contracts = {
        "id": str(contracts_id),
        "awardID": str(award_id),
        "title": contracts_titlex,
        "description": contract_description,
        "status": contracts_status,
        "period":{
            "startDate": contract_contractPeriod_startDate,
            "endDate": contracts_contractPeriod_endDate,
            "durationInDays": contracts_duration
        },

        "value":{
            "amount": contract_value_amount,
            "currency": contracts_value_currency
        }
    }
    # print(contracts)
    contract_json = {
        "contract_id": contract_id_input,
        "contracts": contracts
    }
    # print(contract_json)
    mycol_contract.insert_one(contract_json)

def get_party_json(contract_id, df_byspeed, df_sap_contract, df_bureau_ref, df_sap_po, df_B2G):
    # parties 1
    # parties/name 
    # parties/roles
    # parties/id
    search_value=df_byspeed.iloc[0][" Req Header Column 1 Value"]
    matching_row = df_bureau_ref.loc[df_bureau_ref['BuySpeed Abbreviation '] == search_value]
    if not matching_row.empty:
        party1__name = matching_row.iloc[0]['Buyer/Name']
        party1_id = matching_row.iloc[0]['Buyer/id']
        party1_role = "buyer; procuringEntity"
    else:
        party1__name = ""
        party1_id = ""
        party1_role = ""

    # print(party1__name)
    # print(party1_id)
    # print(party1_role)
    # parties/identifier/scheme
    party1_identifier_scheme = '-'.join(party1_id.rsplit('-', 1)[:-1])
    # print(party1_identifier_scheme)  
    # parties/identifier/id
    party1_identifier_id = party1_id.split('-')[-1]
    # print(party1_identifier_id)
    # parties/contactPoint/name
    party1_contract_name = df_sap_contract.iloc[0]["Project Manager"]
    # print(party1_contract_name)

    # parties/name
    party2_name = df_sap_po.iloc[0]["Name 1"].title()
    # print(party2_name)
    # parties/roles
    party2_role="supplier; tenderer; payer; payee"
    # print(party2_role)
    # parties/id
    party2_identifier_id = df_sap_po.iloc[0]["Vendor"]
    party2_id = f"pdx-vendor-{party2_identifier_id}"
    # print(party2_id)
    # parties/identifier/scheme
    party2_identifier_scheme = '-'.join(party2_id.rsplit('-', 1)[:-1])
    # print(party2_identifier_scheme)  
    # parties/identifier/id
    party2_identifier_id = party2_id.split('-')[-1]
    # print(party2_identifier_id)
    # parties/details/classification/description
    party2_class1_desc = df_B2G.iloc[0]["Ethnicity"]
    # print(party2_class1_desc)
    # parties/details/classification/scheme
    party2_class1_scheme = "Race/Ethnicity"
    # print(party2_class1_scheme)
    #parties/details/classification/description
    party2_class2_desc = df_B2G.iloc[0]["Gender"]
    # print(party2_class2_desc)
    # parties/details/classification/scheme
    party2_class2_scheme = "Gender"
    # print(party2_class2_scheme)
    #parties/details/classification/description
    if df_B2G.iloc[0]["Additional Certifications"]:
        try:
            goal_type_set = set(df_B2G.iloc[0]["Goal Type"].split(", "))
            additional_certifications_set = set(df_B2G.iloc[0]["Additional Certifications"].split(", "))
            merged_set = goal_type_set.union(additional_certifications_set)
            party2_class3_desc = ", ".join(merged_set)
            
        except:
            party2_class3_desc = df_B2G.iloc[0]["Goal Type"]
    else:
        party2_class3_desc = df_B2G.iloc[0]["Goal Type"]
    # print(party2_class3_desc)
    # parties/details/classification/scheme
    party2_class3_scheme = "Certification"
    # print(party2_class3_scheme)
    parties = {
        "party1": {
            "name": party1__name,
            "role": party1_role,
            "id": party1_id,
            "identifier": {
                "scheme": party1_identifier_scheme,
                "id": party1_identifier_id
            },
            "contactPoint": {
                "name": party1_contract_name
            }
        },
        "party2": {
            "name": party2_name,
            "role": party2_role,
            "id": party2_id,
            "identifier": {
                "scheme": party2_identifier_scheme,
                "id": party2_identifier_id
            },
            "details": {
                "classfication1": {
                    "description": party2_class1_desc,
                    "scheme": party2_class1_scheme
                },
                "classfication2": {
                    "description": party2_class2_desc,
                    "scheme": party2_class2_scheme
                },
                "classfication3": {
                    "description": party2_class3_desc,
                    "scheme": party2_class3_scheme
                }
            }
        }
    }
    parties_json = {
        "contract_id": contract_id,
        "parties": parties
    }
    # print(parties_json)
    mycol_party.insert_one(parties_json)

def get_json(contract_id):
    df_bureau_ref = pd.read_excel('master contract 30007897.xlsx', sheet_name='Bureau Reference Sheet')
    df_procurement_ref = pd.read_excel('master contract 30007897.xlsx', sheet_name='Procurement Method Details')
    df_sap_po = pd.read_excel('SAP PO Listing Report FY2019-23.xlsx')
    matching_row = df_sap_po.loc[(df_sap_po['Outline agreement'] == str(contract_id)) & (df_sap_po["Item"] == 10)]
    
    if not matching_row.empty:
        df_sap_po = pd.DataFrame(matching_row.iloc[0]).T
    else:
        # print("NOT FOUND 1")
        return

    df_sap_contract = pd.read_excel('SAP Contract Listing Report FY2019-23 from PO Listing Report.xlsx')
    matching_row = df_sap_contract.loc[(df_sap_contract['Purchasing Document'] == contract_id) & (df_sap_contract["Item"] == 10)]
    if not matching_row.empty:
        df_sap_contract = pd.DataFrame(matching_row.iloc[0]).T
    else:
        # print("NOT FOUND 2")
        pass


    df_byspeed = pd.read_excel('BuySpeed Report.xlsx')
    matching_row = df_byspeed.loc[df_byspeed['Alternate Id'] == str(contract_id)]
    if not matching_row.empty:
        df_byspeed = pd.DataFrame(matching_row.iloc[0]).T
    else:
        # print("NOT FOUND3")
        pass

    df_B2G = pd.read_excel("B2G Contract Status Report.xlsx") 
    # print(df_B2G)
    matching_row = df_B2G.loc[df_B2G['Contract Number'] == str(contract_id)]
    if not matching_row.empty:
        df_B2G = pd.DataFrame(matching_row.iloc[0]).T
    else:
        # print("NOT FOUND3")
        pass
    # print(df_B2G)
    # get_award_json(df_byspeed, df_sap_contract, df_sap_po)


    # get_tender_json(df_byspeed,df_bureau_ref, df_procurement_ref)
    # get_general_json(df_byspeed, df_bureau_ref)
    # get_contract_json(df_byspeed, df_sap_contract, df_sap_po)
    get_party_json(contract_id, df_byspeed, df_sap_contract, df_bureau_ref, df_sap_po,df_B2G)

# contract_id = 30007897
# get_json(30007897)
# get_award_json(30007897)

def get_award_json_and_insert_db():
    df_sap_po = pd.read_excel('SAP PO Listing Report FY2019-23.xlsx')
    df_sap_contract = pd.read_excel('SAP Contract Listing Report FY2019-23 from PO Listing Report.xlsx')
    df_byspeed = pd.read_excel('BuySpeed Report.xlsx')

    contract_ids = df_sap_po['Outline agreement'].unique()
    # print(contract_ids)
    
    total_num = len(contract_ids)
    print("total contract_id num:", total_num)
    num = 0
    for contract_id in contract_ids:
        num += 1
        try:
            contract_id = int(contract_id)
        except:
            continue
        matching_row = df_sap_po.loc[(df_sap_po['Outline agreement'] == str(contract_id)) & (df_sap_po["Item"] == 10)]
        if not matching_row.empty:
            df_sap_po_matched = pd.DataFrame(matching_row.iloc[0]).T
        else:
            # print("NOT FOUND 1 for contract_id:", contract_id)
            continue

    
        matching_row = df_sap_contract.loc[(df_sap_contract['Purchasing Document'] == contract_id) & (df_sap_contract["Item"] == 10)]
        if not matching_row.empty:
            df_sap_contract_matched = pd.DataFrame(matching_row.iloc[0]).T
        else:
            # print("NOT FOUND 2 for contract_id:", contract_id)
            continue

    
        matching_row = df_byspeed.loc[df_byspeed['Alternate Id'] == str(contract_id)]
        if not matching_row.empty:
            df_byspeed_matched = pd.DataFrame(matching_row.iloc[0]).T
        else:
            # print("NOT FOUND3 for contract_id:", contract_id)
            continue

        get_award_json(df_byspeed_matched, df_sap_contract_matched, df_sap_po_matched)
        if num%100 == 0:
            print(f"Finished: {num} / {total_num}!")

def get_general_json_and_insert_db():
    df_bureau_ref = pd.read_excel('master contract 30007897.xlsx', sheet_name='Bureau Reference Sheet')
    df_sap_po = pd.read_excel('SAP PO Listing Report FY2019-23.xlsx')
    df_byspeed = pd.read_excel('BuySpeed Report.xlsx')

    contract_ids = df_sap_po['Outline agreement'].unique()
    # print(contract_ids)
    
    total_num = len(contract_ids)
    print("total contract_id num:", total_num)
    num = 0
    for contract_id in contract_ids:
        num += 1
        try:
            contract_id = int(contract_id)
        except:
            continue
        matching_row = df_byspeed.loc[df_byspeed['Alternate Id'] == str(contract_id)]
        if not matching_row.empty:
            df_byspeed_matched = pd.DataFrame(matching_row.iloc[0]).T
        else:
            # print("NOT FOUND3 for contract_id:", contract_id)
            continue
        try:
            get_general_json(contract_id, df_byspeed_matched, df_bureau_ref)
        except Exception as e:
            pass
            # print(f"An error occurred: {e}")

        if num%100 == 0:
            print(f"Finished: {num} / {total_num}!")

def get_tender_json_and_insert_db():
    df_bureau_ref = pd.read_excel('master contract 30007897.xlsx', sheet_name='Bureau Reference Sheet')
    df_procurement_ref = pd.read_excel('master contract 30007897.xlsx', sheet_name='Procurement Method Details')
    df_sap_po = pd.read_excel('SAP PO Listing Report FY2019-23.xlsx')
    df_byspeed = pd.read_excel('BuySpeed Report.xlsx')

    contract_ids = df_sap_po['Outline agreement'].unique()
    # print(contract_ids)
    
    total_num = len(contract_ids)
    print("total contract_id num:", total_num)
    num = 0
    for contract_id in contract_ids:
        num += 1
        try:
            contract_id = int(contract_id)
        except:
            continue

        matching_row = df_byspeed.loc[df_byspeed['Alternate Id'] == str(contract_id)]
        if not matching_row.empty:
            df_byspeed_matched = pd.DataFrame(matching_row.iloc[0]).T
        else:
            # print("NOT FOUND3 for contract_id:", contract_id)
            continue
        try:
            get_tender_json(contract_id, df_byspeed_matched,df_bureau_ref, df_procurement_ref)
        except Exception as e:
            # print(f"An error occurred: {e}")
            pass

        if num%100 == 0:
            print(f"Finished: {num} / {total_num}!")

def get_party_json_and_insert_db():
    df_sap_contract = pd.read_excel('SAP Contract Listing Report FY2019-23 from PO Listing Report.xlsx')
    df_bureau_ref = pd.read_excel('master contract 30007897.xlsx', sheet_name='Bureau Reference Sheet')
    df_sap_po = pd.read_excel('SAP PO Listing Report FY2019-23.xlsx')
    df_byspeed = pd.read_excel('BuySpeed Report.xlsx')
    df_B2G = pd.read_excel("B2G Contract Status Report.xlsx") 

    contract_ids = df_sap_po['Outline agreement'].unique()
    # print(contract_ids)
    
    total_num = len(contract_ids)
    print("total contract_id num:", total_num)
    num = 0
    for contract_id in contract_ids:
        num += 1
        try:
            contract_id = int(contract_id)
        except:
            continue

        matching_row = df_sap_po.loc[(df_sap_po['Outline agreement'] == str(contract_id)) & (df_sap_po["Item"] == 10)]
        if not matching_row.empty:
            df_sap_po_matched = pd.DataFrame(matching_row.iloc[0]).T
        else:
            # print("NOT FOUND 1 for contract_id:", contract_id)
            continue

        matching_row = df_sap_contract.loc[(df_sap_contract['Purchasing Document'] == contract_id) & (df_sap_contract["Item"] == 10)]
        if not matching_row.empty:
            df_sap_contract_matched = pd.DataFrame(matching_row.iloc[0]).T
        else:
            # print("NOT FOUND 2 for contract_id:", contract_id)
            continue

        matching_row = df_byspeed.loc[df_byspeed['Alternate Id'] == str(contract_id)]
        if not matching_row.empty:
            df_byspeed_matched = pd.DataFrame(matching_row.iloc[0]).T
        else:
            # print("NOT FOUND3 for contract_id:", contract_id)
            continue

        matching_row = df_B2G.loc[df_B2G['Contract Number'] == str(contract_id)]
        if not matching_row.empty:
            df_B2G_matched = pd.DataFrame(matching_row.iloc[0]).T
        else:
            # print("NOT FOUND4 for contract_id:", contract_id)
            continue
        
        try:
            get_party_json(contract_id, df_byspeed_matched, df_sap_contract_matched, df_bureau_ref, df_sap_po_matched, df_B2G_matched)
        except Exception as e:
            # print(f"An error occurred: {e}")
            pass

        if num%100 == 0:
            print(f"Finished: {num} / {total_num}!")

def get_contract_json_and_insert_db():
    df_sap_po = pd.read_excel('SAP PO Listing Report FY2019-23.xlsx')
    df_sap_contract = pd.read_excel('SAP Contract Listing Report FY2019-23 from PO Listing Report.xlsx')
    df_byspeed = pd.read_excel('BuySpeed Report.xlsx')

    contract_ids = df_sap_po['Outline agreement'].unique()
    # print(contract_ids)
    
    total_num = len(contract_ids)
    print("total contract_id num:", total_num)
    num = 0
    for contract_id in contract_ids:
        num += 1
        try:
            contract_id = int(contract_id)
        except:
            continue
        matching_row = df_sap_po.loc[(df_sap_po['Outline agreement'] == str(contract_id)) & (df_sap_po["Item"] == 10)]
        if not matching_row.empty:
            df_sap_po_matched = pd.DataFrame(matching_row.iloc[0]).T
        else:
            # print("NOT FOUND 1 for contract_id:", contract_id)
            continue

    
        matching_row = df_sap_contract.loc[(df_sap_contract['Purchasing Document'] == contract_id) & (df_sap_contract["Item"] == 10)]
        if not matching_row.empty:
            df_sap_contract_matched = pd.DataFrame(matching_row.iloc[0]).T
        else:
            # print("NOT FOUND 2 for contract_id:", contract_id)
            continue

        get_contract_json(contract_id, df_sap_contract_matched, df_sap_po_matched)
        if num%100 == 0:
            print(f"Finished: {num} / {total_num}!")

def create_vendor_directory_in_db():
    cursor = mycol_party.find()
    num = 0
    for data_party in cursor:
        desired_contract_id = data_party["contract_id"]
        data_general = mycol_general.find_one({'contract_id': int(desired_contract_id)})
        data_award = mycol.find_one({'contract_id': int(desired_contract_id)})
        
        if data_general:
            org_name = data_general["general"]["buyer"]["name"]
            # print(org_name)
        else:
            continue
        
        if data_award:
            vendor_name = data_award["awards"]["suppliers"]["name"]
            contract_status = data_award["awards"]["status"]
        else:
            continue
        
        if data_party:
            # certification
            certification = data_party["parties"]["party2"]["details"]["classfication3"]["description"]
            try:
                if math.isnan(certification):
                    certification = "NaN"
            except:
                pass
        else:
            continue
        num += 1
        contract_info = {
            "key": str(num),
            "name": vendor_name,
            "org": org_name,
            "contract": desired_contract_id,
            "cert": certification,
            "aval": "80%",
            "tags": [contract_status]
        }
        # print(contract_info)
        mycol_vendor.insert_one(contract_info)


print("Award ...")
get_award_json_and_insert_db()
print("Award Finished")
print("General ...")
get_general_json_and_insert_db()
print("General Finished")
print("Tender ...")
get_tender_json_and_insert_db()
print("Tender Finished")
print("Party ...")
get_party_json_and_insert_db()
print("Party Finished")
print("Contract ...")
get_contract_json_and_insert_db()
print("Contract Finished")
print("Vendor ...")
create_vendor_directory_in_db()
print("Vendor Finished")