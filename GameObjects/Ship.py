from . import Coordinate


class Ship:
    def __init__(self, start: Coordinate, end: Coordinate):
        if start.letter != end.letter and start.number != end.number:
            raise Exception("Enter correct coordinate")
        self.start = start
        self.end = end

    def __len__(self):
        if self.start.number == self.end.number:
            return abs(self.end.letter_like_number - self.start.letter_like_number)+1
        elif self.start.letter == self.end.letter:
            return abs(self.end.number - self.start.number)+1

    def __str__(self):
        return "start: {}:{}\n end: {}:{}".format(self.start.number, self.start.letter, self.end.number,
                                                  self.end.letter)
