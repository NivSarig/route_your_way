#!/usr/bin/env python
# coding: utf-8

# In[34]:


import requests
from geopy.geocoders import Nominatim
import random
from datetime import datetime, timedelta

api_key = 'AIzaSyDP0EV22kIb6LHSh3zEABMe1CTxwzwSdWs'
DO_PRINT=False
log_file_name = f'/home/niv/dev/route_your_way/log.log'
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"  # Reset color to default

def formated_now():
    return datetime.now().strftime('%Y:%m:%d-%H:%M:%S.%f')

def create_logger(log_file_name):
    print(log_file_name)
    open(log_file_name, 'w').close()
    def log_func(msg, do_print=DO_PRINT, end="\n"):
        mmsg = f"{COLOR_RED}{formated_now()}{COLOR_RESET}, {COLOR_GREEN}msg: {COLOR_RESET}{msg}\n"
        if do_print:
            print(mmsg, end=end)
        with open(log_file_name, 'a+') as fid:
            fid.write(mmsg)
    return log_func

log = create_logger(log_file_name)
log(f"New run start at {formated_now()}")
            
def generate_random_coordinates(city, num_coordinates):
    # Initialize geolocator
    geolocator = Nominatim(user_agent="route-your-way-app")

    # Get city coordinates
    location = geolocator.geocode(city)
    if not location:
        return None

    # Get the bounding box coordinates of the city
    bbox = location.raw['boundingbox']
    min_lat, max_lat, min_lon, max_lon = map(float, bbox)

    # Generate random coordinates within the bounding box
    coordinates = []
    for _ in range(num_coordinates):
        lat = random.uniform(min_lat, max_lat)
        lon = random.uniform(min_lon, max_lon)
        coordinates.append((lat, lon))

    if coordinates:
        for i, (lat, lon) in enumerate(coordinates, 1):
            log(f"Coordinate {i}: Latitude {lat}, Longitude {lon}")
    else:
        log("City not found or coordinates not available.", True)

    coordinate_str = '/'.join(["%20".join([str(lat), str(lon)]) for (lat, lon) in coordinates])
    last_coordinate = "%20".join([str(coordinates[-1][0]), str(coordinates[-1][1])])
    url = "https://www.google.com/maps/dir/{}/@{},16.18z/data=!4m2!4m1!3e0?entry=ttu".format(
        coordinate_str, last_coordinate)
    log("url=", end=" ")
    log("{}".format(url))

    return url, coordinates


def get_route_info(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    log(f"Fetching data from {url}")
    response = requests.get(url, timeout=1)
    log("Got response")
    data = response.json()
    log(f"Found data for {origin}, {destination}")
    if data['status'] == 'OK':
        route = data['routes'][0]
        distance = route['legs'][0]['distance']['value']
        duration = route['legs'][0]['duration']['value']
        return distance, duration
    else:
        log(f"data status {data['status']}", True)
        log(data, True)
        return None, None


def pairwise(iterable):
    """Generate pairs of consecutive elements from an iterable."""
    a, b = iter(iterable), iter(iterable)
    next(b, None)  # Advance b by one element
    return zip(a, b)


def get_distance_and_duration(coordinates):
    coordinates_str = [",".join([str(lat), str(long)]) for lat, long in coordinates]
    distance = 0
    duration = 0
    for origin, destination in pairwise(coordinates_str):
        log((origin, destination))
        seg_distance, seg_duration = get_route_info(origin, destination)
        if seg_distance and seg_duration:
            log((seg_distance, seg_duration))
            distance += seg_distance
            duration += seg_duration
        else:
            log("Failed to retrieve route information.", True)
            
    return distance/1000, seconds_to_hh_mm_ss(duration)
    

def get_coordinates_from_url(url):
    return [coordinate.split("+") for coordinate in url.split('/dir')[1].split("@")[0].split("/")[1:-1]]


def seconds_to_hh_mm_ss(seconds):
    # Create a timedelta object representing the duration
    duration = timedelta(seconds=seconds)
    # Format the duration as HH:MM:SS
    hh_mm_ss = str(duration).split('.')[0]  # Get rid of microseconds
    return hh_mm_ss


def build_all_duration_matrix(coordinates):
    deadhead_index = {}
    for idx, origin in enumerate(coordinates):
        for idy, destination in enumerate(coordinates):
            if idx == idy:
                log(f"origin is location. idx {idx}")
                distance = 0
                duration = 0
            else:
                log(origin)
                log(destination)
                distance, duration = get_route_info(",".join(map(str, origin)), 
                                                    ",".join(map(str, destination)))
            deadhead_index[origin, destination] = {
                "origin_idx": idx,
                "destination_idx": idy,
                "origin": origin,
                "destination": destination,
                "distance": distance,
                "duration": duration}
    return deadhead_index


randomize = True
city = "Moscow"
num_coordinates = 10

if randomize:
    url, coordinates = generate_random_coordinates(city, num_coordinates)
else:
    url = "https://www.google.com/maps/dir/55.8851468503753%2037.51883085420433/55.64084712224211%2037.63753714586377/55.63171357216796%2037.567176092581796/55.71061470072395%2037.645024291490905/55.79635556987808%2037.705739569659144/55.73625845994696%2037.474939644984126/55.6055236828096%2037.55303667588389/55.82474622577668%2037.487459359835334/55.77313511263688%2037.478889483443794/55.767957973285405%2037.48903720422404/@55.767957973285405%2037.48903720422404,16.18z/data=!4m2!4m1!3e0?entry=ttu"
    coordinates = [
        (55.8851468503753, 37.51883085420433),
        (55.64084712224211, 37.63753714586377),
        (55.63171357216796, 37.567176092581796),
        (55.71061470072395, 37.645024291490905),
        (55.79635556987808, 37.705739569659144),
        (55.73625845994696, 37.474939644984126),
        (55.6055236828096, 37.55303667588389),
        (55.82474622577668, 37.487459359835334),
        (55.77313511263688, 37.478889483443794),
        (55.767957973285405, 37.48903720422404)]
print(url)
print(coordinates)


new_url = "https://www.google.com/maps/dir/55.78879096471749+37.56912052075894/55.82394492336372+37.71564443590594/55.718563249961306+37.51647539470249/55.775807492867564+37.51946053900027/55.690901822366115+37.46013158008646/55.80069715769361+37.56576992130943/55.60486832825113+37.466155203107114/55.78130697817363+37.46718729666109/55.70319444748+37.63345154478967/55.843094719260534+37.47741722330984/@55.7272268,37.3982661,11z/data=!3m1!4b1!4m62!4m61!1m5!1m1!1s0x0:0xfebb1ddabbd58077!2m2!1d37.5685818!2d55.7885064!1m5!1m1!1s0x0:0x865d4de12b4564b6!2m2!1d37.716047!2d55.8236744!1m5!1m1!1s0x0:0x5df7cd41dca8f173!2m2!1d37.5139163!2d55.7061335!1m5!1m1!1s0x0:0x8439f8542df1d9a4!2m2!1d37.5198347!2d55.7759439!1m5!1m1!1s0x0:0xd0422de2cbc7203f!2m2!1d37.4600474!2d55.6907233!1m5!1m1!1s0x0:0x9e8663cc32912aa7!2m2!1d37.5659516!2d55.8008145!1m5!1m1!1s0x0:0x23dd95533621b43b!2m2!1d37.4623676!2d55.6028596!1m5!1m1!1s0x0:0x76d30e134b59d2a1!2m2!1d37.4773823!2d55.7750483!1m5!1m1!1s0x0:0xfd468a8f9cf66ed8!2m2!1d37.6333575!2d55.7028242!1m5!1m1!1s0x0:0xa0c2634c7f03102d!2m2!1d37.4773427!2d55.8429622!3e0?entry=ttu"
new_coordinates = get_coordinates_from_url(new_url)
distance, duration = get_distance_and_duration(new_coordinates)
print(distance, duration)


short_coordinates = [
    (55.8851468503753, 37.51883085420433),
    (55.64084712224211, 37.63753714586377)]
deadhead_index = build_all_duration_matrix(short_coordinates)

log(deadhead_index)

log(datetime.now().strftime("%Y:%m:%d-%H:%M:%S"))


# In[ ]:





# In[ ]:




