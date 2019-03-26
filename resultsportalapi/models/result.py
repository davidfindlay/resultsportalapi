import json
from math import floor

from resultsportalapi.models.courses import Courses


class Result:

    def __init__(self, place, swimmer_name, age, age_min, age_max, gender, club_code, distance, discipline, course, msa_id,
                 final_time, split=None, points=None):
        self.place = place
        self.swimmer_name = swimmer_name
        self.age = age
        self.age_min = age_min
        self.age_max = age_max
        self.gender = gender
        self.club_code = club_code
        self.distance = distance
        self.discipline = discipline
        self.msa_id = msa_id
        self.course = course
        self.final_time = floor(final_time * 100)

        if split == " " or split == "":
            self.split = None
        else:
            self.split = split

        if points == " " or points == "":
            self.points = None
        else:
            self.points = points

    def __str__(self):
        return json.dumps(self.__dict__)

    def get_final_time(self):
        return self.final_time / 100

    def to_list_item(self):

        li = self.__dict__

        li['course'] = Courses.to_str(course=li['course'])

        return li

