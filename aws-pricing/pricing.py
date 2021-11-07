import time
import requests
import re
import json
import pandas as pd
from constants import REGIONS, INSTANCE_TYPES


def get_spot_prices():
    url = 'https://spot-price.s3.amazonaws.com/spot.js?callback=callback&_={}'.format(int(time.time()))
    response = requests.get(url)

    # Get data and parse as JSON
    raw_text = response.text
    matches = re.findall(r'callback\((.*)\);', raw_text, re.MULTILINE | re.DOTALL)
    data = json.loads(matches[0])

    # Parse JSON
    parsed = []

    value_columns = data['config']['valueColumns']
    currency = data['config']['currencies'][0]

    for region in data['config']['regions']:
        region_name = region['region']
        
        for instance_type in region['instanceTypes']:
            type_name = instance_type['type']
            instance_type_name, instance_type_generation = INSTANCE_TYPES.get(type_name)
            
            for size in instance_type['sizes']:
                size_name = size['size']
                
                for value_column in size['valueColumns']:
                    value_column_name = value_column['name']
                    value_column_price = value_column['prices'][currency]
                    parsed.append({
                        'region': REGIONS.get(region_name, region_name),
                        'instance_type': instance_type_name,
                        'generation': instance_type_generation,
                        'instance_size': size_name,
                        'system': value_column_name,
                        'price': value_column_price
                    })

    df = pd.DataFrame(parsed)
    return df

def get_researched_instance_options():
    url = 'https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-reservedinstance/metadata.json?timestamp={}'.format(int(time.time()))
    response = requests.get(url)

    # Get data and parse as JSON
    raw_text = response.text
    data = json.loads(raw_text)

    contract_length = data['valueAttributes']['plc:LeaseContractLength']
    purchase_option = data['valueAttributes']['PurchaseOption']
    location = data['valueAttributes']['Location']
    tenancy = data['valueAttributes']['Tenancy']
    system = data['valueAttributes']['plc:OperatingSystem']

    return {
        'contract_length': contract_length,
        'purchase_option': purchase_option,
        'location': location,
        'tenancy': tenancy,
        'system': system
    }