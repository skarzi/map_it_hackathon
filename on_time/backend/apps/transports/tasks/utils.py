import math

EARTH_RADIUS = 6371e3
CENTER = (52.237049, 21.017532)

def is_in_circle(point, radius=5_000):
    point = [float(x) for x in point]
    lat_diff = degrees_to_radians(point[0] - CENTER[0])
    lng_diff = degrees_to_radians(point[1] - CENTER[1])
    tmp = (
        (math.sin(lat_diff / 2) * math.sin(lat_diff / 2))
        + math.cos(degrees_to_radians(CENTER[0]))
        * math.cos(degrees_to_radians(point[1]))
        * math.sin(lng_diff / 2) * math.sin(lng_diff / 2)
    )
    distance = EARTH_RADIUS * (2 * math.atan2(math.sqrt(tmp), math.sqrt(1 - tmp)))
    return distance < radius



def degrees_to_radians(degrees):
    return math.pi * degrees / 180
