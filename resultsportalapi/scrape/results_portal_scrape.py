import re
import requests
import os
from bs4 import BeautifulSoup

from resultsportalapi.models.result import Result
from resultsportalapi.scrape.time_string import convert_time
from resultsportalapi.models.courses import Courses
from resultsportalapi.models.disciplines import Disciplines
from resultsportalapi.models.meet import Meet
from resultsportalapi.models.genders import Genders


class ResultsPortalScrape:

    def get_events(self, year, state="---"):

        events = []

        events_page = requests.get("http://www.portal.msarc.org.au/meets/index.php?scope=&state=" +
                                   state + "&year=" + str(year) + "&Show=Show&js=on").text

        soup = BeautifulSoup(events_page, 'html5lib')

        for table in soup.find_all('table'):
            for subtable in table.find_all('table'):

                i = 0

                for thirdtable in subtable.find_all('table'):

                    if i == 1:

                        links = thirdtable.find_all('a')

                        for link in links:

                            meet_name = link.text
                            m = re.search(r'\d{6}', link['href'])
                            event_id = int(m.group(0))

                            row = link.find_parent('tr')
                            cells = row.find_all('td')

                            course = cells[1].text
                            state = cells[2].text
                            location = cells[3].text
                            meet_date = cells[4].text

                            meet = Meet(event_id, meet_name, meet_date, course, location, state)

                            # TODO: cleanup
                            already_found = False
                            for event in events:
                                if event.event_id == event_id:
                                    already_found = True

                            if not already_found:
                                events.append(meet)

                        # trs = thirdtable.find_all('tr')
                        #
                        # for tr in trs:
                        #
                        #     print(tr)

                    i += 1

        return events

    def find_event(self, year, meet_name):

        all_events = self.get_events(year)

        for event in all_events:

            if event.meet_name == meet_name:
                return event

    def get_event_results(self, event_id):

        event_results = []

        results = requests.get("http://www.portal.msarc.org.au/meets/index.php?EventId=" +
                               str(event_id) + "&filter=*&split=no&scope=&js=on").text

        soup = BeautifulSoup(results, 'html5lib')

        current_distance = 0
        current_gender = None
        current_course = None
        current_discipline = None
        current_age_min = 0
        current_age_max = 0

        for table in soup.find_all('table'):
            for subtable in table.find_all('table'):
                i = 0
                for thirdtable in subtable.find_all('table'):
                    for fourthtable in thirdtable.find_all('table'):
                        for row in fourthtable.find_all('tr'):
                            cols = row.find_all('td')

                            # Detect headings
                            if len(cols) == 1:
                                if 'class' in cols[0].attrs:
                                    if cols[0].attrs['class'][0] == 'groupTitle':
                                        event_details = cols[0].a.text.strip()
                                        event_split = event_details.split(' ')
                                        current_distance = int(re.search(r'\d+', event_split[0]).group())
                                        gender = event_split[-1]

                                        if gender == "Male":
                                            current_gender = Genders.MALE
                                        if gender == "Female":
                                            current_gender = Genders.FEMALE

                                        course = event_split[-3]

                                        if course == "SC":
                                            current_course = Courses.SC
                                        if course == "LC":
                                            current_course = Courses.LC

                                        if 'Freestyle' in event_details:
                                            current_discipline = Disciplines.FREESTYLE

                                        if 'Breaststroke' in event_details:
                                            current_discipline = Disciplines.BREASTSTROKE

                                        if 'Butterfly' in event_details:
                                            current_discipline = Disciplines.BUTTERFLY

                                        if 'Backstroke' in event_details:
                                            current_discipline = Disciplines.BACKSTROKE

                                        if 'Individual Medley' in event_details:
                                            current_discipline = Disciplines.IM

                                        # print("%s %s %s %s" % (current_distance, current_discipline, current_gender,
                                        #                        current_course))

                                    # Look for age group heading
                                    if cols[0].attrs['class'][0] == 'group2':
                                        # print(cols[0].text.strip())

                                        age_group_details = cols[0].text.strip().split(' ')[-1]

                                        if '-' in age_group_details:

                                            age_min, age_max = age_group_details.split('-')

                                            current_age_min = int(age_min)
                                            current_age_max = int(age_max)

                            # Read Result rows
                            # print(len(cols))
                            if len(cols) == 8:

                                if cols[0].text.strip() == "Place":
                                    continue

                                # print(cols)
                                place = int(cols[0].text)
                                swimmer_name = cols[1].text
                                age = int(cols[2].text)
                                club_code = cols[3].text
                                msa_id = int(cols[4].text)
                                final_time = convert_time(cols[5].text)
                                split = cols[6].text
                                points = cols[7].text

                                res = Result(place,
                                             swimmer_name,
                                             age,
                                             current_age_min,
                                             current_age_max,
                                             current_gender,
                                             club_code,
                                             current_distance,
                                             current_discipline,
                                             current_course,
                                             msa_id,
                                             final_time,
                                             split,
                                             points)

                                event_results.append(res)

        return event_results
