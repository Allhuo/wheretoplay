import os
import json


def preprocess_city_data():
    city_file_map = {}
    province_dir = 'data1/geometryProvince'

    for filename in os.listdir(province_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(province_dir, filename)
            with open(file_path, 'r', encoding='utf-8-sig') as f:  # 修改这里
                data = json.load(f)
            for feature in data['features']:
                city_name = feature['properties']['name']
                city_file_map[city_name] = file_path

    return city_file_map


def find_city_boundary(file_path, city_name):
    with open(file_path, 'r', encoding='utf-8-sig') as f:  # 修改这里
        data = json.load(f)
    for feature in data['features']:
        if feature['properties']['name'] == city_name:
            return feature['geometry']['coordinates'][0]

    return None