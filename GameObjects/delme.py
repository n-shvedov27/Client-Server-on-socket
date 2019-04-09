from GameObjects.Matrix import Matrix
from GameObjects.Coordinate import Coordinate
from GameObjects.Ship import Ship


def get_coordinate(ship_length: int, type_coordinate: str) -> Coordinate:
    coord = input("Input {} coord (a:2) with length {}\n".format(type_coordinate, ship_length))
    while coord[0] not in 'abcdefgh' or coord[1] != ':' or coord[2] not in '1234567890' or len(coord) != 3:
        print("Enter correct coordinate")
        coord = input("Input {} coord (a:2) with length {}\n".format(type_coordinate, ship_length))
    return Coordinate(*coord.split(':'))


def get_coordinates(ship_length: int) -> (Coordinate, Coordinate):
    start = get_coordinate(ship_length, 'start')
    if ship_length == 1:
        end = start
    else:
        end = get_coordinate(ship_length, 'end')
    return start, end


def add_ships(matrix: Matrix) -> Matrix:
    for ship_length in range(2, 5):
        for _ in range(4 - (ship_length - 1)):
            start, end = get_coordinates(ship_length)

            ship = Ship(start, end)

            while len(ship) != ship_length:
                print('Uncorrect length')
                start, end = get_coordinates(ship_length)
                ship = Ship(start, end)

            matrix.add_ship(ship)
            matrix.print_matrix()
    return matrix

