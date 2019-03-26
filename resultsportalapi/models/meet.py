import json


class Meet:

    def __init__(self, event_id, meet_name, meet_date='', meet_course='', meet_location='', meet_state=''):

        self.event_id = event_id
        self.meet_name = meet_name
        self.meet_date = meet_date
        self.meet_course = meet_course
        self.meet_location = meet_location
        self.meet_state = meet_state

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return self.__dict__