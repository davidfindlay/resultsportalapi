from enum import IntEnum


class Courses(IntEnum):

    SC = 1
    LC = 2

    def to_str(self, course):

        if course == self.SC:
            return "SC"

        if course == self.LC:
            return "LC"