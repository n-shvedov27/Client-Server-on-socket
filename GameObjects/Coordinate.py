class Coordinate:
    def __init__(self, letter: str, number):
        self.number = int(number)
        self.letter = letter
        self.letter_like_number = 'abcdefgh'.find(letter)

    def __str__(self):
        return "{} : {} : {}".format(self.number, self.letter, self.letter_like_number)
