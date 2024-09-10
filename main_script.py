from external_integrations.gmaps_integration_utils import generate_random_coordinates

from external_integrations.optimization_engine_utils import get_distance_and_duration_from_game_id, \
    get_distance_and_duration_from_game_id_and_compare_with_brute
# from logging_utils import formatted_now
import logging
logger = logging.getLogger(__name__)


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
    # log(url)
    # log(coordinates)

    new_url = "https://www.google.com/maps/dir/55.78879096471749+37.56912052075894/55.82394492336372+37.71564443590594/55.718563249961306+37.51647539470249/55.775807492867564+37.51946053900027/55.690901822366115+37.46013158008646/55.80069715769361+37.56576992130943/55.60486832825113+37.466155203107114/55.78130697817363+37.46718729666109/55.70319444748+37.63345154478967/55.843094719260534+37.47741722330984/@55.7272268,37.3982661,11z/data=!3m1!4b1!4m62!4m61!1m5!1m1!1s0x0:0xfebb1ddabbd58077!2m2!1d37.5685818!2d55.7885064!1m5!1m1!1s0x0:0x865d4de12b4564b6!2m2!1d37.716047!2d55.8236744!1m5!1m1!1s0x0:0x5df7cd41dca8f173!2m2!1d37.5139163!2d55.7061335!1m5!1m1!1s0x0:0x8439f8542df1d9a4!2m2!1d37.5198347!2d55.7759439!1m5!1m1!1s0x0:0xd0422de2cbc7203f!2m2!1d37.4600474!2d55.6907233!1m5!1m1!1s0x0:0x9e8663cc32912aa7!2m2!1d37.5659516!2d55.8008145!1m5!1m1!1s0x0:0x23dd95533621b43b!2m2!1d37.4623676!2d55.6028596!1m5!1m1!1s0x0:0x76d30e134b59d2a1!2m2!1d37.4773823!2d55.7750483!1m5!1m1!1s0x0:0xfd468a8f9cf66ed8!2m2!1d37.6333575!2d55.7028242!1m5!1m1!1s0x0:0xa0c2634c7f03102d!2m2!1d37.4773427!2d55.8429622!3e0?entry=ttu"
    # distance, duration = get_route_info_from_url(new_url)
    # log((distance, duration))

    short_coordinates = [
        (55.8851468503753, 37.51883085420433),
        (55.64084712224211, 37.63753714586377),
    ]
    locations = {
        "Short": [
        (55.8851468503753, 37.51883085420433),
        (55.64084712224211, 37.63753714586377),
    ],
        "Short3": [
        (55.8851468503753, 37.51883085420433),
        (55.64084712224211, 37.63753714586377),
        (55.74084712224211, 37.33753714586377),
    ],
        "Short5": [
        (55.8851468503753, 37.51883085420433),
        (55.64084712224211, 37.63753714586377),
        (55.74084712224211, 37.33753714586377),
        (55.44084712224211, 37.23753714586377),
    ],
        "Short4": [
        (55.8851468503753, 37.51883085420433),
        (55.64084712224211, 37.63753714586377),
        (55.74084712224211, 37.33753714586377),
        (55.44084712224211, 37.23753714586377),
        (55.44084712224211, 37.43753714586377),
    ],
        "TelAviv": [
            [32.1732507, 34.7894517],
            [32.0694666, 34.7699549],
            [32.0737261, 34.765359],
            [32.1145883, 34.8015212],
            [32.0779325, 34.7741353],
            [32.0610971, 34.7919043],
            [32.0810915, 34.7889161],
            [32.0633681, 34.7728317],
            [32.0728065, 34.7948381]
        ],
        "TelAviv6": [
            [32.1732507, 34.7894517],
            [32.0694666, 34.7699549],
            [32.0737261, 34.765359],
            [32.1145883, 34.8015212],
            [32.0779325, 34.7741353],
            [32.0610971, 34.7919043],

        ],
        "TelAvivBad": [
            [32.0732507, 34.7894517],
            [32.0694666, 34.7699549],
            [32.0737261, 34.765359],
            [32.1145883, 34.8015212],
            [32.0779325, 34.7741353],
            [32.0610971, 34.7919043],
            [32.0810915, 34.7889161],
            [32.0633681, 34.7728317],
            [32.0728065, 34.7948381]
        ],
        "London": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5289369, -0.0620099],
            [51.5163462, -0.0468525],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -0.0925782],
            [51.5368766, -0.0945162],
            [51.512813, -0.0836868],
            [51.515942, -0.0908033],
        ],
        "London8": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5289369, -0.0620099],
            [51.5163462, -0.0468525],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -0.0925782]
        ],
        "London9": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5289369, -0.0620099],
            [51.5163462, -0.0468525],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -0.0925782],
            [51.5368766, -0.0945162]
        ],
        "London10": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5289369, -0.0620099],
            [51.5163462, -0.0468525],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -0.0925782],
            [51.5368766, -0.0945162],
            [51.512813, -0.0836868],
        ],
        "London20": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5289369, -0.0620099],
            [51.5163462, -0.0468525],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -0.0925782],
            [51.5368766, -0.0945162],
            [51.512813, -0.0836868],
            [51.6229532, -0.0905527],
            [51.5290351, -0.0804977],
            [51.5389369, -0.0720099],
            [51.5263462, -0.0568525],
            [51.5422395, -0.0982468],
            [51.5183975, -0.08886],
            [51.5305595, -0.0480812],
            [51.5327271, -0.1025782],
            [51.5468766, -0.1045162],
            [51.522813, -0.0936868],
        ],
        "London19": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5289369, -0.0620099],
            [51.5163462, -0.0468525],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -0.0925782],
            [51.5368766, -0.0945162],
            [51.512813, -0.0836868],
            [51.6229532, -0.0905527],
            [51.5290351, -0.0804977],
            [51.5389369, -0.0720099],
            [51.5263462, -0.0568525],
            [51.5422395, -0.0982468],
            [51.5183975, -0.08886],
            [51.5305595, -0.0480812],
            [51.5327271, -0.1025782],
            [51.5468766, -0.1045162],
        ],
        "London18": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5289369, -0.0620099],
            [51.5163462, -0.0468525],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -0.0925782],
            [51.5368766, -0.0945162],
            [51.512813, -0.0836868],
            [51.6229532, -0.0905527],
            [51.5290351, -0.0804977],
            [51.5389369, -0.0720099],
            [51.5263462, -0.0568525],
            [51.5422395, -0.0982468],
            [51.5183975, -0.08886],
            [51.5305595, -0.0480812],
            [51.5327271, -0.1025782],
        ],
        "London17": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5289369, -0.0620099],
            [51.5163462, -0.0468525],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -0.0925782],
            [51.5368766, -0.0945162],
            [51.512813, -0.0836868],
            [51.6229532, -0.0905527],
            [51.5290351, -0.0804977],
            [51.5389369, -0.0720099],
            [51.5263462, -0.0568525],
            [51.5422395, -0.0982468],
            [51.5183975, -0.08886],
            [51.5305595, -0.0480812]
        ],
        "London16": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5289369, -0.0620099],
            [51.5163462, -0.0468525],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -0.0925782],
            [51.5368766, -0.0945162],
            [51.512813, -0.0836868],
            [51.6229532, -0.0905527],
            [51.5290351, -0.0804977],
            [51.5389369, -0.0720099],
            [51.5263462, -0.0568525],
            [51.5422395, -0.0982468],
            [51.5183975, -0.08886],
        ],
        "London15": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5289369, -0.0620099],
            [51.5163462, -0.0468525],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -0.0925782],
            [51.5368766, -0.0945162],
            [51.512813, -0.0836868],
            [51.6229532, -0.0905527],
            [51.5290351, -0.0804977],
            [51.5389369, -0.0720099],
            [51.5263462, -0.0568525],
            [51.5422395, -0.0982468]
        ],
        "London-": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -1.0925782],
            [51.5368766, -0.0945162],
            [51.512813, -0.0836868],
            [51.5290351, -0.0804977],
            [51.5389369, -0.0720099],
            [51.5263462, -0.0568525],
            [51.5422395, -0.0982468]
        ],
        "London+": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
            [51.5205595, -0.0380812],
            [51.5227271, -0.0925782],
            [51.5368766, -0.0945162],
            [51.512813, -0.0836868],
            [51.5290351, -0.0804977],
            [51.5389369, -0.0720099],
            [51.5263462, -0.0568525],
            [51.5422395, -0.0982468]
        ],
        "London6": [
            [51.5229532, -0.0805527],
            [51.5190351, -0.0704977],
            [51.5289369, -0.0620099],
            [51.5163462, -0.0468525],
            [51.5322395, -0.0882468],
            [51.5083975, -0.07886],
        ],
    }
    game_id = "London-"
    # game_id = "TelAvivBad"
    # game_id = "Short"
    use_cache = True

    short_coordinates = locations[game_id]

    # short_coordinates = short_coordinates + [[la+1, lo-1] for la,lo in short_coordinates]

    url, distance, duration, coordinates = get_distance_and_duration_from_game_id(
            short_coordinates, game_id, use_cache=use_cache)
    print("url: {}, distance: {}, duration: {}, game_id: {}".format(url, distance, duration, game_id))
    exit()
    all_games = {}
    for game_id in ['Short', 'Short3', 'Short5', 'Short4', 'TelAviv', 'TelAviv6', 'TelAvivBad', 'London8', 'London9', 'London10', 'London6']:
        # if game_id == "TelAviv":
        #     continue
        short_coordinates = locations[game_id]
        url, distance, duration, coordinates, brute_stops, stops = \
            get_distance_and_duration_from_game_id_and_compare_with_brute(
                short_coordinates, game_id, use_cache=use_cache)
        print("url: {}, distance: {}, duration: {}, game_id: {}".format(url, distance, duration, game_id))
        all_games[game_id] = {"game_id": game_id, "brute_stops": brute_stops, "stops": stops}

    for game_id, game in all_games.items():
        print(game_id)
        print(game['brute_stops'])
        print(game['stops'])
