from enum import IntEnum


class Genders(IntEnum):

    MALE = 1
    FEMALE = 2

    def to_str(self, gender):

        if gender == self.MALE:
            return 'Male'

        if gender == self.FEMALE:
            return 'Female'
