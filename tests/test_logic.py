from GameObjects.Matrix import Matrix
from GameObjects.Coordinate import Coordinate
from GameObjects.Ship import Ship


def test_init_matrix():
    matrix = Matrix()
    assert str(matrix.matrix) != [['#' for i in range(8)] for j in range(8)]


def test_check_dead_ships():
    matrix = Matrix()
    assert matrix.all_ships_are_dead()


def test_add_ship():
    matrix = Matrix()
    matrix.add_ship(Ship(Coordinate('a', 2), Coordinate('a', 3)))
    matrix.add_ship(Ship(Coordinate('b', 4), Coordinate('c', 4)))
    assert not matrix.all_ships_are_dead()


def test_init_coord():
    c = Coordinate('a', 2)
    assert c.number == 2


def test_init_ship():
    ship = Ship(Coordinate('c', 2), Coordinate('a', 2))
    assert len(ship) == 3


def test_init_ship2():
    ship2 = Ship(Coordinate('a', 5), Coordinate('a', 3))
    assert len(ship2) == 3
