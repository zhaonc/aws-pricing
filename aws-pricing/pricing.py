import time
import requests
import re
import json
import pandas as pd
import numpy as np
from constants import REGIONS, INSTANCE_TYPES


def get_spot_prices():
    url = 'https://spot-price.s3.amazonaws.com/spot.js?callback=callback&_={}'.format(int(time.time()))
    response = requests.get(url)

    # Get data and parse as JSON
    raw_text = response.text
    matches = re.findall(r'callback\((.*)\);', raw_text, re.MULTILINE | re.DOTALL)
    data = json.loads(matches[0])

    instance_name_pattern = r'([\w\d-]+)\.([\w\d]+)'

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
                instance_name = size['size']
                if match := re.search(instance_name_pattern, instance_name):
                    instance_family = match.group(1)
                    instance_size = match.group(2)
                
                for value_column in size['valueColumns']:
                    value_column_name = value_column['name']
                    value_column_price = value_column['prices'][currency]
                    try:
                        value_column_price = float(value_column_price)
                    except ValueError:
                        value_column_price = np.nan
                    parsed.append({
                        'region': REGIONS.get(region_name, region_name),
                        'instance_type': instance_type_name,
                        'generation': instance_type_generation,
                        'instance_name': instance_name,
                        'instance_family': instance_family,
                        'instance_size': instance_size,
                        'system': value_column_name,
                        'price': value_column_price
                    })

    df = pd.DataFrame(parsed)
    return df