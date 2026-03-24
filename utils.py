import copy


OBJECT_EMPTY = None
OBJECT_HOUSE = "🏠"
OBJECT_HOSPITAL = "🏥"


MOVE_UP = (0, -1)
MOVE_DOWN = (0, 1)
MOVE_LEFT = (-1, 0)
MOVE_RIGHT = (1, 0)


def is_free_to_move(map, move):
    """
    Check whether a target position is empty and can be moved into.

    Args:
        map: Matrix (list of lists) representing the board.
        move: Position as (x, y), where x is horizontal and y is vertical.

    Returns:
        bool: True if the target cell is empty (None), False otherwise.
    """

    x, y = move

    return not map[y][x]


def is_valid_move(map, move):
    """
    Check whether a position is inside the matrix boundaries.

    Args:
        map: Matrix (list of lists) representing the board.
        move: Position as (x, y), where x is horizontal and y is vertical.

    Returns:
        bool: True if the position is within bounds, False otherwise.
    """

    rows_size = len(map)
    columns_size = len(map[0])

    x, y = move

    if y < 0 or y >= rows_size:
        return False

    if x < 0 or x >= columns_size:
        return False

    return True


def find_objects(map, target_object_symbol):
    """
    Find all coordinates where a given object symbol appears.

    Args:
        map: Matrix (list of lists) representing the board.
        target_object_symbol: Symbol to search for (None, 🏠, or 🏥).

    Returns:
        list[tuple[int, int]]: All matching coordinates as (x, y).
    """

    coordinates = []

    for y, rows in enumerate(map):
        for x, object in enumerate(rows):
            if object == target_object_symbol:
                coordinates.append((x, y))

    return coordinates


def result(map, hospital_coordinates, target_move):
    """
    Create and return a new map after moving one hospital to a target position.

    Args:
        map: Matrix (list of lists) representing the board.
        hospital_coordinates: Current hospital position as (x, y).
        target_move: Destination position as (x, y).

    Returns:
        list[list]: A deep-copied map with the move applied.
    """

    new_map = copy.deepcopy(map)
    x_hospital, y_hospital = hospital_coordinates
    x_target, y_target = target_move

    new_map[y_target][x_target] = OBJECT_HOSPITAL
    new_map[y_hospital][x_hospital] = OBJECT_EMPTY

    return new_map


def manhattan(pos, pos_2):
    """
    Compute the Manhattan distance between two coordinates.

    Args:
        pos: First coordinate as (x, y).
        pos_2: Second coordinate as (x, y).

    Returns:
        int: Distance computed as abs(x2 - x1) + abs(y2 - y1).
    """

    x, y = pos
    x_2, y_2 = pos_2

    return abs(x_2 - x) + abs(y_2 - y)


def cost(map):
    """
    Compute total cost as the sum of distances from each hospital to each house.

    Args:
        map: Matrix (list of lists) representing the board.

    Returns:
        int: Total Manhattan-distance cost.
    """

    hospitals = find_objects(map, OBJECT_HOSPITAL)
    houses = find_objects(map, OBJECT_HOUSE)

    cost = 0

    for hospital in hospitals:
        for house in houses:
            cost += manhattan(hospital, house)

    return cost


def move(pos, pos_2):
    """
    Add two coordinates component-wise.

    Args:
        pos: First coordinate as (x, y).
        pos_2: Second coordinate as (x, y).

    Returns:
        tuple[int, int]: New coordinate as (x1 + x2, y1 + y2).
    """

    return tuple(x + y for x, y in zip(pos, pos_2))


def actions(map, hospital_position):
    """
    Return all valid adjacent moves for a hospital in up, down, left, right order.

    Args:
        map: Matrix (list of lists) representing the board.
        hospital_position: Hospital coordinate as (x, y).

    Returns:
        list[tuple[int, int]]: Valid neighboring positions that are in bounds and free.
    """

    actions = []

    move_up = move(hospital_position, MOVE_UP)
    move_down = move(hospital_position, MOVE_DOWN)
    move_left = move(hospital_position, MOVE_LEFT)
    move_right = move(hospital_position, MOVE_RIGHT)

    for possible_move in [move_up, move_down, move_left, move_right]:
        is_valid = is_valid_move(map, possible_move) and is_free_to_move(
            map, possible_move
        )

        if is_valid:
            actions.append(possible_move)

    return actions
