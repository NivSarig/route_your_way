import os
import time
from random import random

from external_integrations.gmaps_integration_utils import (
    build_all_duration_matrix,
    pairwise,
    get_url_from_coordinates,
    get_distance_and_duration,
)

MOCK = "brute"
MOCK = False


def get_distance_and_duration_from_game_id(short_coordinates, game_id, use_cache=False):
    deadhead_index, stops = solve_tsp_from_coordinate_list(short_coordinates, game_id, use_cache)

    print(f"tsp_stops:{stops}")

    coordinates = []

    for stop in stops:
        coordinates.append(tuple(deadhead_index[stop][stops[0]]["origin"]))

    url = get_url_from_coordinates(coordinates)
    distance, duration = get_distance_and_duration(coordinates)

    print(f"tsp_distance: {distance}, tsp_duration: {duration}")
    return url, distance, duration, coordinates


def get_distance_and_duration_from_game_id_and_compare_with_brute(short_coordinates, game_id, use_cache=False):
    deadhead_index, stops = solve_tsp_from_coordinate_list(short_coordinates, game_id, use_cache)

    print(f"tsp_stops:{stops}")

    coordinates = []

    for stop in stops:
        coordinates.append(tuple(deadhead_index[stop][stops[0]]["origin"]))
    distance, duration = get_distance_and_duration(coordinates)

    brute_coordinates = []
    brute_stops = brute_force_solution(deadhead_index, game_id)
    print(f"brute_stops: {brute_stops}")

    for stop in brute_stops:
        brute_coordinates.append(tuple(deadhead_index[stop][brute_stops[0]]["origin"]))

    url = get_url_from_coordinates(coordinates)
    brute_distance, brute_duration = get_distance_and_duration(brute_coordinates)
    print(f"tsp_stops: {stops}\nbrute_stop: {brute_stops}")
    print(f"brute_distance: {brute_distance}, brute_duration: {brute_duration}")
    print(f"tsp_distance: {distance}, tsp_duration: {duration}")
    assert brute_stops == stops
    return url, distance, duration, coordinates, brute_stops, stops


def solve_tsp_from_coordinate_list(coordinates_list, game_id, use_cache):

    game_directory = os.path.join(os.getcwd(), game_id)
    if not os.path.exists(game_directory):
        os.mkdir(game_directory)

    deadhead_index = build_all_duration_matrix(coordinates_list, use_cache)

    return deadhead_index, solve_tsp_for_deadhead_index(
        deadhead_index, game_directory, game_id, mock=MOCK
    )


def solve_tsp_for_deadhead_index(deadhead_index, game_dir, game_id, mock=MOCK):
    if not os.path.exists(game_dir):
        os.mkdir(game_dir)
    input_file_name = os.path.join(game_dir, "input.tsp")
    output_file_name = os.path.join(game_dir, "output.txt")
    # output_file_name = os.path.join(game_dir, "asym-good_output.txt")
    if os.path.exists(output_file_name) and mock is not False:
        time.sleep(1.5 + random())
        with open(output_file_name, "r") as fid:
            return fid.read().split("\n")

    if mock == "brute":
        all_stop_indices = list(deadhead_index.keys())
        import itertools

        # Generate all permutations
        permutations = itertools.permutations(all_stop_indices)
        best_duration = float("inf")
        best_perm = None
        for permutation in permutations:
            perm_duration = 0
            for perm_pair in pairwise(permutation):
                perm_duration += deadhead_index[str(perm_pair[0])][str(perm_pair[1])][
                    "duration"
                ]
            if perm_duration < best_duration:
                best_duration = perm_duration
                best_perm = permutation
        indices = list(best_perm)
        with open(output_file_name, "w") as fid:
            fid.write("\n".join(indices))
        return indices
    # Make a symmetric TSP out of the asymmetric problem we have
    dimension = len(deadhead_index)
    tsp_dimension = dimension * 2
    INF = str(1000000)  # 'INF'
    mINF = str(-1000000)  # '-INF'
    durations = [[INF] * tsp_dimension for __ in range(tsp_dimension)]
    for k1 in range(dimension):
        for k2 in range(dimension):
            if k1 == k2:
                continue
            int_duration12 = str(deadhead_index[str(k1)][str(k2)]['duration'])
            int_duration21 = str(deadhead_index[str(k2)][str(k1)]['duration'])
            durations[int(k1)][int(k2)] = INF
            durations[int(k2)][int(k1)] = INF
            durations[dimension + int(k1)][dimension + int(k2)] = INF
            durations[dimension + int(k2)][dimension + int(k1)] = INF
            durations[int(k1)][dimension + int(k2)] = int_duration12
            durations[dimension + int(k2)][int(k1)] = int_duration21
        durations[int(k1)][int(k1)] = '0'
        durations[dimension + int(k1)][dimension + int(k1)] = '0'
        durations[int(k1)][dimension + int(k1)] = mINF
        durations[dimension + int(k1)][int(k1)] = mINF

    duration_str = []
    for line_idx, duration_line in enumerate(durations):
        duration_str.append(" ".join(duration_line[: line_idx + 1]))
    duration_str = "\n".join(duration_str)
    file_content = """NAME: {}
TYPE: TSP
COMMENT: Niv
DIMENSION: {}
EDGE_WEIGHT_TYPE: EXPLICIT
EDGE_WEIGHT_FORMAT: LOWER_DIAG_ROW
EDGE_WEIGHT_SECTION
{}
EOF""".format(
        game_id, tsp_dimension, duration_str
    )

    with open(input_file_name, "w") as fid:
        fid.write(file_content)
    print(file_content)

    try:
        os.system(
            "python ./external_integrations/optimization_engine/solve_tsp.py --input {} --output  {}".format(
                input_file_name, output_file_name
            )
        )
        print("Woohoo we are Hackathoning")
    except Exception as e:
        print("Oh boy we are Hackathoning")
    symmetric_output_file_name = os.path.join(game_dir, "good_output.txt")
    symmetric_output_file_name = os.path.join(game_dir, "output.txt")
    with open(symmetric_output_file_name, 'r') as fid:
        asymmetric_output_columns = fid.read().split('\n')[:-1][::2]
    asymmetric_output_file_name = os.path.join(game_dir, "asym-good_output.txt")
    with open(asymmetric_output_file_name, "w") as fid:
        fid.write("\n".join(asymmetric_output_columns))
    return asymmetric_output_columns


def brute_force_solution(deadhead_index, game_id):

    game_directory = os.path.join(os.getcwd(), game_id)
    output_file_name = os.path.join(game_directory, "brute_output.res")
    all_stop_indices = list(deadhead_index.keys())
    print("Finding a brute force solution over {} stops".format(len(all_stop_indices)))
    import itertools
    # Generate all permutations
    permutations = itertools.permutations(all_stop_indices)
    best_duration = float("inf")
    best_perm = None
    number_of_permutations_checked = 0
    for permutation in permutations:
        number_of_permutations_checked += 1
        perm_duration = 0
        for perm_pair in pairwise(permutation):
            perm_duration += deadhead_index[str(perm_pair[0])][str(perm_pair[1])][
                "duration"
            ]
        if perm_duration < best_duration:
            best_duration = perm_duration
            best_perm = permutation
    print(f"Checked {number_of_permutations_checked} permutations for {len(all_stop_indices)} stops")
    indices = list(best_perm)
    with open(output_file_name, "w") as fid:
        fid.write("\n".join(indices))
    return indices


if __name__ == "__main__":
    pass
