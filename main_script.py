from external_integrations.gmaps_integration_utils import generate_random_coordinates, build_all_duration_matrix, \
    coordinate_to_str, \
    get_route_info_from_url, get_url_from_origin_waypoints_and_destination
import requests

from logging_utils import log, formatted_now

if __name__ == "__main__":
    randomize = False
    city = "Moscow"
    num_coordinates = 10

    if randomize:
        url, coordinates = generate_random_coordinates(city, num_coordinates)
    else:
        url = "https://www.google.com/maps/dir/55.8851468503753%2037.51883085420433/55.64084712224211%2037.63753714586377/55.63171357216796%2037.567176092581796/55.71061470072395%2037.645024291490905/55.79635556987808%2037.705739569659144/55.73625845994696%2037.474939644984126/55.6055236828096%2037.55303667588389/55.82474622577668%2037.487459359835334/55.77313511263688%2037.478889483443794/55.767957973285405%2037.48903720422404/@55.767957973285405%2037.48903720422404,16.18z/data=!4m2!4m1!3e0?entry=ttu"
        coordinates = [(55.8851468503753, 37.51883085420433),
                       (55.64084712224211, 37.63753714586377),
                       (55.63171357216796, 37.567176092581796),
                       (55.71061470072395, 37.645024291490905),
                       (55.79635556987808, 37.705739569659144),
                       (55.73625845994696, 37.474939644984126),
                       (55.6055236828096, 37.55303667588389),
                       (55.82474622577668, 37.487459359835334),
                       (55.77313511263688, 37.478889483443794),
                       (55.767957973285405, 37.48903720422404)]
    log(url)
    log(coordinates)

    new_url = "https://www.google.com/maps/dir/55.78879096471749+37.56912052075894/55.82394492336372+37.71564443590594/55.718563249961306+37.51647539470249/55.775807492867564+37.51946053900027/55.690901822366115+37.46013158008646/55.80069715769361+37.56576992130943/55.60486832825113+37.466155203107114/55.78130697817363+37.46718729666109/55.70319444748+37.63345154478967/55.843094719260534+37.47741722330984/@55.7272268,37.3982661,11z/data=!3m1!4b1!4m62!4m61!1m5!1m1!1s0x0:0xfebb1ddabbd58077!2m2!1d37.5685818!2d55.7885064!1m5!1m1!1s0x0:0x865d4de12b4564b6!2m2!1d37.716047!2d55.8236744!1m5!1m1!1s0x0:0x5df7cd41dca8f173!2m2!1d37.5139163!2d55.7061335!1m5!1m1!1s0x0:0x8439f8542df1d9a4!2m2!1d37.5198347!2d55.7759439!1m5!1m1!1s0x0:0xd0422de2cbc7203f!2m2!1d37.4600474!2d55.6907233!1m5!1m1!1s0x0:0x9e8663cc32912aa7!2m2!1d37.5659516!2d55.8008145!1m5!1m1!1s0x0:0x23dd95533621b43b!2m2!1d37.4623676!2d55.6028596!1m5!1m1!1s0x0:0x76d30e134b59d2a1!2m2!1d37.4773823!2d55.7750483!1m5!1m1!1s0x0:0xfd468a8f9cf66ed8!2m2!1d37.6333575!2d55.7028242!1m5!1m1!1s0x0:0xa0c2634c7f03102d!2m2!1d37.4773427!2d55.8429622!3e0?entry=ttu"
    distance, duration = get_route_info_from_url(new_url)
    log((distance, duration))

    short_coordinates = [
        (55.8851468503753, 37.51883085420433),
        (55.64084712224211, 37.63753714586377)]
    deadhead_index = build_all_duration_matrix(short_coordinates)

    log(deadhead_index)

    origin = (55.70319444748, 37.63345154478967)
    destination = (55.843094719260534, 37.47741722330984)
    waypoints = [
        (55.76256915886491, 37.53964491245408),
        (55.79953159156407, 37.62388899803995),
        (55.82000118014139, 37.531695602671846)]
    coordinate_to_str(origin)
    coordinate_to_str(destination)
    coordinates_with_waypoints = "https://maps.googleapis.com/maps/api/directions/json?origin=55.70319444748,37.63345154478967&destination=55.843094719260534,37.47741722330984&waypoints=55.76256915886491,37.53964491245408|55.79953159156407,37.62388899803995|55.82000118014139,37.531695602671844&key=AIzaSyDP0EV22kIb6LHSh3zEABMe1CTxwzwSdWs"
    url_with_waypoints = get_url_from_origin_waypoints_and_destination(origin, destination, coordinates_with_waypoints)
    print(url)
    response = requests.get(url_with_waypoints, timeout=1)
    data = response.json()
    for item in data['routes'][0]['legs']:
        cum_distance = 0
        cum_duration = 0
        for step in item['steps']:
            cum_distance += step['distance']['value']
            cum_duration += step['duration']['value']
        item_distance = item['distance']['value']
        item_duration = item['duration']['value']
        print(cum_distance, item_distance)
        print(cum_duration, item_duration)

    waypoints_str = '55.76256915886491,37.53964491245408|55.79953159156407,37.62388899803995|55.82000118014139,37.531695602671844'
    [tuple(map(float, waypoint.split(','))) for waypoint in waypoints_str.split('|')]

    log(formatted_now("%H:%M:%S.%f"))

    # The model solver does not work (yet)
    # solve_tsp_model(deadhead_index)

