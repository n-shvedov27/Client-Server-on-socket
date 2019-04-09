from .Ship import Ship


class MyIterator:
    def __init__(self, start, stop):
        self._current = start
        self._stop = stop
        if start < stop:
            self._increment = 1
        else:
            self._increment = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self._increment == 1:
            if self._current <= self._stop:
                result = self._current
                self._current += 1
                return result
            else:
                raise StopIteration
        else:
            if self._current >= self._stop:
                result = self._current
                self._current -= 1
                return result
            else:
                raise StopIteration


class Matrix:
    def __init__(self):
        self.matrix = [['#' for i in range(8)] for j in range(8)]

    def all_ships_are_dead(self) -> bool:
        for i in range(8):
            for j in range(8):
                if self.matrix[i][j] == 'X':
                    return False
        return True

    def print_matrix(self):  # pragma: no cover
        print('  abcdefgh')
        for i_raw in range(8):
            raw = str(i_raw) + " "
            for i_coumn in range(8):
                raw += self.matrix[i_raw][i_coumn]
            print(raw)

    def add_ship(self, ship: Ship) -> None:
        start, end = ship.start, ship.end
        if start.letter == end.letter:
            for i in MyIterator(start.number, end.number):

                self.matrix[i][start.letter_like_number] = 'X'
        elif start.number == end.number:
            for i in MyIterator(start.letter_like_number, end.letter_like_number):
                self.matrix[start.number][i] = 'X'
