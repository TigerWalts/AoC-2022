from io import TextIOWrapper
from os import path
from typing import Iterable, Set, Tuple

FOLDER = path.dirname(__file__)
INPUT_EX = path.join(FOLDER, 'input_example.txt')
INPUT = path.join(FOLDER, 'input.txt')

Vec2D = Tuple[int, int]

def iter_line(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def iter_inputs(iter: Iterable[str]):
    for line in iter_line(iter):
        [ _, _, sxeqc, syeqc, _, _, _, _, bxeqc, byeq ] = line.split(' ')
        byeq = byeq + ' '
        [ sensor_x, sensor_y, beacon_x, beacon_y ] = [ int(x[2:-1]) for x in [sxeqc, syeqc, bxeqc, byeq] ]
        yield (sensor_x, sensor_y), (beacon_x, beacon_y)

def difference(a: Vec2D, b:Vec2D) -> Vec2D:
    return tuple(dim_b - dim_a for dim_a, dim_b in zip(a, b))

def mdistance(vec: Vec2D) -> int:
    return sum(abs(x) for x in vec)

def iter_sensors_beacons_mdists(iter: Tuple[Vec2D, Vec2D]):
    for sensor_loc, beacon_loc in iter:
        yield sensor_loc, beacon_loc, mdistance(difference(sensor_loc, beacon_loc))

def get_x_ranges_at_y(sensors_beacons_mdists, search_y):
    return {
        (sensor_loc[0] - mdist + abs(search_y - sensor_loc[1]), sensor_loc[0] + mdist - abs(search_y - sensor_loc[1]))
        for sensor_loc, _, mdist
        in sensors_beacons_mdists
        if abs(search_y - sensor_loc[1]) <= mdist
    }

def reduce_ranges(ranges: Set[Tuple[int, int]]):
    start_count = len(ranges)
    if start_count <= 1:
        return ranges
    while True:
        ranges_reduced = set()
        range1 = None
        for range2 in sorted(ranges, key=lambda x : x[0]):
            if range1 is None:
                # First range : Store and continue
                range1 = range2
                continue
            elif range1[1] + 1 == range2[0]:
                # Contiguous 1->2 : Join
                range1 = (range1[0], range2[1])
            elif range2[1] + 1 == range1[0]:
                # Contiguous 2->1 : Join
                range1 = (range2[0], range1[1])
            elif range1[1] < range2[0] or range2[1] < range1[0]:
                # Do not intesect : Add 1, Store 2
                ranges_reduced.add(range1)
                range1 = range2
            else:
                # Intersect in some way : min-max
                range1 = (min(range1[0], range2[0]), max(range1[1], range2[1]))
        # Add last 1
        ranges_reduced.add(range1)
        end_count = len(ranges_reduced)
        if end_count == start_count:
            # Can't reduce further
            break
        # Re-init
        start_count = end_count
        ranges = ranges_reduced
    return ranges_reduced

def main(input_filepath: str, search_y: int, max_bound: int):
    with open(input_filepath, 'r') as input_file:
        sensors_beacons_mdists = [ x for x in iter_sensors_beacons_mdists(iter_inputs(iter_line(input_file))) ]

    x_ranges_at_y = reduce_ranges(get_x_ranges_at_y(sensors_beacons_mdists, search_y))

    sensors_beacons_xs_on_y = set()
    for sensor_loc, beacon_loc, _ in sensors_beacons_mdists:
        if sensor_loc[1] == search_y:
            sensors_beacons_xs_on_y.add(sensor_loc[0])
        if beacon_loc[1] == search_y:
            sensors_beacons_xs_on_y.add(beacon_loc[0])

    print(
        sum(
            (
                1 + x_range[1] - x_range[0] - sum(
                    1
                    for x
                    in sensors_beacons_xs_on_y 
                    if x_range[0] <= x <= x_range[1]
                )
            ) for x_range in x_ranges_at_y
        )
    )

    for search_y in range(max_bound+1):
        bounded_x_ranges_at_y = reduce_ranges({
            (max(min_x, 0), min(max_x, max_bound))
            for min_x, max_x
            in get_x_ranges_at_y(sensors_beacons_mdists, search_y)
            if min_x <= max_bound or max_x >= 0
        })

        if len(bounded_x_ranges_at_y) < 2:
            continue

        search_x = list(bounded_x_ranges_at_y)[0][1]+1
        print((search_x * 4_000_000) + search_y)
        break


if __name__ == '__main__':
    # main(INPUT_EX, 10, 20)
    main(INPUT, 2_000_000, 4_000_000)
