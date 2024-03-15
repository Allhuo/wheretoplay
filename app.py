from flask import Flask, render_template, request, jsonify
import random
import json
from utils import preprocess_city_data, find_city_boundary

app = Flask(__name__)

city_file_map = preprocess_city_data()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search_cities', methods=['GET'])
def search_cities():
    keyword = request.args.get('keyword', '')
    results = [city for city in city_file_map.keys() if keyword in city]
    print(results)
    return jsonify(results)


@app.route('/get_city_bounds', methods=['POST'])
def get_city_bounds():
    city = request.json['city']
    print(f'请求城市: {city}')
    if city in city_file_map:
        city_boundary = find_city_boundary(city_file_map[city], city)
        print(f'城市边界: {city_boundary}')
        if city_boundary:
            return jsonify(city_boundary)
    return jsonify([])


@app.route('/get_random_point', methods=['POST'])
def get_random_point():
    bounds = request.json['bounds']

    # 找到边界的最小和最大经纬度
    min_lon, min_lat = float('inf'), float('inf')
    max_lon, max_lat = float('-inf'), float('-inf')
    for coord in bounds:
        min_lon = min(min_lon, coord[0])
        min_lat = min(min_lat, coord[1])
        max_lon = max(max_lon, coord[0])
        max_lat = max(max_lat, coord[1])

    # 在边界内随机生成一个点
    while True:
        rand_lon = random.uniform(min_lon, max_lon)
        rand_lat = random.uniform(min_lat, max_lat)
        if point_in_polygon([rand_lon, rand_lat], bounds):
            return jsonify([rand_lon, rand_lat])


def point_in_polygon(point, polygon):
    # 射线法判断点是否在多边形内部
    inside = False
    x, y = point
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        if (y1 <= y < y2) or (y2 <= y < y1):
            if x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                inside = not inside
    return inside


if __name__ == '__main__':
    app.run(debug=True)