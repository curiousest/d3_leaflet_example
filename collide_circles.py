import math
import json
from pprint import pprint

# from https://gist.github.com/rochacbruno/2883505
def haversine_distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def circle_overlapping_area(center_distance, radius):
    if center_distance >= radius * 2:
        return 0
    line_segment = math.sqrt(radius**2 - (center_distance / 2)**2)
    sector_triangle_area = (line_segment / 2) * (center_distance / 2)
    circle_sector_angle = 2 * math.degrees(math.asin(line_segment/radius))
    sector_area = (circle_sector_angle / 360) * math.pi * radius**2
    return 2 * (sector_area - sector_triangle_area)


with open('city.json') as data_file:
    data = json.load(data_file)

    # circles are about 63km in radius
    radius = 63
    circle_area = math.pi * radius**2

    for city in data:
        city_coords = (float(city['lat']), float(city['lon']))
        covered_area_fraction = 0
        # for each possibly intersecting city
        for x_city in data:
            distance = haversine_distance(city_coords, (float(x_city['lat']), float(x_city['lon'])))
            overlapping_area = circle_overlapping_area(distance, radius)
            covered_area_fraction = covered_area_fraction + overlapping_area / circle_area
        city['covered_area'] = covered_area_fraction - 1

    with open('city_'+ str(radius) + '_km_radius_circles.json', 'w') as outfile:
        json.dump(data, outfile)
