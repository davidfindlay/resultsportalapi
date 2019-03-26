from enum import IntEnum


class Levels(IntEnum):

    BRONZE = 1
    SILVER = 2
    GOLD = 3
    PLATINUM = 4

    def to_str(self, level):

        if level == self.BRONZE:
            return 'Bronze'

        if level == self.SILVER:
            return 'Silver'

        if level == self.GOLD:
            return 'Gold'

        if level == self.PLATINUM:
            return 'Platinum'
